# Операторы IN - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/statements/in


```
SELECT UserID IN (123, 456) FROM ...
SELECT (CounterID, UserID) IN ((34, 123), (101500, 456)) FROM ...

```


```
SELECT
    1 IN (tuple(1, 2)) AS one_in_tuple,
    2 IN (tuple(1, 2)) AS two_in_tuple,
    3 IN (tuple(1, 2)) AS three_in_tuple;

```


```
┌─one_in_tuple─┬─two_in_tuple─┬─three_in_tuple─┐
│            1 │            1 │              0 │
└──────────────┴──────────────┴────────────────┘

```


```
SELECT tuple(1, 2) IN (tuple(1, 2)) AS tuple_in_tuple;

```


```
┌─tuple_in_tuple─┐
│              1 │
└────────────────┘

```


```
SELECT 1 IN (tuple(1, 2), tuple(3, 4));

```


```
Code: 43. DB::Exception: Unsupported types for IN. First argument type UInt8. Second argument type Tuple(Tuple(UInt8, UInt8), Tuple(UInt8, UInt8)). (ILLEGAL_TYPE_OF_ARGUMENT)

```


```
SELECT '1' IN (SELECT 1);

```


```
┌─in('1', _subquery49)─┐
│                    1 │
└──────────────────────┘

```


```
SELECT (CounterID, UserID) IN (SELECT CounterID, UserID FROM ...) FROM ...

```


```
SELECT
    EventDate,
    avg(UserID IN
    (
        SELECT UserID
        FROM test.hits
        WHERE EventDate = toDate('2014-03-17')
    )) AS ratio
FROM test.hits
GROUP BY EventDate
ORDER BY EventDate ASC

```


```
┌──EventDate─┬────ratio─┐
│ 2014-03-17 │        1 │
│ 2014-03-18 │ 0.807696 │
│ 2014-03-19 │ 0.755406 │
│ 2014-03-20 │ 0.723218 │
│ 2014-03-21 │ 0.697021 │
│ 2014-03-22 │ 0.647851 │
│ 2014-03-23 │ 0.648416 │
└────────────┴──────────┘

```


## Обработка NULL


```
┌─x─┬────y─┐
│ 1 │ ᴺᵁᴸᴸ │
│ 2 │    3 │
└───┴──────┘

```


```
┌─x─┐
│ 2 │
└───┘

```


```
SELECT y IN (NULL, 3)
FROM t_null

```


```
┌─in(y, tuple(NULL, 3))─┐
│                     0 │
│                     1 │
└───────────────────────┘

```


## Распределённые подзапросы


```
SELECT uniq(UserID) FROM distributed_table

```


```
SELECT uniq(UserID) FROM local_table

```


```
SELECT uniq(UserID) FROM distributed_table WHERE CounterID = 101500 AND UserID IN (SELECT UserID FROM local_table WHERE CounterID = 34)

```

- Вычисление пересечения аудиторий двух сайтов.

```
SELECT uniq(UserID) FROM local_table WHERE CounterID = 101500 AND UserID IN (SELECT UserID FROM local_table WHERE CounterID = 34)

```


```
SELECT uniq(UserID) FROM distributed_table WHERE CounterID = 101500 AND UserID IN (SELECT UserID FROM distributed_table WHERE CounterID = 34)

```


```
SELECT uniq(UserID) FROM local_table WHERE CounterID = 101500 AND UserID IN (SELECT UserID FROM distributed_table WHERE CounterID = 34)

```


```
SELECT UserID FROM local_table WHERE CounterID = 34

```


```
SELECT uniq(UserID) FROM distributed_table WHERE CounterID = 101500 AND UserID GLOBAL IN (SELECT UserID FROM distributed_table WHERE CounterID = 34)

```


```
SELECT UserID FROM distributed_table WHERE CounterID = 34

```


```
SELECT uniq(UserID) FROM local_table WHERE CounterID = 101500 AND UserID GLOBAL IN _data1

```

- При создании временной таблицы данные не становятся уникальными. Чтобы уменьшить объем данных, передаваемых по сети, укажите DISTINCT в подзапросе. (Для обычного `IN` этого делать не нужно.)
- Временная таблица будет отправлена на все удаленные серверы. При передаче не учитывается топология сети. Например, если 10 удаленных серверов находятся в датацентре, значительно удаленном от сервера, инициировавшего запрос, данные будут 10 раз переданы по каналу в этот удаленный датацентр. Старайтесь избегать больших наборов данных при использовании `GLOBAL IN`.
- При передаче данных на удаленные серверы ограничения пропускной способности сети не настраиваются. Это может привести к перегрузке сети.
- Старайтесь распределять данные по серверам так, чтобы не приходилось регулярно использовать `GLOBAL IN`.
- Если вам часто требуется использовать `GLOBAL IN`, спланируйте размещение кластера ClickHouse так, чтобы одна группа реплик находилась не более чем в одном датацентре, а между ними была быстрая сеть, — тогда запрос можно будет полностью обработать в пределах одного датацентра.

### Распределённые подзапросы и max_rows_in_set


```
SELECT * FROM table1 WHERE col1 GLOBAL IN (SELECT col1 FROM table2 WHERE <some_predicate>)

```


### Распределённые подзапросы и max_parallel_replicas


```
SELECT CounterID, count() FROM distributed_table_1 WHERE UserID IN (SELECT UserID FROM local_table_2 WHERE CounterID < 100)
SETTINGS max_parallel_replicas=3

```


```
SELECT CounterID, count() FROM local_table_1 WHERE UserID IN (SELECT UserID FROM local_table_2 WHERE CounterID < 100)
SETTINGS parallel_replicas_count=3, parallel_replicas_offset=M

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
