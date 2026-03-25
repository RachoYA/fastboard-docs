# Команда EXCHANGE | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/sql-reference/statements/exchange

Атомарно меняет местами имена двух таблиц или двух словарей.
Эту задачу можно также выполнить с помощью запросаRENAMEс использованием временного имени, но в этом случае операция не является атомарной.

ЗапросEXCHANGEподдерживается только движками баз данныхAtomicиShared.

Синтаксис


```
EXCHANGE TABLES|DICTIONARIES [db0.]name_A AND [db1.]name_B [ON CLUSTER cluster]

```


## EXCHANGE TABLES​

Обменивает имена двух таблиц.

Синтаксис


```
EXCHANGE TABLES [db0.]table_A AND [db1.]table_B [ON CLUSTER cluster]

```


### ОБМЕН НЕСКОЛЬКИМИ ТАБЛИЦАМИ​

Вы можете поменять местами несколько пар таблиц в одном запросе, разделяя их запятыми.

При обмене несколькими парами таблиц операции выполняютсяпоследовательно, а не атомарно. Если во время операции произойдет ошибка, некоторые пары таблиц уже могут быть обменяны местами, а другие — нет.

Пример


```
-- Create tables
CREATE TABLE a (a UInt8) ENGINE=Memory;
CREATE TABLE b (b UInt8) ENGINE=Memory;
CREATE TABLE c (c UInt8) ENGINE=Memory;
CREATE TABLE d (d UInt8) ENGINE=Memory;

-- Exchange two pairs of tables in one query
EXCHANGE TABLES a AND b, c AND d;

SHOW TABLE a;
SHOW TABLE b;
SHOW TABLE c;
SHOW TABLE d;

```


```
-- Now table 'a' has the structure of 'b', and table 'b' has the structure of 'a'
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

-- Now table 'c' has the structure of 'd', and table 'd' has the structure of 'c'
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


## EXCHANGE DICTIONARIES​

Меняет местами имена двух словарей.

Синтаксис


```
EXCHANGE DICTIONARIES [db0.]dict_A AND [db1.]dict_B [ON CLUSTER cluster]

```

См. также

- Справочники