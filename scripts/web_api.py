#!/usr/bin/env python3
"""HTTP API виджета Фиби на сайте документации.

Тот же RAG и промпт, что у Telegram-бота. Канал — SSE и JSON handoff.
"""

from __future__ import annotations

import json
import logging
import os
import queue
import re
import sys
import threading
import time
from collections import deque
from datetime import date
from typing import Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))
except ImportError:
    pass

import requests
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

from handoff import HANDOFF_MARK, is_handoff
from rag_common import VECTORDB_DIR
from rag_service import answer_stream
from vision import OLLAMA_URL
import web_copy

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("fb-web")

CORS_ORIGINS = [
    o.strip() for o in os.environ.get(
        "CORS_ORIGINS",
        "https://help.fastboard.online,http://localhost:3000",
    ).split(",")
    if o.strip()
]
WEB_RATE_LIMIT = int(os.environ.get("WEB_RATE_LIMIT_PER_HOUR", "60"))
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID", "").strip()
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
SPEND_LIMIT_ALERT = int(os.environ.get("SPEND_LIMIT_ALERT", "0"))
STATE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "state")
SPEND_FILE = os.path.join(STATE_DIR, "web_spend.json")

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


class ChatHistoryItem(BaseModel):
    role: str
    content: str = ""


class StreamBody(BaseModel):
    question: str = ""
    history: List[ChatHistoryItem] = Field(default_factory=list)
    pageUrl: str = ""


class HandoffBody(BaseModel):
    name: str = ""
    phone: str = ""
    email: str = ""
    comment: str = ""
    history: List[ChatHistoryItem] = Field(default_factory=list)
    pageUrl: str = ""
    at: str = ""


class IpRateLimiter:
    def __init__(self, limit: int):
        self.limit = limit
        self._hits: Dict[str, deque] = {}
        self._lock = threading.Lock()

    def allow(self, ip: str) -> bool:
        if self.limit <= 0:
            return True
        now = time.time()
        with self._lock:
            hits = self._hits.setdefault(ip, deque())
            while hits and now - hits[0] > 3600:
                hits.popleft()
            if len(hits) >= self.limit:
                return False
            hits.append(now)
            return True


limiter = IpRateLimiter(WEB_RATE_LIMIT)
_spend_lock = threading.Lock()
_spend_alerted_day: Optional[str] = None


def client_ip(req: Request) -> str:
    forwarded = req.headers.get("x-forwarded-for", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if req.client:
        return req.client.host or "unknown"
    return "unknown"


def bump_spend_and_maybe_alert():
    """Счётчик запросов за сутки; при пороге — сообщение в ADMIN_CHAT_ID."""
    global _spend_alerted_day
    if SPEND_LIMIT_ALERT <= 0 or not ADMIN_CHAT_ID or not TELEGRAM_BOT_TOKEN:
        return
    today = date.today().isoformat()
    with _spend_lock:
        data = {"day": today, "count": 0}
        try:
            os.makedirs(STATE_DIR, exist_ok=True)
            with open(SPEND_FILE, encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError):
            pass
        if data.get("day") != today:
            data = {"day": today, "count": 0}
        data["count"] = int(data.get("count") or 0) + 1
        try:
            with open(SPEND_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f)
        except OSError as e:
            log.warning("spend file: %s", e)
        count = data["count"]
        should_alert = (
            count >= SPEND_LIMIT_ALERT
            and _spend_alerted_day != today
        )
        if should_alert:
            _spend_alerted_day = today
    if should_alert:
        notify_admin(
            f"⚠️ Лимит запросов веб-виджета Фиби за сутки: {count} "
            f"(порог {SPEND_LIMIT_ALERT})."
        )


def notify_admin(text: str) -> bool:
    if not ADMIN_CHAT_ID or not TELEGRAM_BOT_TOKEN:
        return False
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": ADMIN_CHAT_ID, "text": text[:4000]},
            timeout=20,
        )
        return bool(r.json().get("ok"))
    except (requests.RequestException, ValueError) as e:
        log.warning("notify_admin: %s", e)
        return False


