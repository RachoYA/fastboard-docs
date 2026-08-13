#!/usr/bin/env python3
"""Работа с локальной моделью Ollama: чат и распознавание изображений.

Общий модуль для бота (ответы, разбор присланных картинок) и индексатора
(вытаскивание текста из скриншотов документации).

Используется нативный API Ollama, а не OpenAI-совместимый: он принимает
картинки и умеет отключать режим рассуждений (`think: false`), без чего
qwen3.6 отдаёт пустой ответ.
"""

import base64
import os
import re

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
LLM_TIMEOUT = float(os.environ.get("LLM_TIMEOUT", "600"))

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
    resp = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={"model": model or CHAT_MODEL, "messages": msgs,
              "stream": False, "think": False, "options": options},
        timeout=(15, LLM_TIMEOUT),
    )
    resp.raise_for_status()
    content = (resp.json().get("message") or {}).get("content", "")
    return re.sub(r"<think>.*?</think>", "", content, flags=re.S).strip()


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
