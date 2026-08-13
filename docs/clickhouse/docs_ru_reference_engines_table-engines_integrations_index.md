# Движки таблиц для интеграций - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/index


| Страница | Описание |
| --- | --- |
| [Движок таблицы AzureBlobStorage](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/azureBlobStorage) | Этот движок обеспечивает интеграцию с экосистемой Azure Blob Storage. |
| [Движок таблицы DeltaLake](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/deltalake) | Этот движок обеспечивает интеграцию с существующими таблицами Delta Lake в Amazon S3 в режиме только для чтения. |
| [Движок таблицы EmbeddedRocksDB](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/embedded-rocksdb) | Этот движок позволяет интегрировать ClickHouse с RocksDB. |
| [Движок таблицы ExternalDistributed](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/ExternalDistributed) | Движок `ExternalDistributed` позволяет выполнять запросы `SELECT` к данным, хранящимся на удалённых серверах MySQL или PostgreSQL. В качестве аргумента принимает движки MySQL или PostgreSQL, что делает возможным сегментирование данных. |
| [Движок таблицы TimeSeries](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/time-series) | Движок таблицы для хранения временных рядов, то есть набора значений, связанных с временными метками и тегами (или метками). |
| [Движок таблицы HDFS](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/hdfs) | Этот движок обеспечивает интеграцию с экосистемой Apache Hadoop, позволяя управлять данными в HDFS через ClickHouse. Он похож на движки File и URL, но предоставляет возможности, специфичные для Hadoop. |
| [Движок таблицы Hive](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/hive) | Движок Hive позволяет выполнять запросы `SELECT` к Hive-таблице в HDFS. |
| [Движок таблицы Hudi](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/hudi) | Этот движок обеспечивает доступ только для чтения к существующим таблицам Apache Hudi в Amazon S3. |
| [Движок таблицы Iceberg](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/iceberg) | Этот движок обеспечивает доступ только для чтения к существующим таблицам Apache Iceberg в Amazon S3, Azure, HDFS и к локально хранимым таблицам. |
| [Движок таблицы Paimon](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/paimon) | Этот движок обеспечивает доступ только для чтения к существующим таблицам Apache Paimon в Amazon S3, Azure, HDFS, а также к таблицам, хранящимся локально. |
| [Движок таблицы JDBC](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/jdbc) | Позволяет ClickHouse подключаться к внешним базам данных по JDBC. |
| [Движок таблицы Kafka](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/kafka) | Движок таблицы Kafka предназначен для работы с Apache Kafka; он позволяет публиковать данные и подписываться на потоки данных, организовывать отказоустойчивое хранение и обрабатывать потоки по мере их поступления. |
| [Движок таблицы MaterializedPostgreSQL](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/materialized-postgresql) | Создаёт таблицу ClickHouse с начальной выгрузкой данных из таблицы PostgreSQL и запускает процесс репликации. |
| [Движок таблицы MongoDB](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/mongodb) | Движок MongoDB — это движок таблицы только для чтения, который позволяет читать данные из удалённой коллекции. |
| [Документация по движку таблицы MySQL](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/mysql) | Документация по движку таблицы MySQL |
| [Движок таблицы NATS](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/nats) | Этот движок позволяет интегрировать ClickHouse с NATS, публиковать сообщения в subject’ы или подписываться на них, а также обрабатывать новые сообщения по мере их поступления. |
| [Движок таблицы ODBC](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/odbc) | Позволяет ClickHouse подключаться к внешним базам данных по ODBC. |
| [Движок таблицы PostgreSQL](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/postgresql) | Движок PostgreSQL позволяет выполнять запросы `SELECT` и `INSERT` к данным, которые хранятся на удалённом сервере PostgreSQL. |
| [Движок таблицы RabbitMQ](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/rabbitmq) | Этот движок позволяет интегрировать ClickHouse с RabbitMQ. |
| [Движок таблицы Redis](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/redis) | Этот движок позволяет интегрировать ClickHouse с Redis. |
| [Движок таблицы S3](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/s3) | Этот движок обеспечивает интеграцию с экосистемой Amazon S3. Он похож на HDFS engine, но предоставляет специфичные для S3 возможности. |
| [Движок таблицы S3Queue](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/s3queue) | Этот движок обеспечивает интеграцию с экосистемой Amazon S3 и поддерживает потоковый импорт. Аналогичен движкам Kafka и RabbitMQ, но предоставляет возможности, специфичные для S3. |
| [Движок таблицы AzureQueue](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/azure-queue) | Этот движок интегрирован с экосистемой Azure Blob Storage и позволяет выполнять потоковый импорт данных. |
| [Движок таблицы YTsaurus](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/ytsaurus) | Движок таблицы, который позволяет импортировать данные из кластера YTsaurus. |
| [Движок таблицы SQLite](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/sqlite) | Движок позволяет импортировать и экспортировать данные в SQLite, а также выполнять запросы к таблицам SQLite напрямую из ClickHouse. |
| [Движок таблицы ArrowFlight](https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/arrowflight) | Движок позволяет выполнять запросы к удалённым наборам данных и вставку данных в них через Apache Arrow Flight. |

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
