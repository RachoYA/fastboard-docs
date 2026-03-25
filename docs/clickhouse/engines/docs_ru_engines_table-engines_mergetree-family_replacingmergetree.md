# Движок таблицы ReplacingMergeTree | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/engines/table-engines/mergetree-family/replacingmergetree

Этот движок отличается отMergeTreeтем, что удаляет дублирующиеся записи с одинаковым значениемключа сортировки(разделORDER BYв определении таблицы, а неPRIMARY KEY).

Дедупликация данных происходит только во время слияния. Слияния выполняются в фоновом режиме в неизвестный момент времени, поэтому вы не можете планировать их выполнение. Часть данных может остаться необработанной. Хотя вы можете запустить внеплановое слияние с помощью запросаOPTIMIZE, не рассчитывайте на это, потому что запросOPTIMIZEбудет считывать и записывать большой объем данных.

Таким образом,ReplacingMergeTreeподходит для фоновой очистки дублирующихся данных с целью экономии места, но не гарантирует отсутствие дубликатов.

Подробное руководство по ReplacingMergeTree, включая лучшие практики и способы оптимизации производительности, доступноздесь.


## Создание таблицы​


```
CREATE TABLE [IF NOT EXISTS] [db.]table_name [ON CLUSTER cluster]
(
    name1 [type1] [DEFAULT|MATERIALIZED|ALIAS expr1],
    name2 [type2] [DEFAULT|MATERIALIZED|ALIAS expr2],
    ...
) ENGINE = ReplacingMergeTree([ver [, is_deleted]])
[PARTITION BY expr]
[ORDER BY expr]
[PRIMARY KEY expr]
[SAMPLE BY expr]
[SETTINGS name=value, ...]

```

Описание параметров запроса см. вописании оператора.

Уникальность строк определяется разделом таблицыORDER BY, а неPRIMARY KEY.


## Параметры ReplacingMergeTree​


### ver​

ver— столбец с номером версии. ТипUInt*,Date,DateTimeилиDateTime64. Необязательный параметр.

При слиянииReplacingMergeTreeиз всех строк с одинаковым сортировочным ключом оставляет только одну:

- Последнюю в выборке, еслиverне указан. Выборка — это набор строк в наборе кусков, участвующих в слиянии. Самый недавно созданный кусок (последняя вставка) будет последним в выборке. Таким образом, после дедупликации для каждого уникального сортировочного ключа останется самая последняя строка из самой свежей вставки.
- С максимальной версией, еслиverуказан. Еслиverодинаков для нескольких строк, для них используется правило «еслиverне указан», то есть останется самая недавно вставленная строка.
Пример:


```
-- without ver - the last inserted 'wins'
CREATE TABLE myFirstReplacingMT
(
    `key` Int64,
    `someCol` String,
    `eventTime` DateTime
)
ENGINE = ReplacingMergeTree
ORDER BY key;

INSERT INTO myFirstReplacingMT Values (1, 'first', '2020-01-01 01:01:01');
INSERT INTO myFirstReplacingMT Values (1, 'second', '2020-01-01 00:00:00');

SELECT * FROM myFirstReplacingMT FINAL;

┌─key─┬─someCol─┬───────────eventTime─┐
│   1 │ second  │ 2020-01-01 00:00:00 │
└─────┴─────────┴─────────────────────┘


-- with ver - the row with the biggest ver 'wins'
CREATE TABLE mySecondReplacingMT
(
    `key` Int64,
    `someCol` String,
    `eventTime` DateTime
)
ENGINE = ReplacingMergeTree(eventTime)
ORDER BY key;

INSERT INTO mySecondReplacingMT Values (1, 'first', '2020-01-01 01:01:01');
INSERT INTO mySecondReplacingMT Values (1, 'second', '2020-01-01 00:00:00');

SELECT * FROM mySecondReplacingMT FINAL;

┌─key─┬─someCol─┬───────────eventTime─┐
│   1 │ first   │ 2020-01-01 01:01:01 │
└─────┴─────────┴─────────────────────┘

```


### is_deleted​

is_deleted— имя столбца, используемого во время слияния для определения, представляет ли строка состояние или подлежит удалению;1— строка-удаление,0— строка-состояние.

Тип данных столбца —UInt8.

