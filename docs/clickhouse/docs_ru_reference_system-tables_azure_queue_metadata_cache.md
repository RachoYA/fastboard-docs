# system.azure_queue_metadata_cache - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/system-tables/azure_queue_metadata_cache


## Описание


## Столбцы

- `zookeeper_path` ([String](https://clickhouse.com/docs/ru/reference/data-types/index)) — Путь к метаданным в ZooKeeper
- `file_path` ([String](https://clickhouse.com/docs/ru/reference/data-types/index)) — Путь к обрабатываемому файлу
- `file_name` ([String](https://clickhouse.com/docs/ru/reference/data-types/index)) — Имя обрабатываемого файла
- `rows_processed` ([UInt64](https://clickhouse.com/docs/ru/reference/data-types/index)) — Текущее количество обработанных строк
- `status` ([String](https://clickhouse.com/docs/ru/reference/data-types/index)) — Статус обработки: Processed, Processing, Failed
- `processing_start_time` ([Nullable(DateTime)](https://clickhouse.com/docs/ru/reference/data-types/index)) — Время начала обработки файла
- `processing_end_time` ([Nullable(DateTime)](https://clickhouse.com/docs/ru/reference/data-types/index)) — Время завершения обработки файла
- `exception` ([String](https://clickhouse.com/docs/ru/reference/data-types/index)) — Исключение, возникшее в процессе обработки
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
