# Движок таблицы Kafka - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/kafka

- Публикуйте потоки данных или подписывайтесь на них.
- Организуйте отказоустойчивое хранилище.
- Обрабатывайте потоки по мере их поступления.

## Создание таблицы


```
CREATE TABLE [IF NOT EXISTS] [db.]table_name [ON CLUSTER cluster]
(
    name1 [type1] [ALIAS expr1],
    name2 [type2] [ALIAS expr2],
    ...
) ENGINE = Kafka()
SETTINGS
    kafka_broker_list = 'host:port',
    kafka_topic_list = 'topic1,topic2,...',
    kafka_group_name = 'group_name',
    kafka_format = 'data_format'[,]
    [kafka_security_protocol = '',]
    [kafka_sasl_mechanism = '',]
    [kafka_sasl_username = '',]
    [kafka_sasl_password = '',]
    [kafka_autodetect_client_rack = '',]
    [kafka_schema = '',]
    [kafka_num_consumers = N,]
    [kafka_max_block_size = 0,]
    [kafka_skip_broken_messages = N,]
    [kafka_commit_every_batch = 0,]
    [kafka_client_id = '',]
    [kafka_poll_timeout_ms = 0,]
    [kafka_poll_max_batch_size = 0,]
    [kafka_flush_interval_ms = 0,]
    [kafka_consumer_reschedule_ms = 0,]
    [kafka_thread_per_consumer = 0,]
    [kafka_handle_error_mode = 'default',]
    [kafka_commit_on_select = false,]
    [kafka_consumer_acquire_timeout_ms = 30000,]
    [kafka_max_rows_per_message = 1,]
    [kafka_compression_codec = '',]
    [kafka_compression_level = -1];

```

