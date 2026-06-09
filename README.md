# Fastboard & ClickHouse Documentation Knowledge Base

Scraped and structured documentation for **Fastboard** (BI platform) and **ClickHouse** (database).

> Автоматически собрано и проиндексировано AI-консультантом Fastboard.  
> Последнее обновление: 2026-03-25

## Структура

```
docs/
├── fastboard/          # Документация Fastboard (help.fastboard.online/user/)
│   ├── dashboard/      # Конструктор дашбордов
│   ├── widgets/        # Библиотека виджетов
│   ├── data/           # Диспетчер данных
│   ├── sql/            # SQL-редактор
│   ├── access/         # SLS / PLS / RLS
│   ├── admin/          # Администрирование
│   └── quickstart/     # Быстрый старт
└── clickhouse/         # Документация ClickHouse (clickhouse.com/docs/ru)
    ├── data-types/     # Типы данных
    ├── functions/      # Функции
    ├── engines/        # Движки таблиц (MergeTree и др.)
    ├── statements/     # SQL-операторы
    └── getting-started/ # Начало работы
```

## Источники

- **Fastboard**: https://help.fastboard.online/user/
- **ClickHouse (RU)**: https://clickhouse.com/docs/ru

## Статистика

| Источник | Страниц |
|---|---|
| Fastboard | 145 |
| ClickHouse | 105 |
| **Итого** | **250** |

## Использование

Документы в формате Markdown. Можно использовать для:
- RAG / семантического поиска (ChromaDB, Qdrant и др.)
- Обучения моделей
- Справочника по API

## AI-консультант (OpenRouter)

Эмбеддинги для RAG и ответы консультанта работают через [OpenRouter](https://openrouter.ai)
(единый OpenAI-совместимый API).

### Установка

```bash
pip install -r requirements.txt
cp .env.example .env   # впишите OPENROUTER_API_KEY
```

Модели настраиваются в `.env`:

| Переменная | Назначение | По умолчанию |
|---|---|---|
| `OPENROUTER_API_KEY` | Ключ API OpenRouter | — |
| `OPENROUTER_CHAT_MODEL` | Модель ответов | `anthropic/claude-3.5-sonnet` |
| `OPENROUTER_EMBEDDING_MODEL` | Модель эмбеддингов | `openai/text-embedding-3-small` |

### Индексация

```bash
python scripts/scrape_and_index.py
```

> Скрипт заново скрапит документацию и строит векторную базу `vectordb/` на
> эмбеддингах OpenRouter. При смене модели эмбеддингов индекс нужно пересобрать.

### Запрос к консультанту

```bash
# одиночный вопрос
python scripts/consultant.py "Как создать дашборд в Fastboard?"

# поиск только по ClickHouse
python scripts/consultant.py --source clickhouse "Что такое движок MergeTree?"

# интерактивный режим
python scripts/consultant.py
```
