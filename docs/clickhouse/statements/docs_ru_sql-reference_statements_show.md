# Операторы SHOW | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/sql-reference/statements/show

SHOW CREATE (TABLE|DATABASE|USER)скрывает секреты, если не включены следующие настройки:display_secrets_in_show_and_select(настройка сервера)format_display_secrets_in_show_and_select(настройка формата)Кроме того, у пользователя должна быть привилегияdisplaySecretsInShowAndSelect.

- display_secrets_in_show_and_select(настройка сервера)
- format_display_secrets_in_show_and_select(настройка формата)
Кроме того, у пользователя должна быть привилегияdisplaySecretsInShowAndSelect.


## SHOW CREATE TABLE | DICTIONARY | VIEW | DATABASE​

Эти операторы возвращают один столбец типа String,
содержащий запросCREATE, который был использован для создания указанного объекта.


### Синтаксис​


```
SHOW [CREATE] TABLE | TEMPORARY TABLE | DICTIONARY | VIEW | DATABASE [db.]table|view [INTO OUTFILE filename] [FORMAT format]

```

Если вы используете этот оператор, чтобы получить запросCREATEдля системных таблиц,
вы получитефиктивныйзапрос, который объявляет только структуру таблицы
и не может быть использован для создания таблицы.


## SHOW DATABASES​

Эта команда выводит список всех баз данных.


### Синтаксис​


```
SHOW DATABASES [[NOT] LIKE | ILIKE '<pattern>'] [LIMIT <N>] [INTO OUTFILE filename] [FORMAT format]

```

Он идентичен запросу:


```
SELECT name FROM system.databases [WHERE name [NOT] LIKE | ILIKE '<pattern>'] [LIMIT <N>] [INTO OUTFILE filename] [FORMAT format]

```


### Примеры​

В этом примере мы используемSHOW, чтобы получить имена баз данных, в которых присутствует последовательность символов 'de':


```
SHOW DATABASES LIKE '%de%'

```


```
┌─name────┐
│ default │
└─────────┘

```

Мы также можем сделать это без учета регистра:


```
SHOW DATABASES ILIKE '%DE%'

```


```
┌─name────┐
│ default │
└─────────┘

```

Или получить имена баз данных, которые не содержат 'de' в своих названиях:


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

Наконец, мы можем получить имена только первых двух баз данных:


```
SHOW DATABASES LIMIT 2

```


```
┌─name───────────────────────────┐
│ _temporary_and_external_tables │
│ default                        │
└────────────────────────────────┘

```


### См. также​

- CREATE DATABASE

## SHOW TABLES​

ОператорSHOW TABLESотображает список таблиц.


### Синтаксис​


```
SHOW [FULL] [TEMPORARY] TABLES [{FROM | IN} <db>] [[NOT] LIKE | ILIKE '<pattern>'] [LIMIT <N>] [INTO OUTFILE <filename>] [FORMAT <format>]

```

Если предложениеFROMне указано, запрос возвращает список таблиц из текущей базы данных.

Данный оператор эквивалентен следующему запросу:


```
SELECT name FROM system.tables [WHERE name [NOT] LIKE | ILIKE '<pattern>'] [LIMIT <N>] [INTO OUTFILE <filename>] [FORMAT <format>]

```


### Примеры​

В этом примере мы используем операторSHOW TABLES, чтобы найти все таблицы, в именах которых содержится 'user':


```
SHOW TABLES FROM system LIKE '%user%'

```


```
┌─name─────────────┐
│ user_directories │
│ users            │
└──────────────────┘

```

Мы также можем сделать это без учета регистра:


```
SHOW TABLES FROM system ILIKE '%USER%'

```


```
┌─name─────────────┐
│ user_directories │
│ users            │
└──────────────────┘

```

Или чтобы найти таблицы, в именах которых отсутствует буква 's':


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

Наконец, мы можем получить имена только первых двух таблиц:


```
SHOW TABLES FROM system LIMIT 2

```


```
┌─name───────────────────────────┐
│ aggregate_function_combinators │
│ asynchronous_metric_log        │
└────────────────────────────────┘

```


