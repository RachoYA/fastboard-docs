# Оператор GRANT - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/statements/grant

- Выдаёт [привилегии](#privileges) учётным записям пользователей ClickHouse или ролям.
- Назначает роли учётным записям пользователей или другим ролям.

## Синтаксис предоставления привилегий


```
GRANT [ON CLUSTER cluster_name] privilege[(column_name [,...])] [,...] ON {db.table[*]|db[*].*|*.*|table[*]|*} TO {user | role | CURRENT_USER} [,...] [WITH GRANT OPTION] [WITH REPLACE OPTION]

```

- `privilege` — тип привилегии.
- `role` — роль пользователя ClickHouse.
- `user` — учетная запись пользователя ClickHouse.

## Синтаксис назначения роли


```
GRANT [ON CLUSTER cluster_name] role [,...] TO {user | another_role | CURRENT_USER} [,...] [WITH ADMIN OPTION] [WITH REPLACE OPTION]

```

- `role` — роль пользователя ClickHouse.
- `user` — учётная запись пользователя ClickHouse.

## Синтаксис GRANT CURRENT GRANTS


```
GRANT CURRENT GRANTS{(privilege[(column_name [,...])] [,...] ON {db.table|db.*|*.*|table|*}) | ON {db.table|db.*|*.*|table|*}} TO {user | role | CURRENT_USER} [,...] [WITH GRANT OPTION] [WITH REPLACE OPTION]

```

- `privilege` — Тип привилегии.
- `role` — Роль пользователя ClickHouse.
- `user` — Учётная запись пользователя ClickHouse.

## Использование


```
GRANT SELECT(x,y) ON db.table TO john WITH GRANT OPTION

```

- `SELECT x,y FROM db.table`.
- `SELECT x FROM db.table`.
- `SELECT y FROM db.table`.

## Привилегии с подстановочными знаками


```
SELECT * FROM db.my_tables -- выдан
SELECT * FROM db.my_tables_0 -- выдан
SELECT * FROM db.my_tables_1 -- выдан

SELECT * FROM db.other_table -- не_выдан
SELECT * FROM db2.my_tables -- не_выдан

```


```
SELECT * FROM db.my_tables -- выдан
SELECT * FROM db.my_tables_0 -- выдан
SELECT * FROM db.my_tables_1 -- выдан
SELECT * FROM db.other_table -- выдан
SELECT * FROM db2.my_tables -- выдан

```


```
GRANT SELECT ON db.* TO john -- верно
GRANT SELECT ON db*.* TO john -- верно

GRANT SELECT ON *.my_table TO john -- неверно
GRANT SELECT ON foo*bar TO john -- неверно
GRANT SELECT ON *suffix TO john -- неверно
GRANT SELECT(foo) ON db.table* TO john -- неверно

```


## Привилегии

- [`ALL`](#all)
- [`УПРАВЛЕНИЕ ДОСТУПОМ`](#access-management)
- `ALLOW SQL SECURITY NONE`
- `ALTER QUOTA`
- `ALTER ROLE`
- `ALTER ROW POLICY`
- `ALTER SETTINGS PROFILE`
- `ALTER USER`
- `CREATE QUOTA`
- `CREATE ROLE`
- `CREATE ROW POLICY`
- `CREATE SETTINGS PROFILE`
- `CREATE USER`
- `DROP QUOTA`
- `DROP ROLE`
- `DROP ROW POLICY`
- `DROP SETTINGS PROFILE`
- `DROP USER`
- `ROLE ADMIN`
- `SHOW ACCESS`
- `SHOW QUOTAS`
- `SHOW ROLES`
- `SHOW ROW POLICIES`
- `SHOW SETTINGS PROFILES`
- `SHOW USERS`
- [`ALTER`](#alter)
- `ALTER DATABASE`
- `ALTER DATABASE SETTINGS`
- `ALTER TABLE`
- `ALTER COLUMN`
- `ALTER ADD COLUMN`
- `ALTER CLEAR COLUMN`
- `ALTER COMMENT COLUMN`
- `ALTER DROP COLUMN`
- `ALTER MATERIALIZE COLUMN`
- `ALTER MODIFY COLUMN`
- `ALTER RENAME COLUMN`
- `ALTER CONSTRAINT`
- `ALTER ADD CONSTRAINT`
- `ALTER DROP CONSTRAINT`
- `ALTER MODIFY CONSTRAINT`
- `ALTER DELETE`
- `ALTER FETCH PARTITION`
- `ALTER FREEZE PARTITION`
- `ALTER INDEX`
- `ALTER ADD INDEX`
- `ALTER CLEAR INDEX`
- `ALTER DROP INDEX`
- `ALTER MATERIALIZE INDEX`
- `ALTER ORDER BY`
- `ALTER SAMPLE BY`
- `ALTER MATERIALIZE TTL`
- `ALTER MODIFY COMMENT`
- `ALTER MOVE PARTITION`
- `ALTER PROJECTION`
- `ALTER SETTINGS`
- `ALTER STATISTICS`
- `ALTER ADD STATISTICS`
- `ALTER DROP STATISTICS`
- `ALTER MATERIALIZE STATISTICS`
- `ALTER MODIFY STATISTICS`
- `ALTER TTL`
- `ALTER UPDATE`
- `ALTER TABLE EXECUTE`
- `ALTER VIEW`
- `ALTER VIEW MODIFY QUERY`
- `ALTER VIEW REFRESH`
- `ALTER VIEW MODIFY SQL SECURITY`
- [`BACKUP`](#backup)
- [`CLUSTER`](#cluster)
- [`CREATE`](#create)
- `CREATE ARBITRARY TEMPORARY TABLE`
- `CREATE TEMPORARY TABLE`
- `CREATE DATABASE`
- `CREATE DICTIONARY`
- `CREATE FUNCTION`
- `CREATE RESOURCE`
- `CREATE TABLE`
- `CREATE VIEW`
- `CREATE WORKLOAD`
- [`dictGet`](#dictget)
- [`displaySecretsInShowAndSelect`](#displaysecretsinshowandselect)
- [`DROP`](#drop)
- `DROP DATABASE`
- `DROP DICTIONARY`
- `DROP FUNCTION`
- `DROP RESOURCE`
- `DROP TABLE`
- `DROP VIEW`
- `DROP WORKLOAD`
- [`INSERT`](#insert)
- [`INTROSPECTION`](#introspection)
- `addressToLine`
- `addressToLineWithInlines`
- `addressToSymbol`
- `demangle`
- `KILL QUERY`
- `KILL TRANSACTION`
- `MOVE PARTITION BETWEEN SHARDS`
- [`NAMED COLLECTION ADMIN`](#named-collection-admin)
- `ALTER NAMED COLLECTION`
- `CREATE NAMED COLLECTION`
- `DROP NAMED COLLECTION`
- `NAMED COLLECTION`
- `SHOW NAMED COLLECTIONS`
- `SHOW NAMED COLLECTIONS SECRETS`
- [`OPTIMIZE`](#optimize)
- [`SELECT`](#select)
- [`SET DEFINER`](https://clickhouse.com/docs/ru/reference/statements/create/view#sql_security)
- [`SHOW`](#show)
- `SHOW COLUMNS`
- `SHOW DATABASES`
- `SHOW DICTIONARIES`
- `SHOW TABLES`
- `SHOW FILESYSTEM CACHES`
- [`SOURCES`](#sources)
- `AZURE`
- `FILE`
- `HDFS`
- `HIVE`
- `JDBC`
- `KAFKA`
- `MONGO`
- `MYSQL`
- `NATS`
- `ODBC`
- `POSTGRES`
- `RABBITMQ`
- `REDIS`
- `REMOTE`
- `S3`
- `SQLITE`
- `URL`
- [`SYSTEM`](#system)
- `SYSTEM CLEANUP`
- `SYSTEM DROP CACHE`
- `SYSTEM DROP COMPILED EXPRESSION CACHE`
- `SYSTEM DROP CONNECTIONS CACHE`
- `SYSTEM DROP DISTRIBUTED CACHE`
- `SYSTEM DROP DNS CACHE`
- `SYSTEM DROP FILESYSTEM CACHE`
- `SYSTEM DROP FORMAT SCHEMA CACHE`
- `SYSTEM DROP MARK CACHE`
- `SYSTEM DROP MMAP CACHE`
- `SYSTEM DROP PAGE CACHE`
- `SYSTEM DROP PRIMARY INDEX CACHE`
- `SYSTEM DROP QUERY CACHE`
- `SYSTEM DROP S3 CLIENT CACHE`
- `SYSTEM DROP SCHEMA CACHE`
- `SYSTEM DROP UNCOMPRESSED CACHE`
- `SYSTEM DROP PRIMARY INDEX CACHE`
- `SYSTEM DROP REPLICA`
- `SYSTEM FAILPOINT`
- `SYSTEM FETCHES`
- `SYSTEM FLUSH`
- `SYSTEM FLUSH ASYNC INSERT QUEUE`
- `SYSTEM FLUSH LOGS`
- `SYSTEM JEMALLOC`
- `SYSTEM KILL QUERY`
- `SYSTEM KILL TRANSACTION`
- `SYSTEM LISTEN`
- `SYSTEM LOAD PRIMARY KEY`
- `SYSTEM MERGES`
- `SYSTEM MOVES`
- `SYSTEM PULLING REPLICATION LOG`
- `SYSTEM REDUCE BLOCKING PARTS`
- `SYSTEM REPLICATION QUEUES`
- `SYSTEM REPLICA READINESS`
- `SYSTEM RESET DDL WORKER`
- `SYSTEM RESTART DISK`
- `SYSTEM RESTART REPLICA`
- `SYSTEM RESTORE REPLICA`
- `SYSTEM RELOAD`
- `SYSTEM RELOAD ASYNCHRONOUS METRICS`
- `SYSTEM RELOAD CONFIG`
- `SYSTEM RELOAD DICTIONARY`
- `SYSTEM RELOAD EMBEDDED DICTIONARIES`
- `SYSTEM RELOAD FUNCTION`
- `SYSTEM RELOAD MODEL`
- `SYSTEM RELOAD USERS`
- `SYSTEM SENDS`
- `SYSTEM DISTRIBUTED SENDS`
- `SYSTEM REPLICATED SENDS`
- `SYSTEM SHUTDOWN`
- `SYSTEM SYNC DATABASE REPLICA`
- `SYSTEM SYNC FILE CACHE`
- `SYSTEM SYNC FILESYSTEM CACHE`
- `SYSTEM SYNC REPLICA`
- `SYSTEM SYNC TRANSACTION LOG`
- `SYSTEM THREAD FUZZER`
- `SYSTEM TTL MERGES`
- `SYSTEM UNFREEZE`
- `SYSTEM UNLOAD PRIMARY KEY`
- `SYSTEM VIEWS`
- `SYSTEM VIRTUAL PARTS UPDATE`
- `SYSTEM WAIT LOADING PARTS`
- [`TABLE ENGINE`](#table-engine)
- [`TRUNCATE`](#truncate)
- `UNDROP TABLE`
- [`NONE`](#none)
- Привилегия `ALTER` включает все остальные привилегии `ALTER*`.
- `ALTER CONSTRAINT` включает привилегии `ALTER ADD CONSTRAINT`, `ALTER DROP CONSTRAINT` и `ALTER MODIFY CONSTRAINT`.
- `COLUMN` — привилегию можно выдать для столбца, таблицы, базы данных или глобально.
- `TABLE` — привилегию можно выдать для таблицы, базы данных или глобально.
- `VIEW` — привилегию можно выдать для представления, базы данных или глобально.
- `DICTIONARY` — привилегию можно выдать для словаря, базы данных или глобально.
- `DATABASE` — привилегию можно выдать для базы данных или глобально.
- `GLOBAL` — привилегию можно выдать только глобально.
- `GROUP` — группирует привилегии разных уровней. Когда выдается привилегия уровня `GROUP`, выдаются только те привилегии из группы, которые соответствуют используемому синтаксису.
- `GRANT SELECT(x) ON db.table TO user`
- `GRANT SELECT ON db.* TO user`
- `GRANT CREATE USER(x) ON db.table TO user`
- `GRANT CREATE USER ON db.* TO user`

### SELECT


```
GRANT SELECT(x,y) ON db.table TO john

```


### INSERT


```
GRANT INSERT(x,y) ON db.table TO john

```


### ALTER

- `ALTER`. Уровень: `COLUMN`.
- `ALTER TABLE`. Уровень: `GROUP`
- `ALTER UPDATE`. Уровень: `COLUMN`. Псевдонимы: `UPDATE`
- `ALTER DELETE`. Уровень: `COLUMN`. Псевдонимы: `DELETE`
- `ALTER COLUMN`. Уровень: `GROUP`
- `ALTER ADD COLUMN`. Уровень: `COLUMN`. Псевдонимы: `ADD COLUMN`
- `ALTER DROP COLUMN`. Уровень: `COLUMN`. Псевдонимы: `DROP COLUMN`
- `ALTER MODIFY COLUMN`. Уровень: `COLUMN`. Псевдонимы: `MODIFY COLUMN`
- `ALTER COMMENT COLUMN`. Уровень: `COLUMN`. Псевдонимы: `COMMENT COLUMN`
- `ALTER CLEAR COLUMN`. Уровень: `COLUMN`. Псевдонимы: `CLEAR COLUMN`
- `ALTER RENAME COLUMN`. Уровень: `COLUMN`. Псевдонимы: `RENAME COLUMN`
- `ALTER INDEX`. Уровень: `GROUP`. Псевдонимы: `INDEX`
- `ALTER ORDER BY`. Уровень: `TABLE`. Псевдонимы: `ALTER MODIFY ORDER BY`, `MODIFY ORDER BY`
- `ALTER SAMPLE BY`. Уровень: `TABLE`. Псевдонимы: `ALTER MODIFY SAMPLE BY`, `MODIFY SAMPLE BY`
- `ALTER ADD INDEX`. Уровень: `TABLE`. Псевдонимы: `ADD INDEX`
- `ALTER DROP INDEX`. Уровень: `TABLE`. Псевдонимы: `DROP INDEX`
- `ALTER MATERIALIZE INDEX`. Уровень: `TABLE`. Псевдонимы: `MATERIALIZE INDEX`
- `ALTER CLEAR INDEX`. Уровень: `TABLE`. Псевдонимы: `CLEAR INDEX`
- `ALTER CONSTRAINT`. Уровень: `GROUP`. Псевдонимы: `CONSTRAINT`
- `ALTER ADD CONSTRAINT`. Уровень: `TABLE`. Псевдонимы: `ADD CONSTRAINT`
- `ALTER DROP CONSTRAINT`. Уровень: `TABLE`. Псевдонимы: `DROP CONSTRAINT`
- `ALTER MODIFY CONSTRAINT`. Уровень: `TABLE`. Псевдонимы: `MODIFY CONSTRAINT`
- `ALTER TTL`. Уровень: `TABLE`. Псевдонимы: `ALTER MODIFY TTL`, `MODIFY TTL`
- `ALTER MATERIALIZE TTL`. Уровень: `TABLE`. Псевдонимы: `MATERIALIZE TTL`
- `ALTER SETTINGS`. Уровень: `TABLE`. Псевдонимы: `ALTER SETTING`, `ALTER MODIFY SETTING`, `MODIFY SETTING`
- `ALTER MOVE PARTITION`. Уровень: `TABLE`. Псевдонимы: `ALTER MOVE PART`, `MOVE PARTITION`, `MOVE PART`
- `ALTER FETCH PARTITION`. Уровень: `TABLE`. Псевдонимы: `ALTER FETCH PART`, `FETCH PARTITION`, `FETCH PART`
- `ALTER FREEZE PARTITION`. Уровень: `TABLE`. Псевдонимы: `FREEZE PARTITION`
- `ALTER EXECUTE`. Уровень: `TABLE`. Псевдонимы: `ALTER TABLE EXECUTE`
- `ALTER VIEW`. Уровень: `GROUP`
- `ALTER VIEW REFRESH`. Уровень: `VIEW`. Псевдонимы: `REFRESH VIEW`
- `ALTER VIEW MODIFY QUERY`. Уровень: `VIEW`. Псевдонимы: `ALTER TABLE MODIFY QUERY`
- `ALTER VIEW MODIFY SQL SECURITY`. Уровень: `VIEW`. Псевдонимы: `ALTER TABLE MODIFY SQL SECURITY`
- Привилегия `ALTER` включает все остальные привилегии `ALTER*`.
- `ALTER CONSTRAINT` включает привилегии `ALTER ADD CONSTRAINT`, `ALTER DROP CONSTRAINT` и `ALTER MODIFY CONSTRAINT`.
- Привилегия `MODIFY SETTING` позволяет изменять настройки движка таблицы. Она не влияет на настройки или параметры конфигурации сервера.
- Для операции `ATTACH` требуется привилегия [CREATE](#create).
- Для операции `DETACH` требуется привилегия [DROP](#drop).
- Чтобы остановить мутацию запросом [KILL MUTATION](https://clickhouse.com/docs/ru/reference/statements/kill#kill-mutation), необходимо иметь привилегию, позволяющую запускать эту мутацию. Например, если вы хотите остановить запрос `ALTER UPDATE`, вам нужна привилегия `ALTER UPDATE`, `ALTER TABLE` или `ALTER`.

### BACKUP


### CREATE

- `CREATE`. Уровень: `GROUP`
- `CREATE DATABASE`. Уровень: `DATABASE`
- `CREATE TABLE`. Уровень: `TABLE`
- `CREATE ARBITRARY TEMPORARY TABLE`. Уровень: `GLOBAL`
- `CREATE TEMPORARY TABLE`. Уровень: `GLOBAL`
- `CREATE VIEW`. Уровень: `VIEW`
- `CREATE DICTIONARY`. Уровень: `DICTIONARY`
- Чтобы удалить созданную таблицу, пользователю нужна привилегия [DROP](#drop).

### CLUSTER


```
GRANT CLUSTER ON *.* TO <username>

```


```
Недостаточно привилегий. Для выполнения этого запроса необходимо иметь grant CLUSTER ON *.*. 

```


```
<access_control_improvements>
    <on_cluster_queries_require_cluster_grant>true</on_cluster_queries_require_cluster_grant>
</access_control_improvements>

```


### DROP

- `DROP`. Уровень: `GROUP`
- `DROP DATABASE`. Уровень: `DATABASE`
- `DROP TABLE`. Уровень: `TABLE`
- `DROP VIEW`. Уровень: `VIEW`
- `DROP DICTIONARY`. Уровень: `DICTIONARY`

### TRUNCATE


### OPTIMIZE


### SHOW

- `SHOW`. Уровень: `GROUP`
- `SHOW DATABASES`. Уровень: `DATABASE`. Позволяет выполнять запросы `SHOW DATABASES`, `SHOW CREATE DATABASE`, `USE <database>`.
- `SHOW TABLES`. Уровень: `TABLE`. Позволяет выполнять запросы `SHOW TABLES`, `EXISTS <table>`, `CHECK <table>`.
- `SHOW COLUMNS`. Уровень: `COLUMN`. Позволяет выполнять запросы `SHOW CREATE TABLE`, `DESCRIBE`.
- `SHOW DICTIONARIES`. Уровень: `DICTIONARY`. Позволяет выполнять запросы `SHOW DICTIONARIES`, `SHOW CREATE DICTIONARY`, `EXISTS <dictionary>`.

### KILL QUERY


### УПРАВЛЕНИЕ ДОСТУПОМ

- `ACCESS MANAGEMENT`. Уровень: `GROUP`
- `CREATE USER`. Уровень: `GLOBAL`
- `ALTER USER`. Уровень: `GLOBAL`
- `DROP USER`. Уровень: `GLOBAL`
- `CREATE ROLE`. Уровень: `GLOBAL`
- `ALTER ROLE`. Уровень: `GLOBAL`
- `DROP ROLE`. Уровень: `GLOBAL`
- `ROLE ADMIN`. Уровень: `GLOBAL`
- `CREATE ROW POLICY`. Уровень: `GLOBAL`. Псевдонимы: `CREATE POLICY`
- `ALTER ROW POLICY`. Уровень: `GLOBAL`. Псевдонимы: `ALTER POLICY`
- `DROP ROW POLICY`. Уровень: `GLOBAL`. Псевдонимы: `DROP POLICY`
- `CREATE QUOTA`. Уровень: `GLOBAL`
- `ALTER QUOTA`. Уровень: `GLOBAL`
- `DROP QUOTA`. Уровень: `GLOBAL`
- `CREATE SETTINGS PROFILE`. Уровень: `GLOBAL`. Псевдонимы: `CREATE PROFILE`
- `ALTER SETTINGS PROFILE`. Уровень: `GLOBAL`. Псевдонимы: `ALTER PROFILE`
- `DROP SETTINGS PROFILE`. Уровень: `GLOBAL`. Псевдонимы: `DROP PROFILE`
- `SHOW ACCESS`. Уровень: `GROUP`
- `SHOW_USERS`. Уровень: `GLOBAL`. Псевдонимы: `SHOW CREATE USER`
- `SHOW_ROLES`. Уровень: `GLOBAL`. Псевдонимы: `SHOW CREATE ROLE`
- `SHOW_ROW_POLICIES`. Уровень: `GLOBAL`. Псевдонимы: `SHOW POLICIES`, `SHOW CREATE ROW POLICY`, `SHOW CREATE POLICY`
- `SHOW_QUOTAS`. Уровень: `GLOBAL`. Псевдонимы: `SHOW CREATE QUOTA`
- `SHOW_SETTINGS_PROFILES`. Уровень: `GLOBAL`. Псевдонимы: `SHOW PROFILES`, `SHOW CREATE SETTINGS PROFILE`, `SHOW CREATE PROFILE`
- `ALLOW SQL SECURITY NONE`. Уровень: `GLOBAL`. Псевдонимы: `CREATE SQL SECURITY NONE`, `SQL SECURITY NONE`, `SECURITY NONE`

### SYSTEM

- `SYSTEM`. Уровень: `GROUP`
- `SYSTEM SHUTDOWN`. Уровень: `GLOBAL`. Псевдонимы: `SYSTEM KILL`, `SHUTDOWN`
- `SYSTEM DROP CACHE`. Псевдонимы: `DROP CACHE`
- `SYSTEM DROP DNS CACHE`. Уровень: `GLOBAL`. Псевдонимы: `SYSTEM CLEAR DNS CACHE`, `SYSTEM DROP DNS`, `DROP DNS CACHE`, `DROP DNS`
- `SYSTEM DROP MARK CACHE`. Уровень: `GLOBAL`. Псевдонимы: `SYSTEM CLEAR MARK CACHE`, `SYSTEM DROP MARK`, `DROP MARK CACHE`, `DROP MARKS`
- `SYSTEM DROP UNCOMPRESSED CACHE`. Уровень: `GLOBAL`. Псевдонимы: `SYSTEM CLEAR UNCOMPRESSED CACHE`, `SYSTEM DROP UNCOMPRESSED`, `DROP UNCOMPRESSED CACHE`, `DROP UNCOMPRESSED`
- `SYSTEM RELOAD`. Уровень: `GROUP`
- `SYSTEM RELOAD CONFIG`. Уровень: `GLOBAL`. Псевдонимы: `RELOAD CONFIG`
- `SYSTEM RELOAD DICTIONARY`. Уровень: `GLOBAL`. Псевдонимы: `SYSTEM RELOAD DICTIONARIES`, `RELOAD DICTIONARY`, `RELOAD DICTIONARIES`, `SYSTEM UNLOAD DICTIONARY`, `SYSTEM UNLOAD DICTIONARIES`, `UNLOAD DICTIONARY`, `UNLOAD DICTIONARIES`
- `SYSTEM RELOAD EMBEDDED DICTIONARIES`. Уровень: `GLOBAL`. Псевдонимы: `RELOAD EMBEDDED DICTIONARIES`
- `SYSTEM MERGES`. Уровень: `TABLE`. Псевдонимы: `SYSTEM STOP MERGES`, `SYSTEM START MERGES`, `STOP MERGES`, `START MERGES`
- `SYSTEM TTL MERGES`. Уровень: `TABLE`. Псевдонимы: `SYSTEM STOP TTL MERGES`, `SYSTEM START TTL MERGES`, `STOP TTL MERGES`, `START TTL MERGES`
- `SYSTEM FETCHES`. Уровень: `TABLE`. Псевдонимы: `SYSTEM STOP FETCHES`, `SYSTEM START FETCHES`, `STOP FETCHES`, `START FETCHES`
- `SYSTEM MOVES`. Уровень: `TABLE`. Псевдонимы: `SYSTEM STOP MOVES`, `SYSTEM START MOVES`, `STOP MOVES`, `START MOVES`
- `SYSTEM SENDS`. Уровень: `GROUP`. Псевдонимы: `SYSTEM STOP SENDS`, `SYSTEM START SENDS`, `STOP SENDS`, `START SENDS`
- `SYSTEM DISTRIBUTED SENDS`. Уровень: `TABLE`. Псевдонимы: `SYSTEM STOP DISTRIBUTED SENDS`, `SYSTEM START DISTRIBUTED SENDS`, `STOP DISTRIBUTED SENDS`, `START DISTRIBUTED SENDS`
- `SYSTEM REPLICATED SENDS`. Уровень: `TABLE`. Псевдонимы: `SYSTEM STOP REPLICATED SENDS`, `SYSTEM START REPLICATED SENDS`, `STOP REPLICATED SENDS`, `START REPLICATED SENDS`
- `SYSTEM REPLICATION QUEUES`. Уровень: `TABLE`. Псевдонимы: `SYSTEM STOP REPLICATION QUEUES`, `SYSTEM START REPLICATION QUEUES`, `STOP REPLICATION QUEUES`, `START REPLICATION QUEUES`
- `SYSTEM SYNC REPLICA`. Уровень: `TABLE`. Псевдонимы: `SYNC REPLICA`
- `SYSTEM RESTART REPLICA`. Уровень: `TABLE`. Псевдонимы: `RESTART REPLICA`
- `SYSTEM FLUSH`. Уровень: `GROUP`
- `SYSTEM FLUSH DISTRIBUTED`. Уровень: `TABLE`. Псевдонимы: `FLUSH DISTRIBUTED`
- `SYSTEM FLUSH LOGS`. Уровень: `GLOBAL`. Псевдонимы: `FLUSH LOGS`

### INTROSPECTION

- `INTROSPECTION`. Уровень: `GROUP`. Псевдонимы: `INTROSPECTION FUNCTIONS`
- `addressToLine`. Уровень: `GLOBAL`
- `addressToLineWithInlines`. Уровень: `GLOBAL`
- `addressToSymbol`. Уровень: `GLOBAL`
- `demangle`. Уровень: `GLOBAL`

### SOURCES

- `READ`. Уровень: `GLOBAL_WITH_PARAMETER`
- `WRITE`. Уровень: `GLOBAL_WITH_PARAMETER`
- `AZURE`
- `FILE`
- `HDFS`
- `HIVE`
- `JDBC`
- `KAFKA`
- `MONGO`
- `MYSQL`
- `NATS`
- `ODBC`
- `POSTGRES`
- `RABBITMQ`
- `REDIS`
- `REMOTE`
- `S3`
- `SQLITE`
- `URL`
- Чтобы создать таблицу с [движком таблицы MySQL](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/mysql), требуются привилегии `CREATE TABLE (ON db.table_name)` и `MYSQL`.
- Чтобы использовать [табличную функцию mysql](https://clickhouse.com/docs/ru/reference/functions/table-functions/mysql), требуются привилегии `CREATE TEMPORARY TABLE` и `MYSQL`.

### Привилегии для фильтрации источников


```
GRANT READ ON S3('regexp_pattern') TO user

```


```
-- Разрешить пользователю читать только из путей s3://foo/
GRANT READ ON S3('s3://foo/.*') TO john

-- Разрешить пользователю читать из файлов по определённым шаблонам регулярного выражения
GRANT READ ON S3('s3://mybucket/data/2024/.*\.parquet') TO analyst

-- Одному пользователю можно выдать несколько фильтров
GRANT READ ON S3('s3://foo/.*') TO john
GRANT READ ON S3('s3://bar/.*') TO john

```


```
SELECT * FROM url('https://www.google.com');
SELECT * FROM url('https://www-google.com');

```


```
GRANT READ ON URL('https://www\.google\.com') TO john;

```


```
-- Исходная привилегия с GRANT OPTION
GRANT READ ON S3('s3://foo/.*') TO john WITH GRANT OPTION

-- Теперь John может передать этот доступ другим пользователям
GRANT CURRENT GRANTS(READ ON S3) TO alice

```

- **Частичный отзыв не допускается:** Нельзя отозвать только часть ранее выданного шаблона фильтра. При необходимости нужно отозвать весь grant и выдать его заново с новыми шаблонами.
- **Grant с подстановочными знаками не допускаются:** Нельзя использовать `GRANT READ ON *('regexp')` или аналогичные шаблоны, состоящие только из подстановочных знаков. Необходимо указать конкретный источник.

### dictGet

- `dictGet`. Псевдонимы: `dictHas`, `dictGetHierarchy`, `dictGetRoot`, `dictGetChildren`, `dictGetDescendants`, `dictIsIn`
- `GRANT dictGet ON mydb.mydictionary TO john`
- `GRANT dictGet ON mydictionary TO john`

### displaySecretsInShowAndSelect


### NAMED COLLECTION ADMIN

- `NAMED COLLECTION ADMIN`. Уровень: `NAMED_COLLECTION`. Псевдонимы: `NAMED COLLECTION CONTROL`
- `CREATE NAMED COLLECTION`. Уровень: `NAMED_COLLECTION`
- `DROP NAMED COLLECTION`. Уровень: `NAMED_COLLECTION`
- `ALTER NAMED COLLECTION`. Уровень: `NAMED_COLLECTION`
- `SHOW NAMED COLLECTIONS`. Уровень: `NAMED_COLLECTION`. Псевдонимы: `SHOW NAMED COLLECTIONS`
- `SHOW NAMED COLLECTIONS SECRETS`. Уровень: `NAMED_COLLECTION`. Псевдонимы: `SHOW NAMED COLLECTIONS SECRETS`
- `NAMED COLLECTION`. Уровень: `NAMED_COLLECTION`. Псевдонимы: `NAMED COLLECTION USAGE, USE NAMED COLLECTION`
- `GRANT CREATE NAMED COLLECTION ON abc TO john`

### ДВИЖОК ТАБЛИЦЫ

- `GRANT TABLE ENGINE ON * TO john`
- `GRANT TABLE ENGINE ON TinyLog TO john`
- `GRANT READ, WRITE ON AZURE TO john`

### ALL


### NONE


### ADMIN OPTION

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
