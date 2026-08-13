# Движок таблицы TimeSeries - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/time-series


```
metric_name1[tag1=value1, tag2=value2, ...] = {timestamp1: value1, timestamp2: value2, ...}
metric_name2[...] = ...

```


## Синтаксис


```
CREATE TABLE name [(columns)] ENGINE=TimeSeries
[SETTINGS var1=value1, ...]
[SAMPLES db.samples_table_name | [SAMPLES INNER COLUMNS (...)] [SAMPLES INNER ENGINE engine(arguments)]]
[TAGS db.tags_table_name | [TAGS INNER COLUMNS (...)] [TAGS INNER ENGINE engine(arguments)]]
[METRICS db.metrics_table_name | [METRICS INNER COLUMNS (...)] [METRICS INNER ENGINE engine(arguments)]]

```


## Использование


```
CREATE TABLE my_table ENGINE=TimeSeries

```

- [prometheus remote-write](https://clickhouse.com/docs/ru/concepts/features/interfaces/prometheus#remote-write)
- [prometheus remote-read](https://clickhouse.com/docs/ru/concepts/features/interfaces/prometheus#remote-read)

### Внешние столбцы


| Имя | Тип | Описание |
| --- | --- | --- |
| `metric_name` | `String` | Имя метрики |
| `tags` | `Map(String, String)` | Карта тегов (меток) для временного ряда |
| `time_series` | `Array(Tuple(DateTime64(3), Float64))` по умолчанию | Массив пар (временная метка, значение) для временного ряда. Тип временной метки в кортеже и тип его скалярного элемента можно определить по объявлению `INNER COLUMNS` для samples (см. [Указание внешних столбцов](#specifying-outer-columns)) |
| `metric_family` | `String` | Имя семейства метрик (для метаданных метрик) |
| `type` | `String` | Тип метрики (например, “counter”, “gauge”) |
| `unit` | `String` | Единица измерения метрики |
| `help` | `String` | Описание метрики |


```
INSERT INTO my_table (metric_name, tags, time_series) VALUES
    ('cpu_usage', {'job': 'node_exporter', 'instance': 'host1:9100'},
     [(toDateTime64('2024-01-01 00:00:00', 3), 0.5), (toDateTime64('2024-01-01 00:01:00', 3), 0.7)])

```


```
INSERT INTO my_table (tags, time_series) VALUES
    ({'__name__': 'cpu_usage', 'job': 'test'},
     [(toDateTime64('2024-01-01 00:00:00', 3), 0.5)])

```


```
INSERT INTO my_table (metric_name, tags, time_series, metric_family, type, unit, help) VALUES
    ('http_requests_total', {'method': 'GET'}, [(now64(), 100.0)],
     'http_requests_total', 'counter', 'requests', 'Total HTTP requests')

```


### Указание внешних столбцов


```
CREATE TABLE my_table (time_series Array(Tuple(UInt32, Float32))) ENGINE=TimeSeries

```


```
CREATE TABLE my_table ENGINE=TimeSeries
SAMPLES INNER COLUMNS (timestamp UInt32, value Float32)

```


## Целевые таблицы


### Таблица *samples*


| Имя | Обязательно? | Тип по умолчанию | Возможные типы | Описание |
| --- | --- | --- | --- | --- |
| `id` | [x] | `UUID` | любой | Идентифицирует комбинацию имени метрики и тегов |
| `timestamp` | [x] | `DateTime64(3)` | `DateTime64(X)` | Момент времени |
| `value` | [x] | `Float64` | `Float32` или `Float64` | Значение, связанное с `timestamp` |


### Таблица tags


| Имя | Обязательный? | Тип по умолчанию | Возможные типы | Описание |
| --- | --- | --- | --- | --- |
| `id` | [x] | `UUID` | any (must match the type of `id` in the [samples](#samples-table) table) | `id` идентифицирует комбинацию имени метрики и тегов. Выражение DEFAULT задаёт способ вычисления такого идентификатора |
| `metric_name` | [x] | `LowCardinality(String)` | `String` or `LowCardinality(String)` | Имя метрики |
| `<tag_value_column>` | [ ] | `String` | `String` or `LowCardinality(String)` or `LowCardinality(Nullable(String))` | Значение конкретного тега; имя тега и имя соответствующего столбца задаются в настройке [tags_to_columns](#settings) |
| `tags` | [x] | `Map(LowCardinality(String), String)` | `Map(String, String)` or `Map(LowCardinality(String), String)` or `Map(LowCardinality(String), LowCardinality(String))` | Карта тегов, за исключением тега `__name__`, содержащего имя метрики, а также тегов с именами, перечисленными в настройке [tags_to_columns](#settings) |
| `all_tags` | [ ] | `Map(String, String)` | `Map(String, String)` or `Map(LowCardinality(String), String)` or `Map(LowCardinality(String), LowCardinality(String))` | Эфемерный столбец: каждая строка содержит карту всех тегов, за исключением только тега `__name__`, содержащего имя метрики. Этот столбец используется только при вычислении `id` |
| `min_time` | [ ] | `Nullable(DateTime64(3))` | `DateTime64(X)` or `Nullable(DateTime64(X))` | Минимальная временная метка временного ряда с данным `id`. Столбец создаётся, если [store_min_time_and_max_time](#settings) имеет значение `true` |
| `max_time` | [ ] | `Nullable(DateTime64(3))` | `DateTime64(X)` or `Nullable(DateTime64(X))` | Максимальная временная метка временного ряда с данным `id`. Столбец создаётся, если [store_min_time_and_max_time](#settings) имеет значение `true` |


### Таблица metrics


| Имя | Обязательный? | Тип по умолчанию | Возможные типы | Описание |
| --- | --- | --- | --- | --- |
| `metric_family_name` | [x] | `String` | `String` или `LowCardinality(String)` | Имя семейства метрик |
| `type` | [x] | `LowCardinality(String)` | `String` или `LowCardinality(String)` | Тип семейства метрик: один из “counter”, “gauge”, “summary”, “stateset”, “histogram”, “gaugehistogram” |
| `unit` | [x] | `LowCardinality(String)` | `String` или `LowCardinality(String)` | Единица измерения, используемая в метрике |
| `help` | [x] | `String` | `String` или `LowCardinality(String)` | Описание метрики |


## Создание


```
CREATE TABLE my_table ENGINE=TimeSeries

```


```
CREATE TABLE my_table
(
    `metric_name` String,
    `tags` Map(String, String),
    `time_series` Array(Tuple(DateTime64(3), Float64)),
    `metric_family` String,
    `type` String,
    `unit` String,
    `help` String
)
ENGINE = TimeSeries
SAMPLES INNER COLUMNS
(
    `id` UUID,
    `timestamp` DateTime64(3),
    `value` Float64
)
SAMPLES INNER ENGINE = MergeTree ORDER BY (id, timestamp)
TAGS INNER COLUMNS
(
    `id` UUID DEFAULT reinterpretAsUUID(sipHash128(metric_name, all_tags)),
    `metric_name` LowCardinality(String),
    `tags` Map(LowCardinality(String), String),
    `all_tags` Map(String, String) EPHEMERAL,
    `min_time` SimpleAggregateFunction(min, Nullable(DateTime64(3))),
    `max_time` SimpleAggregateFunction(max, Nullable(DateTime64(3)))
)
TAGS INNER ENGINE = AggregatingMergeTree PRIMARY KEY metric_name ORDER BY (metric_name, id) SETTINGS allow_dimensions_outside_sorting_key = 1
METRICS INNER COLUMNS
(
    `metric_family_name` String,
    `type` LowCardinality(String),
    `unit` LowCardinality(String),
    `help` String
)
METRICS INNER ENGINE = ReplacingMergeTree ORDER BY metric_family_name

```


```
CREATE TABLE default.`.inner_id.samples.xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
(
    `id` UUID,
    `timestamp` DateTime64(3),
    `value` Float64
)
ENGINE = MergeTree
ORDER BY (id, timestamp)

```


```
CREATE TABLE default.`.inner_id.tags.xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
(
    `id` UUID DEFAULT reinterpretAsUUID(sipHash128(metric_name, all_tags)),
    `metric_name` LowCardinality(String),
    `tags` Map(LowCardinality(String), String),
    `all_tags` Map(String, String) EPHEMERAL,
    `min_time` SimpleAggregateFunction(min, Nullable(DateTime64(3))),
    `max_time` SimpleAggregateFunction(max, Nullable(DateTime64(3)))
)
ENGINE = AggregatingMergeTree
PRIMARY KEY metric_name
ORDER BY (metric_name, id)
SETTINGS allow_dimensions_outside_sorting_key = 1

```


```
CREATE TABLE default.`.inner_id.metrics.xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
(
    `metric_family_name` String,
    `type` LowCardinality(String),
    `unit` LowCardinality(String),
    `help` String
)
ENGINE = ReplacingMergeTree
ORDER BY metric_family_name

```


## Создание таблицы AS на основе существующей таблицы

- `SETTINGS`
- `INNER COLUMNS` для каждого вида
- `INNER ENGINE` для каждого вида

## Настройка типов столбцов


```
CREATE TABLE my_table ENGINE=TimeSeries
SAMPLES INNER COLUMNS (timestamp DateTime64(6), value Float32)

```


```
CREATE TABLE my_table ENGINE=TimeSeries
SAMPLES INNER COLUMNS (timestamp DateTime64(3) CODEC(DoubleDelta))

```


## Столбец `id`


```
CREATE TABLE my_table ENGINE=TimeSeries
TAGS INNER COLUMNS (id UInt64 DEFAULT sipHash64(metric_name, all_tags))

```


```
CREATE TABLE my_table ENGINE=TimeSeries
SETTINGS id_generator = 'sipHash64(metric_name, all_tags)'

```


## Столбцы `tags` и `all_tags`


```
CREATE TABLE my_table
ENGINE = TimeSeries
SETTINGS tags_to_columns = {'instance': 'instance', 'job': 'job'}

```


## Движки внутренних целевых таблиц

- таблица [samples](#samples-table) использует [MergeTree](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/mergetree);
- таблица [tags](#tags-table) использует [AggregatingMergeTree](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/aggregatingmergetree), поскольку одни и те же данные часто вставляются в эту таблицу несколько раз, поэтому необходим способ удалять дубликаты, а также потому, что для столбцов `min_time` и `max_time` требуется выполнять агрегацию;
- таблица [metrics](#metrics-table) использует [ReplacingMergeTree](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/replacingmergetree), поскольку одни и те же данные часто вставляются в эту таблицу несколько раз, поэтому необходим способ удалять дубликаты.

```
CREATE TABLE my_table ENGINE=TimeSeries
SAMPLES ENGINE=ReplicatedMergeTree
TAGS ENGINE=ReplicatedAggregatingMergeTree
METRICS ENGINE=ReplicatedReplacingMergeTree

```


## Внешние целевые таблицы


```
CREATE TABLE samples_for_my_table
(
    `id` UUID,
    `timestamp` DateTime64(3),
    `value` Float64
)
ENGINE = MergeTree
ORDER BY (id, timestamp);

CREATE TABLE tags_for_my_table ...

CREATE TABLE metrics_for_my_table ...

CREATE TABLE my_table ENGINE=TimeSeries SAMPLES samples_for_my_table TAGS tags_for_my_table METRICS metrics_for_my_table;

```


## Изменение настроек

- `id_generator`
- `filter_by_min_time_and_max_time`

```
ALTER TABLE my_table MODIFY SETTING id_generator = 'sipHash64(metric_name, all_tags)';
ALTER TABLE my_table MODIFY SETTING filter_by_min_time_and_max_time = 0;

```


## Настройки


| Имя | Тип | По умолчанию | Описание |
| --- | --- | --- | --- |
| `id_generator` | Expression | зависит от типа `id` | Выражение, вычисляющее идентификатор (fingerprint) временного ряда по его тегам. Если не задано, используется выражение по умолчанию для столбца `id`. Если выражение по умолчанию для столбца `id` также не задано, выражение выбирается автоматически |
| `tags_to_columns` | Map | Map, задающий, какие теги следует вынести в отдельные столбцы таблицы [tags](#tags-table). Синтаксис: `{'tag1': 'column1', 'tag2' : column2, ...}` |  |
| `use_all_tags_column_to_generate_id` | Bool | true | При формировании выражения для вычисления идентификатора временного ряда этот флаг включает использование в вычислении столбца `all_tags` |
| `store_min_time_and_max_time` | Bool | true | Если установлено значение true, таблица будет хранить `min_time` и `max_time` для каждого временного ряда |
| `aggregate_min_time_and_max_time` | Bool | true | При создании внутренней целевой таблицы `tags` этот флаг включает использование `SimpleAggregateFunction(min, Nullable(DateTime64(3)))` вместо просто `Nullable(DateTime64(3))` в качестве типа столбца `min_time`; то же самое относится и к столбцу `max_time` |
| `filter_by_min_time_and_max_time` | Bool | true | Если установлено значение true, таблица будет использовать столбцы `min_time` и `max_time` для фильтрации временных рядов |


# Функции

- [timeSeriesSamples](https://clickhouse.com/docs/ru/reference/functions/table-functions/timeSeriesSamples)
- [timeSeriesTags](https://clickhouse.com/docs/ru/reference/functions/table-functions/timeSeriesTags)
- [timeSeriesMetrics](https://clickhouse.com/docs/ru/reference/functions/table-functions/timeSeriesMetrics)
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
