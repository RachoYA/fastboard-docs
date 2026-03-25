# Оператор EXISTS | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/sql-reference/statements/exists


```
EXISTS [TEMPORARY] [TABLE|DICTIONARY|DATABASE] [db.]name [INTO OUTFILE filename] [FORMAT format]

```

Возвращает один столбец типаUInt8со значением0, если таблица или база данных не существует, или1, если таблица существует в указанной базе данных.
