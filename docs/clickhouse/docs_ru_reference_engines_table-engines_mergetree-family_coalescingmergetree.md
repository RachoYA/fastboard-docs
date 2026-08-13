# Движок таблицы CoalescingMergeTree - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/coalescingmergetree


## Создание таблицы


```
CREATE TABLE [IF NOT EXISTS] [db.]table_name [ON CLUSTER cluster]
(
    name1 [type1] [DEFAULT|MATERIALIZED|ALIAS expr1],
    name2 [type2] [DEFAULT|MATERIALIZED|ALIAS expr2],
    ...
) ENGINE = CoalescingMergeTree([columns])
[PARTITION BY expr]
[ORDER BY expr]
[SAMPLE BY expr]
[SETTINGS name=value, ...]

```


### Параметры CoalescingMergeTree


#### Столбцы


### Секции запроса


## Пример использования


```
CREATE TABLE test_table
(
    key UInt64,
    value_int Nullable(UInt32),
    value_string Nullable(String),
    value_date Nullable(Date)
)
ENGINE = CoalescingMergeTree()
ORDER BY key

```


```
INSERT INTO test_table VALUES(1, NULL, NULL, '2025-01-01'), (2, 10, 'test', NULL);
INSERT INTO test_table VALUES(1, 42, 'win', '2025-02-01');
INSERT INTO test_table(key, value_date) VALUES(2, '2025-02-01');

```


```
SELECT * FROM test_table ORDER BY key;

```


```
┌─key─┬─value_int─┬─value_string─┬─value_date─┐
│   1 │        42 │ win          │ 2025-02-01 │
│   1 │      ᴺᵁᴸᴸ │ ᴺᵁᴸᴸ         │ 2025-01-01 │
│   2 │      ᴺᵁᴸᴸ │ ᴺᵁᴸᴸ         │ 2025-02-01 │
│   2 │        10 │ test         │       ᴺᵁᴸᴸ │
└─────┴───────────┴──────────────┴────────────┘

```


```
SELECT * FROM test_table FINAL ORDER BY key;

```


```
┌─key─┬─value_int─┬─value_string─┬─value_date─┐
│   1 │        42 │ win          │ 2025-02-01 │
│   2 │        10 │ test         │ 2025-02-01 │
└─────┴───────────┴──────────────┴────────────┘

```


```
SELECT key, last_value(value_int), last_value(value_string), last_value(value_date)  FROM test_table GROUP BY key; -- Не рекомендуется.

```


## Агрегация элементов Tuple

- Подстолбцы, входящие в `Tuple` в ключе сортировки или ключе партиционирования, исключаются из коалесценции.
- Если указан `columns`, коалесценции подвергаются только подстолбцы перечисленных столбцов `Tuple`.

```
CREATE TABLE coalescing_tuples
(
    key UInt64,
    data Tuple(
        value_a Nullable(UInt64),
        value_b Nullable(String),
        nested Tuple(
            value_c Nullable(UInt64)
        )
    )
) ENGINE = CoalescingMergeTree()
ORDER BY key
SETTINGS allow_tuple_element_aggregation = 1;

INSERT INTO coalescing_tuples VALUES (1, (100, NULL, (NULL)));
INSERT INTO coalescing_tuples VALUES (1, (NULL, 'hello', (42)));

SELECT key, data.value_a, data.value_b, data.nested.value_c FROM coalescing_tuples FINAL;

```


```
┌─key─┬─data.value_a─┬─data.value_b─┬─data.nested.value_c─┐
│   1 │          100 │ hello        │                  42 │
└─────┴──────────────┴──────────────┴─────────────────────┘

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