### См. также​

- CREATE TABLE
- SHOW CREATE TABLE

## SHOW COLUMNS​

ОператорSHOW COLUMNSотображает список столбцов.


### Синтаксис​


```
SHOW [EXTENDED] [FULL] COLUMNS {FROM | IN} <table> [{FROM | IN} <db>] [{[NOT] {LIKE | ILIKE} '<pattern>' | WHERE <expr>}] [LIMIT <N>] [INTO
OUTFILE <filename>] [FORMAT <format>]

```

Имя базы данных и таблицы может быть указано в сокращённой форме как<db>.<table>,
то естьFROM tab FROM dbиFROM db.tabэквивалентны.
Если база данных не указана, запрос возвращает список столбцов из текущей базы данных.

Также есть два необязательных ключевых слова:EXTENDEDиFULL. Ключевое словоEXTENDEDв настоящее время не оказывает никакого эффекта
и существует для совместимости с MySQL. Ключевое словоFULLприводит к тому, что в вывод включаются столбцы с информацией о сортировке (collation), комментариях и правах доступа.

ОператорSHOW COLUMNSвозвращает результирующую таблицу со следующей структурой:


### Примеры​

В этом примере мы используем операторSHOW COLUMNS, чтобы получить информацию обо всех столбцах в таблице 'orders',
начиная с 'delivery_':


```
SHOW COLUMNS FROM 'orders' LIKE 'delivery_%'

```


```
┌─field───────────┬─type─────┬─null─┬─key─────┬─default─┬─extra─┐
│ delivery_date   │ DateTime │    0 │ PRI SOR │ ᴺᵁᴸᴸ    │       │
│ delivery_status │ Bool     │    0 │         │ ᴺᵁᴸᴸ    │       │
└─────────────────┴──────────┴──────┴─────────┴─────────┴───────┘

```


### См. также​

- system.columns

## SHOW DICTIONARIES​

ОператорSHOW DICTIONARIESотображает списоксловарей.


### Синтаксис​


```
SHOW DICTIONARIES [FROM <db>] [LIKE '<pattern>'] [LIMIT <N>] [INTO OUTFILE <filename>] [FORMAT <format>]

```

Если предложениеFROMне указано, запрос возвращает список словарей из текущей базы данных.

Те же результаты, что и при выполнении запросаSHOW DICTIONARIES, можно получить следующим образом:


```
SELECT name FROM system.dictionaries WHERE database = <db> [AND name LIKE <pattern>] [LIMIT <N>] [INTO OUTFILE <filename>] [FORMAT <format>]

```


### Примеры​

Следующий запрос выбирает первые две строки из списка таблиц базы данныхsystem, имена которых содержатreg.


```
SHOW DICTIONARIES FROM db LIKE '%reg%' LIMIT 2

```


```
┌─name─────────┐
│ regions      │
│ region_names │
└──────────────┘

```


## SHOW INDEX​

Отображает список первичных и индексов пропуска данных таблицы.

Этот оператор существует главным образом для совместимости с MySQL. Системные таблицыsystem.tables(для
первичных ключей) иsystem.data_skipping_indices(для индексов пропуска данных)
предоставляют эквивалентную информацию, но в более естественной для ClickHouse форме.


### Синтаксис​


```
SHOW [EXTENDED] {INDEX | INDEXES | INDICES | KEYS } {FROM | IN} <table> [{FROM | IN} <db>] [WHERE <expr>] [INTO OUTFILE <filename>] [FORMAT <format>]

```

Имя базы данных и таблицы может быть указано в сокращённой форме как<db>.<table>, т.е.FROM tab FROM dbиFROM db.tabявляются
эквивалентными. Если база данных не указана, в запросе используется текущая база данных.

Необязательное ключевое словоEXTENDEDв данный момент не оказывает никакого эффекта и существует для совместимости с MySQL.

Оператор возвращает результирующую таблицу со следующей структурой:


### Примеры​

В этом примере мы используем операторSHOW INDEX, чтобы получить информацию обо всех индексах в таблице 'tbl'.


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


