# Команды SYSTEM - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/statements/system


## SYSTEM RELOAD EMBEDDED DICTIONARIES


## SYSTEM RELOAD DICTIONARIES


```
SYSTEM RELOAD DICTIONARIES [ON CLUSTER cluster_name]

```


## SYSTEM RELOAD DICTIONARY


```
SYSTEM RELOAD DICTIONARY [ON CLUSTER cluster_name] dictionary_name

```


```
SELECT name, status FROM system.dictionaries;

```


## SYSTEM UNLOAD DICTIONARY


```
SYSTEM UNLOAD DICTIONARY dictionary_name

```


```
SELECT name, status FROM system.dictionaries;

```


## SYSTEM UNLOAD DICTIONARIES


```
SYSTEM UNLOAD DICTIONARIES

```


## SYSTEM RELOAD MODELS


```
SYSTEM RELOAD MODELS [ON CLUSTER cluster_name]

```


## SYSTEM RELOAD MODEL


```
SYSTEM RELOAD MODEL [ON CLUSTER cluster_name] <model_path>

```


## SYSTEM RELOAD FUNCTIONS


```
SYSTEM RELOAD FUNCTIONS [ON CLUSTER cluster_name]
SYSTEM RELOAD FUNCTION [ON CLUSTER cluster_name] function_name

```


## SYSTEM RELOAD ASYNCHRONOUS METRICS


```
SYSTEM RELOAD ASYNCHRONOUS METRICS [ON CLUSTER cluster_name]

```


## SYSTEM CLEAR|DROP DNS CACHE


## SYSTEM CLEAR|DROP MARK CACHE


## SYSTEM CLEAR|DROP PRIMARY INDEX CACHE


## SYSTEM CLEAR|DROP ICEBERG METADATA CACHE


## SYSTEM CLEAR|DROP AVRO SCHEMA CACHE


## SYSTEM DROP PARQUET METADATA CACHE


## SYSTEM CLEAR|DROP PAIMON METADATA CACHE


## SYSTEM CLEAR|DROP POINT IN POLYGON CACHE


## SYSTEM CLEAR|DROP TEXT INDEX CACHES

- `SYSTEM CLEAR TEXT INDEX TOKENS CACHE`,
- `SYSTEM CLEAR TEXT INDEX HEADER CACHE` или
- `SYSTEM CLEAR TEXT INDEX POSTINGS CACHE`

## SYSTEM CLEAR|DROP INDEX MARK CACHE


## SYSTEM CLEAR|DROP INDEX UNCOMPRESSED CACHE


## SYSTEM CLEAR|DROP MMAP CACHE


## SYSTEM CLEAR|DROP PAGE CACHE


## SYSTEM CLEAR|DROP VECTOR SIMILARITY INDEX CACHE


## SYSTEM CLEAR|DROP CONNECTIONS CACHE


## SYSTEM CLEAR|DROP S3 CLIENT CACHE


## SYSTEM PREWARM MARK CACHE


```
SYSTEM PREWARM MARK CACHE [ON CLUSTER cluster_name] [db.]table

```


## SYSTEM PREWARM PRIMARY INDEX CACHE


```
SYSTEM PREWARM PRIMARY INDEX CACHE [ON CLUSTER cluster_name] [db.]table

```


## SYSTEM CLEAR|DROP DISK METADATA CACHE


```
SYSTEM DROP DISK METADATA CACHE <disk_name>

```


## SYSTEM SYNC FILESYSTEM CACHE


```
SYSTEM SYNC FILESYSTEM CACHE ['<cache_name>']

```


## SYSTEM CLEAR|DROP DISTRIBUTED CACHE


```
SYSTEM DROP DISTRIBUTED CACHE [CONNECTIONS | 'server_id']

```


## SYSTEM DROP REPLICA


```
SYSTEM DROP REPLICA 'replica_name' FROM TABLE database.table;
SYSTEM DROP REPLICA 'replica_name' FROM DATABASE database;
SYSTEM DROP REPLICA 'replica_name';
SYSTEM DROP REPLICA 'replica_name' FROM ZKPATH '/path/to/table/in/zk';

```


## SYSTEM DROP DATABASE REPLICA


```
SYSTEM DROP DATABASE REPLICA 'replica_name' [FROM SHARD 'shard_name'] FROM DATABASE database;
SYSTEM DROP DATABASE REPLICA 'replica_name' [FROM SHARD 'shard_name'];
SYSTEM DROP DATABASE REPLICA 'replica_name' [FROM SHARD 'shard_name'] FROM ZKPATH '/path/to/table/in/zk';

```


