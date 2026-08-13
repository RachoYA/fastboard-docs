# Системные таблицы - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/system-tables


| Страница | Описание |
| --- | --- |
| [system.constraints](https://clickhouse.com/docs/ru/reference/system-tables/constraints) | System table containing information about existing constraints in all tables. |
| [System Tables Overview](https://clickhouse.com/docs/ru/reference/system-tables/overview) | Overview of what system tables are and why they are useful. |
| [system.hypothetical_indexes](https://clickhouse.com/docs/ru/reference/system-tables/hypothetical_indexes) | System table listing hypothetical (what-if) indexes defined in the current session |
| [system.stemmers](https://clickhouse.com/docs/ru/reference/system-tables/stemmers) | System table which shows all available stemmers. |
| [INFORMATION_SCHEMA](https://clickhouse.com/docs/ru/reference/system-tables/information_schema) | System database providing an almost standardized DBMS-agnostic view on metadata of database objects. |
| [system.aggregate_function_combinators](https://clickhouse.com/docs/ru/reference/system-tables/aggregate_function_combinators) | Contains a list of all available aggregate function combinators, which could be applied to aggregate functions and change the way they work. |
| [system.aggregated_zookeeper_log](https://clickhouse.com/docs/ru/reference/system-tables/aggregated_zookeeper_log) | System table containing aggregated statistics of ZooKeeper operations grouped by session, path, operation type, component, and subrequest flag. |
| [system.asynchronous_insert_log](https://clickhouse.com/docs/ru/reference/system-tables/asynchronous_insert_log) | System table containing information about async inserts. Each entry represents an insert query buffered into an async insert query. |
| [system.asynchronous_loader](https://clickhouse.com/docs/ru/reference/system-tables/asynchronous_loader) | System table containing information about and status of recent asynchronous jobs (e.g. for tables which are loading). The table contains a row for every job. |
| [system.asynchronous_metric_log](https://clickhouse.com/docs/ru/reference/system-tables/asynchronous_metric_log) | System table containing historical values for `system.asynchronous_metrics`, which are saved once per time interval (one second by default) |
| [system.asynchronous_inserts](https://clickhouse.com/docs/ru/reference/system-tables/asynchronous_inserts) | System table containing information about pending asynchronous inserts in queue. |
| [system.asynchronous_metrics](https://clickhouse.com/docs/ru/reference/system-tables/asynchronous_metrics) | System table containing metrics that are calculated periodically in the background. For example, the amount of RAM in use. |
| [system.azure_queue_settings](https://clickhouse.com/docs/ru/reference/system-tables/azure_queue_settings) | System table containing information about settings of AzureQueue tables. Available from server version `24.10`. |
| [system.azure_queue_metadata_cache](https://clickhouse.com/docs/ru/reference/system-tables/azure_queue_metadata_cache) | Contains in-memory state of AzureQueue metadata and currently processed rows per file. |
| [system.azure_queue_log](https://clickhouse.com/docs/ru/reference/system-tables/azure_queue_log) | Contains log entries with information about files processed by the AzureQueue engine. |
| It is safe to truncate or drop this table at any time. |  |
| [system.background_schedule_pool_log](https://clickhouse.com/docs/ru/reference/system-tables/background_schedule_pool_log) | System table containing history of background schedule pool task executions. |
| [system.background_schedule_pool](https://clickhouse.com/docs/ru/reference/system-tables/background_schedule_pool) | System table containing information about tasks in background schedule pools. |
| [system.backup_log](https://clickhouse.com/docs/ru/reference/system-tables/backup_log) | System table containing logging entries with information about `BACKUP` and `RESTORE` operations. |
| [system.backups](https://clickhouse.com/docs/ru/reference/system-tables/backups) | System table containing logging entries with information about `BACKUP` and `RESTORE` operations. |
| [system.blob_storage_log](https://clickhouse.com/docs/ru/reference/system-tables/blob_storage_log) | System table containing logging entries with information about various blob storage operations such as uploads and deletes. |
| [system.build_options](https://clickhouse.com/docs/ru/reference/system-tables/build_options) | System table containing information about ClickHouse server’s build options. |
| [system.certificates](https://clickhouse.com/docs/ru/reference/system-tables/certificates) | Contains information about available certificates and their sources. |
| [system.clusters](https://clickhouse.com/docs/ru/reference/system-tables/clusters) | System table containing information about clusters available in the config file and the servers defined in them. |
| [system.codecs](https://clickhouse.com/docs/ru/reference/system-tables/codecs) | System table containing information about codecs in queue. |
| [system.collations](https://clickhouse.com/docs/ru/reference/system-tables/collations) | Contains a list of all available collations for alphabetical comparison of strings. |
| [system.columns](https://clickhouse.com/docs/ru/reference/system-tables/columns) | System table containing information about columns in all tables |
| [system.completions](https://clickhouse.com/docs/ru/reference/system-tables/completions) | Contains a list of completion tokens. |
| [system.contributors](https://clickhouse.com/docs/ru/reference/system-tables/contributors) | System table containing information about contributors. |
| [system.crash_log](https://clickhouse.com/docs/ru/reference/system-tables/crash_log) | System table containing information about stack traces for fatal errors. |
| [system.current_roles](https://clickhouse.com/docs/ru/reference/system-tables/current_roles) | System table containing active roles for the current user. |
| [system.dashboards](https://clickhouse.com/docs/ru/reference/system-tables/dashboards) | Contains queries used by `/dashboard` page accessible though the HTTP interface. useful for monitoring and troubleshooting. |
| [system.data_skipping_indices](https://clickhouse.com/docs/ru/reference/system-tables/data_skipping_indices) | System table containing information about existing data skipping indices in all the tables. |
| [system.data_skipping_index_types](https://clickhouse.com/docs/ru/reference/system-tables/data_skipping_index_types) | System table containing a list of data skipping index types supported by the server along with their embedded documentation. |
| [system.data_type_families](https://clickhouse.com/docs/ru/reference/system-tables/data_type_families) | System table containing information about supported data types |
| [system.database_engines](https://clickhouse.com/docs/ru/reference/system-tables/database_engines) | System table containing a list of database engines supported by the server. |
| [system.database_replicas](https://clickhouse.com/docs/ru/reference/system-tables/database_replicas) | System table containing information about and status of replicated database. |
| [system.databases](https://clickhouse.com/docs/ru/reference/system-tables/databases) | System table containing information about the databases that are available to the current user. |
| [system.dead_letter_queue](https://clickhouse.com/docs/ru/reference/system-tables/dead_letter_queue) | System table containing information about messages received via a streaming engine and parsed with errors. |
| [system.delta_lake_metadata_log](https://clickhouse.com/docs/ru/reference/system-tables/delta_metadata_log) | System table containing information about metadata files read from Delta Lake tables. Each entry represents a root metadata JSON file. |
| [system.detached_parts](https://clickhouse.com/docs/ru/reference/system-tables/detached_parts) | System table containing information about detached parts of MergeTree tables |
| [system.detached_tables](https://clickhouse.com/docs/ru/reference/system-tables/detached_tables) | System table containing information about each detached table. |
| [system.dictionaries](https://clickhouse.com/docs/ru/reference/system-tables/dictionaries) | System table containing information about dictionaries |
| [system.dictionary_sources](https://clickhouse.com/docs/ru/reference/system-tables/dictionary_sources) | System table containing a list of dictionary sources supported by the server along with their embedded documentation. |
| [system.dictionary_layouts](https://clickhouse.com/docs/ru/reference/system-tables/dictionary_layouts) | System table containing a list of dictionary layouts supported by the server along with their embedded documentation. |
| [system.dimensional_metrics](https://clickhouse.com/docs/ru/reference/system-tables/dimensional_metrics) | This table contains dimensional metrics that can be calculated instantly and exported in the Prometheus format. It is always up to date. |
| [system.disk_types](https://clickhouse.com/docs/ru/reference/system-tables/disk_types) | System table containing a list of disk types supported by the server along with their embedded documentation. |
| [system.disks](https://clickhouse.com/docs/ru/reference/system-tables/disks) | System table containing information about disks defined in the server configuration |
| [system.distributed_ddl_queue](https://clickhouse.com/docs/ru/reference/system-tables/distributed_ddl_queue) | System table containing information about distributed ddl queries (queries using the ON CLUSTER clause) that were executed on a cluster. |
| [system.distribution_queue](https://clickhouse.com/docs/ru/reference/system-tables/distribution_queue) | System table containing information about local files that are in the queue to be sent to the shards. |
| [system.dns_cache](https://clickhouse.com/docs/ru/reference/system-tables/dns_cache) | System table containing information about cached DNS records. |
| [system.documentation](https://clickhouse.com/docs/ru/reference/system-tables/documentation) | System table that collects the embedded documentation of the uniform components of the system (functions, table engines, data types, and so on) into a single table, with the reference documentation rendered as Markdown. |
| [system.dropped_tables](https://clickhouse.com/docs/ru/reference/system-tables/dropped_tables) | System table containing information about tables that drop table has been executed on but for which data cleanup has not yet been performed |
| [system.dropped_tables_parts](https://clickhouse.com/docs/ru/reference/system-tables/dropped_tables_parts) | System table containing information about parts of MergeTree dropped tables from `system.dropped_tables` |
| [system.enabled_roles](https://clickhouse.com/docs/ru/reference/system-tables/enabled_roles) | System table containing all active roles at the moment, including the current role of the current user and the granted roles for the current role |
| [system.error_log](https://clickhouse.com/docs/ru/reference/system-tables/error_log) | System table containing the history of error values from table `system.errors`, periodically flushed to disk. |
| [system.errors](https://clickhouse.com/docs/ru/reference/system-tables/errors) | System table containing error codes with the number of times they have been triggered. |
| [system.events](https://clickhouse.com/docs/ru/reference/system-tables/events) | System table containing information about the number of events that have occurred in the system. |
| [system.fail_points](https://clickhouse.com/docs/ru/reference/system-tables/fail_points) | Contains a list of all available failpoints with their type and current status. |
| [system.filesystem_cache_settings](https://clickhouse.com/docs/ru/reference/system-tables/filesystem_cache_settings) | Contains information about all filesystem cache settings |
| [system.filesystem_read_prefetches_log](https://clickhouse.com/docs/ru/reference/system-tables/filesystem_read_prefetches_log) | Contains a history of all prefetches done during reading from MergeTree tables backed by a remote filesystem. |
| It is safe to truncate or drop this table at any time. |  |
| [system.filesystem_cache_log](https://clickhouse.com/docs/ru/reference/system-tables/filesystem_cache_log) | Contains a history of all events occurred with filesystem cache for objects on a remote filesystem. |
| It is safe to truncate or drop this table at any time. |  |
| [system.filesystem_cache](https://clickhouse.com/docs/ru/reference/system-tables/filesystem_cache) | Contains information about all entries inside filesystem cache for remote objects. |
| [system.formats](https://clickhouse.com/docs/ru/reference/system-tables/formats) | Contains a list of all the formats along with flags whether a format is suitable for input/output or whether it supports parallelization. |
| [system.functions](https://clickhouse.com/docs/ru/reference/system-tables/functions) | System table containing information about normal and aggregate functions. |
| [system.grants](https://clickhouse.com/docs/ru/reference/system-tables/grants) | System table showing which privileges are granted to ClickHouse user accounts. |
| [system.graphite_retentions](https://clickhouse.com/docs/ru/reference/system-tables/graphite_retentions) | System table containing information about parameters `graphite_rollup` which are used in tables with `GraphiteMergeTree` type engines. |
| [system.histogram_metrics](https://clickhouse.com/docs/ru/reference/system-tables/histogram_metrics) | This table contains histogram metrics that can be calculated instantly and exported in the Prometheus format. It is always up to date. |
| [system.iceberg_history](https://clickhouse.com/docs/ru/reference/system-tables/iceberg_history) | System iceberg snapshot history |
| [system.iceberg_files](https://clickhouse.com/docs/ru/reference/system-tables/iceberg_files) | System table containing per-file metadata of Iceberg tables |
| [system.iceberg_metadata_log](https://clickhouse.com/docs/ru/reference/system-tables/iceberg_metadata_log) | System table containing information about metadata files read from Iceberg tables. Each entry represents either a root metadata file, metadata extracted from an Avro file, or an entry of some Avro file. |
| [system.instrumentation](https://clickhouse.com/docs/ru/reference/system-tables/instrumentation) | System table containing the instrumentation points |
| [system.jemalloc_stats](https://clickhouse.com/docs/ru/reference/system-tables/jemalloc_stats) | Returns jemalloc statistics in a single row with a single column. Equivalent to SYSTEM JEMALLOC STATS command. |
| [system.jemalloc_bins](https://clickhouse.com/docs/ru/reference/system-tables/jemalloc_bins) | System table containing information about memory allocations done via jemalloc allocator in different size classes (bins) aggregated from all arenas. |
| [system.jemalloc_profile_text](https://clickhouse.com/docs/ru/reference/system-tables/jemalloc_profile_text) | Displays the symbolized jemalloc heap profile. Run ‘SYSTEM JEMALLOC FLUSH PROFILE’ to generate a profile first. |
| [system.kafka_consumers](https://clickhouse.com/docs/ru/reference/system-tables/kafka_consumers) | System table containing information about Kafka consumers. |
| [system.keeper_cluster](https://clickhouse.com/docs/ru/reference/system-tables/keeper_cluster) | System table which exists only when this node runs an in-process ClickHouse Keeper. Contains one row per Raft cluster member as seen by this Keeper. |
| [system.keeper_snapshots](https://clickhouse.com/docs/ru/reference/system-tables/keeper_snapshots) | System table which exists only when this node runs an in-process ClickHouse Keeper. Contains one row per on-disk Raft snapshot tracked by the Keeper state machine. |
| [system.keeper_changelogs](https://clickhouse.com/docs/ru/reference/system-tables/keeper_changelogs) | System table which exists only when this node runs an in-process ClickHouse Keeper. Contains one row per on-disk Raft changelog file tracked by the Keeper log store. |
| [system.keywords](https://clickhouse.com/docs/ru/reference/system-tables/keywords) | Contains a list of all keywords used in ClickHouse parser. |
| [system.licenses](https://clickhouse.com/docs/ru/reference/system-tables/licenses) | System table containing licenses of third-party libraries that are located in the contrib directory of ClickHouse sources. |
| [system.macros](https://clickhouse.com/docs/ru/reference/system-tables/macros) | Contains a list of all macros defined in server configuration. |
| [system.masking_policies](https://clickhouse.com/docs/ru/reference/system-tables/masking_policies) | System table containing information about all masking policies in the system. |
| [system.merge_tree_settings](https://clickhouse.com/docs/ru/reference/system-tables/merge_tree_settings) | System table containing information about settings for MergeTree tables. |
| [system.merges](https://clickhouse.com/docs/ru/reference/system-tables/merges) | System table containing information about merges and part mutations currently in process for tables in the MergeTree family. |
| [system.metric_log](https://clickhouse.com/docs/ru/reference/system-tables/metric_log) | System table containing history of metrics values from tables `system.metrics` and `system.events`, periodically flushed to disk. |
| [system.metrics](https://clickhouse.com/docs/ru/reference/system-tables/metrics) | System table containing metrics which can be calculated instantly, or have a current value. |
| [system.models](https://clickhouse.com/docs/ru/reference/system-tables/models) | Contains a list of CatBoost models loaded into a LibraryBridge’s memory along with time when it was loaded. |
| [system.moves](https://clickhouse.com/docs/ru/reference/system-tables/moves) | System table containing information about in-progress data part moves of MergeTree tables. Each data part movement is represented by a single row. |
| [system.mutations](https://clickhouse.com/docs/ru/reference/system-tables/mutations) | System table containing information about mutations of MergeTree tables and their progress. Each mutation command is represented by a single row. |
| [system.named_collections](https://clickhouse.com/docs/ru/reference/system-tables/named_collections) | Содержит список всех именованных коллекций, созданных с помощью SQL-запроса или разобранных из файла конфигурации. |
| [system.numbers_mt](https://clickhouse.com/docs/ru/reference/system-tables/numbers_mt) | Системная таблица, аналогичная `system.numbers`, но чтение в ней распараллелено, и числа могут возвращаться в любом порядке. |
| [system.numbers](https://clickhouse.com/docs/ru/reference/system-tables/numbers) | Системная таблица, содержащая один столбец UInt64 с именем `number`, в котором содержатся почти все натуральные числа, начиная с нуля. |
| [system.one](https://clickhouse.com/docs/ru/reference/system-tables/one) | Системная таблица, содержащая одну строку с одним столбцом UInt8 `dummy`, содержащим значение 0. Аналогична таблице `DUAL`, встречающейся в других СУБД. |
| [system.opentelemetry_span_log](https://clickhouse.com/docs/ru/reference/system-tables/opentelemetry_span_log) | Системная таблица, содержащая информацию о спанах трассировки для выполненных запросов. |
| [system.part_moves_between_shards](https://clickhouse.com/docs/ru/reference/system-tables/part_moves_between_shards) | Содержит информацию о частях, которые в данный момент перемещаются между сегментами, и о ходе этого процесса. |
| [system.part_log](https://clickhouse.com/docs/ru/reference/system-tables/part_log) | Системная таблица, содержащая информацию о событиях, произошедших с частями данных в таблицах семейства MergeTree, таких как добавление данных или слияние. |
| [system.parts](https://clickhouse.com/docs/ru/reference/system-tables/parts) | Системная таблица, содержащая информацию о частях таблиц MergeTree |
| [system.parts_columns](https://clickhouse.com/docs/ru/reference/system-tables/parts_columns) | Системная таблица, содержащая информацию о частях и столбцах таблиц MergeTree. |
| [system.predicate_statistics_log](https://clickhouse.com/docs/ru/reference/system-tables/predicate_statistics_log) | Системная таблица, содержащая выборочную статистику селективности фильтров и индексов, собранную из конвейеров чтения `MergeTree` во время выполнения запросов. |
| [system.primes](https://clickhouse.com/docs/ru/reference/system-tables/primes) | Системная таблица, содержащая единственный столбец UInt64 с именем `prime`, в котором хранятся простые числа в порядке возрастания, начиная с 2. |
| [system.privileges](https://clickhouse.com/docs/ru/reference/system-tables/privileges) | Содержит список всех доступных привилегий, которые могут быть предоставлены пользователю или роли. |
| [system.processes](https://clickhouse.com/docs/ru/reference/system-tables/processes) | Системная таблица, используемая для реализации запроса `SHOW PROCESSLIST`. |
| [system.processors_profile_log](https://clickhouse.com/docs/ru/reference/system-tables/processors_profile_log) | Системная таблица, содержащая информацию профилирования на уровне processors (её можно найти в `EXPLAIN PIPELINE`) |
| [system.projection_parts_columns](https://clickhouse.com/docs/ru/reference/system-tables/projection_parts_columns) | Системная таблица, содержащая информацию о столбцах в частях проекций для таблиц семейства MergeTree |
| [system.projection_parts](https://clickhouse.com/docs/ru/reference/system-tables/projection_parts) | Системная таблица, содержащая информацию о частях проекций для таблиц семейства MergeTree. |
| [system.projections](https://clickhouse.com/docs/ru/reference/system-tables/projections) | Системная таблица, содержащая информацию о существующих проекциях во всех таблицах. |
| [system.query_views_log](https://clickhouse.com/docs/ru/reference/system-tables/query_views_log) | Системная таблица, содержащая информацию о зависимых представлениях, выполняемых при запуске запроса, например об их типе или времени выполнения. |
| [system.query_condition_cache](https://clickhouse.com/docs/ru/reference/system-tables/query_condition_cache) | Системная таблица, показывающая содержимое кэша условий запроса. |
| [system.query_thread_log](https://clickhouse.com/docs/ru/reference/system-tables/query_thread_log) | Системная таблица, содержащая информацию о потоках, выполняющих запросы, например имя потока, время его запуска и длительность обработки запроса. |
| [system.query_metric_log](https://clickhouse.com/docs/ru/reference/system-tables/query_metric_log) | Системная таблица, содержащая историю значений памяти и метрик из таблицы `system.events` для отдельных запросов, периодически сбрасываемую на диск. |
| [system.query_log](https://clickhouse.com/docs/ru/reference/system-tables/query_log) | Системная таблица, содержащая информацию о выполненных запросах, например время начала, длительность обработки и сообщения об ошибках. |
| [system.query_cache](https://clickhouse.com/docs/ru/reference/system-tables/query_cache) | Системная таблица, показывающая содержимое кэша запросов. |
| [system.quota_usage](https://clickhouse.com/docs/ru/reference/system-tables/quota_usage) | Системная таблица, содержащая информацию об использовании квот текущим пользователем, например какая часть квоты использована и сколько осталось. |
| [system.quota_limits](https://clickhouse.com/docs/ru/reference/system-tables/quota_limits) | Системная таблица, содержащая информацию о максимумах для всех интервалов всех квот. Одной квоте может соответствовать любое количество строк или ни одной. |
| [system.quotas_usage](https://clickhouse.com/docs/ru/reference/system-tables/quotas_usage) | Системная таблица, содержащая информацию об использовании квот всеми пользователями. |
| [system.quotas](https://clickhouse.com/docs/ru/reference/system-tables/quotas) | Системная таблица, содержащая информацию о квотах. |
| [system.remote_data_paths](https://clickhouse.com/docs/ru/reference/system-tables/remote_data_paths) | Системная таблица, содержащая информацию о файлах данных, хранящихся на удалённых дисках, таких как S3 или Azure Blob Storage. |
| [system.replicas](https://clickhouse.com/docs/ru/reference/system-tables/replicas) | System table containing information about and status of replicated tables residing on the local server. Useful for monitoring. |
| [system.replicated_merge_tree_settings](https://clickhouse.com/docs/ru/reference/system-tables/replicated_merge_tree_settings) | Contains a list of all ReplicatedMergeTree engine specific settings, their current and default values along with descriptions. You may change any of them in SETTINGS section in CREATE query. |
| [system.replicated_fetches](https://clickhouse.com/docs/ru/reference/system-tables/replicated_fetches) | System table containing information about currently running background fetches. |
| [system.replication_queue](https://clickhouse.com/docs/ru/reference/system-tables/replication_queue) | System table containing information about tasks from replication queues stored in ClickHouse Keeper, or ZooKeeper, for tables in the `ReplicatedMergeTree` family. |
| [system.resources](https://clickhouse.com/docs/ru/reference/system-tables/resources) | System table containing information about resources residing on the local server with one row for every resource. |
| [system.rocksdb](https://clickhouse.com/docs/ru/reference/system-tables/rocksdb) | Contains a list of metrics exposed from embedded RocksDB. |
| [system.role_grants](https://clickhouse.com/docs/ru/reference/system-tables/role_grants) | System table containing the role grants for users and roles. |
| [system.roles](https://clickhouse.com/docs/ru/reference/system-tables/roles) | System table containing information about configured roles. |
| [system.row_policies](https://clickhouse.com/docs/ru/reference/system-tables/row_policies) | System table containing filters for one particular table, as well as a list of roles and/or users which should use this row policy. |
| [system.s3_queue_settings](https://clickhouse.com/docs/ru/reference/system-tables/s3_queue_settings) | System table containing information about the settings of S3Queue tables. Available from server version `24.10`. |
| [system.s3queue_metadata_cache](https://clickhouse.com/docs/ru/reference/system-tables/s3queue_metadata_cache) | Contains in-memory state of S3Queue metadata and currently processed rows per file. |
| [system.s3queue_log](https://clickhouse.com/docs/ru/reference/system-tables/s3queue_log) | Contains log entries with information about files processed by the S3Queue engine. |
| It is safe to truncate or drop this table at any time. |  |
| [system.scheduler](https://clickhouse.com/docs/ru/reference/system-tables/scheduler) | System table containing information about and status of scheduling nodes residing on the local server. |
| [system.schema_inference_cache](https://clickhouse.com/docs/ru/reference/system-tables/schema_inference_cache) | System table containing information about all cached file schemas. |
| [system.server_settings](https://clickhouse.com/docs/ru/reference/system-tables/server_settings) | System table containing formation about global settings for the server, which are specified in `config.xml`. |
| [system.session_log](https://clickhouse.com/docs/ru/reference/system-tables/session_log) | System table containing information about all successful and failed login and logout events. |
| [system.settings](https://clickhouse.com/docs/ru/reference/system-tables/settings) | System table containing information about session settings for current user. |
| [system.settings_profile_elements](https://clickhouse.com/docs/ru/reference/system-tables/settings_profile_elements) | System table which describes the content of the settings profile: constraints, roles and users that the setting applies to, parent settings profiles. |
| [system.settings_changes](https://clickhouse.com/docs/ru/reference/system-tables/settings_changes) | System table containing information about setting changes in previous ClickHouse versions. |
| [system.settings_profiles](https://clickhouse.com/docs/ru/reference/system-tables/settings_profiles) | System table which contains properties of configured setting profiles. |
| [system.stack_trace](https://clickhouse.com/docs/ru/reference/system-tables/stack_trace) | System table which contains stack traces of all server threads. Allows developers to introspect the server state. |
| [system.storage_policies](https://clickhouse.com/docs/ru/reference/system-tables/storage_policies) | System table containing information about storage policies and volumes which are defined in server configuration. |
| [system.symbols](https://clickhouse.com/docs/ru/reference/system-tables/symbols) | System table useful for C++ experts and ClickHouse engineers containing information for introspection of the `clickhouse` binary. |
| [system.table_engines](https://clickhouse.com/docs/ru/reference/system-tables/table_engines) | System table containing descriptions of table engines supported by the server and the features they support. |
| [system.table_functions](https://clickhouse.com/docs/ru/reference/system-tables/table_functions) | Contains a list of all available table functions with their descriptions. |
| [system.tables](https://clickhouse.com/docs/ru/reference/system-tables/tables) | System table containing metadata of each table that the server knows about. |
| [system.text_log](https://clickhouse.com/docs/ru/reference/system-tables/text_log) | System table containing logging entries. |
| [system.time_zones](https://clickhouse.com/docs/ru/reference/system-tables/time_zones) | System table containing a list of time zones that are supported by the ClickHouse server. |
| [system.tokenizers](https://clickhouse.com/docs/ru/reference/system-tables/tokenizers) | System table which shows all available tokenizers. |
| [system.trace_log](https://clickhouse.com/docs/ru/reference/system-tables/trace_log) | System table containing stack traces collected by the sampling query profiler. |
| [system.transactions](https://clickhouse.com/docs/ru/reference/system-tables/transactions) | Contains a list of transactions and their state. |
| [system.transactions_info_log](https://clickhouse.com/docs/ru/reference/system-tables/transactions_info_log) | Contains information about all transactions executed on a current server. |
| It is safe to truncate or drop this table at any time. |  |
| [system.unicode](https://clickhouse.com/docs/ru/reference/system-tables/unicode) | System table containing a list of Unicode characters and their properties. |
| [system.user_processes](https://clickhouse.com/docs/ru/reference/system-tables/user_processes) | System table containing information useful for an overview of memory usage and ProfileEvents of users. |
| [system.user_directories](https://clickhouse.com/docs/ru/reference/system-tables/user_directories) | Contains the information about configured user directories - directories on the file system from which ClickHouse server is allowed to read user provided data. |
| [system.user_defined_functions](https://clickhouse.com/docs/ru/reference/system-tables/user_defined_functions) | System table containing loading status and configuration metadata for User-Defined Functions (UDFs). |
| [system.users](https://clickhouse.com/docs/ru/reference/system-tables/users) | System table containing a list of user accounts configured on the server. |
| [system.view_refreshes](https://clickhouse.com/docs/ru/reference/system-tables/view_refreshes) | System table containing information about Refreshable Materialized Views. |
| [system.warnings](https://clickhouse.com/docs/ru/reference/system-tables/system_warnings) | This table contains warning messages about clickhouse server. |
| [system.warnings](https://clickhouse.com/docs/ru/reference/system-tables/warnings) | Contains warnings about server configuration to be displayed by clickhouse-client right after it connects to the server. |
| [system.workloads](https://clickhouse.com/docs/ru/reference/system-tables/workloads) | System table containing information for workloads residing on the local server. |
| [system.zeros](https://clickhouse.com/docs/ru/reference/system-tables/zeros) | Produces unlimited number of non-materialized zeros. |
| [system.zeros_mt](https://clickhouse.com/docs/ru/reference/system-tables/zeros_mt) | Multithreaded version of system.zeros. |
| [system.zookeeper_watches](https://clickhouse.com/docs/ru/reference/system-tables/zookeeper_watches) | System table showing currently active ZooKeeper watches registered by this ClickHouse server. |
| [system.zookeeper_info](https://clickhouse.com/docs/ru/reference/system-tables/zookeeper_info) | System table which outputs introspection of all available keeper nodes. |
| [system.zookeeper_log](https://clickhouse.com/docs/ru/reference/system-tables/zookeeper_log) | System table containing information about the parameters of the request to the ZooKeeper server and the response from it. |
| [system.zookeeper_connection](https://clickhouse.com/docs/ru/reference/system-tables/zookeeper_connection) | System table which exists only if ZooKeeper is configured. Shows current connections to ZooKeeper (including auxiliary ZooKeepers). |
| [system.zookeeper_connection_log](https://clickhouse.com/docs/ru/reference/system-tables/zookeeper_connection_log) | Shows the history of ZooKeeper connections (including auxiliary ZooKeepers). |
| [system.zookeeper](https://clickhouse.com/docs/ru/reference/system-tables/zookeeper) | System table which exists only if ClickHouse Keeper or ZooKeeper are configured. It exposes data from the Keeper cluster defined in the config. |

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
