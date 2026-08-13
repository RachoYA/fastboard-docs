# Функции для работы со значениями типа Nullable - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/functions/regular-functions/functions-for-nulls


## assumeNotNull


```
assumeNotNull(x)

```

- `x` — Исходное значение любого типа `Nullable`. [`Nullable(T)`](https://clickhouse.com/docs/ru/reference/data-types/nullable)

```
CREATE TABLE t_null (x Int8, y Nullable(Int8))
ENGINE=MergeTree()
ORDER BY x;

INSERT INTO t_null VALUES (1, NULL), (2, 3);

SELECT assumeNotNull(y) FROM t_null;
SELECT toTypeName(assumeNotNull(y)) FROM t_null;

```


```
┌─assumeNotNull(y)─┐
│                0 │
│                3 │
└──────────────────┘
┌─toTypeName(assumeNotNull(y))─┐
│ Int8                         │
│ Int8                         │
└──────────────────────────────┘

```


## coalesce


```
coalesce(x[, y, ...])

```

- `x[, y, ...]` — Любое количество параметров нескалярного типа. Все параметры должны иметь взаимно совместимые типы данных. [`Any`](https://clickhouse.com/docs/ru/reference/data-types/index)

```
-- Consider a list of contacts that may specify multiple ways to contact a customer.

CREATE TABLE aBook
(
    name String,
    mail Nullable(String),
    phone Nullable(String),
    telegram Nullable(UInt32)
)
ENGINE = MergeTree
ORDER BY tuple();

INSERT INTO aBook VALUES ('client 1', NULL, '123-45-67', 123), ('client 2', NULL, NULL, NULL);

-- The mail and phone fields are of type String, but the telegram field is UInt32 so it needs to be converted to String.

-- Get the first available contact method for the customer from the contact list

SELECT name, coalesce(mail, phone, CAST(telegram,'Nullable(String)')) FROM aBook;

```


```
┌─name─────┬─coalesce(mail, phone, CAST(telegram, 'Nullable(String)'))─┐
│ client 1 │ 123-45-67                                                 │
│ client 2 │ ᴺᵁᴸᴸ                                                      │
└──────────┴───────────────────────────────────────────────────────────┘

```


## firstNonDefault


```
firstNonDefault(arg1[, arg2[ ...]])

```

- `arg1` — Первый аргумент для проверки - `arg2` — Второй аргумент для проверки - `...` — Дополнительные аргументы для проверки

```
SELECT firstNonDefault(0, 1, 2)

```


```
1

```


```
SELECT firstNonDefault('', 'hello', 'world')

```


```
'hello'

```


```
SELECT firstNonDefault(NULL, 0 :: UInt8, 1 :: UInt8)

```


```
1

```


```
SELECT firstNonDefault(NULL, 0 :: Nullable(UInt8), 1 :: Nullable(UInt8))

```


```
0

```


## ifNull


```
ifNull(x, alt)

```

- `x` — Значение, проверяемое на `NULL`. [`Any`](https://clickhouse.com/docs/ru/reference/data-types/index)
- `alt` — Значение, которое функция возвращает, если `x` равно `NULL`. [`Any`](https://clickhouse.com/docs/ru/reference/data-types/index)

```
SELECT ifNull('a', 'b'), ifNull(NULL, 'b');

```


```
┌─ifNull('a', 'b')─┬─ifNull(NULL, 'b')─┐
│ a                │ b                 │
└──────────────────┴───────────────────┘

```


## isNotNull


```
isNotNull(x)

```

- `x` — Значение несоставного типа. [`Any`](https://clickhouse.com/docs/ru/reference/data-types/index)

```
CREATE TABLE t_null
(
  x Int32,
  y Nullable(Int32)
)
ENGINE = MergeTree
ORDER BY tuple();

INSERT INTO t_null VALUES (1, NULL), (2, 3);

SELECT x FROM t_null WHERE isNotNull(y);

```


```
┌─x─┐
│ 2 │
└───┘

```


## isNull


```
isNull(x)

```

- `x` — значение не составного типа данных. [`Any`](https://clickhouse.com/docs/ru/reference/data-types/index)

```
CREATE TABLE t_null
(
  x Int32,
  y Nullable(Int32)
)
ENGINE = MergeTree
ORDER BY tuple();

INSERT INTO t_null VALUES (1, NULL), (2, 3);

SELECT x FROM t_null WHERE isNull(y);

```


```
┌─x─┐
│ 1 │
└───┘

```


## isNullable


```
isNullable(x)

```

- `x` — значение любого типа данных. [`Any`](https://clickhouse.com/docs/ru/reference/data-types/index)

```
CREATE TABLE tab (
    ordinary_col UInt32,
    nullable_col Nullable(UInt32)
)
ENGINE = MergeTree
ORDER BY tuple();
INSERT INTO tab (ordinary_col, nullable_col) VALUES (1,1), (2, 2), (3,3);
SELECT isNullable(ordinary_col), isNullable(nullable_col) FROM tab;

```


```
┌───isNullable(ordinary_col)──┬───isNullable(nullable_col)──┐
│                           0 │                           1 │
│                           0 │                           1 │
│                           0 │                           1 │
└─────────────────────────────┴─────────────────────────────┘

```


## isZeroOrNull


```
isZeroOrNull(x)

```

- `x` — числовое значение. [`UInt`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
CREATE TABLE t_null
(
  x Int32,
  y Nullable(Int32)
)
ENGINE = MergeTree
ORDER BY tuple();

INSERT INTO t_null VALUES (1, NULL), (2, 0), (3, 3);

SELECT x FROM t_null WHERE isZeroOrNull(y);

```


```
┌─x─┐
│ 1 │
│ 2 │
└───┘

```


## nullIf


```
nullIf(x, y)

```

- `x` — Первое значение. [`Any`](https://clickhouse.com/docs/ru/reference/data-types/index)
- `y` — Второе значение. [`Any`](https://clickhouse.com/docs/ru/reference/data-types/index)

```
SELECT nullIf(1, 1), nullIf(1, 2);

```


```
┌─nullIf(1, 1)─┬─nullIf(1, 2)─┐
│         ᴺᵁᴸᴸ │            1 │
└──────────────┴──────────────┘

```


## toNullable


```
toNullable(x)

```

- `x` — значение любого нескалярного типа. [`Any`](https://clickhouse.com/docs/ru/reference/data-types/index)

```
SELECT toTypeName(10), toTypeName(toNullable(10));

```


```
┌─toTypeName(10)─┬─toTypeName(toNullable(10))─┐
│ UInt8          │ Nullable(UInt8)            │
└────────────────┴────────────────────────────┘

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
