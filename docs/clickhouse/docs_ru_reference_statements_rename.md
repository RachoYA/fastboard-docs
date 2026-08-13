# Оператор RENAME - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/statements/rename


```
RENAME [DATABASE|TABLE|DICTIONARY] name TO new_name [,...] [ON CLUSTER cluster]

```


## RENAME DATABASE


```
RENAME DATABASE atomic_database1 TO atomic_database2 [,...] [ON CLUSTER cluster]

```


## RENAME TABLE


```
RENAME TABLE [db1.]name1 TO [db2.]name2 [,...] [ON CLUSTER cluster]

```


```
RENAME TABLE table_A TO table_A_bak, table_B TO table_B_bak;

```


```
RENAME table_A TO table_A_bak, table_B TO table_B_bak;

```


## RENAME DICTIONARY


```
RENAME DICTIONARY [db0.]dict_A TO [db1.]dict_B [,...] [ON CLUSTER cluster]

```

- [Словари](https://clickhouse.com/docs/ru/reference/statements/create/dictionary)
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
