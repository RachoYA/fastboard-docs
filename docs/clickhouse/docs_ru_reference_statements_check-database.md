# Оператор CHECK DATABASE - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/statements/check-database


## Синтаксис


```
CHECK DATABASE database_name

```

- `database_name`: Указывает имя базы данных, которую нужно проверить.

## Поведение

- Подключается к внешнему каталогу (например, AWS Glue, Databricks Unity, Hive Metastore или Iceberg REST-каталогу) и получает список таблиц.
- Сообщает об успешном результате, если каталог доступен и аутентификация настроена корректно.
- Не требует, чтобы каталог содержал какие-либо таблицы: пустой, но доступный каталог всё равно считается исправным.

## Примеры


```
CHECK DATABASE datalake;

```


## См. также

- [`CHECK TABLE`](https://clickhouse.com/docs/ru/reference/statements/check-table)
- [`DataLakeCatalog`](https://clickhouse.com/docs/ru/reference/engines/database-engines/datalake)
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
