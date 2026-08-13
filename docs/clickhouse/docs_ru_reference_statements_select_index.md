# Запрос SELECT - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/statements/select/index


## Синтаксис


```
[WITH expr_list(subquery)]
SELECT [DISTINCT [ON (column1, column2, ...)]] expr_list
[FROM [db.]table | (subquery) | table_function] [FINAL]
[SAMPLE sample_coeff]
[ARRAY JOIN ...]
[GLOBAL] [ANY|ALL|ASOF] [INNER|LEFT|RIGHT|FULL|CROSS] [OUTER|SEMI|ANTI] JOIN (subquery)|table [(alias1 [, alias2 ...])] (ON <expr_list>)|(USING <column_list>)
[PREWHERE expr]
[WHERE expr]
[GROUP BY expr_list] [WITH ROLLUP|WITH CUBE] [WITH TOTALS]
[HAVING expr]
[WINDOW window_expr_list]
[QUALIFY expr]
[ORDER BY expr_list] [WITH FILL] [FROM expr] [TO expr] [STEP expr] [INTERPOLATE [(expr_list)]]
[LIMIT [offset_value, ]n BY columns]
[LIMIT [n, ]m] [WITH TIES]
[SETTINGS ...]
[UNION  ...]
[INTO OUTFILE filename [TRUNCATE] [COMPRESSION type [LEVEL level]] ]
[FORMAT format]

```

