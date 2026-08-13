# Оператор ATTACH - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/statements/attach


```
ATTACH TABLE|DICTIONARY|DATABASE [IF NOT EXISTS] [db.]name [ON CLUSTER cluster] ...

```


## Присоединение существующей таблицы


```
ATTACH TABLE [IF NOT EXISTS] [db.]name [ON CLUSTER cluster]

```


## Создать новую таблицу и присоединить данные


### С указанием пути к данным таблицы


```
ATTACH TABLE name FROM 'path/to/data/' (col1 Type1, ...)

```


```
DROP TABLE IF EXISTS test;
INSERT INTO TABLE FUNCTION file('01188_attach/test/data.TSV', 'TSV', 's String, n UInt8') VALUES ('test', 42);
ATTACH TABLE test FROM '01188_attach/test' (s String, n UInt8) ENGINE = File(TSV);
SELECT * FROM test;

```


```
┌─s────┬──n─┐
│ test │ 42 │
└──────┴────┘

```


### С указанием UUID таблицы


```
ATTACH TABLE name UUID '<uuid>' (col1 Type1, ...)

```


## Присоединение таблицы MergeTree как ReplicatedMergeTree


```
ATTACH TABLE [db.]name AS [NOT] REPLICATED

```


```
DETACH TABLE test;
ATTACH TABLE test AS REPLICATED;
SYSTEM RESTORE REPLICA test;

```


```
SELECT replica_name, zookeeper_path FROM system.replicas WHERE table='test';

```


```
┌─replica_name─┬─zookeeper_path─────────────────────────────────────────────┐
│ r1           │ /clickhouse/tables/401e6a1f-9bf2-41a3-a900-abb7e94dff98/s1 │
└──────────────┴────────────────────────────────────────────────────────────┘

```


```
DETACH TABLE test;
ATTACH TABLE test AS NOT REPLICATED;
SYSTEM DROP REPLICA 'r1' FROM ZKPATH '/clickhouse/tables/401e6a1f-9bf2-41a3-a900-abb7e94dff98/s1';

```


## Присоединить существующий словарь


```
ATTACH DICTIONARY [IF NOT EXISTS] [db.]name [ON CLUSTER cluster]

```


## Присоединение существующей базы данных


```
ATTACH DATABASE [IF NOT EXISTS] name [ENGINE=<database engine>] [ON CLUSTER cluster]

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
