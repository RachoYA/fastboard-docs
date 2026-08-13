# Движок таблицы ODBC - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/odbc


## Создание таблицы


```
CREATE TABLE [IF NOT EXISTS] [db.]table_name [ON CLUSTER cluster]
(
    name1 [type1],
    name2 [type2],
    ...
)
ENGINE = ODBC(datasource, external_database, external_table)

```

- Имена столбцов должны совпадать с именами в исходной таблице, но можно использовать только часть этих столбцов и в любом порядке.
- Типы столбцов могут отличаться от типов в исходной таблице. ClickHouse пытается [привести](https://clickhouse.com/docs/ru/reference/functions/regular-functions/type-conversion-functions#CAST) значения к типам данных ClickHouse.
- Настройка [external_table_functions_use_nulls](https://clickhouse.com/docs/ru/reference/settings/session-settings#external_table_functions_use_nulls) определяет, как обрабатывать столбцы с типом Nullable. Значение по умолчанию: 1. Если 0, табличная функция не создаёт столбцы с типом Nullable и вместо null вставляет значения по умолчанию. Это также применимо к значениям NULL внутри массивов.
- `datasource` — Имя раздела с настройками подключения в файле `odbc.ini`.
- `external_database` — Имя базы данных во внешней СУБД.
- `external_table` — Имя таблицы в `external_database`.

## Пример использования


```
$ sudo mysql

```


```
mysql> CREATE USER 'clickhouse'@'localhost' IDENTIFIED BY 'clickhouse';
mysql> GRANT ALL PRIVILEGES ON *.* TO 'clickhouse'@'localhost' WITH GRANT OPTION;

```


```
$ cat /etc/odbc.ini
[mysqlconn]
DRIVER = /usr/local/lib/libmyodbc5w.so
SERVER = 127.0.0.1
PORT = 3306
DATABASE = test
USER = clickhouse
PASSWORD = clickhouse

```


```
$ isql -v mysqlconn
+-------------------------+
| Connected!                            |
|                                       |
...

```


```
mysql> CREATE DATABASE test;
Query OK, 1 row affected (0,01 sec)

mysql> CREATE TABLE `test`.`test` (
    ->   `int_id` INT NOT NULL AUTO_INCREMENT,
    ->   `int_nullable` INT NULL DEFAULT NULL,
    ->   `float` FLOAT NOT NULL,
    ->   `float_nullable` FLOAT NULL DEFAULT NULL,
    ->   PRIMARY KEY (`int_id`));
Query OK, 0 rows affected (0,09 sec)

mysql> insert into test.test (`int_id`, `float`) VALUES (1,2);
Query OK, 1 row affected (0,00 sec)

mysql> select * from test.test;
+------+----------+-----+----------+
| int_id | int_nullable | float | float_nullable |
+------+----------+-----+----------+
|      1 |         NULL |     2 |           NULL |
+------+----------+-----+----------+
1 row in set (0,00 sec)

```


```
CREATE TABLE odbc_t
(
    `int_id` Int32,
    `float_nullable` Nullable(Float32)
)
ENGINE = ODBC('DSN=mysqlconn', 'test', 'test')

```


```
SELECT * FROM odbc_t

```


```
┌─int_id─┬─float_nullable─┐
│      1 │           ᴺᵁᴸᴸ │
└────────┴────────────────┘

```


## См. также

- [Словари ODBC](https://clickhouse.com/docs/ru/reference/statements/create/dictionary/sources/odbc)
- [Табличная функция ODBC](https://clickhouse.com/docs/ru/reference/functions/table-functions/odbc)
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
