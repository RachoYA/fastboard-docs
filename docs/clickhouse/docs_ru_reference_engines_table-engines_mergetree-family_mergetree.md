# Движок таблицы MergeTree - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/mergetree

- Первичный ключ таблицы определяет порядок сортировки внутри каждой части таблицы (кластерный индекс). При этом первичный ключ ссылается не на отдельные строки, а на блоки по 8192 строк, называемые гранулами. Благодаря этому первичные ключи даже для очень больших наборов данных остаются достаточно компактными, чтобы помещаться в оперативной памяти, и при этом обеспечивают быстрый доступ к данным на диске.
- Таблицы можно разбивать на партиции с помощью произвольного выражения партиционирования. Отсечение партиций позволяет не читать партиции, если это допускает запрос.
- Данные могут реплицироваться между несколькими узлами кластера для высокой доступности, переключения при сбоях и обновлений без простоя. См. [Репликация данных](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/replication).
- Движки таблиц `MergeTree` поддерживают различные виды статистики и методы сэмплирования, помогающие оптимизации запросов.

## Создание таблиц


```
CREATE TABLE [IF NOT EXISTS] [db.]table_name [ON CLUSTER cluster]
(
    name1 [type1] [[NOT] NULL] [DEFAULT|MATERIALIZED|ALIAS|EPHEMERAL expr1] [COMMENT ...] [CODEC(codec1)] [STATISTICS(stat1)] [TTL expr1] [PRIMARY KEY] [SETTINGS (name = value, ...)],
    name2 [type2] [[NOT] NULL] [DEFAULT|MATERIALIZED|ALIAS|EPHEMERAL expr2] [COMMENT ...] [CODEC(codec2)] [STATISTICS(stat2)] [TTL expr2] [PRIMARY KEY] [SETTINGS (name = value, ...)],
    ...
    INDEX index_name1 expr1 TYPE type1(...) [GRANULARITY value1],
    INDEX index_name2 expr2 TYPE type2(...) [GRANULARITY value2],
    ...
    PROJECTION projection_name_1 (SELECT <COLUMN LIST EXPR> [GROUP BY] [ORDER BY]),
    PROJECTION projection_name_2 (SELECT <COLUMN LIST EXPR> [GROUP BY] [ORDER BY])
) ENGINE = MergeTree()
ORDER BY expr
[PARTITION BY expr]
[PRIMARY KEY expr]
[SAMPLE BY expr]
[TTL expr
    [DELETE|TO DISK 'xxx'|TO VOLUME 'xxx' [, ...] ]
    [WHERE conditions]
    [GROUP BY key_expr [SET v1 = aggr_func(v1) [, v2 = aggr_func(v2) ...]] ] ]
[SETTINGS name = value, ...]

```


### Секции запроса


#### ENGINE


#### ORDER BY


#### PARTITION BY


#### PRIMARY KEY


#### SAMPLE BY


#### TTL


#### НАСТРОЙКИ


```
ENGINE MergeTree() PARTITION BY toYYYYMM(EventDate) ORDER BY (CounterID, EventDate, intHash32(UserID)) SAMPLE BY intHash32(UserID) SETTINGS index_granularity=8192

```


## Хранение данных


## Первичные ключи и индексы в запросах


```
Все данные:     [---------------------------------------------]
CounterID:      [aaaaaaaaaaaaaaaaaabbbbcdeeeeeeeeeeeeefgggggggghhhhhhhhhiiiiiiiiikllllllll]
Date:           [1111111222222233331233211111222222333211111112122222223111112223311122333]
Метки:           |      |      |      |      |      |      |      |      |      |      |
                a,1    a,2    a,3    b,3    e,2    e,3    g,1    h,2    i,1    i,3    l,3
Номера меток:    0      1      2      3      4      5      6      7      8      9      10

```

- `CounterID in ('a', 'h')`, сервер читает данные в диапазонах меток `[0, 3)` и `[6, 8)`.
- `CounterID IN ('a', 'h') AND Date = 3`, сервер читает данные в диапазонах меток `[1, 3)` и `[7, 8)`.
- `Date = 3`, сервер читает данные в диапазоне меток `[1, 10]`.

### Выбор первичного ключа

- Повысить производительность индекса. Если первичный ключ — `(a, b)`, то добавление ещё одного столбца `c` повысит производительность, если выполняются следующие условия:
- Есть запросы с условием по столбцу `c`.
- Часто встречаются длинные диапазоны данных (в несколько раз длиннее, чем `index_granularity`) с одинаковыми значениями `(a, b)`. Иными словами, если добавление ещё одного столбца позволяет пропускать достаточно длинные диапазоны данных.
- Улучшить сжатие данных. ClickHouse сортирует данные по первичному ключу, поэтому чем выше упорядоченность данных, тем лучше сжатие.
- Обеспечить дополнительную логику при слиянии частей данных в движках [CollapsingMergeTree](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/collapsingmergetree) и [SummingMergeTree](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/summingmergetree). В этом случае имеет смысл указать *ключ сортировки*, который отличается от первичного ключа.

### Выбор первичного ключа, отличающегося от ключа сортировки


