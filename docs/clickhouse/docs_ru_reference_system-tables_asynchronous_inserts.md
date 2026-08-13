# system.asynchronous_inserts - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/system-tables/asynchronous_inserts


## Описание


## Столбцы

- `query` ([String](https://clickhouse.com/docs/ru/reference/data-types/index)) — Текст запроса.
- `database` ([String](https://clickhouse.com/docs/ru/reference/data-types/index)) — Имя базы данных.
- `table` ([String](https://clickhouse.com/docs/ru/reference/data-types/index)) — Имя таблицы.
- `format` ([String](https://clickhouse.com/docs/ru/reference/data-types/index)) — Имя формата.
- `first_update` ([DateTime64(6)](https://clickhouse.com/docs/ru/reference/data-types/index)) — Время первой вставки с точностью до микросекунд.
- `total_bytes` ([UInt64](https://clickhouse.com/docs/ru/reference/data-types/index)) — Общее количество байтов, ожидающих в очереди.
- `entries.query_id` ([Array(String)](https://clickhouse.com/docs/ru/reference/data-types/index)) — Массив идентификаторов запросов на вставку, ожидающих в очереди.
- `entries.bytes` ([Array(UInt64)](https://clickhouse.com/docs/ru/reference/data-types/index)) — Массив значений в байтах для каждого запроса на вставку, ожидающего в очереди.

## Пример


```
SELECT * FROM system.asynchronous_inserts LIMIT 1 \G;

```


```
Row 1:
──────
query:            INSERT INTO public.data_guess (user_id, datasource_id, timestamp, path, type, num, str) FORMAT CSV
database:         public
table:            data_guess
format:           CSV
first_update:     2023-06-08 10:08:54.199606
total_bytes:      133223
entries.query_id: ['b46cd4c4-0269-4d0b-99f5-d27668c6102e']
entries.bytes:    [133223]

```


## См. также

- [system.query_log](https://clickhouse.com/docs/ru/reference/system-tables/query_log) — Описание системной таблицы `query_log`, содержащей общую информацию о выполнении запросов.
- [system.asynchronous_insert_log](https://clickhouse.com/docs/ru/reference/system-tables/asynchronous_insert_log) — Эта таблица содержит информацию о выполненных асинхронных вставках.
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
