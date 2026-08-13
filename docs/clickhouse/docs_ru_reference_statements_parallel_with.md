# Конструкция PARALLEL WITH - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/statements/parallel_with


## Синтаксис


```
statement1 PARALLEL WITH statement2 [PARALLEL WITH statement3 ...]

```


## Примеры


```
CREATE TABLE table1(x Int32) ENGINE = MergeTree ORDER BY tuple()
PARALLEL WITH
CREATE TABLE table2(y String) ENGINE = MergeTree ORDER BY tuple();

```


```
DROP TABLE table1
PARALLEL WITH
DROP TABLE table2;

```


## Настройки


## Сравнение с UNION

- `PARALLEL WITH` не возвращает никаких результатов выполнения своих операндов и может лишь повторно сгенерировать возникшее в них исключение, если оно есть;
- `PARALLEL WITH` не требует, чтобы его операнды имели один и тот же набор результирующих столбцов;
- `PARALLEL WITH` может выполнять любые команды (не только `SELECT`).
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
