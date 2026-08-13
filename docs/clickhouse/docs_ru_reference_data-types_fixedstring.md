# FixedString(N) - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/data-types/fixedstring


```
<column_name> FixedString(N)

```

- Двоичное представление IP-адресов (`FixedString(16)` для IPv6).
- Коды языков (ru_RU, en_US, …).
- Коды валют (USD, RUB, …).
- Двоичное представление хешей (`FixedString(16)` для MD5, `FixedString(32)` для SHA256).
- Дополняет строку null-байтами, если строка содержит меньше `N` байт.
- Генерирует исключение `Too large value for FixedString(N)`, если строка содержит больше `N` байт.

```

INSERT INTO FixedStringTable VALUES ('a'), ('ab'), ('');

```


```
SELECT
    name,
    toTypeName(name),
    length(name),
    empty(name)
FROM FixedStringTable;

```


```
┌─name─┬─toTypeName(name)─┬─length(name)─┬─empty(name)─┐
│ a    │ FixedString(2)   │            2 │           0 │
│ ab   │ FixedString(2)   │            2 │           0 │
│      │ FixedString(2)   │            2 │           1 │
└──────┴──────────────────┴──────────────┴─────────────┘

```

- Если используется оператор равенства `=` или `==` либо функция `equals`, ClickHouse *не* учитывает символ `\0`, то есть запросы `SELECT * FROM FixedStringTable WHERE name = 'a';` и `SELECT * FROM FixedStringTable WHERE name = 'a\0';` возвращают одинаковый результат.
- Если используется предложение `LIKE`, ClickHouse *учитывает* символ `\0`, поэтому в условии фильтрации может потребоваться явно указать символ `\0`.

```
SELECT name
FROM FixedStringTable
WHERE name = 'a'
FORMAT JSONStringsEachRow

{"name":"a\u0000"}

SELECT name
FROM FixedStringTable
WHERE name = 'a\0'
FORMAT JSONStringsEachRow

{"name":"a\u0000"}

SELECT name
FROM FixedStringTable
WHERE name = 'a'
FORMAT JSONStringsEachRow

Query id: c32cec28-bb9e-4650-86ce-d74a1694d79e

{"name":"a\u0000"}

SELECT name
FROM FixedStringTable
WHERE name LIKE 'a'
FORMAT JSONStringsEachRow

0 rows in set.

SELECT name
FROM FixedStringTable
WHERE name LIKE 'a\0'
FORMAT JSONStringsEachRow

{"name":"a\u0000"}

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
