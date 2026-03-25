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

## Обновление

```bash
python scripts/scrape_and_index.py
```
