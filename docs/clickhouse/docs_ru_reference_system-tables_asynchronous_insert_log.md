# system.asynchronous_insert_log - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/system-tables/asynchronous_insert_log


## Описание


## Столбцы

- `hostname` ([LowCardinality(String)](https://clickhouse.com/docs/ru/reference/data-types/lowcardinality)) — Имя хоста сервера, выполняющего запрос.
- `event_date` ([Date](https://clickhouse.com/docs/ru/reference/data-types/date)) — Дата, когда произошла асинхронная вставка.
- `event_time` ([DateTime](https://clickhouse.com/docs/ru/reference/data-types/datetime)) — Дата и время, когда асинхронная вставка завершилась.
- `event_time_microseconds` ([DateTime64(6)](https://clickhouse.com/docs/ru/reference/data-types/datetime64)) — Дата и время, когда асинхронная вставка завершилась, с точностью до микросекунд.
- `query` ([String](https://clickhouse.com/docs/ru/reference/data-types/string)) — Строка запроса.
- `database` ([LowCardinality(String)](https://clickhouse.com/docs/ru/reference/data-types/lowcardinality)) — Имя базы данных, в которой находится таблица.
- `table` ([LowCardinality(String)](https://clickhouse.com/docs/ru/reference/data-types/lowcardinality)) — Имя таблицы.
- `format` ([LowCardinality(String)](https://clickhouse.com/docs/ru/reference/data-types/lowcardinality)) — Имя формата.
- `query_id` ([String](https://clickhouse.com/docs/ru/reference/data-types/string)) — Идентификатор исходного запроса.
- `bytes` ([UInt64](https://clickhouse.com/docs/ru/reference/data-types/int-uint)) — Количество вставленных байтов.
- `rows` ([UInt64](https://clickhouse.com/docs/ru/reference/data-types/int-uint)) — Количество вставленных строк.
- `exception` ([String](https://clickhouse.com/docs/ru/reference/data-types/string)) — Сообщение об исключении.
- `status` ([Enum8(‘Ok’ = 0, ‘ParsingError’ = 1, ‘FlushError’ = 2)](https://clickhouse.com/docs/ru/reference/data-types/enum)) — Статус вставки. Значения: ‘Ok’ = 0 — успешная вставка, ‘ParsingError’ = 1 — исключение при разборе данных, ‘FlushError’ = 2 — исключение при сбросе данных.
- `data_kind` ([Enum8(‘Parsed’ = 0, ‘Preprocessed’ = 1)](https://clickhouse.com/docs/ru/reference/data-types/enum)) — Состояние данных. Значения: ‘Parsed’ и ‘Preprocessed’.
- `flush_time` ([DateTime](https://clickhouse.com/docs/ru/reference/data-types/datetime)) — Дата и время, когда произошел сброс.
- `flush_time_microseconds` ([DateTime64(6)](https://clickhouse.com/docs/ru/reference/data-types/datetime64)) — Дата и время, когда произошел сброс, с точностью до микросекунд.
- `flush_query_id` ([String](https://clickhouse.com/docs/ru/reference/data-types/string)) — Идентификатор запроса сброса.
- `timeout_milliseconds` ([UInt64](https://clickhouse.com/docs/ru/reference/data-types/int-uint)) — Адаптивный тайм-аут, рассчитанный для этой записи.

## Пример


```
SELECT * FROM system.asynchronous_insert_log LIMIT 1 \G;

```


```
hostname:                clickhouse.eu-central1.internal
event_date:              2023-06-08
event_time:              2023-06-08 10:08:53
event_time_microseconds: 2023-06-08 10:08:53.199516
query:                   INSERT INTO public.data_guess (user_id, datasource_id, timestamp, path, type, num, str) FORMAT CSV
database:                public
table:                   data_guess
format:                  CSV
query_id:                b46cd4c4-0269-4d0b-99f5-d27668c6102e
bytes:                   133223
exception:
status:                  Ok
flush_time:              2023-06-08 10:08:55
flush_time_microseconds: 2023-06-08 10:08:55.139676
flush_query_id:          cd2c1e43-83f5-49dc-92e4-2fbc7f8d3716

```


## См. также

- [system.query_log](https://clickhouse.com/docs/ru/reference/system-tables/query_log) — Описание системной таблицы `query_log`, содержащей общую информацию о выполнении запросов.
- [system.asynchronous_inserts](https://clickhouse.com/docs/ru/reference/system-tables/asynchronous_inserts) — Эта таблица содержит информацию об асинхронных вставках, ожидающих выполнения в очереди.
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
