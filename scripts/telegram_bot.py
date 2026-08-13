#!/usr/bin/env python3
"""Telegram-бот AI-консультанта по документации Fastboard и ClickHouse.

Текст — ответ по документации (RAG поверх ChromaDB). Картинки, скриншоты и PDF —
распознавание через vision-модель (описание + извлечение текста с изображения),
затем ответ по документации с учётом распознанного.

Модель работает локально на GPU-сервере через Ollama (SSH-туннель на 127.0.0.1:11434).
Запускается как systemd-сервис, см. deploy/.
"""

import base64
import html
import io
import json
import logging
import os
import queue
import re
import sys
import threading
import time
from collections import deque

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))
except ImportError:
    pass

import chromadb

from rag_common import VECTORDB_DIR, CHAT_MODEL, OpenRouterEmbeddingFunction
from consultant import COLLECTIONS, SYSTEM_PROMPT, retrieve, build_context

# --- Конфигурация ---
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
API = f"https://api.telegram.org/bot{TOKEN}"
FILE_API = f"https://api.telegram.org/file/bot{TOKEN}"

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
VISION_MODEL = os.environ.get("VISION_MODEL", CHAT_MODEL)
# Пустой NUM_CTX = не переопределять контекст (модель на GPU уже загружена с 256k,
# переопределение вызвало бы перезагрузку модели и мешало бы другим сервисам GPU).
NUM_CTX = os.environ.get("NUM_CTX", "").strip()
NUM_PREDICT = int(os.environ.get("NUM_PREDICT", "1400"))
TEMPERATURE = float(os.environ.get("TEMPERATURE", "0.3"))
TOP_K = int(os.environ.get("RAG_TOP_K", "6"))
LLM_TIMEOUT = float(os.environ.get("LLM_TIMEOUT", "600"))
HISTORY_TURNS = int(os.environ.get("HISTORY_TURNS", "6"))
HISTORY_TTL = float(os.environ.get("HISTORY_TTL", "3600"))
MAX_PDF_PAGES = int(os.environ.get("MAX_PDF_PAGES", "5"))
MAX_TEXT_CHARS = int(os.environ.get("MAX_TEXT_CHARS", "20000"))
STATE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "state")
OFFSET_FILE = os.path.join(STATE_DIR, "tg_offset")

TEXT_EXT = (".txt", ".md", ".sql", ".csv", ".log", ".json", ".yaml", ".yml", ".xml", ".ini", ".conf")
IMAGE_EXT = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".heic")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger("fb-bot")

VISION_PROMPT = (
    "Внимательно изучи изображение. Ответь на русском языке строго в таком формате:\n\n"
    "ОПИСАНИЕ: что изображено (тип интерфейса, экран, график, таблица, схема, фото — что именно видно).\n"
    "ТЕКСТ: полностью и дословно выпиши весь текст, который виден на изображении "
    "(надписи, заголовки, подписи осей, значения, пункты меню, сообщения об ошибках, SQL-запросы, числа). "
    "Сохраняй исходную формулировку и язык. Если текста нет — напиши «текста нет».\n"
    "СУТЬ: главное, что нужно понять из изображения (например, какая ошибка возникла "
    "или какие данные показаны)."
)

GREETING = (
    "Здравствуйте! Я AI-консультант по платформе Fastboard и базе данных ClickHouse.\n\n"
    "Что я умею:\n"
    "• отвечаю на вопросы по документации Fastboard и ClickHouse со ссылками на источники;\n"
    "• распознаю картинки и скриншоты — вижу, что на них, и считываю текст с изображения "
    "(ошибки, графики, SQL, настройки);\n"
    "• читаю PDF и текстовые файлы (.txt, .md, .sql, .csv, .log).\n\n"
    "Просто задайте вопрос или пришлите скриншот — можно с подписью, что именно интересует.\n\n"
    "Команды: /help — справка, /reset — очистить историю диалога, /status — состояние сервиса."
)


# --- Telegram API ---
def tg(method, **params):
    """Вызов Telegram Bot API с ретраями."""
    for attempt in range(4):
        try:
            r = requests.post(f"{API}/{method}", json=params, timeout=(10, 65))
            data = r.json()
            if not data.get("ok"):
                log.warning("TG %s -> %s", method, str(data)[:300])
            return data
        except requests.RequestException as e:
            log.warning("TG %s network error (%s/4): %s", method, attempt + 1, e)
            time.sleep(2 * (attempt + 1))
    return {"ok": False}