### Использование индексов и партиций в запросах


```
ENGINE MergeTree()
PARTITION BY toYYYYMM(EventDate)
ORDER BY (CounterID, EventDate)
SETTINGS index_granularity=8192

```


```
SELECT count() FROM table
WHERE EventDate = toDate(now())
AND CounterID = 34

SELECT count() FROM table
WHERE EventDate = toDate(now())
AND (CounterID = 34 OR CounterID = 42)

SELECT count() FROM table
WHERE ((EventDate >= toDate('2014-01-01')
AND EventDate <= toDate('2014-01-31')) OR EventDate = toDate('2014-05-01'))
AND CounterID IN (101500, 731962, 160656)
AND (CounterID = 101500 OR EventDate != toDate('2014-05-01'))

```


```
SELECT count() FROM table WHERE CounterID = 34 OR URL LIKE '%upyachka%'

```


### Использование индекса для детерминированных выражений в первичных ключах


```
ENGINE = MergeTree()
ORDER BY length(user_id)

```


```
SELECT * FROM table WHERE user_id = 'alice';
SELECT * FROM table WHERE user_id IN ('alice', 'bob');
SELECT * FROM table WHERE has(['alice', 'bob'], user_id);

```


```
ENGINE = MergeTree()
ORDER BY hex(p)

```


```
ENGINE = MergeTree()
ORDER BY reverse(tuple(reverse(p), hex(p)))

```


```
SELECT * FROM table WHERE p != 'abc';
SELECT * FROM table WHERE p NOT IN ('abc', '12345');
SELECT * FROM table WHERE NOT has(['abc', '12345'], p);

```


### Использование индекса для частично-монотонных первичных ключей


### Индексы пропуска данных


```
INDEX index_name expr TYPE type(...) [GRANULARITY granularity_value]

```


```
CREATE TABLE table_name
(
    u64 UInt64,
    i32 Int32,
    s String,
    ...
    INDEX idx1 u64 TYPE bloom_filter GRANULARITY 3,
    INDEX idx2 u64 * i32 TYPE minmax GRANULARITY 3,
    INDEX idx3 u64 * length(s) TYPE set(1000) GRANULARITY 4
) ENGINE = MergeTree()
...

```


```
SELECT count() FROM table WHERE u64 == 10;
SELECT count() FROM table WHERE u64 * i32 >= 1234
SELECT count() FROM table WHERE u64 * length(s) == 1234

```


```
-- для столбцов типа Map:
INDEX map_key_index mapKeys(map_column) TYPE bloom_filter
INDEX map_value_index mapValues(map_column) TYPE bloom_filter

-- для столбцов типа JSON:
INDEX json_paths_index JSONAllPaths(json_column) TYPE bloom_filter

-- для столбцов типа Tuple:
INDEX tuple_1_index tuple_column.1 TYPE bloom_filter
INDEX tuple_2_index tuple_column.2 TYPE bloom_filter

-- для столбцов типа Nested:
INDEX nested_1_index col.nested_col1 TYPE bloom_filter
INDEX nested_2_index col.nested_col2 TYPE bloom_filter

```


### Типы индексов пропуска данных

