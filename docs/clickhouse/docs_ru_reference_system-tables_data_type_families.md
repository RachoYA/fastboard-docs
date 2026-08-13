# system.data_type_families - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/system-tables/data_type_families


## Описание


## Столбцы

- `name` ([String](https://clickhouse.com/docs/ru/reference/data-types/index)) — Имя типа данных.
- `case_insensitive` ([UInt8](https://clickhouse.com/docs/ru/reference/data-types/index)) — Свойство, показывающее, можно ли использовать имя типа данных в запросе без учёта регистра. Например, `Date` и `date` оба допустимы.
- `alias_to` ([String](https://clickhouse.com/docs/ru/reference/data-types/index)) — Имя типа данных, для которого `name` является алиасом.
- `description` ([String](https://clickhouse.com/docs/ru/reference/data-types/index)) — Общее описание типа данных.
- `syntax` ([String](https://clickhouse.com/docs/ru/reference/data-types/index)) — Как записывается тип данных в запросе.
- `examples` ([String](https://clickhouse.com/docs/ru/reference/data-types/index)) — Примеры использования.
- `introduced_in` ([String](https://clickhouse.com/docs/ru/reference/data-types/index)) — Версия ClickHouse, в которой тип данных был впервые представлен, в формате major.minor.
- `related` ([Array(String)](https://clickhouse.com/docs/ru/reference/data-types/index)) — Имена связанных типов данных.

## Пример


```
SELECT name, case_insensitive, alias_to FROM system.data_type_families WHERE alias_to = 'String'

```


```
┌─name───────┬─case_insensitive─┬─alias_to─┐
│ LONGBLOB   │                1 │ String   │
│ LONGTEXT   │                1 │ String   │
│ TINYTEXT   │                1 │ String   │
│ TEXT       │                1 │ String   │
│ VARCHAR    │                1 │ String   │
│ MEDIUMBLOB │                1 │ String   │
│ BLOB       │                1 │ String   │
│ TINYBLOB   │                1 │ String   │
│ CHAR       │                1 │ String   │
│ MEDIUMTEXT │                1 │ String   │
└────────────┴──────────────────┴──────────┘

```


## См. также

- [Синтаксис](https://clickhouse.com/docs/ru/reference/syntax) — Сведения о поддерживаемом синтаксисе.
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