def md_to_html(text):
    """Аккуратная разметка для Telegram: код, жирный, курсив. Остальное — экранируется."""
    blocks = []

    def stash_block(m):
        blocks.append(f"<pre><code>{html.escape(m.group(2))}</code></pre>")
        return f"\x00{len(blocks) - 1}\x00"

    def stash_inline(m):
        blocks.append(f"<code>{html.escape(m.group(1))}</code>")
        return f"\x00{len(blocks) - 1}\x00"

    text = re.sub(r"```(\w+)?\n?(.*?)```", stash_block, text, flags=re.S)
    text = re.sub(r"`([^`\n]+)`", stash_inline, text)
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text, flags=re.S)
    text = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<i>\1</i>", text)
    text = re.sub(r"^(#{1,6})\s*(.+)$", r"<b>\2</b>", text, flags=re.M)
    return re.sub(r"\x00(\d+)\x00", lambda m: blocks[int(m.group(1))], text)


def split_chunks(text, limit=3800):
    """Режет длинный ответ по абзацам/строкам под лимит Telegram."""
    out = []
    while len(text) > limit:
        cut = text.rfind("\n\n", 0, limit)
        if cut < limit // 2:
            cut = text.rfind("\n", 0, limit)
        if cut < limit // 2:
            cut = limit
        out.append(text[:cut])
        text = text[cut:].lstrip("\n")
    if text.strip():
        out.append(text)
    return out


def send(chat_id, text, reply_to=None):
    """Отправка ответа: сначала HTML-разметкой, при ошибке — простым текстом."""
    for part in split_chunks(text):
        res = tg("sendMessage", chat_id=chat_id, text=md_to_html(part),
                 parse_mode="HTML", disable_web_page_preview=True,
                 **({"reply_to_message_id": reply_to} if reply_to else {}))
        if not res.get("ok"):
            tg("sendMessage", chat_id=chat_id, text=part, disable_web_page_preview=True)
        reply_to = None


class Typing:
    """Показывает «печатает…» пока идёт долгий запрос к модели."""

    def __init__(self, chat_id, action="typing"):
        self.chat_id, self.action = chat_id, action
        self._stop = threading.Event()

    def __enter__(self):
        def loop():
            while not self._stop.is_set():
                try:
                    requests.post(f"{API}/sendChatAction",
                                  json={"chat_id": self.chat_id, "action": self.action}, timeout=10)
                except requests.RequestException:
                    pass
                self._stop.wait(4)
        threading.Thread(target=loop, daemon=True).start()
        return self

    def __exit__(self, *exc):
        self._stop.set()


def download_file(file_id):
    """Скачивает файл Telegram в память."""
    info = tg("getFile", file_id=file_id)
    if not info.get("ok"):
        return None, None
    path = info["result"]["file_path"]
    r = requests.get(f"{FILE_API}/{path}", timeout=(10, 120))
    r.raise_for_status()
    return r.content, path


# --- Модель ---
def ollama_chat(messages, images=None, model=None):
    """Запрос к Ollama /api/chat. think=False — модель рассуждающая, без этого ответ пуст."""
    msgs = [dict(m) for m in messages]
    if images:
        msgs[-1]["images"] = images
    options = {"temperature": TEMPERATURE, "num_predict": NUM_PREDICT}
    if NUM_CTX:
        options["num_ctx"] = int(NUM_CTX)
    payload = {
        "model": model or CHAT_MODEL,
        "messages": msgs,
        "stream": False,
        "think": False,
        "options": options,
    }
    r = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=(15, LLM_TIMEOUT))
    r.raise_for_status()
    content = (r.json().get("message") or {}).get("content", "")
    return re.sub(r"<think>.*?</think>", "", content, flags=re.S).strip()


def describe_image(image_bytes, hint=""):
    """Распознавание изображения: что на нём и какой текст на нём написан."""
    b64 = base64.b64encode(image_bytes).decode()
    prompt = VISION_PROMPT + (f"\n\nПользователь уточняет: {hint}" if hint else "")
    return ollama_chat([{"role": "user", "content": prompt}], images=[b64], model=VISION_MODEL)


def pdf_to_images(data):
    """Рендерит первые страницы PDF в PNG для vision-модели."""
    import pymupdf
    doc = pymupdf.open(stream=data, filetype="pdf")
    pages = []
    for page in doc[:MAX_PDF_PAGES]:
        pages.append(page.get_pixmap(dpi=150).tobytes("png"))
    return pages, doc.page_count