- индекс [`MinMax`](#minmax)
- индекс [`Set`](#set)
- индекс [`bloom_filter`](#bloom-filter)
- индекс [`ngrambf_v1`](#n-gram-bloom-filter) *(Устарело)*
- индекс [`tokenbf_v1`](#token-bloom-filter) *(Устарело)*
- индекс [`text`](#text)
- индекс [`vector_similarity`](#vector-similarity)

#### Индекс пропуска данных MinMax


```
minmax

```


#### Set


```
set(max_rows)

```


#### Bloom-фильтр


```
bloom_filter([false_positive_rate])

```

- `(U)Int*`
- `Float*`
- `Enum`
- `Date`
- `DateTime`
- `String`
- `FixedString`
- `Array`
- `LowCardinality`
- `Nullable`
- `UUID`
- `Map`

#### N-граммный bloom-фильтр *(Устарело)*


```
ngrambf_v1(n, size_of_bloom_filter_in_bytes, number_of_hash_functions, random_seed)

```


| Параметр | Описание |
| --- | --- |
| `n` | размер n-граммы |
| `size_of_bloom_filter_in_bytes` | Размер bloom-фильтра в байтах. Здесь можно использовать большое значение, например `256` или `512`, так как он хорошо сжимается). |
| `number_of_hash_functions` | Количество хеш-функций, используемых в bloom-фильтре. |
| `random_seed` | seed для хеш-функций bloom-фильтра. |

- [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring)
- [`Map`](https://clickhouse.com/docs/ru/reference/data-types/map)

```
CREATE FUNCTION bfEstimateFunctions [ON CLUSTER cluster]
AS
(total_number_of_all_grams, size_of_bloom_filter_in_bits) -> round((size_of_bloom_filter_in_bits / total_number_of_all_grams) * log(2));

CREATE FUNCTION bfEstimateBmSize [ON CLUSTER cluster]
AS
(total_number_of_all_grams, probability_of_false_positives) -> ceil((total_number_of_all_grams * log(probability_of_false_positives)) / log(1 / pow(2, log(2))));

CREATE FUNCTION bfEstimateFalsePositive [ON CLUSTER cluster]
AS
(total_number_of_all_grams, number_of_hash_functions, size_of_bloom_filter_in_bytes) -> pow(1 - exp(-number_of_hash_functions/ (size_of_bloom_filter_in_bytes / total_number_of_all_grams)), number_of_hash_functions);

CREATE FUNCTION bfEstimateGramNumber [ON CLUSTER cluster]
AS
(number_of_hash_functions, probability_of_false_positives, size_of_bloom_filter_in_bytes) -> ceil(size_of_bloom_filter_in_bytes / (-number_of_hash_functions / log(1 - exp(log(probability_of_false_positives) / number_of_hash_functions))))

```

- `total_number_of_all_grams`
- `probability_of_false_positives`

```
--- estimate number of bits in the filter
SELECT bfEstimateBmSize(4300, 0.0001) / 8 AS size_of_bloom_filter_in_bytes;

┌─size_of_bloom_filter_in_bytes─┐
│                         10304 │
└───────────────────────────────┘

--- estimate number of hash functions
SELECT bfEstimateFunctions(4300, bfEstimateBmSize(4300, 0.0001)) as number_of_hash_functions

┌─number_of_hash_functions─┐
│                       13 │
└──────────────────────────┘

```


#### Токенный bloom-фильтр


```
tokenbf_v1(size_of_bloom_filter_in_bytes, number_of_hash_functions, random_seed)

```


#### Bloom-фильтр для sparse grams


```
sparse_grams(min_ngram_length, max_ngram_length, min_cutoff_length, size_of_bloom_filter_in_bytes, number_of_hash_functions, random_seed)

```


### Текстовый индекс


#### Векторное сходство


### Поддержка функций


| Функция (оператор) / индекс | первичный ключ | minmax | ngrambf_v1 | tokenbf_v1 | bloom_filter | sparse_grams | text |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [равно (=, ==)](https://clickhouse.com/docs/ru/reference/functions/regular-functions/comparison-functions#equals) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| [notEquals(!=, <>)](https://clickhouse.com/docs/ru/reference/functions/regular-functions/comparison-functions#notEquals) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✗ |
| [like](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-search-functions#like) | ✔ | ✔ | ✔ | ✔ | ✗ | ✔ | ✔ |
| [notLike](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-search-functions#notLike) | ✔ | ✔ | ✔ | ✔ | ✗ | ✔ | ✗ |
| [match](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-search-functions#match) | ✗ | ✗ | ✔ | ✔ | ✗ | ✔ | ✔ |
| [startsWith](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-functions#startsWith) | ✔ | ✔ | ✔ | ✔ | ✗ | ✔ | ✔ |
| [endsWith](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-functions#endsWith) | ✗ | ✗ | ✔ | ✔ | ✗ | ✔ | ✔ |
| [multiSearchAny](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-search-functions#multiSearchAny) | ✗ | ✗ | ✔ | ✗ | ✗ | ✗ | ✔ |
| [multiSearchAnyUTF8](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-search-functions#multiSearchAnyUTF8) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✔ |
| [multiMatchAny](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-search-functions#multiMatchAny) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✔ |
| [in](https://clickhouse.com/docs/ru/reference/functions/regular-functions/in-functions) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| [notIn](https://clickhouse.com/docs/ru/reference/functions/regular-functions/in-functions) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✗ |
| [less (`<`)](https://clickhouse.com/docs/ru/reference/functions/regular-functions/comparison-functions#less) | ✔ | ✔ | ✗ | ✗ | ✗ | ✗ | ✗ |
| [greater (`>`)](https://clickhouse.com/docs/ru/reference/functions/regular-functions/comparison-functions#greater) | ✔ | ✔ | ✗ | ✗ | ✗ | ✗ | ✗ |
| [lessOrEquals (`<=`)](https://clickhouse.com/docs/ru/reference/functions/regular-functions/comparison-functions#lessOrEquals) | ✔ | ✔ | ✗ | ✗ | ✗ | ✗ | ✗ |
| [greaterOrEquals (`>=`)](https://clickhouse.com/docs/ru/reference/functions/regular-functions/comparison-functions#greaterOrEquals) | ✔ | ✔ | ✗ | ✗ | ✗ | ✗ | ✗ |
| [empty](https://clickhouse.com/docs/ru/reference/functions/regular-functions/array-functions#empty) | ✔ | ✔ | ✗ | ✗ | ✗ | ✗ | ✗ |
| [notEmpty](https://clickhouse.com/docs/ru/reference/functions/regular-functions/array-functions#notEmpty) | ✗ | ✔ | ✗ | ✗ | ✗ | ✔ | ✗ |
| [has](https://clickhouse.com/docs/ru/reference/functions/regular-functions/array-functions#has) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| [hasAny](https://clickhouse.com/docs/ru/reference/functions/regular-functions/array-functions#hasAny) | ✗ | ✗ | ✔ | ✔ | ✔ | ✔ | ✗ |
| [hasAll](https://clickhouse.com/docs/ru/reference/functions/regular-functions/array-functions#hasAll) | ✗ | ✗ | ✔ | ✔ | ✔ | ✔ | ✗ |
| [hasToken](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-search-functions#hasToken) | ✗ | ✗ | ✗ | ✔ | ✗ | ✗ | ✔ |
| [hasTokenOrNull](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-search-functions#hasTokenOrNull) | ✗ | ✗ | ✗ | ✔ | ✗ | ✗ | ✔ |
| [hasTokenCaseInsensitive (`*`)](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-search-functions#hasTokenCaseInsensitive) | ✗ | ✗ | ✗ | ✔ | ✗ | ✗ | ✗ |
| [hasTokenCaseInsensitiveOrNull (`*`)](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-search-functions#hasTokenCaseInsensitiveOrNull) | ✗ | ✗ | ✗ | ✔ | ✗ | ✗ | ✗ |
| [hasAnyTokens](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-search-functions#hasAnyTokens) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✔ |
| [hasAllTokens](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-search-functions#hasAllTokens) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✔ |
| [pointInPolygon](https://clickhouse.com/docs/ru/reference/functions/regular-functions/geo/coordinates#pointinpolygon) | ✔ | ✔ | ✗ | ✗ | ✗ | ✗ | ✗ |
| [mapContains (mapContainsKey)](https://clickhouse.com/docs/ru/reference/functions/regular-functions/tuple-map-functions#mapContainsKey) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✔ |
| [mapContainsKeyLike](https://clickhouse.com/docs/ru/reference/functions/regular-functions/tuple-map-functions#mapContainsKeyLike) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✔ |
| [mapContainsValue](https://clickhouse.com/docs/ru/reference/functions/regular-functions/tuple-map-functions#mapContainsValue) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✔ |
| [mapContainsValueLike](https://clickhouse.com/docs/ru/reference/functions/regular-functions/tuple-map-functions#mapContainsValueLike) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✔ |

- Могут быть оптимизированы:
- `s LIKE '%test%'`
- `NOT s NOT LIKE '%test%'`
- `s = 1`
- `NOT s != 1`
- `startsWith(s, 'test')`
- Не могут быть оптимизированы:
- `NOT s LIKE '%test%'`
- `s NOT LIKE '%test%'`
- `NOT s = 1`
- `s != 1`
- `NOT startsWith(s, 'test')`

## Проекции


### Запрос проекции


```
SELECT <column list expr> [GROUP BY] <group keys expr> [ORDER BY] <expr>

```


### Индексы проекций


#### Синтаксис


```
PROJECTION <name> INDEX <index_expr> TYPE <index_type>

```


```
CREATE TABLE example
(
    id UInt64,
    region String,
    user_id UInt32,
    PROJECTION region_proj INDEX region TYPE basic,
    PROJECTION uid_proj INDEX user_id TYPE basic
)
ENGINE = MergeTree
ORDER BY id;

```


#### Типы индексов

- **basic**: эквивалентен обычному индексу MergeTree по выражению.

### Хранение проекций


### Анализ запроса

- Проверьте, можно ли использовать проекцию для выполнения данного запроса, то есть даст ли она тот же результат, что и запрос к базовой таблице.
- Выберите наилучший подходящий вариант, для которого требуется прочитать наименьшее число гранул.
- Конвейер запроса, использующий проекции, будет отличаться от того, который использует исходные части. Если в некоторых частях проекция отсутствует, можно добавить конвейер, который построит её на лету.

## Одновременный доступ к данным


## TTL для столбцов и таблиц


```
TTL time_column
TTL time_column + interval

```


```
TTL date_time + INTERVAL 1 MONTH
TTL date_time + INTERVAL 15 HOUR

```


### TTL для столбца


#### Создание таблицы с `TTL`:


```
CREATE TABLE tab
(
    d DateTime,
    a Int TTL d + INTERVAL 1 MONTH,
    b Int TTL d + INTERVAL 1 MONTH,
    c String
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(d)
ORDER BY d;

```


#### Добавление TTL к столбцу существующей таблицы


```
ALTER TABLE tab
    MODIFY COLUMN
    c String TTL d + INTERVAL 1 DAY;

```


#### Изменение TTL для столбца


```
ALTER TABLE tab
    MODIFY COLUMN
    c String TTL d + INTERVAL 1 MONTH;

```


### TTL таблицы


```
TTL expr
    [DELETE|RECOMPRESS codec_name1|TO DISK 'xxx'|TO VOLUME 'xxx'][, DELETE|RECOMPRESS codec_name2|TO DISK 'aaa'|TO VOLUME 'bbb'] ...
    [WHERE conditions]
    [GROUP BY key_expr [SET v1 = aggr_func(v1) [, v2 = aggr_func(v2) ...]] ]

```

- `DELETE` - удалить истёкшие строки (действие по умолчанию);
- `RECOMPRESS codec_name` - повторно сжать часть данных с помощью `codec_name`;
- `TO DISK 'aaa'` - переместить часть на диск `aaa`;
- `TO VOLUME 'bbb'` - переместить часть на диск `bbb`;
- `GROUP BY` - агрегировать истёкшие строки.

```
TTL time_column + INTERVAL 1 MONTH DELETE WHERE column = 'value'

```


#### Создание таблицы с `TTL`:


```
CREATE TABLE tab
(
    d DateTime,
    a Int
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(d)
ORDER BY d
TTL d + INTERVAL 1 MONTH DELETE,
    d + INTERVAL 1 WEEK TO VOLUME 'aaa',
    d + INTERVAL 2 WEEK TO DISK 'bbb';

```


#### Изменение `TTL` у таблицы:


```
ALTER TABLE tab
    MODIFY TTL d + INTERVAL 1 DAY;

```


```
CREATE TABLE table_with_where
(
    d DateTime,
    a Int
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(d)
ORDER BY d
TTL d + INTERVAL 1 MONTH DELETE WHERE toDayOfWeek(d) = 1;

```


#### Создание таблицы, в которой для истёкших строк выполняется повторное сжатие:


```
CREATE TABLE table_for_recompression
(
    d DateTime,
    key UInt64,
    value String
) ENGINE MergeTree()
ORDER BY tuple()
PARTITION BY key
TTL d + INTERVAL 1 MONTH RECOMPRESS CODEC(ZSTD(17)), d + INTERVAL 1 YEAR RECOMPRESS CODEC(LZ4HC(10))
SETTINGS min_rows_for_wide_part = 0, min_bytes_for_wide_part = 0;

```


```
CREATE TABLE table_for_aggregation
(
    d DateTime,
    k1 Int,
    k2 Int,
    x Int,
    y Int
)
ENGINE = MergeTree
ORDER BY (k1, k2)
TTL d + INTERVAL 1 MONTH GROUP BY k1, k2 SET x = max(x), y = min(y);

```


### Удаление устаревших данных

- настройка [ttl_only_drop_parts](https://clickhouse.com/docs/ru/reference/settings/merge-tree-settings#ttl_only_drop_parts)

## Типы дисков

- [`s3` для S3 и MinIO](#table_engine-mergetree-s3)
- [`gcs` для GCS](https://clickhouse.com/docs/ru/integrations/connectors/data-sources/gcs#creating-a-disk)
- [`blob_storage_disk` для Azure Blob Storage](https://clickhouse.com/docs/ru/concepts/features/configuration/server-config/storing-data#azure-blob-storage)
- [`hdfs` для HDFS](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/hdfs)
- [`web` для доступа только для чтения через веб](https://clickhouse.com/docs/ru/concepts/features/configuration/server-config/storing-data#web-storage)
- [`cache` для локального кэширования](https://clickhouse.com/docs/ru/concepts/features/configuration/server-config/storing-data#using-local-cache)
- [`s3_plain` для резервных копий в S3](https://clickhouse.com/docs/ru/concepts/features/backup-restore/local-disk)
- [`s3_plain_rewritable` для неизменяемых нереплицируемых таблиц в S3](https://clickhouse.com/docs/ru/concepts/features/configuration/server-config/storing-data#s3-plain-rewritable-storage)

## Использование нескольких блочных устройств для хранения данных


### Введение


### Термины

- Диск — блочное устройство, смонтированное в файловую систему.
- Диск по умолчанию — диск, соответствующий пути, указанному в настройке сервера [path](https://clickhouse.com/docs/ru/reference/settings/server-settings/settings#path).
- Том — упорядоченный набор одинаковых дисков (аналогично [JBOD](https://en.wikipedia.org/wiki/Non-RAID_drive_architectures)).
- Политика хранения — набор томов и правил перемещения данных между ними.

### Конфигурация


```
<storage_configuration>
    <disks>
        <disk_name_1> <!-- имя диска -->
            <path>/mnt/fast_ssd/clickhouse/</path>
        </disk_name_1>
        <disk_name_2>
            <path>/mnt/hdd1/clickhouse/</path>
            <keep_free_space_bytes>10485760</keep_free_space_bytes>
        </disk_name_2>
        <disk_name_3>
            <path>/mnt/hdd2/clickhouse/</path>
            <keep_free_space_bytes>10485760</keep_free_space_bytes>
        </disk_name_3>

        ...
    </disks>

    ...
</storage_configuration>

```

- `<disk_name_N>` — имя диска. Имена всех дисков должны отличаться.
- `path` — путь, по которому сервер будет хранить данные (папки `data` и `shadow`); должен оканчиваться на ’/’.
- `keep_free_space_bytes` — объём свободного места на диске, который нужно зарезервировать.

```
<storage_configuration>
    ...
    <policies>
        <policy_name_1>
            <volumes>
                <volume_name_1>
                    <disk>disk_name_from_disks_configuration</disk>
                    <max_data_part_size_bytes>1073741824</max_data_part_size_bytes>
                    <load_balancing>round_robin</load_balancing>
                </volume_name_1>
                <volume_name_2>
                    <!-- конфигурация -->
                </volume_name_2>
                <!-- другие тома -->
            </volumes>
            <move_factor>0.2</move_factor>
        </policy_name_1>
        <policy_name_2>
            <!-- конфигурация -->
        </policy_name_2>

        <!-- другие политики -->
    </policies>
    ...
</storage_configuration>

```

- `policy_name_N` — имя политики. Имена политик должны быть уникальными.
- `volume_name_N` — имя тома. Имена томов должны быть уникальными.
- `disk` — диск внутри тома.
- `max_data_part_size_bytes` — максимальный размер части, которая может храниться на любом из дисков тома. Если предполагаемый размер слитой части превышает `max_data_part_size_bytes`, эта часть будет записана на следующий том. По сути, эта возможность позволяет хранить новые/небольшие части на горячем томе (SSD) и перемещать их на холодный том (HDD), когда они становятся большими. Не используйте этот параметр, если в вашей политике только один том.
- `move_factor` — когда объем доступного пространства становится меньше этого коэффициента, данные автоматически начинают перемещаться на следующий том, если он есть (по умолчанию 0.1). ClickHouse сортирует существующие части по размеру от большего к меньшему (по убыванию) и выбирает части, суммарный размер которых достаточен для выполнения условия `move_factor`. Если суммарного размера всех частей недостаточно, будут перемещены все части.
- `perform_ttl_move_on_insert` — отключает TTL move при INSERT части. По умолчанию (если параметр включен), если вставляется часть, которая уже подпадает под правило TTL move, она сразу записывается на том/диск, указанный в правиле перемещения. Это может существенно замедлить вставку, если том/диск пункта назначения медленный (например, S3). Если параметр отключен, уже подпадающая под TTL часть записывается на том по умолчанию, а затем сразу перемещается на TTL-том.
- `load_balancing` - политика балансировки дисков: `round_robin` или `least_used`.
- `least_used_ttl_ms` - настраивает тайм-аут (в миллисекундах) обновления доступного пространства на всех дисках (`0` - обновлять всегда, `-1` - никогда не обновлять, значение по умолчанию — `60000`). Обратите внимание: если диск может использоваться только ClickHouse и не подвержен изменению размера файловой системы в режиме online, можно использовать `-1`; во всех остальных случаях это не рекомендуется, так как со временем это приведет к некорректному распределению пространства.
- `prefer_not_to_merge` — этот параметр не следует использовать. Он отключает слияние частей на этом томе (это вредно и приводит к снижению производительности). Когда этот параметр включен (не делайте этого), слияние данных на этом томе запрещено (а это плохо). Это позволяет (хотя вам это не нужно) контролировать (если вам хочется что-то контролировать, вы, скорее всего, делаете что-то не так), как ClickHouse работает с медленными дисками (но ClickHouse знает лучше, поэтому, пожалуйста, не используйте этот параметр).
- `volume_priority` — определяет приоритет (порядок), в котором заполняются тома. Меньшее значение означает более высокий приоритет. Значения параметра должны быть натуральными числами и в совокупности покрывать диапазон от 1 до N (где N соответствует наименьшему приоритету) без пропуска чисел.
- Если помечены *все* тома, приоритет назначается им в указанном порядке.
- Если помечены только *некоторые* тома, тома без метки получают наименьший приоритет, а между собой упорядочиваются в том порядке, в котором они заданы в config.
- Если не помечен *ни один* том, их приоритет определяется порядком, в котором они объявлены в конфигурации.
- Два тома не могут иметь одинаковое значение приоритета.

```
<storage_configuration>
    ...
    <policies>
        <hdd_in_order> <!-- policy name -->
            <volumes>
                <single> <!-- название тома -->
                    <disk>disk1</disk>
                    <disk>disk2</disk>
                </single>
            </volumes>
        </hdd_in_order>

        <moving_from_ssd_to_hdd>
            <volumes>
                <hot>
                    <disk>fast_ssd</disk>
                    <max_data_part_size_bytes>1073741824</max_data_part_size_bytes>
                </hot>
                <cold>
                    <disk>disk1</disk>
                </cold>
            </volumes>
            <move_factor>0.2</move_factor>
        </moving_from_ssd_to_hdd>

        <small_jbod_with_external_no_merges>
            <volumes>
                <main>
                    <disk>jbod1</disk>
                </main>
                <external>
                    <disk>external</disk>
                </external>
            </volumes>
        </small_jbod_with_external_no_merges>
    </policies>
    ...
</storage_configuration>

```


```
CREATE TABLE table_with_non_default_policy (
    EventDate Date,
    OrderID UInt64,
    BannerID UInt64,
    SearchPhrase String
) ENGINE = MergeTree
ORDER BY (OrderID, BannerID)
PARTITION BY toYYYYMM(EventDate)
SETTINGS storage_policy = 'moving_from_ssd_to_hdd'

```


### Подробности

- В результате вставки (запрос `INSERT`).
- Во время фоновых слияний и [мутаций](https://clickhouse.com/docs/ru/reference/statements/alter/index#mutations).
- При загрузке с другой реплики.
- В результате заморозки партиции [ALTER TABLE … FREEZE PARTITION](https://clickhouse.com/docs/ru/reference/statements/alter/partition#freeze-partition).
- Выбирается первый том (в порядке объявления), на котором достаточно места для хранения части (`unreserved_space > current_part_size`) и который допускает хранение частей такого размера (`max_data_part_size_bytes > current_part_size`).
- Внутри этого тома выбирается диск, следующий за тем, который использовался для хранения предыдущего фрагмента данных, и на котором свободного места больше, чем размер части (`unreserved_space - keep_free_space_bytes > current_part_size`).

## Использование внешнего хранилища для хранения данных


```
<storage_configuration>
    ...
    <disks>
        <s3>
            <type>s3</type>
            <support_batch_delete>true</support_batch_delete>
            <endpoint>https://clickhouse-public-datasets.s3.amazonaws.com/my-bucket/root-path/</endpoint>
            <access_key_id>your_access_key_id</access_key_id>
            <secret_access_key>your_secret_access_key</secret_access_key>
            <region></region>
            <header>Authorization: Bearer SOME-TOKEN</header>
            <server_side_encryption_customer_key_base64>your_base64_encoded_customer_key</server_side_encryption_customer_key_base64>
            <server_side_encryption_kms_key_id>your_kms_key_id</server_side_encryption_kms_key_id>
            <server_side_encryption_kms_encryption_context>your_kms_encryption_context</server_side_encryption_kms_encryption_context>
            <server_side_encryption_kms_bucket_key_enabled>true</server_side_encryption_kms_bucket_key_enabled>
            <proxy>
                <uri>http://proxy1</uri>
                <uri>http://proxy2</uri>
            </proxy>
            <connect_timeout_ms>10000</connect_timeout_ms>
            <request_timeout_ms>5000</request_timeout_ms>
            <retry_attempts>10</retry_attempts>
            <single_read_retries>4</single_read_retries>
            <min_bytes_for_seek>1000</min_bytes_for_seek>
            <metadata_path>/var/lib/clickhouse/disks/s3/</metadata_path>
            <skip_access_check>false</skip_access_check>
        </s3>
        <s3_cache>
            <type>cache</type>
            <disk>s3</disk>
            <path>/var/lib/clickhouse/disks/s3_cache/</path>
            <max_size>10Gi</max_size>
        </s3_cache>
    </disks>
    ...
</storage_configuration>

```


### Использование S3-дисков с несколькими томами


```
<storage_configuration>
    <disks>
        <s3_bucket1>
            <type>s3</type>
            <endpoint>https://s3.amazonaws.com/bucket-1/data/</endpoint>
            <access_key_id>your_access_key_id</access_key_id>
            <secret_access_key>your_secret_access_key</secret_access_key>
        </s3_bucket1>
        <s3_bucket2>
            <type>s3</type>
            <endpoint>https://s3.amazonaws.com/bucket-2/data/</endpoint>
            <access_key_id>your_access_key_id</access_key_id>
            <secret_access_key>your_secret_access_key</secret_access_key>
        </s3_bucket2>
    </disks>
    <policies>
        <s3_multi_bucket>
            <volumes>
                <main>
                    <disk>s3_bucket1</disk>
                    <disk>s3_bucket2</disk>
                </main>
            </volumes>
        </s3_multi_bucket>
    </policies>
</storage_configuration>

```


```
<storage_configuration>
    <disks>
        <local_ssd>
            <path>/mnt/fast_ssd/clickhouse/</path>
        </local_ssd>
        <s3_cold>
            <type>s3</type>
            <endpoint>https://s3.amazonaws.com/cold-storage/data/</endpoint>
            <access_key_id>your_access_key_id</access_key_id>
            <secret_access_key>your_secret_access_key</secret_access_key>
        </s3_cold>
    </disks>
    <policies>
        <local_to_s3>
            <volumes>
                <hot>
                    <disk>local_ssd</disk>
                    <max_data_part_size_bytes>1073741824</max_data_part_size_bytes>
                </hot>
                <cold>
                    <disk>s3_cold</disk>
                </cold>
            </volumes>
            <move_factor>0.2</move_factor>
        </local_to_s3>
    </policies>
</storage_configuration>

```


## Виртуальные столбцы

- `_part` — Имя части.
- `_part_index` — Последовательный индекс части в результате запроса.
- `_part_starting_offset` — Накопительный номер начальной строки части в результате запроса.
- `_part_offset` — Номер строки в части.
- `_part_granule_offset` — Номер гранулы в части.
- `_partition_id` — Имя партиции.
- `_part_uuid` — Уникальный идентификатор части (если включена настройка MergeTree `assign_part_uuids`).
- `_part_data_version` — Версия данных части (минимальный номер блока или версия мутации).
- `_partition_value` — Значения (кортеж) выражения `partition by`.
- `_sample_factor` — Коэффициент выборки (из запроса).
- `_block_number` — Исходный номер блока для строки, назначенный при вставке; сохраняется при слияниях, когда включена настройка `enable_block_number_column`.
- `_block_offset` — Исходный номер строки в блоке, назначенный при вставке; сохраняется при слияниях, когда включена настройка `enable_block_offset_column`.
- `_disk_name` — Имя диска, используемого для хранения.

## Статистика столбцов


```
CREATE TABLE tab
(
    a Int64 STATISTICS(tdigest, uniq),
    b Float64
)
ENGINE = MergeTree
ORDER BY a

```


```
ALTER TABLE tab ADD STATISTICS b TYPE tdigest, uniq;
ALTER TABLE tab DROP STATISTICS a;

```


#### Отсечение частей на основе статистики


```
-- Create a table with basic statistics on the 'value' column
CREATE TABLE test_stats
(
    id UInt64,
    value Int64 STATISTICS(basic)
)
ENGINE = MergeTree
ORDER BY id;

SYSTEM STOP MERGES test_stats;

-- Insert data in separate inserts to create multiple parts
INSERT INTO test_stats SELECT number, number FROM numbers(1000); -- Part 1: value range [0, 999]
INSERT INTO test_stats SELECT number, number + 10000 FROM numbers(1000); -- Part 2: value range [10000, 10999]

SET use_statistics_for_part_pruning = 1;

-- This query will skip Part 1 entirely because its max value (999) < 5000
SELECT count() FROM test_stats WHERE value > 5000;

-- Use EXPLAIN to see the pruning effect
EXPLAIN indexes = 1 SELECT count() FROM test_stats WHERE value > 5000;
-- The output will show "Parts: 1/2" indicating one part was pruned

```


### Доступные типы статистики столбцов

- `basic` Компактный набор однозначных сводных характеристик, вычисляемых по столбцу. В зависимости от типа столбца заполняются следующие компоненты:
- для любого столбца, значения которого представлены числами (целые числа, числа с плавающей точкой, `Decimal*`, `Date*`, `DateTime*`, `Enum*`, `IPv4`, …): минимальное и максимальное значения, которые позволяют оценивать селективность фильтра диапазона и выполнять отсечение частей;
- для столбцов `String` и `FixedString`: суммарная длина в байтах всех значений, отличных от `NULL` (на её основе можно вычислить среднюю длину строки);
- для столбцов `Nullable` и `LowCardinality(Nullable)`: количество значений `NULL`, которое оптимизатор использует, чтобы исключать строки с `NULL` из оценок селективности. Одна статистика `basic` может одновременно заполнять несколько таких компонентов — например, для столбца `Nullable(UInt32)` она отслеживает и числовые минимум/максимум, и количество значений `NULL`. По сравнению с `minmax`, `basic` дополнительно работает со столбцами `String` / `FixedString` и может быть объявлена для обёрток `Nullable` типов вроде `UUID` или `IPv6` исключительно для отслеживания количества значений `NULL`.
- `minmax` (устарело)
- `tdigest`
- `uniq` Скетчи [BJKST](https://people.iith.ac.in/aravind/Files-CS5120/pc-lec14-BJKST.pdf), которые позволяют оценить количество различных значений в столбце. Внутри используется [`uniq`](https://clickhouse.com/docs/ru/reference/functions/aggregate-functions/uniq).
- `uniq_v2` Аналогично `uniq`, но внутри используется [`uniqCombined`](https://clickhouse.com/docs/ru/reference/functions/aggregate-functions/uniqCombined)`(12)` (вариант [HyperLogLog](https://en.wikipedia.org/wiki/HyperLogLog)). Потребляет меньше памяти, чем `uniq`, и может строиться быстрее.
- `countmin`

### Поддерживаемые типы данных


|  | (U)Int*, Float*, Decimal(*), Date*, булевый, Enum* | IPv4 | String или FixedString |
| --- | --- | --- | --- |
| basic | ✔ | ✔ | ✔ |
| countmin | ✔ | ✔ | ✔ |
| minmax | ✔ | ✔ | ✗ |
| tdigest | ✔ | ✗ | ✗ |
| uniq | ✔ | ✔ | ✔ |
| uniq_v2 | ✔ | ✔ | ✔ |


### Поддерживаемые операции


|  | Фильтры равенства (==) | Фильтры диапазона (`>, >=, <, <=`) |
| --- | --- | --- |
| basic | ✗ | ✔ (только числовые столбцы) |
| countmin | ✔ | ✗ |
| minmax | ✗ | ✔ (только числовые столбцы) |
| tdigest | ✗ | ✔ (только числовые столбцы) |
| uniq | ✔ | ✗ |
| uniq_v2 | ✔ | ✗ |


## Настройки на уровне столбцов

- `max_compress_block_size` — Максимальный размер блоков несжатых данных перед сжатием при записи в таблицу.
- `min_compress_block_size` — Минимальный размер блоков несжатых данных, необходимый для сжатия перед записью следующей метки.

```
CREATE TABLE tab
(
    id Int64,
    document String SETTINGS (min_compress_block_size = 16777216, max_compress_block_size = 16777216)
)
ENGINE = MergeTree
ORDER BY id

```

- Удалить `SETTINGS` из определения столбца:

```
ALTER TABLE tab MODIFY COLUMN document REMOVE SETTINGS;

```

- Измените параметр:

```
ALTER TABLE tab MODIFY COLUMN document MODIFY SETTING min_compress_block_size = 8192;

```

- Сбрасывает одну или несколько настроек, а также удаляет объявление настройки из выражения столбца в CREATE-запросе таблицы.

```
ALTER TABLE tab MODIFY COLUMN document RESET SETTING min_compress_block_size;

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