## SYSTEM CLEAR|DROP UNCOMPRESSED CACHE


## SYSTEM CLEAR|DROP COMPILED EXPRESSION CACHE


## SYSTEM CLEAR|DROP QUERY CONDITION CACHE


## SYSTEM CLEAR|DROP ENCRYPTION HEADERS CACHE


## SYSTEM CLEAR|DROP КЭШ ЗАПРОСОВ


```
SYSTEM CLEAR QUERY CACHE;
SYSTEM CLEAR QUERY CACHE TAG '<tag>'

```


## SYSTEM CLEAR|DROP FORMAT SCHEMA CACHE

- Protobuf: удаляет импортированные определения сообщений Protobuf из памяти.
- Files: удаляет кэшированные файлы схем, хранящиеся локально в [`format_schema_path`](https://clickhouse.com/docs/ru/reference/settings/server-settings/settings#format_schema_path) и создаваемые, когда `format_schema_source` имеет значение `query`. Примечание: если цель не указана, очищаются оба кэша.

```
SYSTEM CLEAR|DROP FORMAT SCHEMA CACHE [FOR Protobuf/Files]

```


## SYSTEM FLUSH LOGS


```
SYSTEM FLUSH LOGS [ON CLUSTER cluster_name] [log_name|[database.table]] [, ...]

```


```
SYSTEM FLUSH LOGS query_log, system.query_views_log;

```


## SYSTEM RELOAD CONFIG


```
SYSTEM RELOAD CONFIG [ON CLUSTER cluster_name]

```


## SYSTEM RELOAD USERS


```
SYSTEM RELOAD USERS [ON CLUSTER cluster_name]

```


## SYSTEM SHUTDOWN


## SYSTEM KILL


## SYSTEM INSTRUMENT


### SYSTEM INSTRUMENT ADD


```
SYSTEM INSTRUMENT ADD FUNCTION HANDLER [ARGUMENTS]

```


#### LOG


```
SYSTEM INSTRUMENT ADD 'QueryMetricLog::startQuery' LOG ENTRY 'this is a log printed at entry'
SYSTEM INSTRUMENT ADD 'QueryMetricLog::startQuery' LOG EXIT 'this is a log printed at exit'

```


#### SLEEP


```
SYSTEM INSTRUMENT ADD 'QueryMetricLog::startQuery' SLEEP ENTRY 0.5

```


```
SYSTEM INSTRUMENT ADD 'QueryMetricLog::startQuery' SLEEP ENTRY 0 1

```


#### PROFILE


```
SYSTEM INSTRUMENT ADD 'QueryMetricLog::startQuery' PROFILE

```


### SYSTEM INSTRUMENT REMOVE


```
SYSTEM INSTRUMENT REMOVE ID

```


```
SYSTEM INSTRUMENT REMOVE ALL

```


```
SYSTEM INSTRUMENT REMOVE (SELECT id FROM system.instrumentation WHERE handler = 'log')

```


```
SYSTEM INSTRUMENT REMOVE 'QueryMetricLog::startQuery'

```


## Управление distributed таблицами


### SYSTEM STOP DISTRIBUTED SENDS


```
SYSTEM STOP DISTRIBUTED SENDS [db.]<distributed_table_name> [ON CLUSTER cluster_name]

```


### SYSTEM FLUSH DISTRIBUTED


```
SYSTEM FLUSH DISTRIBUTED [db.]<distributed_table_name> [ON CLUSTER cluster_name] [SETTINGS ...]

```


### SYSTEM START DISTRIBUTED SENDS


```
SYSTEM START DISTRIBUTED SENDS [db.]<distributed_table_name> [ON CLUSTER cluster_name]

```


### SYSTEM STOP LISTEN


```
SYSTEM STOP LISTEN [ON CLUSTER cluster_name] [QUERIES ALL | QUERIES DEFAULT | QUERIES CUSTOM | TCP | TCP WITH PROXY | TCP SECURE | HTTP | HTTPS | MYSQL | GRPC | POSTGRESQL | PROMETHEUS | CUSTOM 'protocol']

```

- Если указан модификатор `CUSTOM 'protocol'`, будет остановлен пользовательский протокол с указанным именем, определённый в разделе `protocols` конфигурации сервера.
- Если указан модификатор `QUERIES ALL [EXCEPT .. [,..]]`, будут остановлены все протоколы, кроме указанных в предложении `EXCEPT`.
- Если указан модификатор `QUERIES DEFAULT [EXCEPT .. [,..]]`, будут остановлены все протоколы по умолчанию, кроме указанных в предложении `EXCEPT`.
- Если указан модификатор `QUERIES CUSTOM [EXCEPT .. [,..]]`, будут остановлены все пользовательские протоколы, кроме указанных в предложении `EXCEPT`.

### SYSTEM START LISTEN


```
SYSTEM START LISTEN [ON CLUSTER cluster_name] [QUERIES ALL | QUERIES DEFAULT | QUERIES CUSTOM | TCP | TCP WITH PROXY | TCP SECURE | HTTP | HTTPS | MYSQL | GRPC | POSTGRESQL | PROMETHEUS | CUSTOM 'protocol']

```


## Управление таблицами MergeTree


### SYSTEM STOP MERGES


```
SYSTEM STOP MERGES [ON CLUSTER cluster_name] [ON VOLUME <volume_name> | [db.]merge_tree_family_table_name]

```


### SYSTEM START MERGES


```
SYSTEM START MERGES [ON CLUSTER cluster_name] [ON VOLUME <volume_name> | [db.]merge_tree_family_table_name]

```


### SYSTEM STOP TTL MERGES


```
SYSTEM STOP TTL MERGES [ON CLUSTER cluster_name] [[db.]merge_tree_family_table_name]

```


### SYSTEM START TTL MERGES


```
SYSTEM START TTL MERGES [ON CLUSTER cluster_name] [[db.]merge_tree_family_table_name]

```


### SYSTEM STOP MOVES


```
SYSTEM STOP MOVES [ON CLUSTER cluster_name] [[db.]merge_tree_family_table_name]

```


### SYSTEM START MOVES


```
SYSTEM START MOVES [ON CLUSTER cluster_name] [[db.]merge_tree_family_table_name]

```


### SYSTEM UNFREEZE


```
SYSTEM UNFREEZE WITH NAME <backup_name>

```


### SYSTEM WAIT LOADING PARTS


```
SYSTEM WAIT LOADING PARTS [ON CLUSTER cluster_name] [db.]merge_tree_family_table_name

```


## Управление таблицами ReplicatedMergeTree


### SYSTEM STOP FETCHES


```
SYSTEM STOP FETCHES [ON CLUSTER cluster_name] [[db.]replicated_merge_tree_family_table_name]

```


### SYSTEM START FETCHES


```
SYSTEM START FETCHES [ON CLUSTER cluster_name] [[db.]replicated_merge_tree_family_table_name]

```


### SYSTEM STOP REPLICATED SENDS


```
SYSTEM STOP REPLICATED SENDS [ON CLUSTER cluster_name] [[db.]replicated_merge_tree_family_table_name]

```


### SYSTEM START REPLICATED SENDS


```
SYSTEM START REPLICATED SENDS [ON CLUSTER cluster_name] [[db.]replicated_merge_tree_family_table_name]

```


### SYSTEM STOP REPLICATION QUEUES


```
SYSTEM STOP REPLICATION QUEUES [ON CLUSTER cluster_name] [[db.]replicated_merge_tree_family_table_name]

```


### SYSTEM START REPLICATION QUEUES


```
SYSTEM START REPLICATION QUEUES [ON CLUSTER cluster_name] [[db.]replicated_merge_tree_family_table_name]

```


### SYSTEM STOP PULLING REPLICATION LOG


```
SYSTEM STOP PULLING REPLICATION LOG [ON CLUSTER cluster_name] [[db.]replicated_merge_tree_family_table_name]

```


### SYSTEM START PULLING REPLICATION LOG


```
SYSTEM START PULLING REPLICATION LOG [ON CLUSTER cluster_name] [[db.]replicated_merge_tree_family_table_name]

```


### SYSTEM SYNC REPLICA


```
SYSTEM SYNC REPLICA [ON CLUSTER cluster_name] [db.]replicated_merge_tree_family_table_name [IF EXISTS] [STRICT | LIGHTWEIGHT [FROM 'srcReplica1'[, 'srcReplica2'[, ...]]] | PULL]

```

- С `IF EXISTS` (доступно начиная с 25.6) запрос не сгенерирует ошибку, если таблица не существует. Это полезно при добавлении новой реплики в кластер, когда она уже входит в конфигурацию кластера, но таблица для неё всё ещё создаётся и синхронизируется.
- Если указан модификатор `STRICT`, запрос ждёт, пока очередь репликации не опустеет. Вариант `STRICT` может так и не завершиться успешно, если в очереди репликации постоянно появляются новые записи.
- Если указан модификатор `LIGHTWEIGHT`, запрос ждёт только обработки записей `GET_PART`, `ATTACH_PART`, `DROP_RANGE`, `REPLACE_RANGE` и `DROP_PART`. Кроме того, модификатор LIGHTWEIGHT поддерживает необязательное выражение FROM ‘srcReplicas’, где ‘srcReplicas’ — это список имён исходных реплик, разделённых запятыми. Это расширение позволяет точнее настраивать синхронизацию, ограничивая её задачами репликации только от указанных исходных реплик.
- Если указан модификатор `PULL`, запрос получает новые записи очереди репликации из ZooKeeper, но не ждёт их обработки.

### SYNC DATABASE REPLICA


```
SYSTEM SYNC DATABASE REPLICA replicated_database_name;

```


### SYSTEM RESTART REPLICA


```
SYSTEM RESTART REPLICA [ON CLUSTER cluster_name] [db.]replicated_merge_tree_family_table_name

```


### SYSTEM RESTORE REPLICA

- Потери корневого пути ZooKeeper `/`.
- Потери пути реплик `/replicas`.
- Потери пути отдельной реплики `/replicas/replica_name/`.

### SYSTEM RESTORE DATABASE REPLICA


```
SYSTEM RESTORE DATABASE REPLICA repl_db [ON CLUSTER cluster]

```


```
CREATE DATABASE repl_db
ENGINE=Replicated("/clickhouse/repl_db", shard1, replica1);

CREATE TABLE repl_db.test_table (n UInt32)
ENGINE = ReplicatedMergeTree
ORDER BY n PARTITION BY n % 10;

-- zookeeper_delete_path("/clickhouse/repl_db", recursive=True) <- потеря корневого узла.

SYSTEM RESTORE DATABASE REPLICA repl_db;

```


```
SYSTEM RESTORE REPLICA [db.]replicated_merge_tree_family_table_name [ON CLUSTER cluster_name]

```


```
SYSTEM RESTORE REPLICA [ON CLUSTER cluster_name] [db.]replicated_merge_tree_family_table_name

```


```
CREATE TABLE test(n UInt32)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/test/', '{replica}')
ORDER BY n PARTITION BY n % 10;

INSERT INTO test SELECT * FROM numbers(1000);

-- zookeeper_delete_path("/clickhouse/tables/test", recursive=True) <- потеря корня.

SYSTEM RESTART REPLICA test;
SYSTEM RESTORE REPLICA test;

```


```
SYSTEM RESTORE REPLICA test ON CLUSTER cluster;

```


### SYSTEM RESTART REPLICAS


### SYSTEM CLEAR|DROP FILESYSTEM CACHE


```
SYSTEM CLEAR FILESYSTEM CACHE [ON CLUSTER cluster_name]

```


### SYSTEM SYNC FILE CACHE


```
SYSTEM SYNC FILE CACHE [ON CLUSTER cluster_name]

```


### SYSTEM LOAD PRIMARY KEY


```
SYSTEM LOAD PRIMARY KEY [db.]name

```


```
SYSTEM LOAD PRIMARY KEY

```


### SYSTEM UNLOAD PRIMARY KEY


```
SYSTEM UNLOAD PRIMARY KEY [db.]name

```


```
SYSTEM UNLOAD PRIMARY KEY

```


## Управление Refreshable Materialized Views


### SYSTEM STOP [REPLICATED] VIEW, STOP VIEWS


```
SYSTEM STOP VIEW [db.]name

```


```
SYSTEM STOP VIEWS

```


### SYSTEM START [REPLICATED] VIEW, START VIEWS


```
SYSTEM START VIEW [db.]name

```


```
SYSTEM START VIEWS

```


### SYSTEM PAUSE VIEW, PAUSE VIEWS


```
SYSTEM PAUSE VIEW [db.]name

```


```
SYSTEM PAUSE VIEWS

```


### SYSTEM REFRESH VIEW


```
SYSTEM REFRESH VIEW [db.]name

```


### SYSTEM WAIT VIEW


```
SYSTEM WAIT VIEW [db.]name

```


### SYSTEM CANCEL VIEW


```
SYSTEM CANCEL VIEW [db.]name

```


## SYSTEM FLUSH OBJECT STORAGE QUEUE


```
SYSTEM FLUSH OBJECT STORAGE QUEUE [db.]table_name PATH 'path'

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
