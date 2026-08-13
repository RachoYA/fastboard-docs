# Оператор SET ROLE - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/statements/set-role


```
SET ROLE {DEFAULT | NONE | role [,...] | ALL | ALL EXCEPT role [,...]}

```


## SET DEFAULT ROLE


```
SET DEFAULT ROLE {NONE | role [,...] | ALL | ALL EXCEPT role [,...]} TO {user|CURRENT_USER} [,...]

```


## Примеры


```
SET DEFAULT ROLE role1, role2, ... TO user

```


```
SET DEFAULT ROLE ALL TO user

```


```
SET DEFAULT ROLE NONE TO user

```


```
SET DEFAULT ROLE ALL EXCEPT role1, role2 TO user

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
