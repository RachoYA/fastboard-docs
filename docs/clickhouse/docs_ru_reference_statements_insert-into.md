# Оператор INSERT INTO - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/statements/insert-into


```
INSERT INTO [TABLE] [db.]table [(c1, c2, c3)] [SETTINGS ...] VALUES (v11, v12, v13), (v21, v22, v23), ...

```


```
SHOW CREATE insert_select_testtable;

```


```
CREATE TABLE insert_select_testtable
(
    `a` Int8,
    `b` String,
    `c` Int8
)
ENGINE = MergeTree()
ORDER BY a

```


```
INSERT INTO insert_select_testtable (*) VALUES (1, 'a', 1) ;

```


```
INSERT INTO insert_select_testtable (* EXCEPT(b)) Values (2, 2);

```


```
SELECT * FROM insert_select_testtable;

```


```
┌─a─┬─b─┬─c─┐
│ 2 │   │ 2 │
└───┴───┴───┘
┌─a─┬─b─┬─c─┐
│ 1 │ a │ 1 │
└───┴───┴───┘

```


```
INSERT INTO insert_select_testtable VALUES (1, DEFAULT, 1) ;

```

- Значениями, вычисленными из выражений `DEFAULT`, указанных в определении таблицы.
- Нулями и пустыми строками, если выражения `DEFAULT` не заданы.

```
INSERT INTO [db.]table [(c1, c2, c3)] FORMAT format_name data_set

```


```
INSERT INTO [db.]table [(c1, c2, c3)] FORMAT Values (v11, v12, v13), (v21, v22, v23), ...

```


```
INSERT INTO t FORMAT TabSeparated
11  Hello, world!
22  Qwerty

```


```
INSERT INTO table SETTINGS ... FORMAT format_name data_set

```


## Ограничения


## Проверка типов данных


```
SET enable_time_time64_type = 1;

CREATE TABLE events
(
    `id` UInt64,
    `event_time` Time
)
ENGINE = MergeTree()
ORDER BY id;

SET enable_time_time64_type = 0;

-- Это работает, даже если настройка теперь отключена.
-- Таблица уже существует, поэтому вставки не блокируются.
INSERT INTO events VALUES (1, '14:30:25');

-- Но создание новой таблицы с типом Time завершится ошибкой.
CREATE TABLE events_new
(
    `id` UInt64,
    `event_time` Time
)
ENGINE = MergeTree()
ORDER BY id; -- ERR: TYPE_TIME_TIME64_IS_NOT_ENABLED

```


## Вставка результатов запроса SELECT


```
INSERT INTO [TABLE] [db.]table [(c1, c2, c3)] SELECT ...

```


```
INSERT INTO x WITH y AS (SELECT * FROM numbers(10)) SELECT * FROM y;
WITH y AS (SELECT * FROM numbers(10)) INSERT INTO x SELECT * FROM y;

```


## Вставка данных из файла


```
INSERT INTO [TABLE] [db.]table [(c1, c2, c3)] FROM INFILE file_name [COMPRESSION type] [SETTINGS ...] [FORMAT format_name]

```


### Один файл с использованием FROM INFILE


```
echo 1,A > input.csv ; echo 2,B >> input.csv
clickhouse-client --query="CREATE TABLE table_from_file (id UInt32, text String) ENGINE=MergeTree() ORDER BY id;"
clickhouse-client --query="INSERT INTO table_from_file FROM INFILE 'input.csv' FORMAT CSV;"
clickhouse-client --query="SELECT * FROM table_from_file FORMAT PrettyCompact;"

```


```
┌─id─┬─text─┐
│  1 │ A    │
│  2 │ B    │
└────┴──────┘

```


### Несколько файлов в FROM INFILE с использованием глоб-шаблонов


```
echo 1,A > input_1.csv ; echo 2,B > input_2.csv
clickhouse-client --query="CREATE TABLE infile_globs (id UInt32, text String) ENGINE=MergeTree() ORDER BY id;"
clickhouse-client --query="INSERT INTO infile_globs FROM INFILE 'input_*.csv' FORMAT CSV;"
clickhouse-client --query="SELECT * FROM infile_globs FORMAT PrettyCompact;"

```


```
INSERT INTO infile_globs FROM INFILE 'input_*.csv' FORMAT CSV;
INSERT INTO infile_globs FROM INFILE 'input_{1,2}.csv' FORMAT CSV;
INSERT INTO infile_globs FROM INFILE 'input_?.csv' FORMAT CSV;

```


## Вставка с помощью табличной функции


```
INSERT INTO [TABLE] FUNCTION table_func ...

```


```
CREATE TABLE simple_table (id UInt32, text String) ENGINE=MergeTree() ORDER BY id;
INSERT INTO TABLE FUNCTION remote('localhost', default.simple_table)
    VALUES (100, 'inserted via remote()');
SELECT * FROM simple_table;

```


```
┌──id─┬─text──────────────────┐
│ 100 │ inserted via remote() │
└─────┴───────────────────────┘

```


## Вставка в ClickHouse Cloud


```
SELECT .... SETTINGS select_sequential_consistency = 1;

```


## Вставка в реплицируемой конфигурации


## Рекомендации по производительности

- Добавляйте данные достаточно крупными батчами, например по 100 000 строк за раз.
- Группируйте данные по ключу партиционирования перед загрузкой в ClickHouse.
- Данные добавляются в реальном времени.
- Вы загружаете данные, которые обычно уже отсортированы по времени.

### Асинхронные вставки


### Крупные или длительные вставки

- [async_insert](https://clickhouse.com/docs/ru/reference/settings/session-settings#async_insert)
- [wait_for_async_insert](https://clickhouse.com/docs/ru/reference/settings/session-settings#wait_for_async_insert)
- [wait_for_async_insert_timeout](https://clickhouse.com/docs/ru/reference/settings/session-settings#wait_for_async_insert_timeout)
- [async_insert_max_data_size](https://clickhouse.com/docs/ru/reference/settings/session-settings#async_insert_max_data_size)
- [async_insert_busy_timeout_ms](https://clickhouse.com/docs/ru/reference/settings/session-settings#async_insert_busy_timeout_max_ms)
- [async_insert_stale_timeout_ms](https://clickhouse.com/docs/ru/reference/settings/session-settings#async_insert_max_data_size)
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
