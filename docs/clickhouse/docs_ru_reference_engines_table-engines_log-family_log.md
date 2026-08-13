# Табличный движок Log - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/log-family/log


## Создание таблицы


```
CREATE TABLE [IF NOT EXISTS] [db.]table_name [ON CLUSTER cluster]
(
    column1_name [type1] [DEFAULT|MATERIALIZED|ALIAS expr1],
    column2_name [type2] [DEFAULT|MATERIALIZED|ALIAS expr2],
    ...
) ENGINE = Log

```


## Запись данных

- `<column>.bin`: файл данных для каждого столбца, содержащий сериализованные и сжатые данные. `__marks.mrk`: файл меток, в котором хранятся смещения и количество строк для каждого вставленного блока данных. Метки используются для эффективного выполнения запросов, позволяя движку пропускать нерелевантные блоки данных при чтении.

### Процесс записи

- Данные сериализуются и сжимаются в блоки.
- Для каждого столбца сжатые данные дописываются в соответствующий файл `<column>.bin`.
- В файл `__marks.mrk` добавляются соответствующие записи, фиксирующие смещение и количество строк для вновь вставленных данных.

## Чтение данных


## Пример использования


```
CREATE TABLE log_table
(
    timestamp DateTime,
    message_type String,
    message String
)
ENGINE = Log

```


```
INSERT INTO log_table VALUES (now(),'REGULAR','The first regular message')
INSERT INTO log_table VALUES (now(),'REGULAR','The second regular message'),(now(),'WARNING','The first warning message')

```


```
SELECT * FROM log_table

```


```
┌───────────timestamp─┬─message_type─┬─message────────────────────┐
│ 2019-01-18 14:27:32 │ REGULAR      │ The second regular message │
│ 2019-01-18 14:34:53 │ WARNING      │ The first warning message  │
└─────────────────────┴──────────────┴────────────────────────────┘
┌───────────timestamp─┬─message_type─┬─message───────────────────┐
│ 2019-01-18 14:23:43 │ REGULAR      │ The first regular message │
└─────────────────────┴──────────────┴───────────────────────────┘

```


```
SELECT * FROM log_table ORDER BY timestamp

```


```
┌───────────timestamp─┬─message_type─┬─message────────────────────┐
│ 2019-01-18 14:23:43 │ REGULAR      │ The first regular message  │
│ 2019-01-18 14:27:32 │ REGULAR      │ The second regular message │
│ 2019-01-18 14:34:53 │ WARNING      │ The first warning message  │
└─────────────────────┴──────────────┴────────────────────────────┘

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
