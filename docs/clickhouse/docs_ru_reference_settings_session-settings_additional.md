# Настройки сеанса additional_* - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/settings/session-settings/additional


## additional_result_filter


```
INSERT INTO table_1 VALUES (1, 'a'), (2, 'bb'), (3, 'ccc'), (4, 'dddd');
SElECT * FROM table_1;

```


```
┌─x─┬─y────┐
│ 1 │ a    │
│ 2 │ bb   │
│ 3 │ ccc  │
│ 4 │ dddd │
└───┴──────┘

```


```
SELECT *
FROM table_1
SETTINGS additional_result_filter = 'x != 2'

```


```
┌─x─┬─y────┐
│ 1 │ a    │
│ 3 │ ccc  │
│ 4 │ dddd │
└───┴──────┘

```


## additional_table_filters


```
INSERT INTO table_1 VALUES (1, 'a'), (2, 'bb'), (3, 'ccc'), (4, 'dddd');
SELECT * FROM table_1;

```


```
┌─x─┬─y────┐
│ 1 │ a    │
│ 2 │ bb   │
│ 3 │ ccc  │
│ 4 │ dddd │
└───┴──────┘

```


```
SELECT *
FROM table_1
SETTINGS additional_table_filters = {'table_1': 'x != 2'}

```


```
┌─x─┬─y────┐
│ 1 │ a    │
│ 3 │ ccc  │
│ 4 │ dddd │
└───┴──────┘

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