def deliver_handoff(body: HandoffBody) -> bool:
    lines = [
        "🙋 Обращение с сайта документации (Фиби)",
        "",
        f"Имя: {body.name.strip()}",
        f"Телефон: {body.phone.strip() or '—'}",
        f"Email: {body.email.strip() or '—'}",
        f"Страница: {body.pageUrl.strip() or '—'}",
        f"Время: {body.at.strip() or '—'}",
    ]
    if body.comment.strip():
        lines += ["", "Комментарий:", body.comment.strip()[:1500]]
    if body.history:
        lines += ["", "История диалога:"]
        for item in body.history[-12:]:
            role = "👤" if item.role == "user" else "🤖"
            lines.append(f"{role} {(item.content or '')[:500]}")
    return notify_admin("\n".join(lines))


app = FastAPI(title="Fibi docs consultant", docs_url=None, redoc_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    chroma_ok = os.path.isdir(VECTORDB_DIR)
    ollama_ok = False
    try:
        r = requests.get(f"{OLLAMA_URL}/api/version", timeout=5)
        ollama_ok = r.ok
    except requests.RequestException:
        pass
    status = "ok" if chroma_ok else "degraded"
    return {
        "status": status,
        "chroma": chroma_ok,
        "ollama": ollama_ok,
    }


@app.get("/chat/copy")
def chat_copy():
    return web_copy.as_dict()


@app.post("/chat/handoff")
def chat_handoff(body: HandoffBody):
    name = body.name.strip()
    phone = body.phone.strip()
    email = body.email.strip()
    if not name:
        raise HTTPException(status_code=400, detail={"error": "name_required"})
    if not phone and not email:
        raise HTTPException(status_code=400, detail={"error": "contact_required"})
    if email and not EMAIL_RE.match(email):
        raise HTTPException(status_code=400, detail={"error": "bad_email"})
    digits = re.sub(r"\D", "", phone)
    if phone and len(digits) < 10:
        raise HTTPException(status_code=400, detail={"error": "bad_phone"})
    if not ADMIN_CHAT_ID or not TELEGRAM_BOT_TOKEN:
        raise HTTPException(status_code=503, detail={"error": "handoff_unavailable"})
    if not deliver_handoff(body):
        raise HTTPException(status_code=502, detail={"error": "handoff_failed"})
    return Response(status_code=204)


@app.post("/chat/stream")
async def chat_stream(body: StreamBody, request: Request):
    ip = client_ip(request)
    if not limiter.allow(ip):
        return JSONResponse(
            status_code=429,
            content={"error": "rate_limited"},
        )
    question = (body.question or "").strip()
    if not question:
        raise HTTPException(status_code=400, detail={"error": "question_required"})

    bump_spend_and_maybe_alert()
    history = [item.model_dump() for item in body.history]

    async def events():
        q: queue.Queue = queue.Queue()
        prev = [""]
        cancel = threading.Event()

        def on_delta(full: str):
            if cancel.is_set():
                return False
            text = full if isinstance(full, str) else ""
            if text.startswith(prev[0]):
                piece = text[len(prev[0]):]
            else:
                piece = text
            prev[0] = text
            if piece:
                q.put(("delta", piece))
            return True

        def worker():
            try:
                result = answer_stream(
                    question,
                    history=history,
                    on_delta=on_delta,
                )
                if is_handoff(result) and not prev[0]:
                    q.put(("delta", HANDOFF_MARK))
                elif result and not prev[0]:
                    q.put(("delta", result))
                q.put(("done", None))
            except Exception as e:
                log.exception("stream failed")
                q.put(("err", e))

        threading.Thread(target=worker, daemon=True).start()

        while True:
            if await request.is_disconnected():
                cancel.set()
                log.info("client disconnected — stop generation")
                break
            try:
                kind, payload = q.get(timeout=0.25)
            except queue.Empty:
                continue
            if kind == "delta":
                yield f"data: {json.dumps({'delta': payload}, ensure_ascii=False)}\n\n"
            elif kind == "err":
                yield f"data: {json.dumps({'error': 'provider_unavailable'}, ensure_ascii=False)}\n\n"
                break
            elif kind == "done":
                break
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        events(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.exception_handler(Exception)
async def unhandled(request: Request, exc: Exception):
    log.exception("unhandled %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"error": "internal"})


if __name__ == "__main__":
    import uvicorn
    host = os.environ.get("WEB_API_HOST", "127.0.0.1")
    port = int(os.environ.get("WEB_API_PORT", "8080"))
    uvicorn.run("web_api:app", host=host, port=port, reload=False)
