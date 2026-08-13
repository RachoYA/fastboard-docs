# Оператор DETACH - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/statements/detach


```
DETACH TABLE|VIEW|DICTIONARY|DATABASE [IF EXISTS] [db.]name [ON CLUSTER cluster] [PERMANENTLY] [SYNC]

```


```
CREATE TABLE test ENGINE = MergeTree ORDER BY () AS SELECT * FROM numbers(10);
SELECT * FROM test;

```


```
┌─number─┐
│      0 │
│      1 │
│      2 │
│      3 │
│      4 │
│      5 │
│      6 │
│      7 │
│      8 │
│      9 │
└────────┘

```


```
DETACH TABLE test;
SELECT * FROM test;

```


```
Received exception from server (version 21.4.1):
Code: 60. DB::Exception: Received from localhost:9000. DB::Exception: Table default.test does not exist.

```

- [Materialized view](https://clickhouse.com/docs/ru/reference/statements/create/view#materialized-view)
- [Словари](https://clickhouse.com/docs/ru/reference/statements/create/dictionary)
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
