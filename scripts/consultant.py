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
    # Справочник свойств виджетов: плотная таблица, поэтому берём из неё
    # заметно меньше фрагментов, чем из обычных статей (см. SEARCH_LIMITS в боте).
    "settings": "widget_settings",
}

SYSTEM_PROMPT = (
    "Ты — инженер службы заботы Fastboard (BI-платформа) и ClickHouse. Отвечай на "
    "русском языке, кратко и по делу, как технический специалист поддержки.\n\n"
    "Как отвечать:\n"
    "1. Сразу по сути, без вступлений и без пересказа того, что прислал пользователь.\n"
    "2. Если есть ошибка (SQL, ClickHouse, код ошибки, синтаксис, тип данных, "
    "подключение) — обязательно разбери её: что означает, из-за чего возникает и как "
    "исправить, с исправленным примером запроса. ClickHouse и SQL — стандартные "
    "технологии, здесь опирайся на свои знания и отвечай всегда, даже если в контексте "
    "документации ничего похожего нет. Отказ вместо разбора ошибки — недопустим.\n"
    "3. Про устройство интерфейса Fastboard (названия кнопок, вкладок, пунктов меню, "
    "путь в настройках) утверждай только то, что есть в контексте. Не выдумывай названия "
    "и пути. Если в контексте этого нет — не описывай интерфейс: дай суть решения и, "
    "если уместно, предложи уточнить у поддержки.\n"
    "4. Фрагменты контекста могут не относиться к вопросу — тогда просто не используй их "
    "и не упоминай.\n"
    "5. Ссылку на статью добавляй, только если в контексте есть подходящая: "
    "«Рекомендуем ознакомиться со статьёй: <название> — <ссылка>», ссылку бери из "
    "контекста дословно, вместе с якорем на нужный раздел, если он есть. Если подходящей "
    "статьи нет — вообще не пиши про статьи. НИКОГДА не выводи заглушки вида "
    "«<название не указано>» или «<ссылка отсутствует>».\n"
    "7. Не пиши «в базе знаний нет описания», если можешь ответить по существу вопроса "
    "своими знаниями. Эта фраза уместна только для вопросов о конкретных возможностях "
    "Fastboard, которых нет в контексте."
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
        choices=list(COLLECTIONS) + ["both"],
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
