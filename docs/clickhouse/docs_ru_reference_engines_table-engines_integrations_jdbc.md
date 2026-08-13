# Движок таблицы JDBC - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/jdbc


## Создание таблицы


```
CREATE TABLE [IF NOT EXISTS] [db.]table_name
(
    columns list...
)
ENGINE = JDBC(datasource, external_database, external_table)

```

- `datasource` — URI или имя внешней СУБД. Формат URI: `jdbc:<driver_name>://<host_name>:<port>/?user=<username>&password=<password>`. Пример для MySQL: `jdbc:mysql://localhost:3306/?user=root&password=root`.
- `external_database` — имя базы данных во внешней СУБД или, в качестве альтернативы, явно заданная схема таблицы (см. примеры).
- `external_table` — имя таблицы во внешней базе данных или SELECT-запрос, например `select * from table1 where column1=1`.
- Эти параметры также можно передавать с помощью [именованных коллекций](https://clickhouse.com/docs/ru/concepts/features/configuration/server-config/named-collections).

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
CREATE TABLE jdbc_table
(
    `int_id` Int32,
    `int_nullable` Nullable(Int32),
    `float` Float32,
    `float_nullable` Nullable(Float32)
)
ENGINE JDBC('jdbc:mysql://localhost:3306/?user=root&password=root', 'test', 'test')

```


```
SELECT *
FROM jdbc_table

```


```
┌─int_id─┬─int_nullable─┬─float─┬─float_nullable─┐
│      1 │         ᴺᵁᴸᴸ │     2 │           ᴺᵁᴸᴸ │
└────────┴──────────────┴───────┴────────────────┘

```


```
INSERT INTO jdbc_table(`int_id`, `float`)
SELECT toInt32(number), toFloat32(number * 1.0)
FROM system.numbers

```


## См. также

- [Табличная функция JDBC](https://clickhouse.com/docs/ru/reference/functions/table-functions/jdbc).
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
