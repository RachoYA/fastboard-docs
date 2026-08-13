# DESCRIBE TABLE - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/statements/describe-table


```
DESC|DESCRIBE TABLE [db.]table [INTO OUTFILE filename] [FORMAT format]

```

- `name` — имя столбца.
- `type` — тип столбца.
- `default_type` — конструкция, используемая в [выражении столбца по умолчанию](https://clickhouse.com/docs/ru/reference/statements/create/table): `DEFAULT`, `MATERIALIZED` или `ALIAS`. Если выражение по умолчанию отсутствует, возвращается пустая строка.
- `default_expression` — выражение, указанное после конструкции `DEFAULT`.
- `comment` — [комментарий столбца](https://clickhouse.com/docs/ru/reference/statements/alter/column#comment-column).
- `codec_expression` — [кодек](https://clickhouse.com/docs/ru/reference/statements/create/table#column_compression_codec), применяемый к столбцу.
- `ttl_expression` — выражение [TTL](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/mergetree#table_engine-mergetree-ttl).
- `is_subcolumn` — флаг, равный `1` для внутренних подстолбцов. Он включается в результат только если описание подстолбцов включено параметром [describe_include_subcolumns](https://clickhouse.com/docs/ru/reference/settings/session-settings#describe_include_subcolumns).

```
CREATE TABLE describe_example (
    id UInt64, text String DEFAULT 'unknown' CODEC(ZSTD),
    user Tuple (name String, age UInt8)
) ENGINE = MergeTree() ORDER BY id;

DESCRIBE TABLE describe_example;
DESCRIBE TABLE describe_example SETTINGS describe_include_subcolumns=1;

```


```
┌─name─┬─type──────────────────────────┬─default_type─┬─default_expression─┬─comment─┬─codec_expression─┬─ttl_expression─┐
│ id   │ UInt64                        │              │                    │         │                  │                │
│ text │ String                        │ DEFAULT      │ 'unknown'          │         │ ZSTD(1)          │                │
│ user │ Tuple(name String, age UInt8) │              │                    │         │                  │                │
└──────┴───────────────────────────────┴──────────────┴────────────────────┴─────────┴──────────────────┴────────────────┘

```


```
┌─name──────┬─type──────────────────────────┬─default_type─┬─default_expression─┬─comment─┬─codec_expression─┬─ttl_expression─┬─is_subcolumn─┐
│ id        │ UInt64                        │              │                    │         │                  │                │            0 │
│ text      │ String                        │ DEFAULT      │ 'unknown'          │         │ ZSTD(1)          │                │            0 │
│ user      │ Tuple(name String, age UInt8) │              │                    │         │                  │                │            0 │
│ user.name │ String                        │              │                    │         │                  │                │            1 │
│ user.age  │ UInt8                         │              │                    │         │                  │                │            1 │
└───────────┴───────────────────────────────┴──────────────┴────────────────────┴─────────┴──────────────────┴────────────────┴──────────────┘

```


```
DESCRIBE SELECT 1 FORMAT TSV;

```


```
DESCRIBE (SELECT 1) FORMAT TSV;

```


```
1       UInt8

```

- настройка [describe_include_subcolumns](https://clickhouse.com/docs/ru/reference/settings/session-settings#describe_include_subcolumns).
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
