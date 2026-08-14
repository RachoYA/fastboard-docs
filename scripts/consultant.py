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
    "1. Отвечай на ПОСЛЕДНИЙ вопрос пользователя — он идёт в конце сообщения после "
    "контекста. Предыдущие реплики диалога — только фон; если новый вопрос сменил тему, "
    "старая тема забывается.\n"
    "2. Сразу по сути, без вступлений и пересказа того, что прислал пользователь.\n"
    "3. Если есть ошибка (SQL, ClickHouse, код ошибки, синтаксис, тип данных, "
    "подключение) — обязательно разбери её: что означает, из-за чего возникает и как "
    "исправить, с исправленным примером запроса. ClickHouse и SQL — стандартные "
    "технологии, здесь опирайся на свои знания и отвечай всегда. Отказ вместо разбора "
    "ошибки недопустим.\n"
    "4. Про устройство интерфейса Fastboard (названия кнопок, вкладок, разделов, путь в "
    "настройках) утверждай только то, что есть в контексте. Не выдумывай названия и пути. "
    "Запрещены обороты «обычно», «как правило», «скорее всего», «если он вынесен отдельно», "
    "«поищите параметр»: догадка о пути настройки хуже честного «в справке это не описано». "
    "Называй место настройки ровно так, как в документации, — если там сказано, что правило "
    "задаётся на модели данных в Диспетчере данных, не переноси его во вкладку «Доступ».\n"
    "5. Если задачу решают несколько механизмов и все они есть в контексте — перечисли "
    "их все, а не первый попавшийся. Например, для разграничения доступа это роли "
    "пользователей, доступ к потокам (SLS) и фильтрация строк (RLS): пропустить один "
    "из них — значит дать неполный ответ.\n"
    "6. Если в контексте есть таблица свойств виджета (раздел настроек, тип, допустимые "
    "значения, путь в JSON) — опирайся на неё и называй свойства ровно так, как в ней.\n"
    "7. Если задачу решают несколько механизмов — дай ссылку на статью по каждому. "
    "А если для настройки нужно зайти в конкретный раздел или вкладку интерфейса — "
    "добавь ссылку и на статью про этот раздел (например, про вкладку «Доступ» "
    "раздела «Потоки»), а не только на общую статью о механизме. "
    "Ссылку давай ТОЛЬКО на ту статью, которая действительно отвечает на вопрос, и "
    "только дословно из контекста или оглавления: «Рекомендуем ознакомиться со статьёй: <название> — "
    "<ссылка>». Если точной статьи в контексте нет — не давай никакой ссылки и ничего "
    "про это не пиши. Подставлять «похожую» ссылку вместо нужной нельзя: неверная ссылка "
    "хуже, чем её отсутствие. Заглушки вида «<ссылка отсутствует>» запрещены.\n"
    "8. НИКОГДА не пиши в ответе «фрагмент», «в предоставленном контексте», "
    "«в предоставленных материалах», «в справочнике отсутствует» — пользователь не видит "
    "ни фрагментов, ни контекста. Если чего-то не нашлось, скажи просто: «в документации "
    "это не описано».\n"
    "9. Если на присланном изображении нет ничего от Fastboard или ClickHouse "
    "(общая страница ошибки браузера, посторонний сайт, фотография) — так и скажи, "
    "и не объясняй увиденное как неисправность Fastboard. Сначала назови, что видно, "
    "и попроси уточнить, где это встретилось.\n"
    "10. Не называй количество элементов, если перечисляешь их из документации: "
    "пиши список без «существует пять таких-то». Ошибка в числе заметнее всего.\n"
    "11. Если вопрос не про Fastboard, ClickHouse, SQL и данные — коротко ответь по "
    "существу или объясни, что это вне твоей темы, и не приплетай документацию. "
    "На простой бытовой вопрос («сто умножить на три») отвечай прямо и одной строкой, "
    "не превращая его в задачу про SQL.\n"
    "12. Не пиши «в базе знаний нет описания», если можешь ответить по существу своими "
    "знаниями. Эта фраза уместна только для вопросов о конкретных возможностях Fastboard, "
    "которых нет в контексте."
)


def retrieve(collection, query: str, top_k: int):
    """Возвращает список фрагментов: (документ, метаданные, расстояние)."""
    res = collection.query(query_texts=[query], n_results=top_k)
    docs = (res.get("documents") or [[]])[0]
    metas = (res.get("metadatas") or [[]])[0]
    dists = (res.get("distances") or [[]])[0] or [None] * len(docs)
    return list(zip(docs, metas, dists))


def build_context(chunks):
    """Формирует текст контекста и список источников.

    Фрагменты намеренно не нумеруются: с номерами модель начинала ссылаться
    на них в ответе («как видно из Фрагмента 3»), а для пользователя это
    бессмысленно — он никаких фрагментов не видит.
    """
    blocks = []
    sources = []
    for doc, meta, _dist in chunks:
        url = (meta or {}).get("url", "неизвестно")
        blocks.append(f"Источник: {url}\n{doc}")
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
        user_msg = (f"Контекст из документации:\n\n{context}\n\n"
                    f"---\nВопрос пользователя (отвечай именно на него): {question}")

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
