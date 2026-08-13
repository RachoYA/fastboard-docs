# Оператор CHECK GRANT - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/statements/check-grant


## Синтаксис


```
CHECK GRANT privilege[(column_name [,...])] [,...] ON {db.table[*]|db[*].*|*.*|table[*]|*}

```

- `privilege` — Тип привилегии.

## Примеры


```
CHECK GRANT SELECT(col1) ON table_1;

```


```
┌─result─┐
│      1 │
└────────┘

```


```
CHECK GRANT SELECT(col2) ON table_2;

```


```
┌─result─┐
│      0 │
└────────┘

```


## Подстановочный знак

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
