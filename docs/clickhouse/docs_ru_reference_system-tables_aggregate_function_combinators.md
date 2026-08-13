# system.aggregate_function_combinators - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/system-tables/aggregate_function_combinators


## Описание


## Столбцы

- `name` ([String](https://clickhouse.com/docs/ru/reference/data-types/index)) — Название комбинатора.
- `is_internal` ([UInt8](https://clickhouse.com/docs/ru/reference/data-types/index)) — Указывает, предназначен ли этот комбинатор только для внутреннего использования.
- `description` ([String](https://clickhouse.com/docs/ru/reference/data-types/index)) — Краткое описание назначения комбинатора.
- `syntax` ([String](https://clickhouse.com/docs/ru/reference/data-types/index)) — Как комбинатор применяется к имени агрегатной функции.
- `examples` ([String](https://clickhouse.com/docs/ru/reference/data-types/index)) — Примеры использования.
- `introduced_in` ([String](https://clickhouse.com/docs/ru/reference/data-types/index)) — Версия ClickHouse, в которой комбинатор впервые появился, в формате major.minor.
- `related` ([Array(String)](https://clickhouse.com/docs/ru/reference/data-types/index)) — Названия связанных комбинаторов.
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
