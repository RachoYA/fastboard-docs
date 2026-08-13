# Команды SHOW - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/statements/show

- [`display_secrets_in_show_and_select`](https://clickhouse.com/docs/ru/reference/settings/server-settings/settings#display_secrets_in_show_and_select) (настройка сервера)
- [`format_display_secrets_in_show_and_select`](https://clickhouse.com/docs/ru/reference/settings/formats#format_display_secrets_in_show_and_select) (настройка формата)

## SHOW CREATE TABLE | DICTIONARY | VIEW | DATABASE


### Синтаксис


```
SHOW [CREATE] TABLE | TEMPORARY TABLE | DICTIONARY | VIEW | DATABASE [db.]table|view [INTO OUTFILE filename] [FORMAT format]

```


## SHOW DATABASES


### Синтаксис


```
SHOW DATABASES [[NOT] LIKE | ILIKE '<pattern>'] [LIMIT <N>] [INTO OUTFILE filename] [FORMAT format]

```


```
SELECT name FROM system.databases [WHERE name [NOT] LIKE | ILIKE '<pattern>'] [LIMIT <N>] [INTO OUTFILE filename] [FORMAT format]

```


### Примеры


```
SHOW DATABASES LIKE '%de%'

```


```
┌─name────┐
│ default │
└─────────┘

```


```
SHOW DATABASES ILIKE '%DE%'

```


```
┌─name────┐
│ default │
└─────────┘

```


```
SHOW DATABASES NOT LIKE '%de%'

```


```
┌─name───────────────────────────┐
│ _temporary_and_external_tables │
│ system                         │
│ test                           │
│ tutorial                       │
└────────────────────────────────┘

```


```
SHOW DATABASES LIMIT 2

```


```
┌─name───────────────────────────┐
│ _temporary_and_external_tables │
│ default                        │
└────────────────────────────────┘

```


### См. также

- [`CREATE DATABASE`](https://clickhouse.com/docs/ru/reference/statements/create/database)

## SHOW TABLES


### Синтаксис


```
SHOW [FULL] [TEMPORARY] TABLES [{FROM | IN} <db>] [[NOT] LIKE | ILIKE '<pattern>'] [LIMIT <N>] [INTO OUTFILE <filename>] [FORMAT <format>]

```


```
SELECT name FROM system.tables [WHERE name [NOT] LIKE | ILIKE '<pattern>'] [LIMIT <N>] [INTO OUTFILE <filename>] [FORMAT <format>]

```


### Примеры


```
SHOW TABLES FROM system LIKE '%user%'

```


```
┌─name─────────────┐
│ user_directories │
│ users            │
└──────────────────┘

```


```
SHOW TABLES FROM system ILIKE '%USER%'

```


```
┌─name─────────────┐
│ user_directories │
│ users            │
└──────────────────┘

```


```
SHOW TABLES FROM system NOT LIKE '%s%'

```


```
┌─name─────────┐
│ metric_log   │
│ metric_log_0 │
│ metric_log_1 │
└──────────────┘

```


```
SHOW TABLES FROM system LIMIT 2

```


```
┌─name───────────────────────────┐
│ aggregate_function_combinators │
│ asynchronous_metric_log        │
└────────────────────────────────┘

```


### См. также

- [`Создание таблиц`](https://clickhouse.com/docs/ru/reference/statements/create/table)
- [`SHOW CREATE TABLE`](#show-create-table--dictionary--view--database)

## SHOW COLUMNS


### Синтаксис


```
SHOW [EXTENDED] [FULL] COLUMNS {FROM | IN} <table> [{FROM | IN} <db>] [{[NOT] {LIKE | ILIKE} '<pattern>' | WHERE <expr>}] [LIMIT <N>] [INTO
OUTFILE <filename>] [FORMAT <format>]

```


| Столбец | Описание | Тип |
| --- | --- | --- |
| `field` | Имя столбца | `String` |
| `type` | Тип данных столбца. Если запрос был выполнен через протокол MySQL, отображается эквивалентное имя типа в MySQL. | `String` |
| `null` | `YES`, если тип данных столбца — Nullable, в противном случае `NO` | `String` |
| `key` | `PRI`, если столбец является частью первичного ключа, `SOR`, если столбец является частью ключа сортировки, в противном случае пусто | `String` |
| `default` | Выражение по умолчанию для столбца, если он имеет тип `ALIAS`, `DEFAULT` или `MATERIALIZED`, иначе `NULL`. | `Nullable(String)` |
| `extra` | Дополнительная информация; в настоящее время не используется | `String` |
| `collation` | (только если указано ключевое слово `FULL`) collation столбца; всегда `NULL`, поскольку в ClickHouse нет collations на уровне столбца | `Nullable(String)` |
| `comment` | (только если указано ключевое слово `FULL`) Комментарий к столбцу | `String` |
| `privilege` | (только если указано ключевое слово `FULL`) Привилегия для этого столбца; в настоящее время недоступна | `String` |


### Примеры


```
SHOW COLUMNS FROM 'orders' LIKE 'delivery_%'

```


```
┌─field───────────┬─type─────┬─null─┬─key─────┬─default─┬─extra─┐
│ delivery_date   │ DateTime │    0 │ PRI SOR │ ᴺᵁᴸᴸ    │       │
│ delivery_status │ Bool     │    0 │         │ ᴺᵁᴸᴸ    │       │
└─────────────────┴──────────┴──────┴─────────┴─────────┴───────┘

```


### См. также

- [`system.columns`](https://clickhouse.com/docs/ru/reference/system-tables/columns)

## SHOW DICTIONARIES


### Синтаксис


```
SHOW DICTIONARIES [FROM <db>] [LIKE '<pattern>'] [LIMIT <N>] [INTO OUTFILE <filename>] [FORMAT <format>]

```


```
SELECT name FROM system.dictionaries WHERE database = <db> [AND name LIKE <pattern>] [LIMIT <N>] [INTO OUTFILE <filename>] [FORMAT <format>]

```


### Примеры


```
SHOW DICTIONARIES FROM db LIKE '%reg%' LIMIT 2

```


```
┌─name─────────┐
│ regions      │
│ region_names │
└──────────────┘

```


## SHOW INDEX


### Синтаксис


```
SHOW [EXTENDED] {INDEX | INDEXES | INDICES | KEYS } {FROM | IN} <table> [{FROM | IN} <db>] [WHERE <expr>] [INTO OUTFILE <filename>] [FORMAT <format>]

```


| Столбец | Описание | Тип |
| --- | --- | --- |
| `table` | Имя таблицы. | `String` |
| `non_unique` | Всегда `1`, так как ClickHouse не поддерживает ограничения уникальности. | `UInt8` |
| `key_name` | Имя индекса; `PRIMARY`, если индекс является индексом первичного ключа. | `String` |
| `seq_in_index` | Для индекса первичного ключа — позиция столбца, начиная с `1`. Для data skipping index — всегда `1`. | `UInt8` |
| `column_name` | Для индекса первичного ключа — имя столбца. Для data skipping index — `''` (пустая строка), см. поле “expression”. | `String` |
| `collation` | Порядок сортировки столбца в индексе: `A` — по возрастанию, `D` — по убыванию, `NULL` — без сортировки. | `Nullable(String)` |
| `cardinality` | Оценка мощности индекса (числа уникальных значений в индексе). В настоящее время всегда `0`. | `UInt64` |
| `sub_part` | Всегда `NULL`, потому что ClickHouse не поддерживает префиксы индексов, как в MySQL. | `Nullable(String)` |
| `packed` | Всегда `NULL`, потому что ClickHouse не поддерживает упакованные индексы (как в MySQL). | `Nullable(String)` |
| `null` | В настоящее время не используется. |  |
| `index_type` | Тип индекса, например `PRIMARY`, `MINMAX`, `BLOOM_FILTER` и т. д. | `String` |
| `comment` | Дополнительная информация об индексе; в настоящее время всегда `''` (пустая строка). | `String` |
| `index_comment` | `''` (пустая строка), потому что индексы в ClickHouse не могут иметь поле `COMMENT` (как в MySQL). | `String` |
| `visible` | Указывает, виден ли индекс оптимизатору; всегда `YES`. | `String` |
| `expression` | Для data skipping index — выражение индекса. Для индекса первичного ключа — `''` (пустая строка). | `String` |


### Примеры


```
SHOW INDEX FROM 'tbl'

```


```
┌─table─┬─non_unique─┬─key_name─┬─seq_in_index─┬─column_name─┬─collation─┬─cardinality─┬─sub_part─┬─packed─┬─null─┬─index_type───┬─comment─┬─index_comment─┬─visible─┬─expression─┐
│ tbl   │          1 │ blf_idx  │ 1            │ 1           │ ᴺᵁᴸᴸ      │ 0           │ ᴺᵁᴸᴸ     │ ᴺᵁᴸᴸ   │ ᴺᵁᴸᴸ │ BLOOM_FILTER │         │               │ YES     │ d, b       │
│ tbl   │          1 │ mm1_idx  │ 1            │ 1           │ ᴺᵁᴸᴸ      │ 0           │ ᴺᵁᴸᴸ     │ ᴺᵁᴸᴸ   │ ᴺᵁᴸᴸ │ MINMAX       │         │               │ YES     │ a, c, d    │
│ tbl   │          1 │ mm2_idx  │ 1            │ 1           │ ᴺᵁᴸᴸ      │ 0           │ ᴺᵁᴸᴸ     │ ᴺᵁᴸᴸ   │ ᴺᵁᴸᴸ │ MINMAX       │         │               │ YES     │ c, d, e    │
│ tbl   │          1 │ PRIMARY  │ 1            │ c           │ A         │ 0           │ ᴺᵁᴸᴸ     │ ᴺᵁᴸᴸ   │ ᴺᵁᴸᴸ │ PRIMARY      │         │               │ YES     │            │
│ tbl   │          1 │ PRIMARY  │ 2            │ a           │ A         │ 0           │ ᴺᵁᴸᴸ     │ ᴺᵁᴸᴸ   │ ᴺᵁᴸᴸ │ PRIMARY      │         │               │ YES     │            │
│ tbl   │          1 │ set_idx  │ 1            │ 1           │ ᴺᵁᴸᴸ      │ 0           │ ᴺᵁᴸᴸ     │ ᴺᵁᴸᴸ   │ ᴺᵁᴸᴸ │ SET          │         │               │ YES     │ e          │
└───────┴────────────┴──────────┴──────────────┴─────────────┴───────────┴─────────────┴──────────┴────────┴──────┴──────────────┴─────────┴───────────────┴─────────┴────────────┘

```


### См. также

- [`system.tables`](https://clickhouse.com/docs/ru/reference/system-tables/tables)
- [`system.data_skipping_indices`](https://clickhouse.com/docs/ru/reference/system-tables/data_skipping_indices)

## SHOW PROCESSLIST


### Синтаксис


```
SHOW PROCESSLIST [INTO OUTFILE filename] [FORMAT format]

```


```
$ watch -n1 "clickhouse-client --query='SHOW PROCESSLIST'"

```


## SHOW GRANTS


### Синтаксис


```
SHOW GRANTS [FOR user1 [, user2 ...]] [WITH IMPLICIT] [FINAL]

```


## SHOW CREATE USER


### Синтаксис


```
SHOW CREATE USER [name1 [, name2 ...] | CURRENT_USER]

```


## SHOW CREATE ROLE


### Синтаксис


```
SHOW CREATE ROLE name1 [, name2 ...]

```


## SHOW CREATE ROW POLICY


### Синтаксис


```
SHOW CREATE [ROW] POLICY name ON [database1.]table1 [, [database2.]table2 ...]

```


## SHOW CREATE QUOTA


### Синтаксис


```
SHOW CREATE QUOTA [name1 [, name2 ...] | CURRENT]

```


## SHOW CREATE SETTINGS PROFILE


### Синтаксис


```
SHOW CREATE [SETTINGS] PROFILE name1 [, name2 ...]

```


## SHOW USERS


### Синтаксис


```
SHOW USERS

```


## SHOW ROLES


### Синтаксис


```
SHOW [CURRENT|ENABLED] ROLES

```


## SHOW PROFILES


### Синтаксис


```
SHOW [SETTINGS] PROFILES

```


## SHOW POLICIES


### Синтаксис


```
SHOW [ROW] POLICIES [ON [db.]table]

```


## SHOW QUOTAS


### Синтаксис


```
SHOW QUOTAS

```


## SHOW QUOTA


### Синтаксис


```
SHOW [CURRENT] QUOTA

```


## SHOW ACCESS


### Синтаксис


```
SHOW ACCESS

```


## SHOW CLUSTER(S)


### Синтаксис


```
SHOW CLUSTER '<name>'
SHOW CLUSTERS [[NOT] LIKE|ILIKE '<pattern>'] [LIMIT <N>]

```


### Примеры


```
SHOW CLUSTERS;

```


```
┌─cluster──────────────────────────────────────┐
│ test_cluster_two_shards                      │
│ test_cluster_two_shards_internal_replication │
│ test_cluster_two_shards_localhost            │
│ test_shard_localhost                         │
│ test_shard_localhost_secure                  │
│ test_unavailable_shard                       │
└──────────────────────────────────────────────┘

```


```
SHOW CLUSTERS LIKE 'test%' LIMIT 1;

```


```
┌─cluster─────────────────┐
│ test_cluster_two_shards │
└─────────────────────────┘

```


```
SHOW CLUSTER 'test_shard_localhost' FORMAT Vertical;

```


```
Row 1:
──────
cluster:                 test_shard_localhost
shard_num:               1
replica_num:             1
host_name:               localhost
host_address:            127.0.0.1
port:                    9000

```


## SHOW SETTINGS


### Синтаксис


```
SHOW [CHANGED] SETTINGS LIKE|ILIKE <name>

```


### Предложения


### Примеры


```
SHOW SETTINGS LIKE 'send_timeout';

```


```
┌─name─────────┬─type────┬─value─┐
│ send_timeout │ Seconds │ 300   │
└──────────────┴─────────┴───────┘

```


```
SHOW SETTINGS ILIKE '%CONNECT_timeout%'

```


```
┌─name────────────────────────────────────┬─type─────────┬─value─┐
│ connect_timeout                         │ Seconds      │ 10    │
│ connect_timeout_with_failover_ms        │ Milliseconds │ 50    │
│ connect_timeout_with_failover_secure_ms │ Milliseconds │ 100   │
└─────────────────────────────────────────┴──────────────┴───────┘

```


```
SHOW CHANGED SETTINGS ILIKE '%MEMORY%'

```


```
┌─name─────────────┬─type───┬─value───────┐
│ max_memory_usage │ UInt64 │ 10000000000 │
└──────────────────┴────────┴─────────────┘

```


## SHOW SETTING


### Синтаксис


```
SHOW SETTING <name>

```


### См. также

- таблица [`system.settings`](https://clickhouse.com/docs/ru/reference/system-tables/settings)

## SHOW FILESYSTEM CACHES


### Примеры


```
SHOW FILESYSTEM CACHES

```


```
┌─Caches────┐
│ s3_cache  │
└───────────┘

```


### См. также

- таблица [`system.settings`](https://clickhouse.com/docs/ru/reference/system-tables/settings)

## SHOW ENGINES


### Синтаксис


```
SHOW ENGINES [INTO OUTFILE filename] [FORMAT format]

```


### См. также

- таблица [system.table_engines](https://clickhouse.com/docs/ru/reference/system-tables/table_engines)

## SHOW FUNCTIONS


### Синтаксис


```
SHOW FUNCTIONS [LIKE | ILIKE '<pattern>']

```


### См. также

- таблица [`system.functions`](https://clickhouse.com/docs/ru/reference/system-tables/functions)

## SHOW MERGES


| Столбец | Описание |
| --- | --- |
| `table` | Имя таблицы. |
| `database` | Имя базы данных, в которой находится таблица. |
| `estimate_complete` | Оценочное время до завершения (в секундах). |
| `elapsed` | Время, прошедшее с момента начала слияния (в секундах). |
| `progress` | Процент выполненной работы (от 0 до 100). |
| `is_mutation` | 1, если этот процесс является мутацией части. |
| `size_compressed` | Общий размер сжатых данных слитых частей. |
| `memory_usage` | Использование памяти процессом слияния. |


### Синтаксис


```
SHOW MERGES [[NOT] LIKE|ILIKE '<table_name_pattern>'] [LIMIT <N>]

```


### Примеры


```
SHOW MERGES;

```


```
┌─table──────┬─database─┬─estimate_complete─┬─elapsed─┬─progress─┬─is_mutation─┬─size_compressed─┬─memory_usage─┐
│ your_table │ default  │              0.14 │    0.36 │    73.01 │           0 │        5.40 MiB │    10.25 MiB │
└────────────┴──────────┴───────────────────┴─────────┴──────────┴─────────────┴─────────────────┴──────────────┘

```


```
SHOW MERGES LIKE 'your_t%' LIMIT 1;

```


```
┌─table──────┬─database─┬─estimate_complete─┬─elapsed─┬─progress─┬─is_mutation─┬─size_compressed─┬─memory_usage─┐
│ your_table │ default  │              0.14 │    0.36 │    73.01 │           0 │        5.40 MiB │    10.25 MiB │
└────────────┴──────────┴───────────────────┴─────────┴──────────┴─────────────┴─────────────────┴──────────────┘

```


## SHOW CREATE MASKING POLICY


### Синтаксис


```
SHOW CREATE MASKING POLICY name ON [database.]table

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
