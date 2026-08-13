# Движок таблицы PostgreSQL - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/postgresql


## Создание таблицы


```
CREATE TABLE [IF NOT EXISTS] [db.]table_name [ON CLUSTER cluster]
(
    name1 type1 [DEFAULT|MATERIALIZED|ALIAS expr1],
    name2 type2 [DEFAULT|MATERIALIZED|ALIAS expr2],
    ...
) ENGINE = PostgreSQL({host:port, database, table, user, password[, schema, [, on_conflict]] | named_collection[, option=value [,..]]})
SETTINGS
    [ postgresql_connection_pool_size=16, ]
    [ postgresql_connection_pool_wait_timeout=5000, ]
    [ postgresql_connection_pool_retries=2, ]
    [ postgresql_connection_pool_auto_close_connection=false, ]
    [ postgresql_connection_attempt_timeout=2 ]
;

```

- Имена столбцов должны совпадать с именами в исходной таблице PostgreSQL, но можно использовать только часть этих столбцов и в любом порядке.
- Типы столбцов могут отличаться от типов в исходной таблице PostgreSQL. ClickHouse пытается [преобразовывать](https://clickhouse.com/docs/ru/reference/engines/database-engines/postgresql#data_types-support) значения в типы данных ClickHouse.
- Настройка [external_table_functions_use_nulls](https://clickhouse.com/docs/ru/reference/settings/session-settings#external_table_functions_use_nulls) определяет, как обрабатывать столбцы с типом Nullable. Значение по умолчанию: 1. Если указано 0, табличная функция не создаёт столбцы с типом Nullable и вставляет значения по умолчанию вместо null. Это также применимо к значениям NULL внутри массивов.
- `host:port` — адрес сервера PostgreSQL.
- `database` — имя удалённой базы данных.
- `table` — имя удалённой таблицы или запрос, передаваемый в PostgreSQL как есть (см. [Передача запроса вместо имени таблицы](#passing-a-query)).
- `user` — пользователь PostgreSQL.
- `password` — пароль пользователя.
- `schema` — схема таблицы, отличная от используемой по умолчанию. Необязательно.
- `on_conflict` — стратегия разрешения конфликтов. Пример: `ON CONFLICT DO NOTHING`. Необязательно. Примечание: добавление этой опции сделает вставку менее эффективной.

```
<named_collections>
    <postgres_creds>
        <host>localhost</host>
        <port>5432</port>
        <user>postgres</user>
        <password>****</password>
        <schema>schema1</schema>
    </postgres_creds>
</named_collections>

```


```
SELECT * FROM postgresql(postgres_creds, table='table1');

```


## Настройки


### `postgresql_connection_pool_size`


### `postgresql_connection_pool_wait_timeout`


### `postgresql_connection_pool_retries`


### `postgresql_connection_pool_auto_close_connection`


### `postgresql_connection_attempt_timeout`


```
CREATE TABLE pg_table
(
    `float_nullable` Nullable(Float32),
    `str` String,
    `int_id` Int32
)
ENGINE = PostgreSQL('localhost:5432', 'public', 'test', 'postgres_user', 'postgres_password')
SETTINGS postgresql_connection_pool_size = 32, postgresql_connection_pool_auto_close_connection = 1;

```


## Подробности реализации


## Передача запроса вместо имени таблицы


```
CREATE TABLE pg_table ENGINE = PostgreSQL('localhost:5432', 'test', (SELECT a, b FROM t1 JOIN t2 USING (id) WHERE a > 0), 'user', 'password');
CREATE TABLE pg_table ENGINE = PostgreSQL('localhost:5432', 'test', query('SELECT a, b FROM t1 JOIN t2 USING (id) WHERE a > 0'), 'user', 'password');

```


```
CREATE TABLE test_replicas (id UInt32, name String) ENGINE = PostgreSQL(`postgres{2|3|4}:5432`, 'clickhouse', 'test_replicas', 'postgres', 'mysecretpassword');

```


```
<postgresql>
    <port>5432</port>
    <user>clickhouse</user>
    <password>qwerty</password>
    <replica>
        <host>example01-1</host>
        <priority>1</priority>
    </replica>
    <replica>
        <host>example01-2</host>
        <priority>2</priority>
    </replica>
    <db>db_name</db>
    <table>table_name</table>
    <where>id=10</where>
    <invalidate_query>SQL_QUERY</invalidate_query>
</postgresql>
</source>

```


## Пример использования


### Таблица в PostgreSQL


```
postgres=# CREATE TABLE "public"."test" (
"int_id" SERIAL,
"int_nullable" INT NULL DEFAULT NULL,
"float" FLOAT NOT NULL,
"str" VARCHAR(100) NOT NULL DEFAULT '',
"float_nullable" FLOAT NULL DEFAULT NULL,
PRIMARY KEY (int_id));

CREATE TABLE

postgres=# INSERT INTO test (int_id, str, "float") VALUES (1,'test',2);
INSERT 0 1

postgresql> SELECT * FROM test;
int_id | int_nullable | float | str  | float_nullable
--------+--------------+-------+------+----------------
       1 |              |     2 | test |
(1 row)

```


### Создание таблицы в ClickHouse и подключение к таблице PostgreSQL, созданной выше


```
CREATE TABLE default.postgresql_table
(
    `float_nullable` Nullable(Float32),
    `str` String,
    `int_id` Int32
)
ENGINE = PostgreSQL('localhost:5432', 'public', 'test', 'postgres_user', 'postgres_password');

```


### Вставка исходных данных из таблицы PostgreSQL в таблицу ClickHouse с помощью запроса SELECT


```
CREATE TABLE default.postgresql_copy
(
    `float_nullable` Nullable(Float32),
    `str` String,
    `int_id` Int32
)
ENGINE = MergeTree
ORDER BY (int_id);

```


```
INSERT INTO default.postgresql_copy
SELECT * FROM postgresql('localhost:5432', 'public', 'test', 'postgres_user', 'postgres_password');

```


### Вставка инкрементальных данных из таблицы PostgreSQL в таблицу ClickHouse


```
SELECT max(`int_id`) AS maxIntID FROM default.postgresql_copy;

```


```
INSERT INTO default.postgresql_copy
SELECT * FROM postgresql('localhost:5432', 'public', 'test', 'postgres_user', 'postgres_password')
WHERE int_id > (SELECT max(int_id) FROM default.postgresql_copy);

```


### Выборка данных из итоговой таблицы ClickHouse


```
SELECT * FROM postgresql_copy WHERE str IN ('test');

```


```
┌─float_nullable─┬─str──┬─int_id─┐
│           ᴺᵁᴸᴸ │ test │      1 │
└────────────────┴──────┴────────┘

```


### Использование нестандартной схемы


```
postgres=# CREATE SCHEMA "nice.schema";

postgres=# CREATE TABLE "nice.schema"."nice.table" (a integer);

postgres=# INSERT INTO "nice.schema"."nice.table" SELECT i FROM generate_series(0, 99) as t(i)

```


```
CREATE TABLE pg_table_schema_with_dots (a UInt32)
        ENGINE PostgreSQL('localhost:5432', 'clickhouse', 'nice.table', 'postgrsql_user', 'password', 'nice.schema');

```

- [Табличная функция `postgresql`](https://clickhouse.com/docs/ru/reference/functions/table-functions/postgresql)
- [Использование PostgreSQL в качестве источника для словаря](https://clickhouse.com/docs/ru/reference/statements/create/dictionary/sources/postgresql)

## Связанные материалы

- Блог: [ClickHouse и PostgreSQL — идеальная пара для работы с данными — часть 1](https://clickhouse.com/blog/migrating-data-between-clickhouse-postgres)
- Блог: [ClickHouse и PostgreSQL — идеальная пара для работы с данными — часть 2](https://clickhouse.com/blog/migrating-data-between-clickhouse-postgres-part-2)
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
