# Движок таблицы MySQL - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/mysql


## Создание таблицы


```
CREATE TABLE [IF NOT EXISTS] [db.]table_name [ON CLUSTER cluster]
(
    name1 [type1] [DEFAULT|MATERIALIZED|ALIAS expr1],
    name2 [type2] [DEFAULT|MATERIALIZED|ALIAS expr2],
    ...
) ENGINE = MySQL({host:port, database, table, user, password[, replace_query, on_duplicate_clause] | named_collection[, option=value [,..]]})
SETTINGS
    [ connection_pool_size=16, ]
    [ connection_max_tries=3, ]
    [ connection_wait_timeout=5, ]
    [ connection_auto_close=true, ]
    [ connect_timeout=10, ]
    [ read_write_timeout=300, ]
    [ enable_compression=false ]
;

```

- Имена столбцов должны совпадать с именами в исходной таблице MySQL, но можно использовать только часть этих столбцов и в любом порядке.
- Типы столбцов могут отличаться от типов в исходной таблице MySQL. ClickHouse пытается [преобразовать](https://clickhouse.com/docs/ru/reference/engines/database-engines/mysql#data_types-support) значения в типы данных ClickHouse.
- Настройка [external_table_functions_use_nulls](https://clickhouse.com/docs/ru/reference/settings/session-settings#external_table_functions_use_nulls) определяет, как обрабатывать столбцы Nullable. Значение по умолчанию: 1. Если установлено значение 0, функция таблицы не создаёт столбцы типа Nullable и вместо NULL выполняет вставку значений по умолчанию. Это также применимо к значениям NULL внутри массивов.
- `host:port` — адрес сервера MySQL.
- `database` — имя удалённой базы данных.
- `table` — имя удалённой таблицы или запрос, передаваемый в MySQL как есть (см. [Передача запроса вместо имени таблицы](#passing-a-query)).
- `user` — пользователь MySQL.
- `password` — пароль пользователя.
- `replace_query` — флаг, преобразующий запросы `INSERT INTO` в `REPLACE INTO`. Если `replace_query=1`, запрос заменяется.
- `on_duplicate_clause` — выражение `ON DUPLICATE KEY on_duplicate_clause`, которое добавляется к запросу `INSERT`. Пример: `INSERT INTO t (c1,c2) VALUES ('a', 2) ON DUPLICATE KEY UPDATE c2 = c2 + 1`, где `on_duplicate_clause` — это `UPDATE c2 = c2 + 1`. См. [документацию MySQL](https://dev.mysql.com/doc/refman/8.0/en/insert-on-duplicate.html), чтобы узнать, какие `on_duplicate_clause` можно использовать с секцией `ON DUPLICATE KEY`. Чтобы указать `on_duplicate_clause`, нужно передать `0` в параметр `replace_query`. Если одновременно передать `replace_query = 1` и `on_duplicate_clause`, ClickHouse сгенерирует исключение.

## Передача запроса вместо имени таблицы


```
CREATE TABLE mysql_table ENGINE = MySQL('localhost:3306', 'test', (SELECT a, b FROM t1 JOIN t2 USING (id) WHERE a > 0), 'user', 'password');
CREATE TABLE mysql_table ENGINE = MySQL('localhost:3306', 'test', query('SELECT a, b FROM t1 JOIN t2 USING (id) WHERE a > 0'), 'user', 'password');

```


```
CREATE TABLE test_replicas (id UInt32, name String, age UInt32, money UInt32) ENGINE = MySQL(`mysql{2|3|4}:3306`, 'clickhouse', 'test_replicas', 'root', 'clickhouse');

```


## Пример использования


```
mysql> CREATE TABLE `test`.`test` (
    ->   `int_id` INT NOT NULL AUTO_INCREMENT,
    ->   `int_nullable` INT NULL DEFAULT NULL,
    ->   `float` FLOAT NOT NULL,
    ->   `float_nullable` FLOAT NULL DEFAULT NULL,
    ->   PRIMARY KEY (`int_id`));
Query OK, 0 rows affected (0,09 sec)

mysql> insert into test (`int_id`, `float`) VALUES (1,2);
Query OK, 1 row affected (0,00 sec)

mysql> select * from test;
+------+----------+-----+----------+
| int_id | int_nullable | float | float_nullable |
+------+----------+-----+----------+
|      1 |         NULL |     2 |           NULL |
+------+----------+-----+----------+
1 row in set (0,00 sec)

```


```
CREATE TABLE mysql_table
(
    `float_nullable` Nullable(Float32),
    `int_id` Int32
)
ENGINE = MySQL('localhost:3306', 'test', 'test', 'bayonet', '123')

```


```
CREATE NAMED COLLECTION creds AS
        host = 'localhost',
        port = 3306,
        database = 'test',
        user = 'bayonet',
        password = '123';
CREATE TABLE mysql_table
(
    `float_nullable` Nullable(Float32),
    `int_id` Int32
)
ENGINE = MySQL(creds, table='test')

```


```
SELECT * FROM mysql_table

```


```
┌─float_nullable─┬─int_id─┐
│           ᴺᵁᴸᴸ │      1 │
└────────────────┴────────┘

```


## Настройки


### `connection_auto_close`

- 1 — автоматическое закрытие соединения разрешено, поэтому его повторное использование отключено
- 0 — автоматическое закрытие соединения не разрешено, поэтому его повторное использование включено

### `connection_max_tries`

- Положительное целое число.
- 0 — Для пула с failover повторные попытки не выполняются.

### `connection_pool_size`

- Положительное целое число.

### `connection_wait_timeout`

- Положительное целое число.

### `connect_timeout`

- Положительное целое число.

### `read_write_timeout`

- Положительное целое число.

### `enable_compression`

- движку таблицы `MySQL`;
- движку базы данных `MySQL`;
- табличной функции `mysql`;
- именованным коллекциям, используемым в интеграциях MySQL.

```
CREATE TABLE mysql_engine_compression
(
    id UInt32,
    name String,
    age UInt32,
    money UInt32
)
ENGINE = MySQL('mysql80:3306', 'clickhouse', 'test_table', 'root', 'password')
SETTINGS enable_compression = 1;

```


## См. также

- [Табличная функция MySQL](https://clickhouse.com/docs/ru/reference/functions/table-functions/mysql)
- [Использование MySQL в качестве источника данных для словаря](https://clickhouse.com/docs/ru/reference/statements/create/dictionary/sources/mysql)
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
