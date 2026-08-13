#!/usr/bin/env python3
"""Telegram-бот AI-консультанта по документации Fastboard и ClickHouse.

Текст — ответ по документации (RAG поверх ChromaDB). Картинки, скриншоты и PDF —
распознавание через vision-модель (описание + извлечение текста с изображения),
затем ответ по документации с учётом распознанного.

Модель работает локально на GPU-сервере через Ollama (SSH-туннель на 127.0.0.1:11434).
Запускается как systemd-сервис, см. deploy/.
"""

import html
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
from vision import OLLAMA_URL, VISION_MODEL, describe_image, ollama_chat, ollama_chat_stream

# --- Конфигурация ---
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
API = f"https://api.telegram.org/bot{TOKEN}"
FILE_API = f"https://api.telegram.org/file/bot{TOKEN}"

TOP_K = int(os.environ.get("RAG_TOP_K", "10"))
# Справочник настроек — плотная таблица на тысячи строк: без отдельного лимита
# он вытеснил бы из выдачи обычные статьи справки.
SETTINGS_TOP_K = int(os.environ.get("SETTINGS_TOP_K", "4"))
# И только если он вообще близок к вопросу: иначе таблица свойств виджетов
# подмешивалась к вопросам про доступ, роли и прочее, где она не при чём.
SETTINGS_MAX_DISTANCE = float(os.environ.get("SETTINGS_MAX_DISTANCE", "0.95"))
# Разбиение вопроса на отдельные поисковые запросы. В вопросе вида «директор
# видит все отчёты, а менеджер только один и только по Сибири» два разных
# механизма, и один общий вектор находил только второй из них.
QUERY_SPLIT = os.environ.get("QUERY_SPLIT", "1") == "1"
MAX_QUERIES = int(os.environ.get("MAX_QUERIES", "3"))
# Стриминг ответа черновиком Telegram: текст виден по мере генерации.
DRAFT_STREAMING = os.environ.get("DRAFT_STREAMING", "1") == "1"
DRAFT_INTERVAL = float(os.environ.get("DRAFT_INTERVAL", "0.4"))
DRAFT_MAX_CHARS = int(os.environ.get("DRAFT_MAX_CHARS", "3900"))
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


class Draft:
    """Черновик Telegram (sendMessageDraft, Bot API 10.0) — стриминг ответа.

    Пока модель пишет, текст проявляется в чате. Отправка идёт отдельным
    потоком: сеть до Telegram не должна тормозить чтение потока от модели.
    Черновик в истории не сохраняется — итог уходит обычным сообщением.
    """

    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.draft_id = int(time.time() * 1000) % 2147483647
        self._text = ""
        self._shown = ""
        self._stop = threading.Event()

    def _push(self, text):
        try:
            requests.post(f"{API}/sendMessageDraft",
                          json={"chat_id": self.chat_id, "draft_id": self.draft_id, "text": text},
                          timeout=10)
        except requests.RequestException:
            pass  # стриминг — украшение: сбой показа не должен ломать ответ

    def update(self, text):
        """Вызывается на каждом кусочке ответа: только запоминает, без сети."""
        self._text = text

    def __enter__(self):
        if not DRAFT_STREAMING:
            return self

        def loop():
            while not self._stop.is_set():
                text = self._text
                if text != self._shown and 0 < len(text) <= DRAFT_MAX_CHARS:
                    self._shown = text
                    self._push(text)
                self._stop.wait(DRAFT_INTERVAL)
        threading.Thread(target=loop, daemon=True).start()
        return self

    def __exit__(self, *exc):
        self._stop.set()
        if DRAFT_STREAMING and self._shown:
            self._push("")   # убрать черновик перед итоговым сообщением


def download_file(file_id):
    """Скачивает файл Telegram в память."""
    info = tg("getFile", file_id=file_id)
    if not info.get("ok"):
        return None, None
    path = info["result"]["file_path"]
    r = requests.get(f"{FILE_API}/{path}", timeout=(10, 120))
    r.raise_for_status()
    return r.content, path


def pdf_to_images(data):
    """Рендерит первые страницы PDF в PNG для vision-модели."""
    import pymupdf
    doc = pymupdf.open(stream=data, filetype="pdf")
    pages = []
    for page in doc[:MAX_PDF_PAGES]:
        pages.append(page.get_pixmap(dpi=150).tobytes("png"))
    return pages, doc.page_count


