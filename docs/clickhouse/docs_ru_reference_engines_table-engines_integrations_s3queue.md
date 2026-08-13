# движок таблицы S3Queue - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/s3queue


## CREATE TABLE


```
CREATE TABLE s3_queue_engine_table (name String, value UInt32)
    ENGINE = S3Queue(path, [NOSIGN, | aws_access_key_id, aws_secret_access_key,] format, [compression], [headers], [extra_credentials])
    [SETTINGS]
    [mode = '',]
    [after_processing = 'keep',]
    [keeper_path = '',]
    [loading_retries = 10,]
    [processing_threads_num = 16,]
    [parallel_inserts = false,]
    [enable_logging_to_queue_log = true,]
    [last_processed_path = "",]
    [tracked_files_limit = 1000,]
    [tracked_file_ttl_sec = 0,]
    [polling_min_timeout_ms = 1000,]
    [polling_max_timeout_ms = 600000,]
    [polling_backoff_ms = 30000,]
    [cleanup_interval_min_ms = 60000,]
    [cleanup_interval_max_ms = 60000,]
    [buckets = 0,]
    [list_objects_batch_size = 1000,]
    [enable_hash_ring_filtering = 0,]
    [max_processed_files_before_commit = 100,]
    [max_processed_rows_before_commit = 0,]
    [max_processed_bytes_before_commit = 0,]
    [max_processing_time_sec_before_commit = 0,]

```


```
CREATE TABLE s3queue_engine_table (name String, value UInt32)
ENGINE=S3Queue('https://clickhouse-public-datasets.s3.amazonaws.com/my-test-bucket-768/*', 'CSV', 'gzip')
SETTINGS
    mode = 'unordered';

```


```
<clickhouse>
    <named_collections>
        <s3queue_conf>
            <url>https://clickhouse-public-datasets.s3.amazonaws.com/my-test-bucket-768/*</url>
            <access_key_id>test</access_key_id>
            <secret_access_key>test</secret_access_key>
        </s3queue_conf>
    </named_collections>
</clickhouse>

```


```
CREATE TABLE s3queue_engine_table (name String, value UInt32)
ENGINE=S3Queue(s3queue_conf, format = 'CSV', compression_method = 'gzip')
SETTINGS
    mode = 'ordered';

```


## Настройки

- **Современный синтаксис** (24.7+): `processing_threads_num`, `tracked_file_ttl_sec` и т. д.
- **Устаревший синтаксис** (все версии): `s3queue_processing_threads_num`, `s3queue_tracked_file_ttl_sec` и т. д.

### Режим

- unordered — В режиме unordered множество уже обработанных файлов отслеживается с помощью постоянных узлов в ZooKeeper.
- ordered — В режиме ordered файлы обрабатываются в лексикографическом порядке. Это означает, что если файл с именем ‘BBB’ был обработан в какой-то момент, а позже в бакет будет добавлен файл с именем ‘AA’, он будет проигнорирован. В ZooKeeper сохраняются только максимальное имя (в лексикографическом смысле) успешно обработанного файла и имена файлов, для которых будут выполняться повторные попытки после неудачной загрузки.

### `after_processing`

- keep.
- delete.
- move.
- tag.

```
CREATE TABLE s3queue_engine_table (name String, value UInt32)
ENGINE=S3Queue('https://clickhouse-public-datasets.s3.amazonaws.com/my-test-bucket-768/*', 'CSV', 'gzip')
SETTINGS
    mode = 'unordered',
    after_processing = 'move',
    after_processing_retries = 20,
    after_processing_move_prefix = 'dst_prefix',
    after_processing_move_uri = 'https://clickhouse-public-datasets.s3.amazonaws.com/dst-bucket',
    after_processing_move_access_key_id = 'test',
    after_processing_move_secret_access_key = 'test';

```


### `after_processing_retries`

- Неотрицательное целое число.

### `after_processing_move_access_key_id`

- String.

### `after_processing_move_prefix`

- String.

### `after_processing_move_preserve_path`

- `true` / `false`.

### `after_processing_move_secret_access_key`

- String.

### `after_processing_move_uri`

- String.

### `after_processing_tag_key`

- String.

### `after_processing_tag_value`

- String.

### `keeper_path`

- String.

### `loading_retries`

- Неотрицательное целое число.

### `processing_threads_num`


### `parallel_inserts`


### `enable_logging_to_queue_log`


### `polling_min_timeout_ms`

- Положительное целое число.

### `polling_max_timeout_ms`

- Положительное целое число.

### `polling_backoff_ms`

- Положительное целое число.

### `tracked_files_limit`

- Положительное целое число.

### `tracked_file_ttl_sec`

- Положительное целое число.

### `cleanup_interval_min_ms`


### `cleanup_interval_max_ms`


### `buckets`


### `use_persistent_processing_nodes`


### `persistent_processing_node_ttl_seconds`


## Настройки, связанные с S3


## Ролевой доступ на основе ролей к S3


```
CREATE TABLE s3_table
(
    ts DateTime,
    value UInt64
)
ENGINE = S3Queue(
                'https://<your_bucket>/*.csv',
                extra_credentials(role_arn = 'arn:aws:iam::111111111111:role/<your_role>')
                ,'CSV')
SETTINGS
    ...

```


## Упорядоченный режим S3Queue


## SELECT из движка таблицы S3Queue


## Описание

- С помощью движка создайте таблицу для чтения из указанного пути в S3 и рассматривайте её как поток данных.
- Создайте таблицу с нужной структурой.
- Создайте materialized view, который преобразует данные из движка и помещает их в ранее созданную таблицу.

