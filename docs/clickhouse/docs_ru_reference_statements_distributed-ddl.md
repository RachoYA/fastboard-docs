# Запросы Distributed DDL (предложение ON CLUSTER) - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/statements/distributed-ddl


```
CREATE TABLE IF NOT EXISTS all_hits ON CLUSTER cluster (p Date, i Int32) ENGINE = Distributed(cluster, default, hits)

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
