# system.azure_queue_log - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/system-tables/azure_queue_log

- `hostname` ([LowCardinality(String)](https://clickhouse.com/docs/ru/reference/data-types/lowcardinality)) — Имя хоста
- `event_date` ([Date](https://clickhouse.com/docs/ru/reference/data-types/date)) — Дата события при записи этой строки Log
- `event_time` ([DateTime](https://clickhouse.com/docs/ru/reference/data-types/datetime)) — Время события при записи этой строки Log
- `database` ([String](https://clickhouse.com/docs/ru/reference/data-types/string)) — Имя базы данных, в которой находится таблица очереди (`S3Queue` или `AzureQueue`).
- `table` ([String](https://clickhouse.com/docs/ru/reference/data-types/string)) — Имя таблицы очереди (`S3Queue` или `AzureQueue`).
- `uuid` ([String](https://clickhouse.com/docs/ru/reference/data-types/string)) — UUID таблицы очереди (`S3Queue` или `AzureQueue`).
- `file_name` ([String](https://clickhouse.com/docs/ru/reference/data-types/string)) — Имя обрабатываемого файла.
- `rows_processed` ([UInt64](https://clickhouse.com/docs/ru/reference/data-types/int-uint)) — Количество обработанных строк.
- `status` ([Enum8(‘Processed’ = 0, ‘Failed’ = 1)](https://clickhouse.com/docs/ru/reference/data-types/enum)) — Статус обрабатываемого файла.
- `processing_start_time` ([Nullable(DateTime)](https://clickhouse.com/docs/ru/reference/data-types/nullable)) — Время начала обработки файла.
- `processing_end_time` ([Nullable(DateTime)](https://clickhouse.com/docs/ru/reference/data-types/nullable)) — Время окончания обработки файла.
- `exception` ([String](https://clickhouse.com/docs/ru/reference/data-types/string)) — Сообщение об исключении, если оно возникло.
- `commit_id` ([UInt64](https://clickhouse.com/docs/ru/reference/data-types/int-uint)) — Идентификатор транзакции, в которой был зафиксирован этот файл.
- `commit_time` ([DateTime](https://clickhouse.com/docs/ru/reference/data-types/datetime)) — Время фиксации файла в Keeper (как ошибочного или обработанного).
- `transaction_start_time` ([DateTime](https://clickhouse.com/docs/ru/reference/data-types/datetime)) — Время начала всей транзакции обработки.
- `get_object_time_ms` ([UInt64](https://clickhouse.com/docs/ru/reference/data-types/int-uint)) — Время, потребовавшееся для поиска объекта в Объектном хранилище.
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