# --- RAG ---
QUERY_PROMPT = (
    "Пользователь спрашивает службу заботы BI-платформы Fastboard (визуализации, "
    "дашборды, доступы, SQL, ClickHouse). Составь от одного до {n} коротких поисковых "
    "запросов к документации, которые нужны, чтобы полностью ответить на его вопрос. "
    "Если в вопросе несколько задач — по запросу на каждую. Пиши терминами документации. "
    "Каждый запрос с новой строки, без нумерации, пояснений и кавычек.\n\n"
    "Вопрос: {question}"
)


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
        return list(self._cols.items())

    def make_queries(self, question):
        """Разбивает вопрос на поисковые запросы; при сбое ищет как есть."""
        if not QUERY_SPLIT or len(question) < 25:
            return [question]
        try:
            raw = ollama_chat(
                [{"role": "user", "content": QUERY_PROMPT.format(n=MAX_QUERIES, question=question[:2000])}],
                num_predict=160, temperature=0.1)
        except Exception as e:
            log.warning("Не удалось разбить вопрос на запросы: %s", e)
            return [question]

        queries = [line.strip(" -•*\t") for line in raw.splitlines() if line.strip()]
        queries = [q for q in queries if 3 < len(q) < 200][:MAX_QUERIES]
        log.info("поисковые запросы: %s", queries)
        return queries or [question]

    def search(self, query, top_k=TOP_K):
        chunks, reference = [], []
        for key, col in self.collections():
            limit = SETTINGS_TOP_K if key == "settings" else top_k
            try:
                found = retrieve(col, query, limit)
            except Exception as e:
                log.warning("Ошибка поиска в %s: %s", col.name, e)
                continue
            (reference if key == "settings" else chunks).extend(found)

        by_distance = lambda c: (c[2] is None, c[2] if c[2] is not None else 0)
        chunks.sort(key=by_distance)
        reference.sort(key=by_distance)
        # Справочник добавляется к статьям, а не конкурирует с ними за места
        relevant = [c for c in reference
                    if c[2] is None or c[2] <= SETTINGS_MAX_DISTANCE][:SETTINGS_TOP_K]
        return chunks[:top_k] + relevant

    def search_all(self, question, top_k=TOP_K):
        """Ищет по каждому подзапросу и объединяет результаты без повторов."""
        queries = self.make_queries(question)
        if len(queries) == 1:
            return self.search(queries[0], top_k)

        best = {}
        for query in queries:
            for chunk in self.search(query, top_k):
                doc, meta, dist = chunk
                key = ((meta or {}).get("url"), (meta or {}).get("chunk"))
                if key not in best or (dist is not None and dist < best[key][2]):
                    best[key] = chunk
        found = sorted(best.values(), key=lambda c: (c[2] is None, c[2] if c[2] is not None else 0))
        return found[:top_k + SETTINGS_TOP_K]

    def answer(self, question, history=(), extra_context="", search_query=None, on_delta=None):
        chunks = self.search_all(search_query or question)
        context, _sources = build_context(chunks) if chunks else ("", [])
        # Вопрос идёт последним: когда он был в начале, модель после длинного
        # контекста цеплялась за предыдущую тему диалога и отвечала на прошлый вопрос.
        parts = ["Контекст из документации:\n\n" + (context or "(подходящих материалов не нашлось)")]
        if extra_context:
            parts.append(
                "Пользователь прислал изображение или файл. Вот что на нём "
                "(пользователь это уже видел — пересказывать содержимое не нужно, "
                "используй как условие задачи):\n" + extra_context)
        parts.append(f"---\nВопрос пользователя (отвечай именно на него): {question}")
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages += list(history)
        messages.append({"role": "user", "content": "\n\n".join(parts)})
        # Ссылки не приклеиваем списком: нерелевантные фрагменты давали мусорные
        # «источники». Нужную статью модель рекомендует сама — по системному промпту.
        if on_delta:
            return ollama_chat_stream(messages, on_delta=on_delta)
        return ollama_chat(messages)


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
        for _key, col in rag.collections():
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


def read_media(msg, hint):
    """Скачивает вложение и возвращает распознанный текст (или None, если нечего)."""
    file_id, name, kind = extract_media(msg)
    if not file_id:
        return None, name, kind

    data, _path = download_file(file_id)
    if not data:
        return None, name, "error"
    log.info("файл=%s тип=%s размер=%sБ", name, kind, len(data))

    if kind == "image":
        return describe_image(data, hint), name, kind
    if kind == "pdf":
        pages, total = pdf_to_images(data)
        parts = [f"[Страница {i}]\n" + describe_image(png, hint) for i, png in enumerate(pages, 1)]
        if total > len(pages):
            log.info("PDF: обработаны первые %s из %s страниц", len(pages), total)
        return "\n\n".join(parts), name, kind
    return data.decode("utf-8", errors="replace")[:MAX_TEXT_CHARS], name, kind