### См. также​

- system.tables
- system.data_skipping_indices

## SHOW PROCESSLIST​

Выводит содержимое таблицыsystem.processes, в которой хранится список запросов, обрабатываемых в данный момент, за исключением запросовSHOW PROCESSLIST.


### Синтаксис​


```
SHOW PROCESSLIST [INTO OUTFILE filename] [FORMAT format]

```

ЗапросSELECT * FROM system.processesвозвращает данные обо всех выполняющихся запросах.

Выполните в консоли:$ watch -n1 "clickhouse-client --query='SHOW PROCESSLIST'"


```
$ watch -n1 "clickhouse-client --query='SHOW PROCESSLIST'"

```


## SHOW GRANTS​

ОператорSHOW GRANTSотображает привилегии, предоставленные пользователю.


### Синтаксис​


```
SHOW GRANTS [FOR user1 [, user2 ...]] [WITH IMPLICIT] [FINAL]

```

Если пользователь не указан, запрос возвращает привилегии для текущего пользователя.

МодификаторWITH IMPLICITпозволяет отображать неявно предоставленные привилегии (например,GRANT SELECT ON system.one).

МодификаторFINALобъединяет все привилегии, выданные пользователю и его ролям (с учетом наследования).


## SHOW CREATE USER​

ОператорSHOW CREATE USERвыводит параметры, которые были заданы присоздании пользователя.


### Синтаксис​


```
SHOW CREATE USER [name1 [, name2 ...] | CURRENT_USER]

```


## SHOW CREATE ROLE​

КомандаSHOW CREATE ROLEвыводит параметры, использованные присоздании роли.


### Синтаксис​


```
SHOW CREATE ROLE name1 [, name2 ...]

```


## SHOW CREATE ROW POLICY​

ОператорSHOW CREATE ROW POLICYвыводит параметры, которые были использованы присоздании политики строк.


### Синтаксис​


```
SHOW CREATE [ROW] POLICY name ON [database1.]table1 [, [database2.]table2 ...]

```


## SHOW CREATE QUOTA​

ОператорSHOW CREATE QUOTAотображает параметры, использованные присоздании квоты.


### Синтаксис​


```
SHOW CREATE QUOTA [name1 [, name2 ...] | CURRENT]

```


## SHOW CREATE SETTINGS PROFILE​

ОператорSHOW CREATE SETTINGS PROFILEвыводит параметры, которые были использованы присоздании профиля настроек.


### Синтаксис​


```
SHOW CREATE [SETTINGS] PROFILE name1 [, name2 ...]

```


## SHOW USERS​

ОператорSHOW USERSвозвращает список именучетных записей пользователей.
Чтобы просмотреть параметры учетных записей пользователей, обратитесь к системной таблицеsystem.users.


### Синтаксис​


```
SHOW USERS

```


## SHOW ROLES​

ОператорSHOW ROLESвозвращает списокролей.
Для просмотра дополнительных параметров
см. системные таблицыsystem.rolesиsystem.role_grants.


### Синтаксис​


```
SHOW [CURRENT|ENABLED] ROLES

```


## SHOW PROFILES​

ОператорSHOW PROFILESвозвращает списокпрофилей настроек.
Для просмотра параметров учетных записей пользователей см. системную таблицуsettings_profiles.


### Синтаксис​


```
SHOW [SETTINGS] PROFILES

```


## SHOW POLICIES​

ОператорSHOW POLICIESвозвращает списокполитик строкдля указанной таблицы.
Чтобы просмотреть параметры учетных записей пользователей, см. системную таблицуsystem.row_policies.


### Синтаксис​


```
SHOW [ROW] POLICIES [ON [db.]table]

```


## SHOW QUOTAS​

ОператорSHOW QUOTASвозвращает списокквот.
Для просмотра параметров квот см. системную таблицуsystem.quotas.


### Синтаксис​


```
SHOW QUOTAS

```


## SHOW QUOTA​

