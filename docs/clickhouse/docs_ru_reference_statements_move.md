# Оператор MOVE для объекта управления доступом - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/statements/move


```
MOVE {USER, ROLE, QUOTA, SETTINGS PROFILE, ROW POLICY} name1 [, name2, ...] TO access_storage_type

```

- `local_directory`
- `memory`
- `replicated`
- `users_xml` (ro)
- `ldap` (ro)

```
MOVE USER test TO local_directory

```


```
MOVE ROLE test TO memory

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
