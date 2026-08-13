# Движок таблицы EmbeddedRocksDB - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/embedded-rocksdb


## Создание таблицы


```
CREATE TABLE [IF NOT EXISTS] [db.]table_name [ON CLUSTER cluster]
(
    name1 [type1] [DEFAULT|MATERIALIZED|ALIAS expr1],
    name2 [type2] [DEFAULT|MATERIALIZED|ALIAS expr2],
    ...
) ENGINE = EmbeddedRocksDB([ttl, rocksdb_dir, read_only]) PRIMARY KEY(primary_key_name)
[ SETTINGS name=value, ... ]

```

- `ttl` - время жизни значений. TTL указывается в секундах. Если TTL равен 0, используется обычный экземпляр RocksDB (без TTL).
- `rocksdb_dir` - путь к каталогу существующей RocksDB или путь назначения для создаваемой RocksDB. Таблица открывается с указанным `rocksdb_dir`.
- `read_only` - если `read_only` установлено в true, используется режим только для чтения. Для хранилища с TTL compaction не будет запускаться ни вручную, ни автоматически, поэтому записи с истекшим сроком жизни не будут удаляться.
- `primary_key_name` – любое имя столбца в списке столбцов.
- `primary key` должен быть указан; поддерживается только один столбец в первичном ключе. Первичный ключ будет сериализован в бинарном виде как `rocksdb key`.
- столбцы, кроме первичного ключа, будут сериализованы в бинарном виде как значение `rocksdb` в соответствующем порядке.
- запросы с фильтрацией по ключу через `equals` или `in` будут оптимизированы в поиск по нескольким ключам в `rocksdb`.
- `optimize_for_bulk_insert` – таблица оптимизирована для массовых вставок (конвейер вставки будет создавать SST-файлы и импортировать их в базу данных rocksdb вместо записи в memtables); значение по умолчанию: `1`.
- `bulk_insert_block_size` - минимальный размер SST-файлов (в строках), создаваемых при массовой вставке; значение по умолчанию: `1048449`.

```
CREATE TABLE test
(
    `key` String,
    `v1` UInt32,
    `v2` String,
    `v3` Float32
)
ENGINE = EmbeddedRocksDB
PRIMARY KEY key

```


## Метрики


```
SELECT
    name,
    value
FROM system.rocksdb

┌─name──────────────────────┬─value─┐
│ no.file.opens             │     1 │
│ number.block.decompressed │     1 │
└───────────────────────────┴───────┘

```


## Конфигурация


```
<rocksdb>
    <options>
        <max_background_jobs>8</max_background_jobs>
    </options>
    <column_family_options>
        <num_levels>2</num_levels>
    </column_family_options>
    <tables>
        <table>
            <name>TABLE</name>
            <options>
                <max_background_jobs>8</max_background_jobs>
            </options>
            <column_family_options>
                <num_levels>2</num_levels>
            </column_family_options>
        </table>
    </tables>
</rocksdb>

```


## Поддерживаемые операции


### Вставки


```
INSERT INTO test VALUES ('some key', 1, 'value', 3.2);

```


### Удаление


```
DELETE FROM test WHERE key LIKE 'some%' AND v1 > 1;

```


```
ALTER TABLE test DELETE WHERE key LIKE 'some%' AND v1 > 1;

```


```
TRUNCATE TABLE test;

```


### Обновления


```
ALTER TABLE test UPDATE v1 = v1 * 10 + 2 WHERE key LIKE 'some%' AND v3 > 3.1;

```


### Операции JOIN


```
SET join_algorithm = 'direct, hash'

```


#### Пример


```
CREATE TABLE rdb
(
    `key` UInt32,
    `value` Array(UInt32),
    `value2` String
)
ENGINE = EmbeddedRocksDB
PRIMARY KEY key

```


```
INSERT INTO rdb
    SELECT
        toUInt32(sipHash64(number) % 10) AS key,
        [key, key+1] AS value,
        ('val2' || toString(key)) AS value2
    FROM numbers_mt(10);

```


```
CREATE TABLE t2
(
    `k` UInt16
)
ENGINE = TinyLog

```


```
INSERT INTO t2 SELECT number AS k
FROM numbers_mt(10)

```


```
SET join_algorithm = 'direct'

```


```
SELECT *
FROM
(
    SELECT k AS key
    FROM t2
) AS t2
INNER JOIN rdb ON rdb.key = t2.key
ORDER BY key ASC

```


```
┌─key─┬─rdb.key─┬─value──┬─value2─┐
│   0 │       0 │ [0,1]  │ val20  │
│   2 │       2 │ [2,3]  │ val22  │
│   3 │       3 │ [3,4]  │ val23  │
│   6 │       6 │ [6,7]  │ val26  │
│   7 │       7 │ [7,8]  │ val27  │
│   8 │       8 │ [8,9]  │ val28  │
│   9 │       9 │ [9,10] │ val29  │
└─────┴─────────┴────────┴────────┘

```


### Подробнее об операции JOIN

- [настройка `join_algorithm`](https://clickhouse.com/docs/ru/reference/settings/session-settings#join_algorithm)
- [оператор JOIN](https://clickhouse.com/docs/ru/reference/statements/select/join)
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
