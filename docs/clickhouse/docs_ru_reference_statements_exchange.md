# Оператор EXCHANGE - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/statements/exchange


```
EXCHANGE TABLES|DICTIONARIES [db0.]name_A AND [db1.]name_B [ON CLUSTER cluster]

```


## EXCHANGE TABLES


```
EXCHANGE TABLES [db0.]table_A AND [db1.]table_B [ON CLUSTER cluster]

```


### EXCHANGE НЕСКОЛЬКИХ ТАБЛИЦ


```
-- Создать таблицы
CREATE TABLE a (a UInt8) ENGINE=Memory;
CREATE TABLE b (b UInt8) ENGINE=Memory;
CREATE TABLE c (c UInt8) ENGINE=Memory;
CREATE TABLE d (d UInt8) ENGINE=Memory;

-- Обменять две пары таблиц в одном запросе
EXCHANGE TABLES a AND b, c AND d;

SHOW TABLE a;
SHOW TABLE b;
SHOW TABLE c;
SHOW TABLE d;

```


```
-- Теперь таблица 'a' имеет структуру 'b', а таблица 'b' имеет структуру 'a'
┌─statement──────────────┐
│ CREATE TABLE default.a↴│
│↳(                     ↴│
│↳    `b` UInt8         ↴│
│↳)                     ↴│
│↳ENGINE = Memory        │
└────────────────────────┘
┌─statement──────────────┐
│ CREATE TABLE default.b↴│
│↳(                     ↴│
│↳    `a` UInt8         ↴│
│↳)                     ↴│
│↳ENGINE = Memory        │
└────────────────────────┘

-- Теперь таблица 'c' имеет структуру 'd', а таблица 'd' имеет структуру 'c'
┌─statement──────────────┐
│ CREATE TABLE default.c↴│
│↳(                     ↴│
│↳    `d` UInt8         ↴│
│↳)                     ↴│
│↳ENGINE = Memory        │
└────────────────────────┘
┌─statement──────────────┐
│ CREATE TABLE default.d↴│
│↳(                     ↴│
│↳    `c` UInt8         ↴│
│↳)                     ↴│
│↳ENGINE = Memory        │
└────────────────────────┘

```


## EXCHANGE СЛОВАРЕЙ


```
EXCHANGE DICTIONARIES [db0.]dict_A AND [db1.]dict_B [ON CLUSTER cluster]

```

- [Словари](https://clickhouse.com/docs/ru/reference/statements/create/dictionary)
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
