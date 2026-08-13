# Оператор REVOKE - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/statements/revoke


## Синтаксис


```
REVOKE [ON CLUSTER cluster_name] privilege[(column_name [,...])] [,...] ON {db.table|db.*|*.*|table|*} FROM {user | CURRENT_USER} [,...] | ALL | ALL EXCEPT {user | CURRENT_USER} [,...]

```


```
REVOKE [ON CLUSTER cluster_name] [ADMIN OPTION FOR] role [,...] FROM {user | role | CURRENT_USER} [,...] | ALL | ALL EXCEPT {user_name | role_name | CURRENT_USER} [,...]

```


## Описание


### Частичный отзыв привилегий


## Примеры


```
GRANT SELECT ON *.* TO john;
REVOKE SELECT ON accounts.* FROM john;

```


```
GRANT SELECT ON accounts.staff TO mira;
REVOKE SELECT(wage) ON accounts.staff FROM mira;

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
