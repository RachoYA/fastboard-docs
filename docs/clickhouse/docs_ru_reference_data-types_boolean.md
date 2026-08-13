# Bool - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/data-types/boolean


```
SELECT true AS col, toTypeName(col);
┌─col──┬─toTypeName(true)─┐
│ true │ Bool             │
└──────┴──────────────────┘

select true == 1 as col, toTypeName(col);
┌─col─┬─toTypeName(equals(true, 1))─┐
│   1 │ UInt8                       │
└─────┴─────────────────────────────┘

```


```
CREATE TABLE test_bool
(
    `A` Int64,
    `B` Bool
)
ENGINE = Memory;

INSERT INTO test_bool VALUES (1, true),(2,0);

SELECT * FROM test_bool;
┌─A─┬─B─────┐
│ 1 │ true  │
│ 2 │ false │
└───┴───────┘

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
