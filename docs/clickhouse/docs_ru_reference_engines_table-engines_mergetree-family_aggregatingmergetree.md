# Движок таблицы AggregatingMergeTree - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/aggregatingmergetree

- [`AggregateFunction`](https://clickhouse.com/docs/ru/reference/data-types/aggregatefunction)
- [`SimpleAggregateFunction`](https://clickhouse.com/docs/ru/reference/data-types/simpleaggregatefunction)

## Создание таблицы


```
CREATE TABLE [IF NOT EXISTS] [db.]table_name [ON CLUSTER cluster]
(
    name1 [type1] [DEFAULT|MATERIALIZED|ALIAS expr1],
    name2 [type2] [DEFAULT|MATERIALIZED|ALIAS expr2],
    ...
) ENGINE = AggregatingMergeTree()
[PARTITION BY expr]
[ORDER BY expr]
[SAMPLE BY expr]
[TTL expr]
[SETTINGS name=value, ...]

```


## SELECT и INSERT


## Пример агрегированного materialized view


```
CREATE DATABASE test;

```


```
CREATE TABLE test.visits
 (
    StartDate DateTime64 NOT NULL,
    CounterID UInt64,
    Sign Nullable(Int32),
    UserID Nullable(Int32)
) ENGINE = MergeTree ORDER BY (StartDate, CounterID);

```


```
CREATE TABLE test.agg_visits (
    StartDate DateTime64 NOT NULL,
    CounterID UInt64,
    Visits AggregateFunction(sum, Nullable(Int32)),
    Users AggregateFunction(uniq, Nullable(Int32))
)
ENGINE = AggregatingMergeTree() ORDER BY (StartDate, CounterID);

```


```
CREATE MATERIALIZED VIEW test.visits_mv TO test.agg_visits
AS SELECT
    StartDate,
    CounterID,
    sumState(Sign) AS Visits,
    uniqState(UserID) AS Users
FROM test.visits
GROUP BY StartDate, CounterID;

```


```
INSERT INTO test.visits (StartDate, CounterID, Sign, UserID)
VALUES (1667446031000, 1, 3, 4), (1667446031000, 1, 6, 3);

```


```
SELECT
    StartDate,
    sumMerge(Visits) AS Visits,
    uniqMerge(Users) AS Users
FROM test.visits_mv
GROUP BY StartDate
ORDER BY StartDate;

```


```
┌───────────────StartDate─┬─Visits─┬─Users─┐
│ 2022-11-03 03:27:11.000 │      9 │     2 │
└─────────────────────────┴────────┴───────┘

```


```
INSERT INTO test.visits (StartDate, CounterID, Sign, UserID)
VALUES (1669446031000, 2, 5, 10), (1667446031000, 3, 7, 5);

```


```
┌───────────────StartDate─┬─Visits─┬─Users─┐
│ 2022-11-03 03:27:11.000 │     16 │     3 │
│ 2022-11-26 07:00:31.000 │      5 │     1 │
└─────────────────────────┴────────┴───────┘

```


```
CREATE MATERIALIZED VIEW test.visits_mv TO test.agg_visits
AS SELECT
    StartDate,
    CounterID,
    initializeAggregation('sumState', Sign) AS Visits,
    initializeAggregation('uniqState', UserID) AS Users
FROM test.visits;

```


## Агрегация элементов Tuple


```
CREATE TABLE agg_tuples
(
    key UInt32,
    metrics Tuple(
        total_visits SimpleAggregateFunction(sum, UInt64),
        unique_users SimpleAggregateFunction(max, UInt64)
    )
) ENGINE = AggregatingMergeTree()
ORDER BY key
SETTINGS allow_tuple_element_aggregation = 1;

INSERT INTO agg_tuples VALUES (1, (100, 5));
INSERT INTO agg_tuples VALUES (1, (200, 8));
INSERT INTO agg_tuples VALUES (2, (50, 3));

OPTIMIZE TABLE agg_tuples FINAL;

SELECT key, metrics.total_visits, metrics.unique_users FROM agg_tuples ORDER BY key;

```


```
┌─key─┬─metrics.total_visits─┬─metrics.unique_users─┐
│   1 │                  300 │                    8 │
│   2 │                   50 │                    3 │
└─────┴──────────────────────┴──────────────────────┘

```


## Материалы по теме

- Блог: [Использование комбинаторов агрегатных функций в ClickHouse](https://clickhouse.com/blog/aggregate-functions-combinators-in-clickhouse-for-arrays-maps-and-states)
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
