# Движок таблицы ExternalDistributed - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/ExternalDistributed


## Создание таблицы


```
CREATE TABLE [IF NOT EXISTS] [db.]table_name [ON CLUSTER cluster]
(
    name1 [type1] [DEFAULT|MATERIALIZED|ALIAS expr1] [TTL expr1],
    name2 [type2] [DEFAULT|MATERIALIZED|ALIAS expr2] [TTL expr2],
    ...
) ENGINE = ExternalDistributed('engine', 'host:port', 'database', 'table', 'user', 'password');

```

- Имена столбцов должны совпадать с именами в исходной таблице, но можно использовать только часть этих столбцов и в любом порядке.
- Типы столбцов могут отличаться от типов в исходной таблице. ClickHouse пытается [преобразовать](https://clickhouse.com/docs/ru/reference/functions/regular-functions/type-conversion-functions#CAST) значения в типы данных ClickHouse.
- `engine` — движок таблицы `MySQL` или `PostgreSQL`.
- `host:port` — адрес сервера MySQL или PostgreSQL.
- `database` — имя удалённой базы данных.
- `table` — имя удалённой таблицы.
- `user` — имя пользователя.
- `password` — пароль пользователя.

## Подробности реализации


```
CREATE TABLE test_shards (id UInt32, name String, age UInt32, money UInt32) ENGINE = ExternalDistributed('MySQL', `mysql{1|2}:3306,mysql{3|4}:3306`, 'clickhouse', 'test_replicas', 'root', 'clickhouse');

```

- [движок таблицы MySQL](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/mysql)
- [движок таблицы PostgreSQL](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/postgresql)
- [движок таблицы Distributed](https://clickhouse.com/docs/ru/reference/engines/table-engines/special/distributed)
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
