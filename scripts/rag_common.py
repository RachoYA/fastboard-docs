#!/usr/bin/env python3
"""Общая конфигурация и клиент OpenRouter для базы знаний Fastboard/ClickHouse.

Один OpenAI-совместимый эндпоинт OpenRouter обслуживает и эмбеддинги (RAG),
и чат (ответы консультанта). Конфигурация берётся из переменных окружения,
см. `.env.example`.
"""

import os

# Необязательная подгрузка .env (если установлен python-dotenv)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# --- Пути ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
VECTORDB_DIR = os.path.join(BASE_DIR, "vectordb")

# --- Конфигурация OpenRouter ---
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
CHAT_MODEL = os.environ.get("OPENROUTER_CHAT_MODEL", "anthropic/claude-3.5-sonnet")
EMBEDDING_MODEL = os.environ.get("OPENROUTER_EMBEDDING_MODEL", "openai/text-embedding-3-small")

# Атрибуция для рейтингов OpenRouter (необязательно)
_HTTP_REFERER = os.environ.get("OPENROUTER_HTTP_REFERER", "https://github.com/RachoYA/fastboard-docs")
_X_TITLE = os.environ.get("OPENROUTER_X_TITLE", "Fastboard Docs Consultant")


def get_client():
    """Возвращает OpenAI-совместимый клиент, настроенный на OpenRouter."""
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
        default_headers={"HTTP-Referer": _HTTP_REFERER, "X-Title": _X_TITLE},
    )


class OpenRouterEmbeddingFunction:
    """Эмбеддинг-функция для ChromaDB поверх эндпоинта OpenRouter `/embeddings`.

    Совместима с интерфейсом chromadb: реализует `__call__(self, input)` и `name()`.
    """

    def __init__(self, model: str = EMBEDDING_MODEL, batch_size: int = 64):
        self._client = get_client()
        self._model = model
        self._batch_size = max(1, int(batch_size))

    def name(self) -> str:  # требуется chromadb для метаданных коллекции
        return f"openrouter:{self._model}"

    def __call__(self, input):
        # chromadb передаёт список строк под именем 'input'
        texts = [t if isinstance(t, str) else str(t) for t in input]
        embeddings = []
        for i in range(0, len(texts), self._batch_size):
            batch = texts[i:i + self._batch_size]
            resp = self._client.embeddings.create(model=self._model, input=batch)
            # сохраняем исходный порядок
            for item in sorted(resp.data, key=lambda d: d.index):
                embeddings.append(item.embedding)
        return embeddings