# --- RAG ---
class Rag:
    """Поиск по документации. Клиенты создаются один раз и переиспользуются."""

    def __init__(self):
        self.ef = OpenRouterEmbeddingFunction()
        self.chroma = chromadb.PersistentClient(path=VECTORDB_DIR)
        self._cols = {}

    def collections(self):
        for key, name in COLLECTIONS.items():
            if key not in self._cols:
                try:
                    self._cols[key] = self.chroma.get_collection(name, embedding_function=self.ef)
                except Exception as e:
                    log.warning("Коллекция %s недоступна: %s", name, e)
        return list(self._cols.values())

    def search(self, query, top_k=TOP_K):
        chunks = []
        for col in self.collections():
            try:
                chunks.extend(retrieve(col, query, top_k))
            except Exception as e:
                log.warning("Ошибка поиска в %s: %s", col.name, e)
        chunks.sort(key=lambda c: (c[2] is None, c[2] if c[2] is not None else 0))
        return chunks[:top_k]

    def answer(self, question, history=(), extra_context=""):
        chunks = self.search(question)
        context, sources = build_context(chunks) if chunks else ("", [])
        parts = []
        if extra_context:
            parts.append(f"Данные, присланные пользователем (распознано с изображения/файла):\n{extra_context}")
        parts.append(f"Вопрос: {question}")
        parts.append("Контекст из документации:\n\n" + (context or "(релевантных фрагментов не найдено)"))
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages += list(history)
        messages.append({"role": "user", "content": "\n\n".join(parts)})
        reply = ollama_chat(messages)
        if sources:
            reply += "\n\n📚 Источники:\n" + "\n".join(f"  - {s}" for s in sources)
        return reply


# --- История диалога ---
class History:
    def __init__(self):
        self._data = {}
        self._lock = threading.Lock()

    def get(self, chat_id):
        with self._lock:
            item = self._data.get(chat_id)
            if not item or time.time() - item["ts"] > HISTORY_TTL:
                return []
            return list(item["msgs"])

    def add(self, chat_id, user_msg, bot_msg):
        with self._lock:
            item = self._data.setdefault(chat_id, {"msgs": deque(maxlen=HISTORY_TURNS), "ts": 0})
            item["msgs"].append({"role": "user", "content": user_msg[:4000]})
            item["msgs"].append({"role": "assistant", "content": bot_msg[:4000]})
            item["ts"] = time.time()

    def clear(self, chat_id):
        with self._lock:
            self._data.pop(chat_id, None)


rag = Rag()
history = History()


# --- Обработка сообщений ---
def handle_commands(chat_id, text):
    cmd = text.split()[0].split("@")[0].lower()
    if cmd in ("/start", "/help"):
        send(chat_id, GREETING)
        return True
    if cmd == "/reset":
        history.clear(chat_id)
        send(chat_id, "История диалога очищена. Задавайте новый вопрос.")
        return True
    if cmd == "/status":
        try:
            tags = requests.get(f"{OLLAMA_URL}/api/tags", timeout=10).json()
            models = [m["name"] for m in tags.get("models", [])]
            gpu_ok = VISION_MODEL in models
        except requests.RequestException as e:
            models, gpu_ok = [], False
            log.warning("status: %s", e)
        counts = []
        for col in rag.collections():
            try:
                counts.append(f"{col.name}: {col.count()}")
            except Exception:
                counts.append(f"{col.name}: ?")
        send(chat_id,
             f"Модель: {CHAT_MODEL}\n"
             f"GPU-сервер: {'на связи' if gpu_ok else 'недоступен'}\n"
             f"Распознавание изображений: {'включено' if gpu_ok else 'недоступно'}\n"
             f"База знаний — фрагментов:\n  " + "\n  ".join(counts or ["нет коллекций"]))
        return True
    return False


def extract_media(msg):
    """Возвращает (file_id, имя, тип) для фото/документа, иначе (None, None, None)."""
    if msg.get("photo"):
        return max(msg["photo"], key=lambda p: p.get("file_size", 0))["file_id"], "photo.jpg", "image"
    doc = msg.get("document")
    if doc:
        name = (doc.get("file_name") or "file").lower()
        mime = doc.get("mime_type") or ""
        if mime.startswith("image/") or name.endswith(IMAGE_EXT):
            return doc["file_id"], name, "image"
        if mime == "application/pdf" or name.endswith(".pdf"):
            return doc["file_id"], name, "pdf"
        if mime.startswith("text/") or name.endswith(TEXT_EXT):
            return doc["file_id"], name, "text"
        return doc["file_id"], name, "unsupported"
    if msg.get("sticker") or msg.get("video") or msg.get("voice") or msg.get("audio"):
        return None, None, "unsupported"
    return None, None, None


