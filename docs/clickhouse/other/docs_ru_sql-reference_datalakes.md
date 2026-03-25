# Озера данных | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/sql-reference/datalakes

В этом разделе мы рассмотрим поддержку озер данных в ClickHouse.
ClickHouse поддерживает многие из самых популярных форматов таблиц и каталогов данных, включая Iceberg, Delta Lake, Hudi, AWS Glue, REST Catalog, Unity Catalog и Microsoft OneLake.


## Iceberg​

См. функциюiceberg, которая поддерживает чтение из Amazon S3 и S3-совместимых сервисов, HDFS, Azure и локальных файловых систем.icebergCluster— это распределённый вариант функцииiceberg.


## Delta Lake​

См. описание функцииdeltaLake, поддерживающей чтение из Amazon S3 и S3‑совместимых сервисов, Azure и локальных файловых систем.deltaLakeCluster— это распределённый вариант функцииdeltaLake.


## Hudi​

См.hudi, которая поддерживает чтение из Amazon S3 и S3-совместимых сервисов.hudiCluster— это распределённый вариант функцииhudi.


# Каталоги данных


## AWS Glue​

AWS Glue Data Catalog можно использовать с таблицами Iceberg. Вы можете использовать его с движком таблицыicebergили с движком базы данныхDataLakeCatalog.


## Iceberg REST Catalog​

REST-каталог Iceberg можно использовать с таблицами Iceberg. Вы можете использовать его с табличным движкомicebergили с движком базы данныхDataLakeCatalog.


## Unity Catalog​

Unity Catalog можно использовать как с таблицами Delta Lake, так и с таблицами Iceberg. Вы можете использовать его с движками таблицicebergилиdeltaLake, а также с движком базы данныхDataLakeCatalog.


## Microsoft OneLake​

Microsoft OneLake совместим как с таблицами Delta Lake, так и с таблицами Iceberg. Его можно использовать с движком базы данныхDataLakeCatalog.
