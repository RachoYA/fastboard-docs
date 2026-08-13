# Команды DROP - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/statements/drop


## DROP DATABASE


```
DROP DATABASE [IF EXISTS] db [ON CLUSTER cluster] [SYNC]

```


## DROP TABLE


```
DROP [TEMPORARY] TABLE [IF EXISTS] [IF EMPTY]  [db1.]name_1[, [db2.]name_2, ...] [ON CLUSTER cluster] [SYNC]

```

- Если указано условие `IF EMPTY`, сервер проверяет, пуста ли таблица, только на реплике, получившей запрос.
- Удаление нескольких таблиц одновременно не является атомарной операцией: если удаление одной из таблиц завершается ошибкой, последующие таблицы удалены не будут.

## DROP DICTIONARY


```
DROP DICTIONARY [IF EXISTS] [db.]name [SYNC]

```


## DROP USER


```
DROP USER [IF EXISTS] name [,...] [ON CLUSTER cluster_name] [FROM access_storage_type]

```


## DROP ROLE


```
DROP ROLE [IF EXISTS] name [,...] [ON CLUSTER cluster_name] [FROM access_storage_type]

```


## DROP ROW POLICY


```
DROP [ROW] POLICY [IF EXISTS] name [,...] ON [database.]table [,...] [ON CLUSTER cluster_name] [FROM access_storage_type]

```


## DROP MASKING POLICY


```
DROP MASKING POLICY [IF EXISTS] name ON [database.]table [ON CLUSTER cluster_name] [FROM access_storage_type]

```


## DROP QUOTA


```
DROP QUOTA [IF EXISTS] name [,...] [ON CLUSTER cluster_name] [FROM access_storage_type]

```


## DROP SETTINGS PROFILE


```
DROP [SETTINGS] PROFILE [IF EXISTS] name [,...] [ON CLUSTER cluster_name] [FROM access_storage_type]

```


## DROP VIEW


```
DROP VIEW [IF EXISTS] [db.]name [ON CLUSTER cluster] [SYNC]

```


## DROP FUNCTION


```
DROP FUNCTION [IF EXISTS] function_name [on CLUSTER cluster]

```


```
CREATE FUNCTION linear_equation AS (x, k, b) -> k*x + b;
DROP FUNCTION linear_equation;

```


## DROP NAMED COLLECTION


```
DROP NAMED COLLECTION [IF EXISTS] name [on CLUSTER cluster]

```


```
CREATE NAMED COLLECTION foobar AS a = '1', b = '2';
DROP NAMED COLLECTION foobar;

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
