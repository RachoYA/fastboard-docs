# Оператор EXECUTE AS - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/statements/execute_as


## Синтаксис


```
EXECUTE AS target_user;
EXECUTE AS target_user subquery;

```


```
GRANT IMPERSONATE ON user1 TO user2;
GRANT IMPERSONATE ON * TO user3;

```


## Примеры


```
SELECT currentUser(), authenticatedUser(); -- выводит "default    default"
CREATE USER james;
EXECUTE AS james SELECT currentUser(), authenticatedUser(); -- выводит "james    default"

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
