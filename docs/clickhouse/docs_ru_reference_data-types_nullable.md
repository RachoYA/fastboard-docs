# Nullable(T) - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/data-types/nullable

- [Array](https://clickhouse.com/docs/ru/reference/data-types/array) — Не поддерживается
- [Map](https://clickhouse.com/docs/ru/reference/data-types/map) — Не поддерживается
- [Tuple](https://clickhouse.com/docs/ru/reference/data-types/tuple) — Доступна бета-поддержка*
- [Nullable(Tuple(…))](https://clickhouse.com/docs/ru/reference/data-types/tuple#nullable-tuple) поддерживается, если включен параметр `enable_nullable_tuple_type = 1`.

## Особенности хранилища


## Поиск NULL


```
CREATE TABLE nullable (`n` Nullable(UInt32)) ENGINE = MergeTree ORDER BY tuple();

INSERT INTO nullable VALUES (1) (NULL) (2) (NULL);

SELECT n.null FROM nullable;

```


```
┌─n.null─┐
│      0 │
│      1 │
│      0 │
│      1 │
└────────┘

```


## Пример использования


```
CREATE TABLE t_null(x Int8, y Nullable(Int8)) ENGINE TinyLog

```


```
INSERT INTO t_null VALUES (1, NULL), (2, 3)

```


```
SELECT x + y FROM t_null

```


```
┌─plus(x, y)─┐
│       ᴺᵁᴸᴸ │
│          5 │
└────────────┘

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
