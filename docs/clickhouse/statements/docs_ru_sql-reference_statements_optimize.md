# Команда OPTIMIZE | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/sql-reference/statements/optimize

Этот запрос пытается инициировать внеплановое слияние частей данных таблиц. Обратите внимание, что в целом мы не рекомендуем использоватьOPTIMIZE TABLE ... FINAL(см.документацию), поскольку эта команда предназначена для административных задач, а не для повседневных операций.

OPTIMIZEне может исправить ошибкуToo many parts.

Синтаксис


```
OPTIMIZE TABLE [db.]name [ON CLUSTER cluster] [PARTITION partition | PARTITION ID 'partition_id'] [FINAL | FORCE] [DEDUPLICATE [BY expression]]

```


```
OPTIMIZE TABLE [db.]name DRY RUN PARTS 'part_name1', 'part_name2' [, ...] [DEDUPLICATE [BY expression]] [CLEANUP]

```

ЗапросOPTIMIZEподдерживается для семействаMergeTree(включаяmaterialized views) и движкаBuffer. Другие табличные движкиOPTIMIZEне поддерживают.

КогдаOPTIMIZEиспользуется с семейством табличных движковReplicatedMergeTree, ClickHouse создает задачу на выполнение слияния и ожидает её завершения на всех репликах (если настройкаalter_syncустановлена в значение2) или на текущей реплике (если настройкаalter_syncустановлена в значение1).

- ЕслиOPTIMIZEпо какой-либо причине не выполняет слияние, клиент не получает об этом уведомления. Чтобы включить уведомления, используйте настройкуoptimize_throw_if_noop.
- Если вы указываетеPARTITION, оптимизируется только указанная партиция.Как задать выражение партиции.
- Если вы указываетеFINALилиFORCE, оптимизация выполняется даже тогда, когда все данные уже находятся в одной части. Вы можете управлять этим поведением с помощьюoptimize_skip_merged_partitions. Кроме того, слияние принудительно выполняется даже при наличии параллельных слияний.
- Если вы указываетеDEDUPLICATE, то полностью идентичные строки (если не указано предложение BY) будут удалены как дубликаты (сравниваются все столбцы). Это имеет смысл только для движка MergeTree.
Вы можете задать, как долго (в секундах) ждать выполнения запросовOPTIMIZEна неактивных репликах с помощью настройкиreplication_wait_for_inactive_replica_timeout.

Еслиalter_syncустановлен в значение2, и некоторые реплики неактивны дольше времени, заданного настройкойreplication_wait_for_inactive_replica_timeout, генерируется исключениеUNFINISHED.


## DRY RUN​

ПредложениеDRY RUNимитирует слияние указанных частей без фиксации результата. Слитая часть записывается во временное место на диске, проходит проверку и затем удаляется. Исходные части и данные таблицы остаются неизменными.

Это полезно для:

- Тестирования корректности слияния между разными версиями ClickHouse.
- Детерминированного воспроизведения ошибок, связанных со слияниями.
- Измерения производительности слияния.
DRY RUNподдерживается только для таблиц семействаMergeTree. Требуется ключевое словоPARTSсо списком имён частей. Все указанные части должны существовать, быть активными и принадлежать одной и той же партиции.

DRY RUNнесовместим сFINALиPARTITION. Его можно комбинировать сDEDUPLICATE(с необязательным указанием столбцов) иCLEANUP(для таблицReplacingMergeTree).

Синтаксис


```
OPTIMIZE TABLE [db.]name DRY RUN PARTS 'part_name1', 'part_name2' [, ...] [DEDUPLICATE [BY expression]] [CLEANUP]

```

По умолчанию результирующая часть после слияния проверяется аналогично запросуCHECK TABLE. Это поведение контролируется настройкойoptimize_dry_run_check_part(включена по умолчанию). При её отключении валидация не выполняется, что может быть полезно для бенчмаркинга самой операции слияния.

Пример


```
CREATE TABLE dry_run_example (key UInt64, value String) ENGINE = MergeTree ORDER BY key;

INSERT INTO dry_run_example VALUES (1, 'a'), (2, 'b');
INSERT INTO dry_run_example VALUES (1, 'c'), (4, 'd');

-- Simulate merging using two parts
OPTIMIZE TABLE dry_run_example DRY RUN PARTS 'all_1_1_0', 'all_2_2_0';

-- Simulate merging with deduplication
OPTIMIZE TABLE dry_run_example DRY RUN PARTS 'all_1_1_0', 'all_2_2_0' DEDUPLICATE;

-- Parts and data remain unchanged after DRY RUN
SELECT name, rows FROM system.parts
WHERE database = currentDatabase() AND table = 'dry_run_example' AND active
ORDER BY name;

```


```
┌─name────────┬─rows─┐
│ all_1_1_0   │    2 │
│ all_2_2_0   │    2 │
└─────────────┴──────┘

```


## Выражение BY​

Если вы хотите выполнять дедупликацию по произвольному набору столбцов, а не по всем, вы можете явно указать список столбцов или использовать любую комбинацию выражений*,COLUMNSилиEXCEPT. Явно заданный или неявно развёрнутый список столбцов должен включать все столбцы, указанные в выражении упорядочивания строк (как первичного, так и сортировочного ключей), а также в выражении партиционирования (ключ партиционирования).

Обратите внимание, что*ведёт себя так же, как вSELECT: столбцыMATERIALIZEDиALIASне используются при разворачивании списка.Также является ошибкой указывать пустой список столбцов, писать выражение, приводящее к пустому списку столбцов, или выполнять дедупликацию по столбцуALIAS.

Также является ошибкой указывать пустой список столбцов, писать выражение, приводящее к пустому списку столбцов, или выполнять дедупликацию по столбцуALIAS.