ОператорSHOW QUOTAвозвращает информацию об использованииквотдля всех пользователей или только для текущего пользователя.
Для просмотра дополнительных параметров используйте системные таблицыsystem.quotas_usageиsystem.quota_usage.


### Синтаксис​


```
SHOW [CURRENT] QUOTA

```


## SHOW ACCESS​

ОператорSHOW ACCESSотображает всехпользователей,роли,профилии т.д., а также все ихправа доступа.


### Синтаксис​


```
SHOW ACCESS

```


## SHOW CLUSTER(S)​

ОператорSHOW CLUSTER(S)возвращает список кластеров.
Все доступные кластеры перечислены в таблицеsystem.clusters.

ЗапросSHOW CLUSTER nameотображает поляcluster,shard_num,replica_num,host_name,host_addressиportтаблицыsystem.clustersдля кластера с указанным именем.


### Синтаксис​


```
SHOW CLUSTER '<name>'
SHOW CLUSTERS [[NOT] LIKE|ILIKE '<pattern>'] [LIMIT <N>]

```


### Примеры​


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


## SHOW SETTINGS​

ОператорSHOW SETTINGSвозвращает список системных настроек и их значений.
Он запрашивает данные из таблицыsystem.settings.


### Синтаксис​


```
SHOW [CHANGED] SETTINGS LIKE|ILIKE <name>

```


### Условия​

LIKE|ILIKEпозволяют задать шаблон для имени настройки. Он может содержать шаблонные символы, такие как%или_. УсловиеLIKEчувствительно к регистру,ILIKE— нечувствительно.

Когда используется условиеCHANGED, запрос возвращает только те настройки, которые были изменены по сравнению со значениями по умолчанию.


### Примеры​

Запрос с условиемLIKE:


```
SHOW SETTINGS LIKE 'send_timeout';

```


```
┌─name─────────┬─type────┬─value─┐
│ send_timeout │ Seconds │ 300   │
└──────────────┴─────────┴───────┘

```

Запрос с условиемILIKE:


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

Запрос с условиемCHANGED:


```
SHOW CHANGED SETTINGS ILIKE '%MEMORY%'

```


```
┌─name─────────────┬─type───┬─value───────┐
│ max_memory_usage │ UInt64 │ 10000000000 │
└──────────────────┴────────┴─────────────┘

```


## SHOW SETTING​

ОператорSHOW SETTINGвыводит значение указанной настройки.


### Синтаксис​


```
SHOW SETTING <name>

```


### См. также​

- таблицаsystem.settings

## Просмотр кэшей файловой системы​


### Примеры​


```
SHOW FILESYSTEM CACHES

```


```
┌─Caches────┐
│ s3_cache  │
└───────────┘

```


### См. также​

- таблицаsystem.settings

## SHOW ENGINES​

ОператорSHOW ENGINESвыводит содержимое таблицыsystem.table_engines,
которая содержит описание движков таблиц, поддерживаемых сервером, и информацию о поддерживаемых ими возможностях.


### Синтаксис​


```
SHOW ENGINES [INTO OUTFILE filename] [FORMAT format]

```


### См. также​

- таблицаsystem.table_engines

## SHOW FUNCTIONS​

ОператорSHOW FUNCTIONSвыводит содержимое таблицыsystem.functions.


### Синтаксис​


```
SHOW FUNCTIONS [LIKE | ILIKE '<pattern>']

```

Если указан операторLIKEилиILIKE, запрос возвращает список системных функций, имена которых соответствуют указанному шаблону<pattern>.


### См. также​

- Таблицаsystem.functions

## SHOW MERGES​

ОператорSHOW MERGESвозвращает список слияний.
Все слияния перечислены в таблицеsystem.merges:


### Синтаксис​


```
SHOW MERGES [[NOT] LIKE|ILIKE '<table_name_pattern>'] [LIMIT <N>]

```


### Примеры​


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


## SHOW CREATE MASKING POLICY​

ОператорSHOW CREATE MASKING POLICYвыводит параметры, которые были использованы присоздании политики маскирования.


### Синтаксис​


```
SHOW CREATE MASKING POLICY name ON [database.]table

```
