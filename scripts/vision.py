#!/usr/bin/env python3
"""Работа с локальной моделью Ollama: чат и распознавание изображений.

Общий модуль для бота (ответы, разбор присланных картинок) и индексатора
(вытаскивание текста из скриншотов документации).

Используется нативный API Ollama, а не OpenAI-совместимый: он принимает
картинки и умеет отключать режим рассуждений (`think: false`), без чего
qwen3.6 отдаёт пустой ответ.
"""

import base64
import json
import os
import re
import time

import requests

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))
except ImportError:
    pass

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
VISION_MODEL = os.environ.get("VISION_MODEL", os.environ.get("OPENROUTER_CHAT_MODEL", "qwen3.6:27b-256k"))
CHAT_MODEL = os.environ.get("OPENROUTER_CHAT_MODEL", VISION_MODEL)
# Пусто = не переопределять контекст: модель на GPU уже загружена с большим
# контекстом, а смена num_ctx заставила бы Ollama перезагрузить модель.
NUM_CTX = os.environ.get("NUM_CTX", "").strip()
NUM_PREDICT = int(os.environ.get("NUM_PREDICT", "1400"))
TEMPERATURE = float(os.environ.get("TEMPERATURE", "0.2"))
# Один зависший запрос блокировал очередь на десять минут: при деградации
# скорости генерации таймаут в 600 секунд гарантированно вырабатывался целиком.
LLM_TIMEOUT = float(os.environ.get("LLM_TIMEOUT", "240"))

DESCRIBE_PROMPT = (
    "Внимательно изучи изображение. Ответь на русском языке строго в таком формате:\n\n"
    "ОПИСАНИЕ: что изображено (тип интерфейса, экран, график, таблица, схема, фото — что именно видно).\n"
    "ТЕКСТ: полностью и дословно выпиши весь текст, который виден на изображении "
    "(надписи, заголовки, подписи осей, значения, пункты меню, сообщения об ошибках, SQL-запросы, числа). "
    "Сохраняй исходную формулировку и язык. Если текста нет — напиши «текста нет».\n"
    "СУТЬ: главное, что нужно понять из изображения (например, какая ошибка возникла "
    "или какие данные показаны)."
)

# Для индексации: нужен только полезный текст, без рассуждений о стиле картинки.
OCR_PROMPT = (
    "Это скриншот из документации BI-платформы Fastboard. Выпиши на русском языке:\n"
    "1) весь видимый текст дословно — названия полей, кнопок, пунктов меню, вкладок, "
    "подписи, значения, формулы, SQL;\n"
    "2) одной строкой — что показывает скриншот.\n"
    "Только текст с картинки и краткое пояснение, без вступлений и без домыслов. "
    "Если текста на изображении нет — ответь «нет текста»."
)


# Слот генерации на GPU один и делится с другими сервисами, поэтому запрос
# может не уложиться в таймаут просто из-за чужой очереди. Один повтор дешевле,
# чем потерянный вопрос пользователя.
RETRIES = int(os.environ.get("LLM_RETRIES", "1"))


def _with_retry(call, what):
    last = None
    for attempt in range(RETRIES + 1):
        try:
            return call()
        except (requests.Timeout, requests.ConnectionError) as e:
            last = e
            if attempt < RETRIES:
                print(f"  повтор запроса к модели ({what}): {type(e).__name__}")
                time.sleep(2)
    raise last


def ollama_chat(messages, images=None, model=None, num_predict=None, temperature=None):
    """Запрос к Ollama /api/chat. think=False обязателен: модель рассуждающая."""
    msgs = [dict(m) for m in messages]
    if images:
        msgs[-1]["images"] = images
    options = {
        "temperature": TEMPERATURE if temperature is None else temperature,
        "num_predict": NUM_PREDICT if num_predict is None else num_predict,
    }
    if NUM_CTX:
        options["num_ctx"] = int(NUM_CTX)
    def call():
        resp = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={"model": model or CHAT_MODEL, "messages": msgs,
                  "stream": False, "think": False, "options": options},
            timeout=(15, LLM_TIMEOUT),
        )
        resp.raise_for_status()
        return resp

    content = (_with_retry(call, "ответ").json().get("message") or {}).get("content", "")
    return re.sub(r"<think>.*?</think>", "", content, flags=re.S).strip()


def ollama_chat_stream(messages, model=None, num_predict=None, temperature=None, on_delta=None):
    """То же, что ollama_chat, но с потоковой выдачей.

    on_delta(накопленный_текст) вызывается по мере генерации — чтобы показывать
    ответ в чате, пока модель ещё пишет. Возвращает полный текст.
    """
    options = {
        "temperature": TEMPERATURE if temperature is None else temperature,
        "num_predict": NUM_PREDICT if num_predict is None else num_predict,
    }
    if NUM_CTX:
        options["num_ctx"] = int(NUM_CTX)

    parts = []

    def open_stream():
        return requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={"model": model or CHAT_MODEL, "messages": [dict(m) for m in messages],
                  "stream": True, "think": False, "options": options},
            timeout=(15, LLM_TIMEOUT), stream=True)

    # Повтор имеет смысл только пока не пришло ни одного куска ответа:
    # иначе пользователь увидел бы начало ответа дважды.
    with _with_retry(open_stream, "поток") as resp:
        resp.raise_for_status()
        for line in resp.iter_lines(decode_unicode=True):
            if not line:
                continue
            try:
                chunk = json.loads(line)
            except json.JSONDecodeError:
                continue
            piece = (chunk.get("message") or {}).get("content", "")
            if piece:
                parts.append(piece)
                if on_delta:
                    try:
                        on_delta("".join(parts))
                    except Exception:
                        pass  # проблемы с показом не должны рвать генерацию
            if chunk.get("done"):
                break
    return re.sub(r"<think>.*?</think>", "", "".join(parts), flags=re.S).strip()


def describe_image(image_bytes, hint=""):
    """Разбор картинки, присланной пользователем: что на ней и какой текст."""
    prompt = DESCRIBE_PROMPT + (f"\n\nПользователь уточняет: {hint}" if hint else "")
    return ollama_chat([{"role": "user", "content": prompt}],
                       images=[base64.b64encode(image_bytes).decode()], model=VISION_MODEL)


def ocr_image(image_bytes, num_predict=700):
    """Текст со скриншота документации — для индексации в базу знаний."""
    return ollama_chat([{"role": "user", "content": OCR_PROMPT}],
                       images=[base64.b64encode(image_bytes).decode()],
                       model=VISION_MODEL, num_predict=num_predict)
