#!/usr/bin/env python3
"""Общая конфигурация и клиент OpenRouter для базы знаний Fastboard/ClickHouse.

Один OpenAI-совместимый эндпоинт OpenRouter обслуживает и эмбеддинги (RAG),
и чат (ответы консультанта). Конфигурация берётся из переменных окружения,
см. `.env.example`.
"""

import os
from typing import Any, Dict

# Необязательная подгрузка .env (если установлен python-dotenv)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from chromadb import Documents, EmbeddingFunction, Embeddings

# --- Пути ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
VECTORDB_DIR = os.path.join(BASE_DIR, "vectordb")

# --- Конфигурация OpenRouter ---
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
CHAT_MODEL = os.environ.get("OPENROUTER_CHAT_MODEL", "anthropic/claude-sonnet-4.5")
EMBEDDING_MODEL = os.environ.get("OPENROUTER_EMBEDDING_MODEL", "openai/text-embedding-3-small")

# Сетевые параметры (ретраи/таймаут для устойчивости к 429/5xx/сетевым сбоям)
OPENROUTER_MAX_RETRIES = int(os.environ.get("OPENROUTER_MAX_RETRIES", "5"))
OPENROUTER_TIMEOUT = float(os.environ.get("OPENROUTER_TIMEOUT", "60"))

# Атрибуция для рейтингов OpenRouter (необязательно)
_HTTP_REFERER = os.environ.get("OPENROUTER_HTTP_REFERER", "https://github.com/RachoYA/fastboard-docs")
_X_TITLE = os.environ.get("OPENROUTER_X_TITLE", "Fastboard Docs Consultant")


def get_client():
    """Возвращает OpenAI-совместимый клиент, настроенный на OpenRouter.

    Клиент SDK сам делает экспоненциальный backoff для 429/5xx/сетевых ошибок
    (до OPENROUTER_MAX_RETRIES попыток).
    """
    try:
        from openai import OpenAI
    except ImportError as e:
        raise RuntimeError(
            "Нужен пакет 'openai' (>=1.0). Установите: pip install -r requirements.txt"
        ) from e

    if not OPENROUTER_API_KEY:
        raise RuntimeError(
            "Не задан OPENROUTER_API_KEY. Скопируйте .env.example в .env и впишите ключ, "
            "либо экспортируйте переменную окружения OPENROUTER_API_KEY."
        )

    return OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url=OPENROUTER_BASE_URL,
        max_retries=OPENROUTER_MAX_RETRIES,
        timeout=OPENROUTER_TIMEOUT,
        default_headers={"HTTP-Referer": _HTTP_REFERER, "X-Title": _X_TITLE},
    )


class OpenRouterEmbeddingFunction(EmbeddingFunction[Documents]):
    """Эмбеддинг-функция ChromaDB поверх эндпоинта OpenRouter `/embeddings`.

    Реализует контракт ChromaDB: `__call__`, `name`, `get_config`,
    `build_from_config` — чтобы конфигурацию можно было сохранить в коллекции и
    корректно восстановить при повторном открытии.
    """

    def __init__(self, model: str = EMBEDDING_MODEL, batch_size: int = 64):
        self._client = get_client()
        self._model = model
        self._batch_size = max(1, int(batch_size))

    @property
    def model(self) -> str:
        return self._model

    def __call__(self, input: Documents) -> Embeddings:
        texts = [t if isinstance(t, str) else str(t) for t in input]
        embeddings: Embeddings = []
        for i in range(0, len(texts), self._batch_size):
            batch = texts[i:i + self._batch_size]
            resp = self._client.embeddings.create(model=self._model, input=batch)
            # сохраняем исходный порядок
            for item in sorted(resp.data, key=lambda d: d.index):
                embeddings.append(item.embedding)
        return embeddings

    @staticmethod
    def name() -> str:
        return "openrouter"

    def get_config(self) -> Dict[str, Any]:
        return {"model": self._model, "batch_size": self._batch_size}

    @staticmethod
    def build_from_config(config: Dict[str, Any]) -> "OpenRouterEmbeddingFunction":
        return OpenRouterEmbeddingFunction(
            model=config.get("model", EMBEDDING_MODEL),
            batch_size=config.get("batch_size", 64),
        )