def process(msg):
    chat_id = msg["chat"]["id"]
    mid = msg.get("message_id")
    text = (msg.get("text") or "").strip()
    caption = (msg.get("caption") or "").strip()

    if text.startswith("/") and handle_commands(chat_id, text):
        return

    file_id, name, kind = extract_media(msg)

    if kind == "unsupported":
        send(chat_id, "Пока я работаю с текстом, изображениями (скриншоты, фото), PDF "
                      "и текстовыми файлами. Пришлите, пожалуйста, в одном из этих форматов.")
        return

    if file_id:
        with Typing(chat_id):
            data, path = download_file(file_id)
            if not data:
                send(chat_id, "Не удалось скачать файл. Попробуйте отправить его ещё раз.")
                return
            log.info("chat=%s файл=%s тип=%s размер=%sБ", chat_id, name, kind, len(data))

            if kind == "image":
                recognized = describe_image(data, caption)
                header = "🖼 Распознано на изображении:\n\n" + recognized
            elif kind == "pdf":
                try:
                    pages, total = pdf_to_images(data)
                except Exception as e:
                    log.exception("PDF")
                    send(chat_id, f"Не смог прочитать PDF: {e}")
                    return
                parts = []
                for i, png in enumerate(pages, 1):
                    parts.append(f"[Страница {i}]\n" + describe_image(png, caption))
                recognized = "\n\n".join(parts)
                more = f" (обработаны первые {len(pages)} из {total})" if total > len(pages) else ""
                header = f"📄 Распознано в PDF{more}:\n\n{recognized}"
            else:
                recognized = data.decode("utf-8", errors="replace")[:MAX_TEXT_CHARS]
                header = f"📎 Файл {name} прочитан ({len(recognized)} символов)."

            send(chat_id, header, reply_to=mid)

            question = caption or (
                "Объясни, что показано, и подскажи, что с этим делать в Fastboard/ClickHouse. "
                "Если видна ошибка — объясни причину и как её исправить."
            )
            answer = rag.answer(question, history.get(chat_id), extra_context=recognized)
            send(chat_id, answer)
            history.add(chat_id, f"[файл {name}] {question}\n{recognized[:2000]}", answer)
        return

    if not text:
        send(chat_id, "Напишите вопрос текстом или пришлите скриншот.")
        return

    log.info("chat=%s вопрос=%r", chat_id, text[:120])
    with Typing(chat_id):
        answer = rag.answer(text, history.get(chat_id))
        send(chat_id, answer, reply_to=mid)
        history.add(chat_id, text, answer)


# --- Очередь и цикл опроса ---
jobs = queue.Queue(maxsize=200)


def worker():
    """GPU обслуживает один запрос за раз — обрабатываем сообщения последовательно."""
    while True:
        msg = jobs.get()
        try:
            process(msg)
        except Exception as e:
            log.exception("Ошибка обработки")
            try:
                send(msg["chat"]["id"],
                     "Извините, при обработке запроса произошла ошибка. "
                     f"Попробуйте ещё раз.\n\nДетали: {type(e).__name__}: {str(e)[:200]}")
            except Exception:
                pass
        finally:
            jobs.task_done()


def load_offset():
    try:
        with open(OFFSET_FILE) as f:
            return int(f.read().strip())
    except (OSError, ValueError):
        return 0


def save_offset(offset):
    os.makedirs(STATE_DIR, exist_ok=True)
    tmp = OFFSET_FILE + ".tmp"
    with open(tmp, "w") as f:
        f.write(str(offset))
    os.replace(tmp, OFFSET_FILE)


def main():
    if not TOKEN:
        log.error("Не задан TELEGRAM_BOT_TOKEN (см. .env)")
        sys.exit(1)

    me = tg("getMe")
    if not me.get("ok"):
        log.error("Telegram не принял токен: %s", me)
        sys.exit(1)
    log.info("Бот @%s запущен. Модель: %s", me["result"]["username"], CHAT_MODEL)

    tg("setMyCommands", commands=[
        {"command": "help", "description": "Что умеет бот"},
        {"command": "reset", "description": "Очистить историю диалога"},
        {"command": "status", "description": "Состояние сервиса"},
    ])

    threading.Thread(target=worker, daemon=True).start()

    offset = load_offset()
    while True:
        try:
            r = requests.get(f"{API}/getUpdates",
                             params={"offset": offset, "timeout": 30,
                                     "allowed_updates": json.dumps(["message"])},
                             timeout=(10, 40))
            data = r.json()
            if not data.get("ok"):
                log.warning("getUpdates: %s", str(data)[:200])
                time.sleep(3)
                continue
            for upd in data["result"]:
                offset = upd["update_id"] + 1
                save_offset(offset)
                msg = upd.get("message")
                if msg and not msg.get("from", {}).get("is_bot"):
                    try:
                        jobs.put_nowait(msg)
                    except queue.Full:
                        send(msg["chat"]["id"], "Сейчас много запросов, попробуйте через минуту.")
        except requests.RequestException as e:
            log.warning("Сеть: %s", e)
            time.sleep(5)
        except Exception:
            log.exception("Цикл опроса")
            time.sleep(5)


if __name__ == "__main__":
    main()
