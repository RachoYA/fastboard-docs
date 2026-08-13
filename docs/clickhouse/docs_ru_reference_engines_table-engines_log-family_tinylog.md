# TinyLog — движок таблицы - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/log-family/tinylog


## Характеристики

- **Более простая структура**: В отличие от движка Log, TinyLog не использует файлы меток. Это упрощает структуру, но также ограничивает возможности оптимизации производительности для больших наборов данных.
- **Запросы в одном потоке**: Запросы к таблицам TinyLog выполняются в одном потоке, что делает этот движок подходящим для сравнительно небольших таблиц — обычно до 1 000 000 строк.
- **Эффективен для небольших таблиц**: Благодаря простоте движок TinyLog удобен при работе с большим количеством небольших таблиц, так как требует меньше файловых операций по сравнению с движком Log.

## Создание таблицы


```
CREATE TABLE [IF NOT EXISTS] [db.]table_name [ON CLUSTER cluster]
(
    column1_name [type1] [DEFAULT|MATERIALIZED|ALIAS expr1],
    column2_name [type2] [DEFAULT|MATERIALIZED|ALIAS expr2],
    ...
) ENGINE = TinyLog

```


## Запись данных

- `<column>.bin`: файл данных для каждого столбца, содержащий сериализованные и сжатые данные.

## Пример использования


```
CREATE TABLE tiny_log_table
(
    timestamp DateTime,
    message_type String,
    message String
)
ENGINE = TinyLog

```


```
INSERT INTO tiny_log_table VALUES (now(),'REGULAR','The first regular message')
INSERT INTO tiny_log_table VALUES (now(),'REGULAR','The second regular message'),(now(),'WARNING','The first warning message')

```


```
SELECT * FROM tiny_log_table

```


```
┌───────────timestamp─┬─message_type─┬─message────────────────────┐
│ 2024-12-10 13:11:58 │ REGULAR      │ The first regular message  │
│ 2024-12-10 13:12:12 │ REGULAR      │ The second regular message │
│ 2024-12-10 13:12:12 │ WARNING      │ The first warning message  │
└─────────────────────┴──────────────┴────────────────────────────┘

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
