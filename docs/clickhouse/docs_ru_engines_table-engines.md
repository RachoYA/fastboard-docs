# Движки таблиц - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/engines/table-engines

- Как и где хранятся данные, куда они записываются и откуда читаются.
- Какие запросы поддерживаются и каким образом.
- Параллельный доступ к данным.
- Использование индексов, если они есть.
- Возможно ли многопоточное выполнение запросов.
- Параметры репликации данных.

## Семейства движков


### MergeTree


| Движки MergeTree |
| --- |
| [Обзор семейства MergeTree](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/index) |
| [MergeTree](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/mergetree) |
| [ReplacingMergeTree](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/replacingmergetree) |
| [SummingMergeTree](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/summingmergetree) |
| [AggregatingMergeTree](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/aggregatingmergetree) |
| [CollapsingMergeTree](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/collapsingmergetree) |
| [VersionedCollapsingMergeTree](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/versionedcollapsingmergetree) |
| [GraphiteMergeTree](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/graphitemergetree) |
| [CoalescingMergeTree](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/coalescingmergetree) |
| [Точный и приблизительный векторный поиск](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/annindexes) |
| [Пользовательский ключ партиционирования](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/custom-partitioning-key) |
| [Движки таблиц Replicated*](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/replication) |
| [Полнотекстовый поиск с текстовыми индексами](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/textindexes) |


### Log


| Движки семейства Log |
| --- |
| [Семейство движков Log](https://clickhouse.com/docs/ru/reference/engines/table-engines/log-family/index) |
| [TinyLog](https://clickhouse.com/docs/ru/reference/engines/table-engines/log-family/tinylog) |
| [StripeLog](https://clickhouse.com/docs/ru/reference/engines/table-engines/log-family/stripelog) |
| [Log](https://clickhouse.com/docs/ru/reference/engines/table-engines/log-family/log) |


### Интеграционные движки


| Интеграционные движки |
| --- |
| [Движки таблиц для интеграций](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/index) |
| [ODBC](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/odbc) |
| [JDBC](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/jdbc) |
| [MySQL](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/mysql) |
| [MongoDB](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/mongodb) |
| [Redis](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/redis) |
| [HDFS](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/hdfs) |
| [S3](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/s3) |
| [Kafka](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/kafka) |
| [EmbeddedRocksDB](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/embedded-rocksdb) |
| [RabbitMQ](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/rabbitmq) |
| [PostgreSQL](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/postgresql) |
| [S3Queue](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/s3queue) |
| [TimeSeries](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/time-series) |
| [ArrowFlight](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/arrowflight) |
| [AzureQueue](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/azure-queue) |
| [AzureBlobStorage](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/azureBlobStorage) |
| [DeltaLake](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/deltalake) |
| [ExternalDistributed](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/ExternalDistributed) |
| [Hive](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/hive) |
| [Hudi](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/hudi) |
| [Iceberg](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/iceberg) |
| [MaterializedPostgreSQL](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/materialized-postgresql) |
| [NATS](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/nats) |
| [Paimon](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/paimon) |
| [SQLite](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/sqlite) |
| [YTsaurus](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/ytsaurus) |


### Специальные движки


| Специальные движки |
| --- |
| [Специальные движки таблиц](https://clickhouse.com/docs/ru/reference/engines/table-engines/special/index) |
| [Псевдоним](https://clickhouse.com/docs/ru/reference/engines/table-engines/special/alias) |
| [Distributed](https://clickhouse.com/docs/ru/reference/engines/table-engines/special/distributed) |
| [Словарь](https://clickhouse.com/docs/ru/reference/engines/table-engines/special/dictionary) |
| [Merge](https://clickhouse.com/docs/ru/reference/engines/table-engines/special/merge) |
| [Executable](https://clickhouse.com/docs/ru/reference/engines/table-engines/special/executable) |
| [File](https://clickhouse.com/docs/ru/reference/engines/table-engines/special/file) |
| [Null](https://clickhouse.com/docs/ru/reference/engines/table-engines/special/null) |
| [Set](https://clickhouse.com/docs/ru/reference/engines/table-engines/special/set) |
| [JOIN](https://clickhouse.com/docs/ru/reference/engines/table-engines/special/join) |
| [URL](https://clickhouse.com/docs/ru/reference/engines/table-engines/special/url) |
| [View](https://clickhouse.com/docs/ru/reference/engines/table-engines/special/view) |
| [Memory](https://clickhouse.com/docs/ru/reference/engines/table-engines/special/memory) |
| [Buffer](https://clickhouse.com/docs/ru/reference/engines/table-engines/special/buffer) |
| [Внешние данные](https://clickhouse.com/docs/ru/reference/engines/table-engines/special/external-data) |
| [GenerateRandom](https://clickhouse.com/docs/ru/reference/engines/table-engines/special/generate) |
| [KeeperMap](https://clickhouse.com/docs/ru/reference/engines/table-engines/special/keepermap) |
| [FileLog](https://clickhouse.com/docs/ru/reference/engines/table-engines/special/filelog) |


## Виртуальные столбцы

- `_table` — содержит имя таблицы, из которой были прочитаны данные. Тип: [String](https://clickhouse.com/docs/ru/reference/data-types/string). Независимо от используемого движка таблицы, каждая таблица включает универсальный виртуальный столбец с именем `_table`. При выполнении запроса к таблице с движком Merge можно задать константные условия для `_table` в выражении `WHERE/PREWHERE` (например, `WHERE _table='xyz'`). В этом случае чтение выполняется только для тех таблиц, которые удовлетворяют условию по `_table`, поэтому столбец `_table` действует как индекс. При использовании запросов вида `SELECT ... FROM (... UNION ALL ...)` можно определить, из какой именно таблицы происходят возвращаемые строки, указав столбец `_table`.
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