- [конструкция WITH](https://clickhouse.com/docs/ru/reference/statements/select/with)
- [секция SELECT](#select-clause)
- [секция ALL](https://clickhouse.com/docs/ru/reference/statements/select/all)
- [секция DISTINCT](https://clickhouse.com/docs/ru/reference/statements/select/distinct)
- [секция FROM](https://clickhouse.com/docs/ru/reference/statements/select/from)
- [предложение SAMPLE](https://clickhouse.com/docs/ru/reference/statements/select/sample)
- [секция ARRAY JOIN](https://clickhouse.com/docs/ru/reference/statements/select/array-join)
- [секция JOIN](https://clickhouse.com/docs/ru/reference/statements/select/join)
- [секция PREWHERE](https://clickhouse.com/docs/ru/reference/statements/select/prewhere)
- [предложение WHERE](https://clickhouse.com/docs/ru/reference/statements/select/where)
- [секция GROUP BY](https://clickhouse.com/docs/ru/reference/statements/select/group-by)
- [секция HAVING](https://clickhouse.com/docs/ru/reference/statements/select/having)
- [секция WINDOW](https://clickhouse.com/docs/ru/reference/functions/window-functions/index)
- [предложение QUALIFY](https://clickhouse.com/docs/ru/reference/statements/select/qualify)
- [предложение ORDER BY](https://clickhouse.com/docs/ru/reference/statements/select/order-by)
- [предложение LIMIT BY](https://clickhouse.com/docs/ru/reference/statements/select/limit-by)
- [секция LIMIT](https://clickhouse.com/docs/ru/reference/statements/select/limit)
- [секция OFFSET](https://clickhouse.com/docs/ru/reference/statements/select/offset)
- [секция UNION](https://clickhouse.com/docs/ru/reference/statements/select/union)
- [секция INTERSECT](https://clickhouse.com/docs/ru/reference/statements/select/intersect)
- [оператор EXCEPT](https://clickhouse.com/docs/ru/reference/statements/select/except)
- [Предложение INTO OUTFILE](https://clickhouse.com/docs/ru/reference/statements/select/into-outfile)
- [предложение FORMAT](https://clickhouse.com/docs/ru/reference/statements/select/format)

## Секция SELECT


### Динамический выбор столбцов


```
COLUMNS('regexp')

```


```
CREATE TABLE default.col_names (aa Int8, ab Int8, bc Int8) ENGINE = TinyLog

```


```
SELECT COLUMNS('a') FROM col_names

```


```
┌─aa─┬─ab─┐
│  1 │  1 │
└────┴────┘

```


```
SELECT COLUMNS('a'), COLUMNS('c'), toTypeName(COLUMNS('c')) FROM col_names

```


```
┌─aa─┬─ab─┬─bc─┬─toTypeName(bc)─┐
│  1 │  1 │  1 │ Int8           │
└────┴────┴────┴────────────────┘

```


```
SELECT COLUMNS('a') + COLUMNS('c') FROM col_names

```


```
Received exception from server (version 19.14.1):
Code: 42. DB::Exception: Received from localhost:9000. DB::Exception: Number of arguments for function plus does not match: passed 3, should be 2.

```


#### Выбор столбцов с `LIKE` или `ILIKE`


```
SELECT * ILIKE 'a%' FROM col_names

```


```
┌─aa─┬─ab─┐
│  1 │  1 │
└────┴────┘

```


```
SELECT * ILIKE 'a_' FROM col_names

```


```
SELECT t.* ILIKE 'a%' EXCEPT (ab) FROM col_names AS t

```


```
┌─aa─┐
│  1 │
└────┘

```


### Звёздочка

- При создании дампа таблицы.
- Для таблиц, содержащих всего несколько столбцов, например системных таблиц.
- Чтобы получить информацию о том, какие столбцы есть в таблице. В этом случае задайте `LIMIT 1`. Но лучше использовать запрос `DESC TABLE`.
- Когда по небольшому числу столбцов выполняется жёсткая фильтрация с помощью `PREWHERE`.
- В подзапросах (поскольку столбцы, не нужные для внешнего запроса, из подзапросов исключаются).

### Экстремальные значения


### Примечания


## Подробности реализации

- `max_memory_usage`
- `max_rows_to_group_by`
- `max_rows_to_sort`
- `max_rows_in_distinct`
- `max_bytes_in_distinct`
- `max_rows_in_set`
- `max_bytes_in_set`
- `max_rows_in_join`
- `max_bytes_in_join`
- `max_bytes_before_external_sort`
- `max_bytes_ratio_before_external_sort`
- `max_bytes_before_external_group_by`
- `max_bytes_ratio_before_external_group_by`

## Модификаторы SELECT


| Modifier | Description |
| --- | --- |
| [`APPLY`](https://clickhouse.com/docs/ru/reference/statements/select/apply_modifier) | Позволяет применить некоторую функцию к каждой строке, возвращаемой внешним табличным выражением запроса. |
| [`EXCEPT`](https://clickhouse.com/docs/ru/reference/statements/select/except_modifier) | Указывает имена одного или нескольких столбцов, которые нужно исключить из результата. Все совпадающие имена столбцов исключаются из вывода. |
| [`REPLACE`](https://clickhouse.com/docs/ru/reference/statements/select/replace_modifier) | Указывает один или несколько [псевдонимов выражений](https://clickhouse.com/docs/ru/reference/syntax#expression-aliases). Каждый псевдоним должен совпадать с именем столбца из оператора `SELECT *`. В итоговом списке столбцов столбец, совпадающий с псевдонимом, заменяется выражением из этого `REPLACE`. Этот модификатор не изменяет имена или порядок столбцов. Однако он может изменить значение и тип значения. |


### Комбинации модификаторов


```
SELECT COLUMNS('[jk]') APPLY(toString) APPLY(length) APPLY(max) FROM columns_transformers;

```


```
┌─max(length(toString(j)))─┬─max(length(toString(k)))─┐
│                        2 │                        3 │
└──────────────────────────┴──────────────────────────┘

```


```
SELECT * REPLACE(i + 1 AS i) EXCEPT (j) APPLY(sum) from columns_transformers;

```


```
┌─sum(plus(i, 1))─┬─sum(k)─┐
│             222 │    347 │
└─────────────────┴────────┘

```


## SETTINGS в SELECT-запросе


```
SELECT * FROM some_table SETTINGS optimize_read_in_order=1, cast_keep_nullable=1;

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
