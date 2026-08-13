# system.azure_queue_settings - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/system-tables/azure_queue_settings


## Описание


## Столбцы

- `database` ([String](https://clickhouse.com/docs/ru/reference/data-types/index)) — База данных таблицы с движком AzureQueue.
- `table` ([String](https://clickhouse.com/docs/ru/reference/data-types/index)) — Имя таблицы с движком AzureQueue.
- `name` ([String](https://clickhouse.com/docs/ru/reference/data-types/index)) — Имя настройки.
- `value` ([String](https://clickhouse.com/docs/ru/reference/data-types/index)) — Значение настройки.
- `type` ([String](https://clickhouse.com/docs/ru/reference/data-types/index)) — Тип настройки (строковое значение, зависящее от реализации).
- `changed` ([UInt8](https://clickhouse.com/docs/ru/reference/data-types/index)) — 1, если настройка была явно задана в конфигурации или явно изменена.
- `description` ([String](https://clickhouse.com/docs/ru/reference/data-types/index)) — Описание настройки.
- `alterable` ([UInt8](https://clickhouse.com/docs/ru/reference/data-types/index)) — Показывает, может ли текущий пользователь изменить настройку с помощью ALTER TABLE MODIFY SETTING: 0 — текущий пользователь не может изменить настройку, 1 — текущий пользователь может изменить настройку.
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