- `kafka_broker_list` — Список брокеров, разделённых запятыми (например, `localhost:9092`).
- `kafka_topic_list` — Список топиков Kafka.
- `kafka_group_name` — Группа потребителей Kafka. Смещения чтения отслеживаются отдельно для каждой группы. Если вы не хотите, чтобы сообщения дублировались в кластере, используйте везде одно и то же имя группы.
- `kafka_format` — Формат сообщений. Используется та же нотация, что и для SQL-функции `FORMAT`, например `JSONEachRow`. Дополнительные сведения см. в разделе [Форматы](https://clickhouse.com/docs/ru/reference/formats/index).
- `kafka_security_protocol` — протокол, используемый для связи с брокерами. Возможные значения: `plaintext`, `ssl`, `sasl_plaintext`, `sasl_ssl`.
- `kafka_sasl_mechanism` - механизм SASL, используемый для аутентификации. Возможные значения: `GSSAPI`, `PLAIN`, `SCRAM-SHA-256`, `SCRAM-SHA-512`, `OAUTHBEARER`, `AWS_MSK_IAM`.
- `kafka_aws_region` - регион AWS для аутентификации MSK IAM. Если не указан, автоматически определяется по адресу брокера. Указывайте его явно при использовании псевдонимов PrivateLink или пользовательских DNS-имен хостов, не содержащих информации о регионе. По умолчанию: пусто (автоопределение).
- `kafka_sasl_username` - имя пользователя для SASL-аутентификации при использовании механизмов `PLAIN` и `SASL-SCRAM-..`.
- `kafka_sasl_password` — пароль SASL для механизмов `PLAIN` и `SASL-SCRAM-..`.
- `kafka_schema` — параметр, который необходимо использовать, если для формата требуется определение схемы. Например, [Cap’n Proto](https://capnproto.org/) требует указать путь к файлу схемы и имя корневого объекта `schema.capnp:Message`.
- `kafka_schema_registry_skip_bytes` — Количество байтов, которое нужно пропустить в начале каждого сообщения при использовании schema registry с заголовками обёртки (например, AWS Glue Schema Registry, который добавляет 19-байтную обёртку). Диапазон: `[0, 255]`. По умолчанию: `0`.
- `kafka_num_consumers` — Количество consumers на таблицу. Укажите больше consumers, если пропускной способности одного consumer недостаточно. Общее количество consumers не должно превышать количество партиций в topic, поскольку на одну партицию может быть назначен только один consumer, и не должно быть больше количества физических ядер на сервере, где развернут ClickHouse. По умолчанию: `1`.
- `kafka_max_block_size` — Максимальный размер батча (в сообщениях) при выполнении poll. По умолчанию: [max_insert_block_size](https://clickhouse.com/docs/ru/reference/settings/session-settings#max_insert_block_size).
- `kafka_skip_broken_messages` — допустимое для парсера сообщений Kafka число несовместимых со схемой сообщений на блок. Если `kafka_skip_broken_messages = N`, то движок пропускает *N* сообщений Kafka, которые не удаётся разобрать (одно сообщение соответствует одной строке данных). Значение по умолчанию: `0`.
- `kafka_commit_every_batch` — Выполнять коммит для каждого потреблённого и обработанного батча, а не один коммит после записи всего блока. По умолчанию: `0`.
- `kafka_client_id` — идентификатор клиента. По умолчанию пустой.
- `kafka_poll_timeout_ms` — тайм-аут для одного опроса из Kafka. По умолчанию: [stream_poll_timeout_ms](https://clickhouse.com/docs/ru/reference/settings/session-settings#stream_poll_timeout_ms).
- `kafka_poll_max_batch_size` — Максимальное количество сообщений, получаемых за один опрос Kafka. По умолчанию: [max_block_size](https://clickhouse.com/docs/ru/reference/settings/session-settings#max_block_size).
- `kafka_flush_interval_ms` — Тайм-аут для сброса данных из Kafka. По умолчанию: [stream_flush_interval_ms](https://clickhouse.com/docs/ru/reference/settings/session-settings#stream_flush_interval_ms).
- `kafka_consumer_reschedule_ms` — интервал перепланирования при остановке потоковой обработки Kafka (например, когда нет доступных для чтения сообщений). Эта настройка определяет задержку перед тем, как consumer повторит опрос. Не должно превышать `kafka_consumers_pool_ttl_ms`. По умолчанию: `500` миллисекунд.
- `kafka_thread_per_consumer` — Выделяет отдельный поток для каждого консьюмера. Если включен, каждый консьюмер независимо сбрасывает данные, параллельно (в противном случае строки от нескольких консьюмеров объединяются в один блок). По умолчанию: `0`.
- `kafka_handle_error_mode` — как обрабатывать ошибки в движке Kafka. Возможные значения: default (если не удастся разобрать сообщение, будет сгенерировано исключение), stream (сообщение об исключении и исходное сообщение будут сохранены в виртуальных столбцах `_error` и `_raw_message`), dead_letter_queue (данные, связанные с ошибкой, будут сохранены в system.dead_letter_queue).
- `kafka_commit_on_select` — Выполнять коммит сообщений при выполнении запроса SELECT. Значение по умолчанию: `false`.
- `kafka_consumer_acquire_timeout_ms` — тайм-аут в миллисекундах на получение потребителя Kafka при выполнении прямых `SELECT`-запросов к таблице `Kafka2` (с хранением смещений в Keeper). Когда к одной и той же таблице одновременно выполняются несколько прямых `SELECT`-запросов, каждый из них должен ждать, пока потребители не станут доступны. Тайм-аут предотвращает взаимные блокировки в случаях, когда запросы удерживают разные подмножества потребителей. Значение по умолчанию: `30000`.
- `kafka_max_rows_per_message` — Максимальное количество строк, записываемых в одно сообщение Kafka для построчных форматов. По умолчанию: `1`.
- `kafka_autodetect_client_rack` — автоматически задаёт параметр `client.rack` для `librdkafka`, чтобы отдавать предпочтение ближайшим репликам Kafka. Поддерживаемые источники: `AWS_ZONE_ID` — идентификатор зоны доступности AWS IMDSv2, например `euc1-az1`; `AWS_ZONE_NAME` — имя зоны доступности AWS IMDSv2, например `eu-central-1a`; `GCP_ZONE` — зона сервиса метаданных GCP, например `europe-central2-a`; `CLICKHOUSE` — использовать внутреннее определение ClickHouse, которое может опираться на метаданные облака или конфигурацию; `AWS_ZONE_NAME_THEN_GCP_ZONE` — сначала попытаться использовать `AWS_ZONE_NAME`, а затем `GCP_ZONE`. По умолчанию: пустая строка, отключено. Совет: в разных средах используются разные форматы зон доступности. Amazon MSK обычно использует идентификаторы зон, поэтому предпочтителен `AWS_ZONE_ID`. Confluent Cloud обычно использует имена зон, поэтому предпочтителен `AWS_ZONE_NAME`. Если вы не уверены, используйте `AWS_ZONE_NAME_THEN_GCP_ZONE` или проверьте значение `broker.rack` в вашем кластере. Примечание: брокеры Kafka должны быть настроены с `broker.rack` и `replica.selector.class=org.apache.kafka.common.replica.RackAwareReplicaSelector`.
- `kafka_compression_codec` — кодек сжатия, используемый при отправке сообщений. Поддерживаются: пустая строка, `none`, `gzip`, `snappy`, `lz4`, `zstd`. Если указана пустая строка, кодек сжатия таблицей не задаётся, поэтому будут использоваться значения из файлов конфигурации или значение по умолчанию из `librdkafka`. По умолчанию: пустая строка.
- `kafka_compression_level` — параметр уровня сжатия для алгоритма, выбранного с помощью kafka_compression_codec. Более высокие значения обеспечивают лучшее сжатие, но требуют больше ресурсов CPU. Допустимый диапазон зависит от алгоритма: `[0-9]` для `gzip`; `[0-12]` для `lz4`; только `0` для `snappy`; `[0-12]` для `zstd`; `-1` = уровень сжатия по умолчанию, зависящий от кодека. Значение по умолчанию: `-1`.
- `kafka_map_virtual_columns_on_write` — Если включено, столбцы со специальными именами `_key`, `_timestamp`, `_headers.name` и `_headers.value` в схеме таблицы сопоставляются с соответствующими метаданными сообщений Kafka при `INSERT` и исключаются из полезной нагрузки сообщения. См. [Сопоставление столбцов с метаданными сообщений Kafka](#mapping-columns-to-kafka-message-metadata). По умолчанию: `false`.

```
CREATE TABLE queue (
    timestamp UInt64,
    level String,
    message String
  ) ENGINE = Kafka('localhost:9092', 'topic', 'group1', 'JSONEachRow');

  SELECT * FROM queue LIMIT 5;

CREATE TABLE queue2 (
    timestamp UInt64,
    level String,
    message String
  ) ENGINE = Kafka SETTINGS kafka_broker_list = 'localhost:9092',
                            kafka_topic_list = 'topic',
                            kafka_group_name = 'group1',
                            kafka_format = 'JSONEachRow',
                            kafka_num_consumers = 4;

CREATE TABLE queue3 (
    timestamp UInt64,
    level String,
    message String
  ) ENGINE = Kafka('localhost:9092', 'topic', 'group1')
              SETTINGS kafka_format = 'JSONEachRow',
                       kafka_num_consumers = 4;

```


## Описание

- Используйте движок, чтобы создать consumer Kafka, и рассматривайте его как поток данных.
- Создайте таблицу с нужной структурой.
- Создайте materialized view, которое преобразует данные из движка и помещает их в ранее созданную таблицу.

```
  CREATE NAMED COLLECTION kafka_creds AS
    kafka_broker_list = 'localhost:9092',
    kafka_topic_list = 'topic',
    kafka_group_name = 'group1',
    kafka_format = 'JSONEachRow';

  CREATE TABLE queue (
    timestamp UInt64,
    level String,
    message String
  ) ENGINE = Kafka(kafka_creds);

  CREATE TABLE daily (
    day Date,
    level String,
    total UInt64
  ) ENGINE = SummingMergeTree
  PARTITION BY toYYYYMM(day)
  ORDER BY (day, level);

  CREATE MATERIALIZED VIEW consumer TO daily
    AS SELECT toDate(toDateTime(timestamp)) AS day, level, count() AS total
    FROM queue GROUP BY day, level;

  SELECT level, sum(total) FROM daily GROUP BY level;

```


```
DETACH TABLE consumer;
ATTACH TABLE consumer;

```


## Конфигурация


```
<kafka>
    <!-- Global configuration options for all tables of Kafka engine type -->
    <debug>cgrp</debug>
    <statistics_interval_ms>3000</statistics_interval_ms>

    <kafka_topic>
        <name>logs</name>
        <statistics_interval_ms>4000</statistics_interval_ms>
    </kafka_topic>

    <!-- Settings for consumer -->
    <consumer>
        <auto_offset_reset>smallest</auto_offset_reset>
        <kafka_topic>
            <name>logs</name>
            <fetch_min_bytes>100000</fetch_min_bytes>
        </kafka_topic>

        <kafka_topic>
            <name>stats</name>
            <fetch_min_bytes>50000</fetch_min_bytes>
        </kafka_topic>
    </consumer>

    <!-- Settings for producer -->
    <producer>
        <kafka_topic>
            <name>logs</name>
            <retry_backoff_ms>250</retry_backoff_ms>
        </kafka_topic>

        <kafka_topic>
            <name>stats</name>
            <retry_backoff_ms>400</retry_backoff_ms>
        </kafka_topic>
    </producer>
</kafka>

```


### Аутентификация AWS MSK IAM


```
CREATE TABLE msk_queue (
    timestamp UInt64,
    level String,
    message String
) ENGINE = Kafka()
SETTINGS
    kafka_broker_list = 'b-1.mycluster.kafka.us-east-1.amazonaws.com:9098',
    kafka_topic_list = 'my-topic',
    kafka_group_name = 'my-group',
    kafka_format = 'JSONEachRow',
    kafka_sasl_mechanism = 'AWS_MSK_IAM';

```

- Provisioned MSK: `b-X.cluster.kafka.<region>.amazonaws.com:9098`
- Serverless MSK: `boot-X.kafka-serverless.<region>.amazonaws.com:9098`
- VPC Endpoint: `vpce-X.kafka.<region>.vpce.amazonaws.com:9098`

```
<kafka>
  <use_environment_credentials>true</use_environment_credentials>
</kafka>

```


```
CREATE TABLE msk_privatelink_queue (
    timestamp UInt64,
    level String,
    message String
) ENGINE = Kafka()
SETTINGS
    kafka_broker_list = 'my-privatelink-alias.internal.example.com:9098',
    kafka_topic_list = 'my-topic',
    kafka_group_name = 'my-group',
    kafka_format = 'JSONEachRow',
    kafka_sasl_mechanism = 'AWS_MSK_IAM',
    kafka_aws_region = 'us-east-1';

```


```
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": [
      "kafka-cluster:Connect",
      "kafka-cluster:DescribeTopic",
      "kafka-cluster:ReadData",
      "kafka-cluster:AlterGroup",
      "kafka-cluster:DescribeGroup"
    ],
    "Resource": [
      "arn:aws:kafka:REGION:ACCOUNT:cluster/CLUSTER_NAME/*",
      "arn:aws:kafka:REGION:ACCOUNT:topic/CLUSTER_NAME/TOPIC_NAME/*",
      "arn:aws:kafka:REGION:ACCOUNT:group/CLUSTER_NAME/CONSUMER_GROUP/*"
    ]
  }]
}

```


```
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": [
      "kafka-cluster:Connect",
      "kafka-cluster:DescribeTopic",
      "kafka-cluster:WriteData"
    ],
    "Resource": [
      "arn:aws:kafka:REGION:ACCOUNT:cluster/CLUSTER_NAME/*",
      "arn:aws:kafka:REGION:ACCOUNT:topic/CLUSTER_NAME/TOPIC_NAME/*"
    ]
  }]
}

```


### Поддержка Kerberos


```
<!-- Kerberos-aware Kafka -->
<kafka>
<security_protocol>SASL_PLAINTEXT</security_protocol>
<sasl_kerberos_keytab>/home/kafkauser/kafkauser.keytab</sasl_kerberos_keytab>
<sasl_kerberos_principal>kafkauser/kafkahost@EXAMPLE.COM</sasl_kerberos_principal>
</kafka>

```


## Виртуальные столбцы

- `_topic` — топик Kafka. Тип данных: `LowCardinality(String)`.
- `_key` — ключ сообщения. Тип данных: `String`.
- `_offset` — смещение сообщения. Тип данных: `UInt64`.
- `_timestamp` — временная метка сообщения. Тип данных: `Nullable(DateTime)`.
- `_timestamp_ms` — временная метка сообщения в миллисекундах. Тип данных: `Nullable(DateTime64(3))`.
- `_partition` — партиция топика Kafka. Тип данных: `UInt64`.
- `_headers.name` — массив ключей заголовков сообщения. Тип данных: `Array(String)`.
- `_headers.value` — массив значений заголовков сообщения. Тип данных: `Array(String)`.
- `_raw_message` - необработанное сообщение, которое не удалось успешно разобрать. Тип данных: `String`.
- `_error` - сообщение об исключении, возникшем при неудачном разборе. Тип данных: `String`.

## Сопоставление столбцов с метаданными сообщений Kafka

- `_key` (тип `String`) — сопоставляется с ключом сообщения Kafka.
- `_timestamp` (тип `DateTime`) — сопоставляется с временной меткой сообщения Kafka.
- `_headers.name` (тип `Array(String)`) и `_headers.value` (тип `Array(String)`) — сопоставляются с заголовками сообщений Kafka. Каждая пара `(_headers.name[i], _headers.value[i])` становится одним заголовком Kafka. Поскольку `_headers.name` и `_headers.value` имеют общий вложенный префикс `_headers`, ClickHouse требует, чтобы оба массива имели одинаковый размер в каждой строке.

```
CREATE TABLE kafka_out
(
    event_json String,
    `_key` String,
    `_timestamp` DateTime,
    `_headers.name` Array(String),
    `_headers.value` Array(String)
)
ENGINE = Kafka
SETTINGS
    kafka_broker_list = 'broker:9092',
    kafka_topic_list = 'events',
    kafka_group_name = 'events-producer',
    kafka_format = 'JSONEachRow',
    kafka_map_virtual_columns_on_write = 1;

INSERT INTO kafka_out VALUES
    ('{"a":1}', 'session-42', now(), ['source', 'trace_id'], ['api', 'abc-123']);

```


## Поддержка форматов данных

- Для построчных форматов количество строк в одном сообщении Kafka можно задать с помощью настройки `kafka_max_rows_per_message`.
- Для блочных форматов блок нельзя разбить на более мелкие части, но количество строк в одном блоке можно задать с помощью общей настройки [max_block_size](https://clickhouse.com/docs/ru/reference/settings/session-settings#max_block_size).

## Движок для хранения зафиксированных смещений в ClickHouse Keeper

- `kafka_keeper_path` задает путь к таблице в ClickHouse Keeper
- `kafka_replica_name` задает имя реплики в ClickHouse Keeper

```
CREATE TABLE experimental_kafka (key UInt64, value UInt64)
ENGINE = Kafka('localhost:19092', 'my-topic', 'my-consumer', 'JSONEachRow')
SETTINGS
kafka_keeper_path = '/clickhouse/{database}/{uuid}',
kafka_replica_name = '{replica}'
SETTINGS allow_experimental_kafka_offsets_storage_in_keeper=1;

```


### Известные ограничения

- Быстрое удаление и повторное создание таблицы либо указание одного и того же пути ClickHouse Keeper для разных движков может привести к проблемам. В качестве рекомендации можно использовать `{uuid}` в `kafka_keeper_path`, чтобы избежать конфликтов путей.
- Чтобы обеспечить повторяемые чтения, нельзя потреблять сообщения из нескольких партиций в одном потоке. С другой стороны, потребителей Kafka нужно регулярно опрашивать, чтобы они оставались активными. Из-за этих двух требований мы решили разрешить создание нескольких потребителей только при включённом `kafka_thread_per_consumer`, иначе становится слишком сложно избежать проблем, связанных с их регулярным опросом.
- [Виртуальные столбцы](https://clickhouse.com/docs/ru/reference/engines/table-engines/index#table_engines-virtual_columns)
- [background_message_broker_schedule_pool_size](https://clickhouse.com/docs/ru/reference/settings/server-settings/settings#background_message_broker_schedule_pool_size)
- [system.kafka_consumers](https://clickhouse.com/docs/ru/reference/system-tables/kafka_consumers)
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