```
CREATE TABLE s3queue_engine_table (name String, value UInt32)
    ENGINE=S3Queue('https://clickhouse-public-datasets.s3.amazonaws.com/my-test-bucket-768/*', 'CSV', 'gzip')
    SETTINGS
        mode = 'unordered';

CREATE TABLE stats (name String, value UInt32)
    ENGINE = MergeTree() ORDER BY name;

CREATE MATERIALIZED VIEW consumer TO stats
    AS SELECT name, value FROM s3queue_engine_table;

  SELECT * FROM stats ORDER BY name;

```


## Виртуальные столбцы

- `_path` — Путь к файлу.
- `_file` — Имя файла.
- `_size` — Размер файла.
- `_time` — Время создания файла.

## Подстановочные шаблоны в path

- `*` — Заменяет любое количество любых символов, кроме `/`, включая пустую строку.
- `**` — Заменяет любое количество любых символов, включая `/`, включая пустую строку.
- `?` — Заменяет любой отдельный символ.
- `{some_string,another_string,yet_another_one}` — Заменяет любую из строк: `'some_string'`, `'another_string'`, `'yet_another_one'`.
- `{N..M}` — Заменяет любое число в диапазоне от N до M включительно. N и M могут содержать ведущие нули, например `000..078`.

## Ограничения

- Дублирующиеся строки могут возникать в результате:
- исключения во время парсинга в середине обработки файла, если повторные попытки включены через `s3queue_loading_retries`;
- `S3Queue` настроен на нескольких серверах, указывающих на один и тот же path в ZooKeeper, и сеанс Keeper истекает до того, как один из серверов успевает закоммитить обработанный файл. Это может привести к тому, что другой сервер начнёт обрабатывать файл, который уже был частично или полностью обработан первым сервером. Однако начиная с версии 25.8 это больше неактуально, если `use_persistent_processing_nodes = 1`.
- аварийного завершения работы сервера.
- Если `S3Queue` настроен на нескольких серверах, указывающих на один и тот же path в ZooKeeper, и используется режим `Ordered`, то `s3queue_loading_retries` не будет работать. Это скоро исправят.

## Интроспекция

- `system.s3queue_metadata_cache`. Эта таблица не является постоянной и показывает текущее состояние `S3Queue` в памяти: какие файлы обрабатываются в данный момент, какие уже обработаны, а какие завершились ошибкой.

```
┌─statement──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ CREATE TABLE system.s3queue_metadata_cache
(
    `database` String,
    `table` String,
    `file_name` String,
    `rows_processed` UInt64,
    `status` String,
    `processing_start_time` Nullable(DateTime),
    `processing_end_time` Nullable(DateTime),
    `ProfileEvents` Map(String, UInt64)
    `exception` String
)
ENGINE = SystemS3Queue
COMMENT 'Contains in-memory state of S3Queue metadata and currently processed rows per file.' │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

```


```

SELECT *
FROM system.s3queue_metadata_cache

Row 1:
──────
zookeeper_path:        /clickhouse/s3queue/25ea5621-ae8c-40c7-96d0-cec959c5ab88/3b3f66a1-9866-4c2e-ba78-b6bfa154207e
file_name:             wikistat/original/pageviews-20150501-030000.gz
rows_processed:        5068534
status:                Processed
processing_start_time: 2023-10-13 13:09:48
processing_end_time:   2023-10-13 13:10:31
ProfileEvents:         {'ZooKeeperTransactions':3,'ZooKeeperGet':2,'ZooKeeperMulti':1,'SelectedRows':5068534,'SelectedBytes':198132283,'ContextLock':1,'S3QueueSetFileProcessingMicroseconds':2480,'S3QueueSetFileProcessedMicroseconds':9985,'S3QueuePullMicroseconds':273776,'LogTest':17}
exception:

```

- `system.s3queue_log`. Постоянная таблица. Содержит ту же информацию, что и `system.s3queue_metadata_cache`, но для файлов со статусами `processed` и `failed`.

```
SHOW CREATE TABLE system.s3queue_log

Query id: 0ad619c3-0f2a-4ee4-8b40-c73d86e04314

┌─statement──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ CREATE TABLE system.s3queue_log
(
    `event_date` Date,
    `event_time` DateTime,
    `table_uuid` String,
    `file_name` String,
    `rows_processed` UInt64,
    `status` Enum8('Processed' = 0, 'Failed' = 1),
    `processing_start_time` Nullable(DateTime),
    `processing_end_time` Nullable(DateTime),
    `ProfileEvents` Map(String, UInt64),
    `exception` String
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(event_date)
ORDER BY (event_date, event_time) │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

```


```
    <s3queue_log>
        <database>system</database>
        <table>s3queue_log</table>
    </s3queue_log>

```


```
SELECT *
FROM system.s3queue_log

Row 1:
──────
event_date:            2023-10-13
event_time:            2023-10-13 13:10:12
table_uuid:
file_name:             wikistat/original/pageviews-20150501-020000.gz
rows_processed:        5112621
status:                Processed
processing_start_time: 2023-10-13 13:09:48
processing_end_time:   2023-10-13 13:10:12
ProfileEvents:         {'ZooKeeperTransactions':3,'ZooKeeperGet':2,'ZooKeeperMulti':1,'SelectedRows':5112621,'SelectedBytes':198577687,'ContextLock':1,'S3QueueSetFileProcessingMicroseconds':1934,'S3QueueSetFileProcessedMicroseconds':17063,'S3QueuePullMicroseconds':5841972,'LogTest':17}
exception:

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
