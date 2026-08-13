# Оператор CHECK TABLE - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/statements/check-table


## Синтаксис


```
CHECK TABLE table_name [PARTITION partition_expression | PART part_name] [FORMAT format] [SETTINGS check_query_single_value_result = (0|1) [, other_settings]]

```

- `table_name`: Указывает имя таблицы, которую нужно проверить.
- `partition_expression`: (Необязательно) Если нужно проверить конкретную партицию таблицы, это выражение можно использовать для указания партиции.
- `part_name`: (Необязательно) Если нужно проверить конкретную часть таблицы, можно добавить строковый литерал с именем части.
- `FORMAT format`: (Необязательно) Позволяет указать формат вывода результата.
- `SETTINGS`: (Необязательно) Позволяет задать дополнительные настройки.
- (Необязательно): [check_query_single_value_result](https://clickhouse.com/docs/ru/reference/settings/session-settings#check_query_single_value_result): Эта настройка определяет, будет ли вывод подробным (`0`) или сводным (`1`).
- Можно также применять и другие настройки. Если детерминированный порядок результатов не требуется, для ускорения запроса можно установить max_threads в значение больше единицы.
- `part_path`: Указывает путь к части данных или имя файла.
- `is_passed`: Возвращает 1, если проверка этой части прошла успешно, иначе 0.
- `message`: Любые дополнительные сообщения, связанные с проверкой, например сообщения об ошибках или об успешной проверке.
- [Log](https://clickhouse.com/docs/ru/reference/engines/table-engines/log-family/log)
- [TinyLog](https://clickhouse.com/docs/ru/reference/engines/table-engines/log-family/tinylog)
- [StripeLog](https://clickhouse.com/docs/ru/reference/engines/table-engines/log-family/stripelog)
- [семейство MergeTree](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/mergetree)

## Примеры


```
CHECK TABLE test_table;

```


```
┌─result─┐
│      1 │
└────────┘

```


```
CHECK TABLE t0 PARTITION ID '201003'
FORMAT PrettyCompactMonoBlock
SETTINGS check_query_single_value_result = 0

```


```
┌─part_path────┬─is_passed─┬─message─┐
│ 201003_7_7_0 │         1 │         │
│ 201003_3_3_0 │         1 │         │
└──────────────┴───────────┴─────────┘

```


```
CHECK TABLE t0 PART '201003_7_7_0'
FORMAT PrettyCompactMonoBlock
SETTINGS check_query_single_value_result = 0

```


```
┌─part_path────┬─is_passed─┬─message─┐
│ 201003_7_7_0 │         1 │         │
└──────────────┴───────────┴─────────┘

```


```
CHECK TABLE t0 PART '201003_111_222_0'

```


```
DB::Exception: No such data part '201003_111_222_0' to check in table 'default.t0'. (NO_SUCH_DATA_PART)

```


### Получение результата «Corrupted»


```
rm /var/lib/clickhouse-server/data/default/t0/201003_3_3_0/checksums.txt

```


```
CHECK TABLE t0 PARTITION ID '201003'
FORMAT PrettyCompactMonoBlock
SETTINGS check_query_single_value_result = 0

```


```
┌─part_path────┬─is_passed─┬─message──────────────────────────────────┐
│ 201003_7_7_0 │         1 │                                          │
│ 201003_3_3_0 │         1 │ Checksums recounted and written to disk. │
└──────────────┴───────────┴──────────────────────────────────────────┘

```


```
CHECK ALL TABLES
FORMAT PrettyCompactMonoBlock
SETTINGS check_query_single_value_result = 0

```


```
┌─database─┬─table────┬─part_path───┬─is_passed─┬─message─┐
│ default  │ t2       │ all_1_95_3  │         1 │         │
│ db1      │ table_01 │ all_39_39_0 │         1 │         │
│ default  │ t1       │ all_39_39_0 │         1 │         │
│ db1      │ t1       │ all_39_39_0 │         1 │         │
│ db1      │ table_01 │ all_1_6_1   │         1 │         │
│ default  │ t1       │ all_1_6_1   │         1 │         │
│ db1      │ t1       │ all_1_6_1   │         1 │         │
│ db1      │ table_01 │ all_7_38_2  │         1 │         │
│ db1      │ t1       │ all_7_38_2  │         1 │         │
│ default  │ t1       │ all_7_38_2  │         1 │         │
└──────────┴──────────┴─────────────┴───────────┴─────────┘

```


## Если данные повреждены

- Создайте новую таблицу с той же структурой, что и поврежденная. Для этого выполните запрос `CREATE TABLE <new_table_name> AS <damaged_table_name>`.
- Установите значение `max_threads` равным 1, чтобы следующий запрос выполнялся в одном потоке. Для этого выполните запрос `SET max_threads = 1`.
- Выполните запрос `INSERT INTO <new_table_name> SELECT * FROM <damaged_table_name>`. Он скопирует неповрежденные данные из поврежденной таблицы в другую. Будут скопированы только данные, расположенные до поврежденной части.
- Перезапустите `clickhouse-client`, чтобы сбросить значение `max_threads`.
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