def process(batch):
    """Обрабатывает пачку сообщений как один вопрос и отвечает один раз.

    Сообщения, отправленные подряд (текст + скриншот, несколько картинок,
    мысль в двух сообщениях), — это один контекст, а не несколько вопросов.
    """
    chat_id = batch[0]["chat"]["id"]
    reply_to = batch[-1].get("message_id")

    # Команда в пачке выполняется сразу и отдельно от остального
    for msg in batch:
        text = (msg.get("text") or "").strip()
        if text.startswith("/") and handle_commands(chat_id, text):
            return

    texts = []
    for msg in batch:
        for field in ("text", "caption"):
            value = (msg.get(field) or "").strip()
            if value and not value.startswith("/"):
                texts.append(value)
    hint = "\n".join(texts)

    with Typing(chat_id):
        recognized_parts = []
        unsupported = False
        for msg in batch:
            try:
                recognized, name, kind = read_media(msg, hint)
            except Exception:
                log.exception("Не удалось разобрать вложение")
                send(chat_id, "Не смог прочитать вложение. Попробуйте прислать его ещё раз "
                              "или другим форматом.")
                return
            if kind == "unsupported":
                unsupported = True
            elif kind == "error":
                send(chat_id, "Не удалось скачать файл. Попробуйте отправить его ещё раз.")
                return
            elif recognized:
                label = f"[{name}]" if len(batch) > 1 else ""
                recognized_parts.append(f"{label}\n{recognized}".strip())

        if not recognized_parts and not texts:
            send(chat_id, "Пока я работаю с текстом, изображениями (скриншоты, фото), PDF "
                          "и текстовыми файлами."
                 if unsupported else "Напишите вопрос текстом или пришлите скриншот.")
            return

        recognized = "\n\n".join(recognized_parts)
        question = hint or (
            "Что делать в ситуации на изображении? Если видна ошибка — объясни "
            "причину и как её исправить средствами Fastboard/ClickHouse."
        )
        log.info("chat=%s сообщений=%s вопрос=%r вложений=%s",
                 chat_id, len(batch), question[:120], len(recognized_parts))

        with Draft(chat_id) as draft:
            answer = rag.answer(question, history.get(chat_id), extra_context=recognized,
                                search_query=f"{hint} {recognized[:1500]}".strip(),
                                on_delta=draft.update)
        send(chat_id, answer, reply_to=reply_to)
        history.add(chat_id, f"{question}\n{recognized[:2000]}".strip(), answer)


# --- Склейка сообщений, очередь и цикл опроса ---
jobs = queue.Queue(maxsize=200)

# Сообщения, пришедшие подряд, — один вопрос. Ждём паузу в разговоре и только
# потом отвечаем, одним ответом на всю пачку.
AGGREGATE_WINDOW = float(os.environ.get("AGGREGATE_WINDOW", "2.5"))
_pending = {}
_pending_lock = threading.Lock()


def enqueue(msg):
    """Кладёт сообщение в буфер чата; в работу пачка уйдёт после паузы."""
    with _pending_lock:
        item = _pending.setdefault(msg["chat"]["id"], {"msgs": [], "last": 0.0})
        item["msgs"].append(msg)
        item["last"] = time.time()


def collector():
    """Отдаёт в работу те чаты, где пользователь замолчал дольше паузы."""
    while True:
        ready = []
        now = time.time()
        with _pending_lock:
            for chat_id, item in list(_pending.items()):
                if now - item["last"] >= AGGREGATE_WINDOW:
                    ready.append(item["msgs"])
                    del _pending[chat_id]
        for batch in ready:
            try:
                jobs.put_nowait(batch)
            except queue.Full:
                send(batch[0]["chat"]["id"], "Сейчас много запросов, попробуйте через минуту.")
        time.sleep(0.3)


def worker():
    """GPU обслуживает один запрос за раз — обрабатываем пачки последовательно."""
    while True:
        batch = jobs.get()
        try:
            process(batch)
        except Exception as e:
            log.exception("Ошибка обработки")
            try:
                send(batch[0]["chat"]["id"],
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
    threading.Thread(target=collector, daemon=True).start()

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
                    enqueue(msg)
        except requests.RequestException as e:
            log.warning("Сеть: %s", e)
            time.sleep(5)
        except Exception:
            log.exception("Цикл опроса")
            time.sleep(5)


if __name__ == "__main__":
    main()
