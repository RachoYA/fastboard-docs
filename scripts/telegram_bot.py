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

from rag_common import BASE_DIR, VECTORDB_DIR, CHAT_MODEL, OpenRouterEmbeddingFunction
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
# Оглавление документации в контексте каждого ответа: 144 строки «название — ссылка».
# Нужно, чтобы бот рекомендовал точную статью, даже если её фрагмент не попал в
# выдачу поиска — иначе он давал ссылку на «похожую» статью.
INDEX_IN_CONTEXT = os.environ.get("INDEX_IN_CONTEXT", "1") == "1"

# Кто может пользоваться ботом. Пусто = все: один воркер и один слот GPU,
# поэтому публичная ссылка без ограничений выстроит очередь из посторонних.
ALLOWED_CHATS = {c.strip() for c in os.environ.get("ALLOWED_CHATS", "").split(",") if c.strip()}
RATE_LIMIT_PER_HOUR = int(os.environ.get("RATE_LIMIT_PER_HOUR", "30"))
SUPPORT_CONTACT = os.environ.get("SUPPORT_CONTACT", "").strip()
# Кэш ответов: чем больше пользователей, тем чаще повторяются одни и те же
# вопросы, а каждый ответ стоит около минуты монопольного времени GPU.
ANSWER_CACHE_TTL = float(os.environ.get("ANSWER_CACHE_TTL", "86400"))
ANSWER_CACHE_SIZE = int(os.environ.get("ANSWER_CACHE_SIZE", "500"))
WORKERS = int(os.environ.get("WORKERS", "2"))
QUEUE_SIZE = int(os.environ.get("QUEUE_SIZE", "25"))
# Стриминг ответа черновиком Telegram: текст виден по мере генерации.
DRAFT_STREAMING = os.environ.get("DRAFT_STREAMING", "1") == "1"
DRAFT_INTERVAL = float(os.environ.get("DRAFT_INTERVAL", "0.4"))
DRAFT_MAX_CHARS = int(os.environ.get("DRAFT_MAX_CHARS", "3900"))
HISTORY_TURNS = int(os.environ.get("HISTORY_TURNS", "6"))
HISTORY_TTL = float(os.environ.get("HISTORY_TTL", "3600"))
MAX_PDF_PAGES = int(os.environ.get("MAX_PDF_PAGES", "3"))
MAX_TEXT_CHARS = int(os.environ.get("MAX_TEXT_CHARS", "20000"))
STATE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "state")
OFFSET_FILE = os.path.join(STATE_DIR, "tg_offset")

TEXT_EXT = (".txt", ".md", ".sql", ".csv", ".log", ".json", ".yaml", ".yml", ".xml", ".ini", ".conf")
IMAGE_EXT = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".heic")

def mask_secrets(text):
    """Прячет токен бота в тексте: он попадает в URL внутри исключений requests."""
    return text.replace(TOKEN, "<токен>") if TOKEN and TOKEN in text else text


class MaskingFormatter(logging.Formatter):
    """Маскирует токен в готовой строке журнала, включая тексты исключений.

    requests кладёт полный URL в сообщение об ошибке, поэтому строка вида
    «Max retries exceeded with url: /bot<токен>/getUpdates» уносила токен
    в systemd-журнал открытым текстом.
    """

    def format(self, record):
        return mask_secrets(super().format(record))


_handler = logging.StreamHandler(sys.stdout)
_handler.setFormatter(MaskingFormatter("%(asctime)s %(levelname)s %(message)s"))
logging.basicConfig(level=logging.INFO, handlers=[_handler])
log = logging.getLogger("fb-bot")