Синтаксис


```
OPTIMIZE TABLE table DEDUPLICATE; -- all columns
OPTIMIZE TABLE table DEDUPLICATE BY *; -- excludes MATERIALIZED and ALIAS columns
OPTIMIZE TABLE table DEDUPLICATE BY colX,colY,colZ;
OPTIMIZE TABLE table DEDUPLICATE BY * EXCEPT colX;
OPTIMIZE TABLE table DEDUPLICATE BY * EXCEPT (colX, colY);
OPTIMIZE TABLE table DEDUPLICATE BY COLUMNS('column-matched-by-regex');
OPTIMIZE TABLE table DEDUPLICATE BY COLUMNS('column-matched-by-regex') EXCEPT colX;
OPTIMIZE TABLE table DEDUPLICATE BY COLUMNS('column-matched-by-regex') EXCEPT (colX, colY);

```

Примеры

Рассмотрим следующую таблицу:


```
CREATE TABLE example (
    primary_key Int32,
    secondary_key Int32,
    value UInt32,
    partition_key UInt32,
    materialized_value UInt32 MATERIALIZED 12345,
    aliased_value UInt32 ALIAS 2,
    PRIMARY KEY primary_key
) ENGINE=MergeTree
PARTITION BY partition_key
ORDER BY (primary_key, secondary_key);

```


```
INSERT INTO example (primary_key, secondary_key, value, partition_key)
VALUES (0, 0, 0, 0), (0, 0, 0, 0), (1, 1, 2, 2), (1, 1, 2, 3), (1, 1, 3, 3);

```


```
SELECT * FROM example;

```

Результат:


```

┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           0 │             0 │     0 │             0 │
│           0 │             0 │     0 │             0 │
└─────────────┴───────────────┴───────┴───────────────┘
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           1 │             1 │     2 │             2 │
└─────────────┴───────────────┴───────┴───────────────┘
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           1 │             1 │     2 │             3 │
│           1 │             1 │     3 │             3 │
└─────────────┴───────────────┴───────┴───────────────┘

```

Все последующие примеры выполняются для этого состояния с 5 строками.


#### DEDUPLICATE​

Когда столбцы для дедупликации не указаны, учитываются все столбцы. Строка удаляется только в том случае, если все значения во всех столбцах равны соответствующим значениям в предыдущей строке:


```
OPTIMIZE TABLE example FINAL DEDUPLICATE;

```


```
SELECT * FROM example;

```

Результат:


```
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           1 │             1 │     2 │             2 │
└─────────────┴───────────────┴───────┴───────────────┘
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           0 │             0 │     0 │             0 │
└─────────────┴───────────────┴───────┴───────────────┘
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           1 │             1 │     2 │             3 │
│           1 │             1 │     3 │             3 │
└─────────────┴───────────────┴───────┴───────────────┘

```


#### DEDUPLICATE BY *​

Когда столбцы задаются неявно, дедупликация таблицы выполняется по всем столбцам, которые не являютсяALIASилиMATERIALIZED. Для таблицы выше это столбцыprimary_key,secondary_key,valueиpartition_key:


```
OPTIMIZE TABLE example FINAL DEDUPLICATE BY *;

```


```
SELECT * FROM example;

```

Результат:


```
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           1 │             1 │     2 │             2 │
└─────────────┴───────────────┴───────┴───────────────┘
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           0 │             0 │     0 │             0 │
└─────────────┴───────────────┴───────┴───────────────┘
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           1 │             1 │     2 │             3 │
│           1 │             1 │     3 │             3 │
└─────────────┴───────────────┴───────┴───────────────┘

```


#### DEDUPLICATE BY * EXCEPT​

Выполняет дедупликацию по всем столбцам, которые не являютсяALIASилиMATERIALIZED, при этом явно исключается столбецvalue, то есть используется набор столбцовprimary_key,secondary_keyиpartition_key.


```
OPTIMIZE TABLE example FINAL DEDUPLICATE BY * EXCEPT value;

```


```
SELECT * FROM example;

```

Результат:


```
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           1 │             1 │     2 │             2 │
└─────────────┴───────────────┴───────┴───────────────┘
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           0 │             0 │     0 │             0 │
└─────────────┴───────────────┴───────┴───────────────┘
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           1 │             1 │     2 │             3 │
└─────────────┴───────────────┴───────┴───────────────┘

```


#### DEDUPLICATE BY <list of columns>​

Выполните явную дедупликацию по столбцамprimary_key,secondary_keyиpartition_key:


```
OPTIMIZE TABLE example FINAL DEDUPLICATE BY primary_key, secondary_key, partition_key;

```


```
SELECT * FROM example;

```

Результат:


```
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           1 │             1 │     2 │             2 │
└─────────────┴───────────────┴───────┴───────────────┘
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           0 │             0 │     0 │             0 │
└─────────────┴───────────────┴───────┴───────────────┘
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           1 │             1 │     2 │             3 │
└─────────────┴───────────────┴───────┴───────────────┘

```


#### DEDUPLICATE BY COLUMNS(<regex>)​

Удаляет дубликаты по всем столбцам, соответствующим регулярному выражению: столбцамprimary_key,secondary_keyиpartition_key:


```
OPTIMIZE TABLE example FINAL DEDUPLICATE BY COLUMNS('.*_key');

```


```
SELECT * FROM example;

```

Результат:


```
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           0 │             0 │     0 │             0 │
└─────────────┴───────────────┴───────┴───────────────┘
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           1 │             1 │     2 │             2 │
└─────────────┴───────────────┴───────┴───────────────┘
┌─primary_key─┬─secondary_key─┬─value─┬─partition_key─┐
│           1 │             1 │     2 │             3 │
└─────────────┴───────────────┴───────┴───────────────┘

```