is_deletedможет быть включён только при использованииver.Независимо от выполняемой над данными операции, версия должна увеличиваться. Если две вставленные строки имеют одинаковый номер версии, сохраняется последняя вставленная строка.По умолчанию ClickHouse сохраняет последнюю строку для ключа, даже если эта строка является строкой удаления. Это нужно для того, чтобы любые будущие строки с более низкими версиями могли быть безопасно вставлены, и строка удаления всё равно применялась.Чтобы навсегда удалить такие строки удаления, включите настройку таблицыallow_experimental_replacing_merge_with_cleanupи выполните одно из следующих действий:Задайте настройки таблицыenable_replacing_merge_with_cleanup_for_min_age_to_force_merge,min_age_to_force_merge_on_partition_onlyиmin_age_to_force_merge_seconds. Если все части в партиции старше, чемmin_age_to_force_merge_seconds, ClickHouse выполнит их слияние
в одну часть и удалит все строки удаления.Вручную выполнитеOPTIMIZE TABLE table [PARTITION partition | PARTITION ID 'partition_id'] FINAL CLEANUP.

Независимо от выполняемой над данными операции, версия должна увеличиваться. Если две вставленные строки имеют одинаковый номер версии, сохраняется последняя вставленная строка.По умолчанию ClickHouse сохраняет последнюю строку для ключа, даже если эта строка является строкой удаления. Это нужно для того, чтобы любые будущие строки с более низкими версиями могли быть безопасно вставлены, и строка удаления всё равно применялась.Чтобы навсегда удалить такие строки удаления, включите настройку таблицыallow_experimental_replacing_merge_with_cleanupи выполните одно из следующих действий:Задайте настройки таблицыenable_replacing_merge_with_cleanup_for_min_age_to_force_merge,min_age_to_force_merge_on_partition_onlyиmin_age_to_force_merge_seconds. Если все части в партиции старше, чемmin_age_to_force_merge_seconds, ClickHouse выполнит их слияние
в одну часть и удалит все строки удаления.Вручную выполнитеOPTIMIZE TABLE table [PARTITION partition | PARTITION ID 'partition_id'] FINAL CLEANUP.

По умолчанию ClickHouse сохраняет последнюю строку для ключа, даже если эта строка является строкой удаления. Это нужно для того, чтобы любые будущие строки с более низкими версиями могли быть безопасно вставлены, и строка удаления всё равно применялась.Чтобы навсегда удалить такие строки удаления, включите настройку таблицыallow_experimental_replacing_merge_with_cleanupи выполните одно из следующих действий:Задайте настройки таблицыenable_replacing_merge_with_cleanup_for_min_age_to_force_merge,min_age_to_force_merge_on_partition_onlyиmin_age_to_force_merge_seconds. Если все части в партиции старше, чемmin_age_to_force_merge_seconds, ClickHouse выполнит их слияние
в одну часть и удалит все строки удаления.Вручную выполнитеOPTIMIZE TABLE table [PARTITION partition | PARTITION ID 'partition_id'] FINAL CLEANUP.

Чтобы навсегда удалить такие строки удаления, включите настройку таблицыallow_experimental_replacing_merge_with_cleanupи выполните одно из следующих действий:Задайте настройки таблицыenable_replacing_merge_with_cleanup_for_min_age_to_force_merge,min_age_to_force_merge_on_partition_onlyиmin_age_to_force_merge_seconds. Если все части в партиции старше, чемmin_age_to_force_merge_seconds, ClickHouse выполнит их слияние
в одну часть и удалит все строки удаления.Вручную выполнитеOPTIMIZE TABLE table [PARTITION partition | PARTITION ID 'partition_id'] FINAL CLEANUP.

- Задайте настройки таблицыenable_replacing_merge_with_cleanup_for_min_age_to_force_merge,min_age_to_force_merge_on_partition_onlyиmin_age_to_force_merge_seconds. Если все части в партиции старше, чемmin_age_to_force_merge_seconds, ClickHouse выполнит их слияние
в одну часть и удалит все строки удаления.
Задайте настройки таблицыenable_replacing_merge_with_cleanup_for_min_age_to_force_merge,min_age_to_force_merge_on_partition_onlyиmin_age_to_force_merge_seconds. Если все части в партиции старше, чемmin_age_to_force_merge_seconds, ClickHouse выполнит их слияние
в одну часть и удалит все строки удаления.

- Вручную выполнитеOPTIMIZE TABLE table [PARTITION partition | PARTITION ID 'partition_id'] FINAL CLEANUP.
Вручную выполнитеOPTIMIZE TABLE table [PARTITION partition | PARTITION ID 'partition_id'] FINAL CLEANUP.

Пример:


```
-- with ver and is_deleted
CREATE OR REPLACE TABLE myThirdReplacingMT
(
    `key` Int64,
    `someCol` String,
    `eventTime` DateTime,
    `is_deleted` UInt8
)
ENGINE = ReplacingMergeTree(eventTime, is_deleted)
ORDER BY key
SETTINGS allow_experimental_replacing_merge_with_cleanup = 1;

INSERT INTO myThirdReplacingMT Values (1, 'first', '2020-01-01 01:01:01', 0);
INSERT INTO myThirdReplacingMT Values (1, 'first', '2020-01-01 01:01:01', 1);

select * from myThirdReplacingMT final;

0 rows in set. Elapsed: 0.003 sec.

-- delete rows with is_deleted
OPTIMIZE TABLE myThirdReplacingMT FINAL CLEANUP;

INSERT INTO myThirdReplacingMT Values (1, 'first', '2020-01-01 00:00:00', 0);

select * from myThirdReplacingMT final;

┌─key─┬─someCol─┬───────────eventTime─┬─is_deleted─┐
│   1 │ first   │ 2020-01-01 00:00:00 │          0 │
└─────┴─────────┴─────────────────────┴────────────┘

```

select * from myThirdReplacingMT final;

0 строк в наборе. Прошло: 0.003 сек.

-- удалить строки с is_deleted
OPTIMIZE TABLE myThirdReplacingMT FINAL CLEANUP;

INSERT INTO myThirdReplacingMT Values (1, 'first', '2020-01-01 00:00:00', 0);

select * from myThirdReplacingMT final;

┌─key─┬─someCol─┬───────────eventTime─┬─is_deleted─┐
│   1 │ first   │ 2020-01-01 00:00:00 │          0 │
└─────┴─────────┴─────────────────────┴────────────┘


```
CREATE TABLE [IF NOT EXISTS] [db.]table_name [ON CLUSTER cluster]
(
    name1 [type1] [DEFAULT|MATERIALIZED|ALIAS expr1],
    name2 [type2] [DEFAULT|MATERIALIZED|ALIAS expr2],
    ...
) ENGINE [=] ReplacingMergeTree(date-column [, sampling_expression], (primary, key), index_granularity, [ver])

```


## Части запроса​

При создании таблицыReplacingMergeTreeнеобходимо указывать те жечасти запроса, что и при создании таблицыMergeTree.

Не используйте этот способ в новых проектах и, по возможности, переведите старые проекты на способ, описанный выше.


```
CREATE TABLE rmt_example
(
    `number` UInt16
)
ENGINE = ReplacingMergeTree
ORDER BY number

INSERT INTO rmt_example SELECT floor(randUniform(0, 100)) AS number
FROM numbers(1000000000)

0 rows in set. Elapsed: 19.958 sec. Processed 1.00 billion rows, 8.00 GB (50.11 million rows/s., 400.84 MB/s.)

```

Все параметры, за исключениемver, имеют тот же смысл, что и вMergeTree.ver— столбец с версией. Необязательный параметр. Описание см. в тексте выше.

- ver— столбец с версией. Необязательный параметр. Описание см. в тексте выше.

## Дедупликация при выполнении запроса & FINAL​

Во время слияния ReplacingMergeTree определяет дублирующиеся строки, используя значения столбцовORDER BY(указанных при создании таблицы) в качестве уникального идентификатора и сохраняя только самую позднюю версию. Однако это обеспечивает лишь корректность «в конечном счёте» — нет гарантии, что строки будут дедуплицированы, и полагаться на это не следует. Поэтому запросы могут возвращать некорректные результаты, так как строки с обновлениями и удалениями учитываются в запросах.

Для получения корректных результатов пользователям необходимо дополнять фоновые слияния дедупликацией и удалением строк при выполнении запроса. Это можно сделать с помощью оператораFINAL. Например, рассмотрим следующий пример:


```
SELECT count()
FROM rmt_example

┌─count()─┐
│     200 │
└─────────┘

1 row in set. Elapsed: 0.002 sec.

```

Запрос безFINALвозвращает некорректный результат подсчёта (точное значение будет отличаться в зависимости от выполняемых слияний):


```
SELECT count()
FROM rmt_example
FINAL

┌─count()─┐
│     100 │
└─────────┘

1 row in set. Elapsed: 0.002 sec.

```

Добавление FINAL даёт правильный результат:


```
SELECT count()
FROM rmt_example
FINAL

┌─count()─┐
│     100 │
└─────────┘

1 строка в наборе. Затрачено: 0.002 сек.

```

Для получения дополнительных сведений оFINAL, включая рекомендации по оптимизации его производительности, мы рекомендуем ознакомиться сподробным руководством по ReplacingMergeTree.