GREETING = (
    "Здравствуйте! Я AI-консультант по платформе Fastboard и базе данных ClickHouse.\n\n"
    "Что я умею:\n"
    "• отвечаю на вопросы по документации Fastboard и ClickHouse со ссылками на источники;\n"
    "• распознаю картинки и скриншоты — вижу, что на них, и считываю текст с изображения "
    "(ошибки, графики, SQL, настройки);\n"
    "• читаю PDF и текстовые файлы (.txt, .md, .sql, .csv, .log).\n\n"
    "Просто задайте вопрос или пришлите скриншот — можно с подписью, что именно интересует.\n\n"
    "Я AI-консультант и отвечаю по документации: могу ошибаться, важное перепроверяйте "
    "по статьям, ссылки на которые я привожу. Нужен живой специалист — команда /human.\n\n"
    "Команды: /help — справка, /human — связаться с человеком, /reset — очистить историю "
    "диалога, /status — состояние сервиса."
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
        self.draft_id = (int(time.time() * 1000) ^ threading.get_ident()) % 2147483647
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


def build_article_index():
    """Оглавление «Название статьи — ссылка» по страницам, которые реально в базе.

    Берём список из манифеста, а не из каталога docs: на диске остаются файлы
    от прежних схем обхода и исключённого раздела /gostech/, и по ним модель
    выдавала пользователю ссылки на страницы-заглушки.
    """
    try:
        with open(os.path.join(BASE_DIR, "scrape_manifest.json"), encoding="utf-8") as f:
            pages = json.load(f).get("pages", {})
    except (OSError, json.JSONDecodeError) as e:
        log.warning("Не удалось прочитать манифест для оглавления: %s", e)
        return ""

    entries = []
    for url, meta in sorted(pages.items()):
        if not url.startswith("http") or meta.get("collection") == "widget_settings":
            continue
        path = os.path.join(BASE_DIR, meta.get("file", ""))
        title = ""
        try:
            with open(path, encoding="utf-8") as f:
                title = f.readline().lstrip("# ").split("|")[0].strip()
        except OSError:
            continue
        if title:
            entries.append(f"{title} — {url}")
    log.info("оглавление документации: %s статей", len(entries))
    return "\n".join(entries)


class Rag:
    """Поиск по документации. Клиенты создаются один раз и переиспользуются."""

    def __init__(self):
        self.ef = OpenRouterEmbeddingFunction()
        self.chroma = chromadb.PersistentClient(path=VECTORDB_DIR)
        self._cols = {}
        self._index = ""
        self._index_ts = 0.0

    def article_index(self):
        """Оглавление с суточным обновлением — база пополняется по ночам."""
        if INDEX_IN_CONTEXT and time.time() - self._index_ts > 3600:
            self._index = build_article_index()
            self._index_ts = time.time()
        return self._index

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
        # Лишний вызов модели стоит около восьми секунд, поэтому короткий
        # односоставный вопрос ищем как есть.
        compound = len(question) > 120 or question.count("?") > 1 or " и " in question.lower()
        if not QUERY_SPLIT or not compound:
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
        return self.search_all(query, top_k, split=False)

    def search_all(self, question, top_k=TOP_K, split=True):
        """Ищет по подзапросам и объединяет результаты без повторов.

        Эмбеддинги всех подзапросов считаются одним обращением к модели, а
        каждая коллекция опрашивается один раз сразу всеми векторами: раньше
        это были девять последовательных вызовов на один вопрос.
        """
        queries = self.make_queries(question) if split else [question]
        try:
            vectors = self.ef(queries)
        except Exception as e:
            log.warning("Не удалось посчитать эмбеддинги: %s", e)
            return []

        # Вопрос про JSON и свойства виджета обслуживает справочник настроек:
        # ему нужно больше места в выдаче и мягче порог близости, иначе ответ
        # собирается по обычным статьям и путает соседние свойства.
        about_settings = any(word in question.lower() for word in
                             ("json", "свойств", "настройк", "параметр", "settings"))
        settings_limit = SETTINGS_TOP_K * 2 if about_settings else SETTINGS_TOP_K
        settings_max_distance = (SETTINGS_MAX_DISTANCE + 0.15 if about_settings
                                 else SETTINGS_MAX_DISTANCE)

        best = {}
        for key, col in self.collections():
            limit = settings_limit if key == "settings" else top_k
            try:
                res = col.query(query_embeddings=vectors, n_results=limit)
            except Exception as e:
                log.warning("Ошибка поиска в %s: %s", col.name, e)
                continue
            documents = res.get("documents") or []
            metadatas = res.get("metadatas") or []
            distances = res.get("distances") or []
            for i in range(len(documents)):
                dists = distances[i] if i < len(distances) else [None] * len(documents[i])
                for doc, meta, dist in zip(documents[i], metadatas[i], dists):
                    ident = (key, (meta or {}).get("url"), (meta or {}).get("chunk"))
                    known = best.get(ident)
                    if known is None or (dist is not None and dist < known[1][2]):
                        best[ident] = (key, (doc, meta, dist))

        by_distance = lambda item: (item[2] is None, item[2] if item[2] is not None else 0)
        chunks = sorted((c for k, c in best.values() if k != "settings"), key=by_distance)
        reference = sorted((c for k, c in best.values() if k == "settings"), key=by_distance)
        relevant = [c for c in reference
                    if c[2] is None or c[2] <= settings_max_distance][:settings_limit]
        return chunks[:top_k] + relevant

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
        # Оглавление (около 13 тысяч токенов) держим в системном сообщении, а не в
        # пользовательском: так начало промпта неизменно от запроса к запросу и
        # попадает в кэш модели. Когда оглавление лежало в конце, вместе с
        # контекстом и вопросом, оно пересчитывалось заново на каждый вопрос.
        system = SYSTEM_PROMPT
        index = self.article_index()
        if index:
            system += ("\n\nОглавление документации (названия статей и точные ссылки). "
                       "Ссылку для рекомендации бери отсюда, но содержимое статьи, "
                       "которой нет в контексте вопроса, не пересказывай:\n" + index)
        messages = [{"role": "system", "content": system}]
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
            if not item:
                return []
            if time.time() - item["ts"] > HISTORY_TTL:
                # Просроченные диалоги именно удаляем: раньше они оставались
                # в памяти навсегда и бот тяжелел с каждым новым чатом.
                del self._data[chat_id]
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


class AnswerCache:
    """Готовые ответы на повторяющиеся вопросы.

    Сбрасывается, когда обновилась база знаний: иначе после ночной
    переиндексации бот сутки отдавал бы ответы по старой документации.
    """

    def __init__(self):
        self._data = {}
        self._lock = threading.Lock()
        self._stamp = None

    @staticmethod
    def _key(question):
        return " ".join(question.lower().split())

    def _base_stamp(self):
        try:
            return os.path.getmtime(os.path.join(BASE_DIR, "scrape_manifest.json"))
        except OSError:
            return None

    def get(self, question):
        stamp = self._base_stamp()
        with self._lock:
            if stamp != self._stamp:
                self._data.clear()
                self._stamp = stamp
                return None
            item = self._data.get(self._key(question))
            if not item or time.time() - item[1] > ANSWER_CACHE_TTL:
                return None
            return item[0]

    def put(self, question, answer):
        with self._lock:
            if len(self._data) >= ANSWER_CACHE_SIZE:
                oldest = min(self._data, key=lambda k: self._data[k][1])
                del self._data[oldest]
            self._data[self._key(question)] = (answer, time.time())


class RateLimiter:
    """Не больше RATE_LIMIT_PER_HOUR вопросов на чат в час."""

    def __init__(self):
        self._hits = {}
        self._lock = threading.Lock()

    def allow(self, chat_id):
        if RATE_LIMIT_PER_HOUR <= 0:
            return True, 0
        now = time.time()
        with self._lock:
            hits = [t for t in self._hits.get(chat_id, []) if now - t < 3600]
            if len(hits) >= RATE_LIMIT_PER_HOUR:
                self._hits[chat_id] = hits
                return False, int((3600 - (now - hits[0])) / 60) + 1
            hits.append(now)
            self._hits[chat_id] = hits
            return True, 0


rag = Rag()
history = History()
limiter = RateLimiter()
answer_cache = AnswerCache()


# --- Обработка сообщений ---
def handle_commands(chat_id, text):
    cmd = text.split()[0].split("@")[0].lower()
    if cmd in ("/start", "/help"):
        send(chat_id, GREETING)
        return True
    if cmd == "/human":
        send(chat_id, "Передаю вопрос живому специалисту.\n\n" + (
            SUPPORT_CONTACT if SUPPORT_CONTACT
            else "Напишите вашему менеджеру Fastboard — он подключит поддержку. "
                 "А я останусь на связи по вопросам документации."))
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

        # Кэш только для обычных текстовых вопросов вне диалога: ответ с
        # картинкой или с учётом предыдущих реплик у каждого свой.
        cacheable = not recognized and not history.get(chat_id)
        cached = answer_cache.get(question) if cacheable else None
        if cached:
            log.info("chat=%s ответ из кэша", chat_id)
            answer = cached
        else:
            with Draft(chat_id) as draft:
                answer = rag.answer(question, history.get(chat_id), extra_context=recognized,
                                    search_query=f"{hint} {recognized[:1500]}".strip(),
                                    on_delta=draft.update)
            if cacheable and len(answer) > 40:
                answer_cache.put(question, answer)
        send(chat_id, answer, reply_to=reply_to)
        history.add(chat_id, f"{question}\n{recognized[:2000]}".strip(), answer)


# --- Склейка сообщений, очередь и цикл опроса ---
jobs = queue.Queue(maxsize=QUEUE_SIZE)

# Сообщения, пришедшие подряд, — один вопрос. Ждём паузу в разговоре и только
# потом отвечаем, одним ответом на всю пачку.
AGGREGATE_WINDOW = float(os.environ.get("AGGREGATE_WINDOW", "2.5"))
_pending = {}
_pending_lock = threading.Lock()


def enqueue(msg):
    """Кладёт сообщение в буфер чата; в работу пачка уйдёт после паузы."""
    chat_id = msg["chat"]["id"]

    if ALLOWED_CHATS and str(chat_id) not in ALLOWED_CHATS:
        log.info("chat=%s не в списке доступа — отказ", chat_id)
        send(chat_id, "Этот бот доступен ограниченному кругу пользователей. "
                      "За доступом обратитесь к своему менеджеру Fastboard.")
        return

    allowed, minutes = limiter.allow(chat_id)
    if not allowed:
        log.info("chat=%s превысил лимит вопросов", chat_id)
        send(chat_id, f"Вы задали много вопросов подряд. Продолжим через {minutes} мин — "
                      "так очередь к модели остаётся живой для всех.")
        return

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
                send(batch[0]["chat"]["id"],
                     "Сейчас очередь вопросов заполнена — модель отвечает по одному. "
                     "Задайте вопрос через несколько минут.")
        time.sleep(0.3)


def worker():
    """Генерацию GPU всё равно сериализует, но поиск, скачивание файлов и
    отправку в Telegram несколько потоков делают параллельно."""
    while True:
        batch = jobs.get()
        try:
            process(batch)
        except Exception as e:
            log.exception("Ошибка обработки")
            try:
                send(batch[0]["chat"]["id"],
                     "Извините, при обработке запроса произошла ошибка. "
                     f"Попробуйте ещё раз.\n\nДетали: {mask_secrets(f'{type(e).__name__}: {e}')[:200]}")
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
        {"command": "human", "description": "Связаться с живым специалистом"},
        {"command": "reset", "description": "Очистить историю диалога"},
        {"command": "status", "description": "Состояние сервиса"},
    ])

    for _ in range(max(1, WORKERS)):
        threading.Thread(target=worker, daemon=True).start()
    threading.Thread(target=collector, daemon=True).start()
    log.info("рабочих потоков: %s, очередь: %s", WORKERS, QUEUE_SIZE)

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
