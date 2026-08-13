# Гипотетические индексы - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/statements/hypothetical-index


## CREATE HYPOTHETICAL INDEX


```
CREATE HYPOTHETICAL INDEX [IF NOT EXISTS] name
    ON [db.]table_name (expression) TYPE type[(args)] [GRANULARITY value]

```

- `name` — имя индекса; должно быть уникальным в рамках `(database, table)` для данного сеанса.
- `expression` — столбец или выражение для индексирования.
- `TYPE type` — `minmax`, `set(N)`, `bloom_filter(p)`, `ngrambf_v1(...)`, `tokenbf_v1(...)`. `text` и `vector_similarity` не поддерживаются и отклоняются на этапе `CREATE`, поскольку их фактическая проверка в `ALTER TABLE ... ADD INDEX` зависит от настроек на уровне таблицы, которые хранилище, существующее только в рамках сеанса, не может воспроизвести.
- `GRANULARITY value` — количество гранул данных на одну гранулу индекса. Значение по умолчанию — 1.

```
CREATE HYPOTHETICAL INDEX idx_b ON t (b) TYPE minmax GRANULARITY 1;

```


## Оценка гипотетического индекса с помощью EXPLAIN WHATIF


```
CREATE TABLE t (a UInt64, b UInt64) ENGINE = MergeTree ORDER BY a
SETTINGS index_granularity = 100;

INSERT INTO t SELECT number, number FROM numbers(10000);

CREATE HYPOTHETICAL INDEX idx_b ON t (b) TYPE minmax GRANULARITY 1;

EXPLAIN WHATIF SELECT * FROM t WHERE b = 42;

```


```
Baseline (after PK + partition + existing indexes):
  table:       default.t
  parts:       1
  marks:       100
  est_bytes:   85.52 KiB

With idx_b (minmax, hypothetical):
  status:       applicable
  marks:        1
  est_bytes:    875.00 B
  skip_ratio:   99.0%

Estimation:
  source:           empirical
  empirical_status: ok
  sampled_parts:    1 / 1
  sampled_marks:    100 / 100
  elapsed_us:       631

```


```
ALTER TABLE t ADD STATISTICS b TYPE TDigest;
ALTER TABLE t MATERIALIZE STATISTICS b SETTINGS mutations_sync = 1;

EXPLAIN WHATIF empirical = 0 SELECT * FROM t WHERE b < 10;

```


```
With idx_b (minmax, hypothetical):
  status:       applicable
  marks:        1
  est_bytes:    1.66 KiB
  skip_ratio:   99.9%

Estimation:
  source:           statistical
  empirical_status: disabled

```


## DROP HYPOTHETICAL INDEX


```
DROP HYPOTHETICAL INDEX [IF EXISTS] name ON [db.]table_name

```


## DROP ALL HYPOTHETICAL INDEXES


```
DROP ALL HYPOTHETICAL INDEXES

```


## Область действия и время существования

- Гипотетические индексы существуют только в **текущем сеансе** — они невидимы для других сеансов и удаляются по завершении сеанса.
- Создание или удаление такого индекса не приводит к построению какого-либо индекса и никак не влияет на обычные запросы к таблице. При эмпирическом `EXPLAIN WHATIF` данные таблицы действительно считываются, чтобы построить кандидатный индекс в памяти, и это сканирование засчитывается в лимиты чтения и квоты сеанса.
- Просмотреть гипотетические индексы текущего сеанса можно через [`system.hypothetical_indexes`](https://clickhouse.com/docs/ru/reference/system-tables/hypothetical_indexes).

## Ограничения


## Необходимые привилегии


## См. также

- [`EXPLAIN WHATIF`](https://clickhouse.com/docs/ru/reference/statements/explain#explain-whatif)
- [`system.hypothetical_indexes`](https://clickhouse.com/docs/ru/reference/system-tables/hypothetical_indexes)
- [Индексы пропуска данных](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/mergetree#table_engine-mergetree-data_skipping-indexes)
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
