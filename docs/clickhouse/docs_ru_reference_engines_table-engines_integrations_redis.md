# Движок таблицы Redis - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/redis


## Создание таблицы


```
CREATE TABLE [IF NOT EXISTS] [db.]table_name
(
    name1 [type1],
    name2 [type2],
    ...
) ENGINE = Redis({host:port[, db_index[, password[, pool_size]]] | named_collection[, option=value [,..]] })
PRIMARY KEY(primary_key_name);

```

- `host:port` — адрес сервера Redis; порт можно не указывать, тогда будет использован стандартный порт Redis 6379.
- `db_index` — индекс БД Redis в диапазоне от 0 до 15, по умолчанию — 0.
- `password` — пароль пользователя, по умолчанию — пустая строка.
- `pool_size` — максимальный размер пула соединений Redis, по умолчанию — 16.
- `primary_key_name` — любое имя столбца из списка столбцов.

## Пример использования


```
CREATE TABLE redis_table
(
    `key` String,
    `v1` UInt32,
    `v2` String,
    `v3` Float32
)
ENGINE = Redis('redis1:6379') PRIMARY KEY(key);

```


```
<named_collections>
    <redis_creds>
        <host>localhost</host>
        <port>6379</port>
        <password>****</password>
        <pool_size>16</pool_size>
        <db_index>0</db_index>
    </redis_creds>
</named_collections>

```


```
CREATE TABLE redis_table
(
    `key` String,
    `v1` UInt32,
    `v2` String,
    `v3` Float32
)
ENGINE = Redis(redis_creds) PRIMARY KEY(key);

```


```
INSERT INTO redis_table VALUES('1', 1, '1', 1.0), ('2', 2, '2', 2.0);

```


```
SELECT COUNT(*) FROM redis_table;

```


```
┌─count()─┐
│       2 │
└─────────┘

```


```
SELECT * FROM redis_table WHERE key='1';

```


```
┌─key─┬─v1─┬─v2─┬─v3─┐
│ 1   │  1 │ 1  │  1 │
└─────┴────┴────┴────┘

```


```
SELECT * FROM redis_table WHERE v1=2;

```


```
┌─key─┬─v1─┬─v2─┬─v3─┐
│ 2   │  2 │ 2  │  2 │
└─────┴────┴────┴────┘

```


```
ALTER TABLE redis_table UPDATE v1=2 WHERE key='1';

```


```
ALTER TABLE redis_table DELETE WHERE key='1';

```


```
TRUNCATE TABLE redis_table SYNC;

```


```
SELECT * FROM redis_table JOIN merge_tree_table ON merge_tree_table.key=redis_table.key;

```


## Ограничения

- В очень редких случаях во время рехеширования сканирующий запрос может возвращать дублирующиеся ключи. Подробности см. в [Redis Scan](https://github.com/redis/redis/blob/e4d183afd33e0b2e6e8d1c79a832f678a04a7886/src/dict.c#L1186-L1269).
- Во время сканирования ключи могут создаваться и удаляться, поэтому получившийся набор данных не может представлять согласованное состояние на какой-либо момент времени.
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
