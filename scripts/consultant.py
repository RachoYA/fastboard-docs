#!/usr/bin/env python3
"""AI-консультант по документации Fastboard и ClickHouse (RAG поверх OpenRouter).

Принимает вопрос, ищет релевантные фрагменты в ChromaDB (эмбеддинги OpenRouter)
и генерирует ответ чат-моделью через OpenRouter.

Примеры:
    python scripts/consultant.py "Как создать дашборд в Fastboard?"
    python scripts/consultant.py --source clickhouse "Что такое движок MergeTree?"
    python scripts/consultant.py            # интерактивный режим
"""

import argparse
import sys

import chromadb

from rag_common import (
    VECTORDB_DIR,
    CHAT_MODEL,
    CHAT_EXTRA_BODY,
    EMBEDDING_MODEL,
    get_client,
    OpenRouterEmbeddingFunction,
)

COLLECTIONS = {
    "fastboard": "fastboard_docs",
    "clickhouse": "clickhouse_docs",
}

SYSTEM_PROMPT = (
    "Ты — AI-консультант службы заботы по платформе Fastboard (BI) и базе данных "
    "ClickHouse. Отвечай на русском языке, коротко и по делу, опираясь ТОЛЬКО на "
    "приведённый ниже контекст из документации. Если в контексте нет ответа — честно "
    "скажи об этом и не выдумывай. Где уместно, приводи примеры SQL.\n\n"
    "Правила ответа:\n"
    "1. Сразу отвечай по сути вопроса, без вступлений и пересказа того, что прислал "
    "пользователь.\n"
    "2. НИЧЕГО НЕ ПРИДУМЫВАЙ. Разрешено утверждать только то, что дословно есть в "
    "контексте. Запрещено: догадываться о названиях кнопок, полей, пунктов меню и "
    "настроек; описывать шаги «по аналогии с другими BI-системами»; писать «обычно», "
    "«как правило», «скорее всего», «поищите параметр». Если точного ответа в "
    "контексте нет — так и напиши: «В базе знаний нет описания этого сценария», "
    "и предложи ближайшую подходящую статью, не выдумывая её содержание.\n"
    "3. Не перечисляй названия разделов справки как ответ — это не ответ.\n"
    "4. В конце обязательно порекомендуй одну-две самые подходящие статьи базы знаний "
    "в формате: «Рекомендуем ознакомиться со статьёй: <название> — <ссылка>». "
    "Ссылки бери только из контекста; если в контексте есть якорь на нужный подраздел "
    "(например, #продвинутые-триггеры), указывай ссылку вместе с якорем. "
    "Не сочиняй ссылки и не меняй их.\n"
    "5. Если задача решается конкретным виджетом или инструментом Fastboard "
    "(например, виджетом «Айфрейм» или триггерами) — прямо назови его, но только если "
    "он упомянут в контексте."
)


def retrieve(collection, query: str, top_k: int):
    """Возвращает список фрагментов: (документ, метаданные, расстояние)."""
    res = collection.query(query_texts=[query], n_results=top_k)
    docs = (res.get("documents") or [[]])[0]
    metas = (res.get("metadatas") or [[]])[0]
    dists = (res.get("distances") or [[]])[0] or [None] * len(docs)
    return list(zip(docs, metas, dists))


def build_context(chunks):
    """Формирует текст контекста и список источников."""
    blocks = []
    sources = []
    for i, (doc, meta, _dist) in enumerate(chunks, 1):
        url = (meta or {}).get("url", "неизвестно")
        blocks.append(f"[Фрагмент {i}] Источник: {url}\n{doc}")
        if url not in sources:
            sources.append(url)
    return "\n\n---\n\n".join(blocks), sources


class Consultant:
    """Держит клиентов OpenRouter/ChromaDB, чтобы не пересоздавать их на каждый вопрос."""

    def __init__(self):
        self.ef = OpenRouterEmbeddingFunction()
        self.chroma = chromadb.PersistentClient(path=VECTORDB_DIR)
        self.client = get_client()

    def answer(self, question: str, sources_filter: str, top_k: int, model: str) -> str:
        targets = (
            list(COLLECTIONS.values())
            if sources_filter == "both"
            else [COLLECTIONS[sources_filter]]
        )

        chunks = []
        missing = []
        for name in targets:
            try:
                col = self.chroma.get_collection(name, embedding_function=self.ef)
            except Exception:
                missing.append(name)
                print(
                    f"⚠️  Коллекция '{name}' не найдена. Сначала запустите индексацию:\n"
                    f"    python scripts/scrape_and_index.py",
                    file=sys.stderr,
                )
                continue
            chunks.extend(retrieve(col, question, top_k))

        if not chunks:
            return ("Не нашёл релевантных данных. Проверьте, что база проиндексирована "
                    "(scripts/scrape_and_index.py).")

        # самые близкие сверху (меньше расстояние = ближе); None — в конец
        chunks.sort(key=lambda c: (c[2] is None, c[2] if c[2] is not None else 0))
        chunks = chunks[:top_k]

        context, sources = build_context(chunks)
        user_msg = f"Вопрос: {question}\n\nКонтекст из документации:\n\n{context}"

        resp = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.2,
            extra_body=CHAT_EXTRA_BODY or None,
        )
        reply = resp.choices[0].message.content or ""

        if missing:
            reply = (f"⚠️ Часть источников недоступна ({', '.join(missing)}) — "
                     f"ответ может быть неполным.\n\n" + reply)
        if sources:
            reply += "\n\n📚 Источники:\n" + "\n".join(f"  - {s}" for s in sources)
        return reply


def main():
    parser = argparse.ArgumentParser(
        description="AI-консультант по документации Fastboard и ClickHouse (OpenRouter)."
    )
    parser.add_argument("question", nargs="*", help="Вопрос. Без аргументов — интерактивный режим.")
    parser.add_argument(
        "--source",
        choices=["fastboard", "clickhouse", "both"],
        default="both",
        help="В каких коллекциях искать (по умолчанию: both).",
    )
    parser.add_argument("--top-k", type=int, default=6, help="Сколько фрагментов брать в контекст.")
    parser.add_argument("--model", default=CHAT_MODEL, help="Модель OpenRouter для ответа.")
    args = parser.parse_args()

    print(f"🤖 Консультант: чат={args.model}, эмбеддинги={EMBEDDING_MODEL}\n")

    consultant = Consultant()

    if args.question:
        print(consultant.answer(" ".join(args.question), args.source, args.top_k, args.model))
        return

    print("Интерактивный режим. Пустая строка или Ctrl+C — выход.\n")
    try:
        while True:
            q = input("❓ Вопрос: ").strip()
            if not q:
                break
            print("\n" + consultant.answer(q, args.source, args.top_k, args.model) + "\n")
    except (KeyboardInterrupt, EOFError):
        print("\nДо встречи!")


if __name__ == "__main__":
    main()
