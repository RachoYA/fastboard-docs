# Движок таблицы SummingMergeTree - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/summingmergetree


## Создание таблицы


```
CREATE TABLE [IF NOT EXISTS] [db.]table_name [ON CLUSTER cluster]
(
    name1 [type1] [DEFAULT|MATERIALIZED|ALIAS expr1],
    name2 [type2] [DEFAULT|MATERIALIZED|ALIAS expr2],
    ...
) ENGINE = SummingMergeTree([columns])
[PARTITION BY expr]
[ORDER BY expr]
[SAMPLE BY expr]
[SETTINGS name=value, ...]

```


### Параметры SummingMergeTree


#### Столбцы


### Секции запроса


## Пример использования


```
CREATE TABLE summtt
(
    key UInt32,
    value UInt32
)
ENGINE = SummingMergeTree()
ORDER BY key

```


```
INSERT INTO summtt VALUES(1,1),(1,2),(2,1)

```


```
SELECT key, sum(value) FROM summtt GROUP BY key

```


```
┌─key─┬─sum(value)─┐
│   2 │          1 │
│   1 │          3 │
└─────┴────────────┘

```


## Обработка данных


### Общие правила суммирования


### Суммирование в столбцах AggregateFunction


### Вложенные структуры

- первый столбец — числовой `(*Int*, Date, DateTime)` или строковый `(String, FixedString)`, назовём его `key`,
- остальные столбцы — арифметические `(*Int*, Float32/64)`, назовём их `(values...)`,

```
DROP TABLE IF EXISTS nested_sum;
CREATE TABLE nested_sum
(
    date Date,
    site UInt32,
    hitsMap Nested(
        browser String,
        imps UInt32,
        clicks UInt32
    )
) ENGINE = SummingMergeTree
PRIMARY KEY (date, site);

INSERT INTO nested_sum VALUES ('2020-01-01', 12, ['Firefox', 'Opera'], [10, 5], [2, 1]);
INSERT INTO nested_sum VALUES ('2020-01-01', 12, ['Chrome', 'Firefox'], [20, 1], [1, 1]);
INSERT INTO nested_sum VALUES ('2020-01-01', 12, ['IE'], [22], [0]);
INSERT INTO nested_sum VALUES ('2020-01-01', 10, ['Chrome'], [4], [3]);

OPTIMIZE TABLE nested_sum FINAL; -- emulate merge

SELECT * FROM nested_sum;
┌───────date─┬─site─┬─hitsMap.browser───────────────────┬─hitsMap.imps─┬─hitsMap.clicks─┐
│ 2020-01-01 │   10 │ ['Chrome']                        │ [4]          │ [3]            │
│ 2020-01-01 │   12 │ ['Chrome','Firefox','IE','Opera'] │ [20,11,22,5] │ [1,3,0,1]      │
└────────────┴──────┴───────────────────────────────────┴──────────────┴────────────────┘

SELECT
    site,
    browser,
    impressions,
    clicks
FROM
(
    SELECT
        site,
        sumMap(hitsMap.browser, hitsMap.imps, hitsMap.clicks) AS imps_map
    FROM nested_sum
    GROUP BY site
)
ARRAY JOIN
    imps_map.1 AS browser,
    imps_map.2 AS impressions,
    imps_map.3 AS clicks;

┌─site─┬─browser─┬─impressions─┬─clicks─┐
│   12 │ Chrome  │          20 │      1 │
│   12 │ Firefox │          11 │      3 │
│   12 │ IE      │          22 │      0 │
│   12 │ Opera   │           5 │      1 │
│   10 │ Chrome  │           4 │      3 │
└──────┴─────────┴─────────────┴────────┘

```


### Агрегация элементов Tuple

- Суммируются только числовые подстолбцы.
- Подстолбцы, входящие в `Tuple` в ключе сортировки или ключе партиционирования, исключаются из суммирования.
- Если указан `columns`, суммируются только подстолбцы перечисленных столбцов `Tuple`.
- Если после суммирования все числовые подстолбцы строки равны нулю, строка удаляется.

```
CREATE TABLE summing_tuples
(
    key UInt32,
    metrics Tuple(
        impressions UInt64,
        clicks UInt64,
        nested Tuple(
            conversions UInt64
        )
    )
) ENGINE = SummingMergeTree()
ORDER BY key
SETTINGS allow_tuple_element_aggregation = 1;

INSERT INTO summing_tuples VALUES (1, (100, 10, (1)));
INSERT INTO summing_tuples VALUES (1, (200, 20, (3)));

OPTIMIZE TABLE summing_tuples FINAL;

SELECT key, metrics.impressions, metrics.clicks, metrics.nested.conversions FROM summing_tuples;

```


```
┌─key─┬─metrics.impressions─┬─metrics.clicks─┬─metrics.nested.conversions─┐
│   1 │                 300 │             30 │                          4 │
└─────┴─────────────────────┴────────────────┴────────────────────────────┘

```


## См. также

- Блог: [Использование комбинаторов агрегатных функций в ClickHouse](https://clickhouse.com/blog/aggregate-functions-combinators-in-clickhouse-for-arrays-maps-and-states)
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
