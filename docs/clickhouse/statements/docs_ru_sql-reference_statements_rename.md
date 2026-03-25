# Оператор RENAME | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/sql-reference/statements/rename

Переименовывает базы данных, таблицы или словари. В одном запросе можно переименовать несколько сущностей.
Обратите внимание, что запросRENAMEс несколькими сущностями является не атомарной операцией. Чтобы атомарно поменять местами имена сущностей, используйте операторEXCHANGE.

Синтаксис


```
RENAME [DATABASE|TABLE|DICTIONARY] name TO new_name [,...] [ON CLUSTER cluster]

```


## RENAME DATABASE​

Переименовывает базу данных.

Синтаксис


```
RENAME DATABASE atomic_database1 TO atomic_database2 [,...] [ON CLUSTER cluster]

```


## RENAME TABLE​

Переименовывает одну или несколько таблиц.

Переименование таблиц — легковесная операция. Если вы укажете другую базу данных послеTO, таблица будет перемещена в эту базу данных. Однако каталоги баз данных должны находиться в одной файловой системе. В противном случае будет возвращена ошибка.
Если вы переименовываете несколько таблиц в одном запросе, операция не является атомарной. Она может быть выполнена частично, и запросы из других сессий могут получить ошибкуTable ... does not exist ....

Синтаксис


```
RENAME TABLE [db1.]name1 TO [db2.]name2 [,...] [ON CLUSTER cluster]

```

Пример


```
RENAME TABLE table_A TO table_A_bak, table_B TO table_B_bak;

```

Также можно использовать более простой SQL‑запрос:


```
RENAME table_A TO table_A_bak, table_B TO table_B_bak;

```


## RENAME DICTIONARY​

Переименовывает один или несколько словарей. Этот запрос можно использовать для перемещения словарей между базами данных.

Синтаксис


```
RENAME DICTIONARY [db0.]dict_A TO [db1.]dict_B [,...] [ON CLUSTER cluster]

```

См. также

- Справочники