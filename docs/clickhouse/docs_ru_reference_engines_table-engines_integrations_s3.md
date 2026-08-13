# Движок таблицы S3 - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/s3


## Пример


```
CREATE TABLE s3_engine_table (name String, value UInt32)
    ENGINE=S3('https://clickhouse-public-datasets.s3.amazonaws.com/my-test-bucket-768/test-data.csv.gz', 'CSV', 'gzip')
    SETTINGS input_format_with_names_use_header = 0;

INSERT INTO s3_engine_table VALUES ('one', 1), ('two', 2), ('three', 3);

SELECT * FROM s3_engine_table LIMIT 2;

```


```
┌─name─┬─value─┐
│ one  │     1 │
│ two  │     2 │
└──────┴───────┘

```


## Создайте таблицу


```
CREATE TABLE s3_engine_table (name String, value UInt32)
    ENGINE = S3(path [, NOSIGN | aws_access_key_id, aws_secret_access_key,] format, [compression], [partition_strategy], [partition_columns_in_data_file], [extra_credentials])
    [PARTITION BY expr]
    [SETTINGS ...]

```


### Параметры движка

- `path` — URL бакета с путём к файлу. В режиме `readonly` поддерживаются следующие подстановочные шаблоны: `*`, `**`, `?`, `{abc,def}` и `{N..M}`, где `N`, `M` — числа, а `'abc'`, `'def'` — строки. Подробнее см. [ниже](#wildcards-in-path).
- `NOSIGN` - Если это ключевое слово указано вместо учётных данных, запросы не будут подписываться.
- `format` — [Формат](https://clickhouse.com/docs/ru/reference/formats/index#formats-overview) файла.
- `aws_access_key_id`, `aws_secret_access_key` - Долговременные учётные данные пользователя аккаунта [AWS](https://aws.amazon.com/). Их можно использовать для аутентификации запросов. Параметр необязателен. Если учётные данные не указаны, они берутся из файла конфигурации. Подробнее см. [Использование S3 для хранения данных](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/mergetree#table_engine-mergetree-s3).
- `compression` — Тип сжатия. Поддерживаемые значения: `none`, `gzip/gz`, `brotli/br`, `xz/LZMA`, `zstd/zst`. Параметр необязателен. По умолчанию тип сжатия определяется автоматически по расширению файла.
- `partition_strategy` – Варианты: `wildcard` или `hive`. Для `wildcard` в пути должен присутствовать `{_partition_id}`, который заменяется ключом партиционирования. `hive` не поддерживает подстановочные шаблоны, предполагает, что путь указывает на корень таблицы, и генерирует каталоги партиций в стиле Hive, где в качестве имён файлов используются Snowflake ID, а расширением служит формат файла. По умолчанию используется настройка `file_like_engine_default_partition_strategy` (`wildcard` при настройках `compatibility` старше `26.6`, в противном случае `hive`).
- `partition_columns_in_data_file` - Используется только со стратегией партиционирования `hive`. Указывает, должен ли ClickHouse ожидать, что столбцы партиции будут записаны в файл данных. По умолчанию — `false`.
- `storage_class_name` - Варианты: `STANDARD`, `REDUCED_REDUNDANCY`, `STANDARD_IA`, `ONEZONE_IA`, `INTELLIGENT_TIERING`, `GLACIER_IR`, `EXPRESS_ONEZONE`. Поддерживаются только классы хранилища S3, допускающие немедленное извлечение данных (архивные классы, такие как `GLACIER` и `DEEP_ARCHIVE`, не поддерживаются). Позволяет указать [AWS S3 Intelligent Tiering](https://aws.amazon.com/s3/storage-classes/intelligent-tiering/).
- `extra_credentials` - Необязательный параметр. Используется для передачи `role_arn` для ролевого доступа в ClickHouse Cloud. Инструкции по настройке см. в [Secure S3](https://clickhouse.com/docs/ru/products/cloud/guides/data-sources/accessing-s3-data-securely).

### Кэш данных


```
SELECT *
FROM s3('http://minio:10000/clickhouse//test_3.csv', 'minioadmin', 'minioadminpassword', 'CSV')
SETTINGS filesystem_cache_name = 'cache_for_s3', enable_filesystem_cache = 1;

```

- добавьте следующий раздел в конфигурационный файл ClickHouse:

```
<clickhouse>
    <filesystem_caches>
        <cache_for_s3>
            <path>путь к каталогу кэша</path>
            <max_size>10Gi</max_size>
        </cache_for_s3>
    </filesystem_caches>
</clickhouse>

```

- повторно использовать конфигурацию кэша (а значит, и хранилище кэша) из раздела `storage_configuration` в ClickHouse, [описанного здесь](https://clickhouse.com/docs/ru/concepts/features/configuration/server-config/storing-data#using-local-cache)

### PARTITION BY


#### Стратегия партиционирования


```
CREATE TABLE t_03363_parquet (year UInt16, country String, counter UInt8)
ENGINE = S3(s3_conn, filename = 't_03363_parquet', format = Parquet, partition_strategy='hive')
PARTITION BY (year, country);

INSERT INTO t_03363_parquet VALUES
    (2022, 'USA', 1),
    (2022, 'Canada', 2),
    (2023, 'USA', 3),
    (2023, 'Mexico', 4),
    (2024, 'France', 5),
    (2024, 'Germany', 6),
    (2024, 'Germany', 7),
    (1999, 'Brazil', 8),
    (2100, 'Japan', 9),
    (2024, 'CN', 10),
    (2025, '', 11);

select _path, * from t_03363_parquet;

```


```
┌─_path──────────────────────────────────────────────────────────────────────┬─year─┬─country─┬─counter─┐
│ test/t_03363_parquet/year=2100/country=Japan/7329604473272971264.parquet   │ 2100 │ Japan   │       9 │
│ test/t_03363_parquet/year=2024/country=France/7329604473323302912.parquet  │ 2024 │ France  │       5 │
│ test/t_03363_parquet/year=2022/country=Canada/7329604473314914304.parquet  │ 2022 │ Canada  │       2 │
│ test/t_03363_parquet/year=1999/country=Brazil/7329604473289748480.parquet  │ 1999 │ Brazil  │       8 │
│ test/t_03363_parquet/year=2023/country=Mexico/7329604473293942784.parquet  │ 2023 │ Mexico  │       4 │
│ test/t_03363_parquet/year=2023/country=USA/7329604473319108608.parquet     │ 2023 │ USA     │       3 │
│ test/t_03363_parquet/year=2025/country=/7329604473327497216.parquet        │ 2025 │         │      11 │
│ test/t_03363_parquet/year=2024/country=CN/7329604473310720000.parquet      │ 2024 │ CN      │      10 │
│ test/t_03363_parquet/year=2022/country=USA/7329604473298137088.parquet     │ 2022 │ USA     │       1 │
│ test/t_03363_parquet/year=2024/country=Germany/7329604473306525696.parquet │ 2024 │ Germany │       6 │
│ test/t_03363_parquet/year=2024/country=Germany/7329604473306525696.parquet │ 2024 │ Germany │       7 │
└────────────────────────────────────────────────────────────────────────────┴──────┴─────────┴─────────┘

```


### Запросы к данным, разбитым на партиции


#### Создание таблицы


```
CREATE TABLE p
(
    `column1` UInt32,
    `column2` UInt32,
    `column3` UInt32
)
ENGINE = S3(
           'http://minio:10000/clickhouse//test_{_partition_id}.csv',
           'minioadmin',
           'minioadminpassword',
           'CSV',
           partition_strategy='wildcard')
PARTITION BY column3

```


#### Вставка данных


```
INSERT INTO p VALUES (1, 2, 3), (3, 2, 1), (78, 43, 45)

```


#### Выборка из партиции 3


```
SELECT *
FROM s3('http://minio:10000/clickhouse//test_3.csv', 'minioadmin', 'minioadminpassword', 'CSV')

```


```
┌─c1─┬─c2─┬─c3─┐
│  1 │  2 │  3 │
└────┴────┴────┘

```


#### Выборка из партиции 1


```
SELECT *
FROM s3('http://minio:10000/clickhouse//test_1.csv', 'minioadmin', 'minioadminpassword', 'CSV')

```


```
┌─c1─┬─c2─┬─c3─┐
│  3 │  2 │  1 │
└────┴────┴────┘

```


#### Выборка данных из партиции 45


```
SELECT *
FROM s3('http://minio:10000/clickhouse//test_45.csv', 'minioadmin', 'minioadminpassword', 'CSV')

```


```
┌─c1─┬─c2─┬─c3─┐
│ 78 │ 43 │ 45 │
└────┴────┴────┘

```


#### Ограничение


```
SELECT * FROM p

```


```
Received exception from server (version 23.4.1):
Code: 48. DB::Exception: Received from localhost:9000. DB::Exception: Reading from a partitioned S3 storage is not implemented yet. (NOT_IMPLEMENTED)

```


## Вставка данных


## Виртуальные столбцы

- `_path` — Путь к файлу. Тип: `LowCardinality(String)`.
- `_file` — Имя файла. Тип: `LowCardinality(String)`.
- `_size` — Размер файла в байтах. Тип: `Nullable(UInt64)`. Если размер неизвестен, значение равно `NULL`.
- `_time` — Время последнего изменения файла. Тип: `Nullable(DateTime)`. Если время неизвестно, значение равно `NULL`.
- `_etag` — ETag файла. Тип: `LowCardinality(String)`. Если ETag неизвестен, значение равно `NULL`.
- `_tags` — Метки файла. Тип: `Map(String, String)`. Если меток нет, значение — пустой `Map` `{}`.

## Подробности реализации

- Чтение и запись могут выполняться параллельно
- Не поддерживаются:
- операции `ALTER` и `SELECT...SAMPLE`.
- индексы.
- возможна [репликация с нулевым копированием](https://clickhouse.com/docs/ru/concepts/features/configuration/server-config/storing-data#zero-copy), но она не поддерживается.

## Подстановочные шаблоны в path

- `*` — Подставляет любое количество любых символов, кроме `/`, включая пустую строку.
- `**` — Подставляет любое количество любых символов, включая `/`, включая пустую строку.
- `?` — Подставляет любой отдельный символ.
- `{some_string,another_string,yet_another_one}` — Подставляет любую из строк `'some_string', 'another_string', 'yet_another_one'`.
- `{N..M}` — Подставляет любое число в диапазоне от N до M включительно. N и M могут содержать ведущие нули, например `000..078`.

```
CREATE TABLE big_table (name String, value UInt32)
    ENGINE = S3('https://clickhouse-public-datasets.s3.amazonaws.com/my-bucket/my_folder/file-{000..999}.csv', 'CSV');

```

- ‘[https://clickhouse-public-datasets.s3.amazonaws.com/my-bucket/some&#95;folder/some&#95;file&#95;1.csv&#39](https://clickhouse-public-datasets.s3.amazonaws.com/my-bucket/some&#95;folder/some&#95;file&#95;1.csv&#39);
- ‘[https://clickhouse-public-datasets.s3.amazonaws.com/my-bucket/some&#95;folder/some&#95;file&#95;2.csv&#39](https://clickhouse-public-datasets.s3.amazonaws.com/my-bucket/some&#95;folder/some&#95;file&#95;2.csv&#39);
- ‘[https://clickhouse-public-datasets.s3.amazonaws.com/my-bucket/some&#95;folder/some&#95;file&#95;3.csv&#39](https://clickhouse-public-datasets.s3.amazonaws.com/my-bucket/some&#95;folder/some&#95;file&#95;3.csv&#39);
- ‘[https://clickhouse-public-datasets.s3.amazonaws.com/my-bucket/another&#95;folder/some&#95;file&#95;1.csv&#39](https://clickhouse-public-datasets.s3.amazonaws.com/my-bucket/another&#95;folder/some&#95;file&#95;1.csv&#39);
- ‘[https://clickhouse-public-datasets.s3.amazonaws.com/my-bucket/another&#95;folder/some&#95;file&#95;2.csv&#39](https://clickhouse-public-datasets.s3.amazonaws.com/my-bucket/another&#95;folder/some&#95;file&#95;2.csv&#39);
- ‘[https://clickhouse-public-datasets.s3.amazonaws.com/my-bucket/another&#95;folder/some&#95;file&#95;3.csv&#39](https://clickhouse-public-datasets.s3.amazonaws.com/my-bucket/another&#95;folder/some&#95;file&#95;3.csv&#39);
- Укажите диапазон суффиксов файлов:

```
CREATE TABLE table_with_range (name String, value UInt32)
    ENGINE = S3('https://clickhouse-public-datasets.s3.amazonaws.com/my-bucket/{some,another}_folder/some_file_{1..3}', 'CSV');

```

- Возьмите все файлы с префиксом `some_file_` (в обеих папках не должно быть других файлов с таким префиксом):

```
CREATE TABLE table_with_question_mark (name String, value UInt32)
    ENGINE = S3('https://clickhouse-public-datasets.s3.amazonaws.com/my-bucket/{some,another}_folder/some_file_?', 'CSV');

```

- Возьмите все файлы из обеих папок (все файлы должны соответствовать формату и схеме, указанным в запросе):

```
CREATE TABLE table_with_asterisk (name String, value UInt32)
    ENGINE = S3('https://clickhouse-public-datasets.s3.amazonaws.com/my-bucket/{some,another}_folder/*', 'CSV');

```


## Настройки хранилища

- [s3_truncate_on_insert](https://clickhouse.com/docs/ru/reference/settings/session-settings#s3_truncate_on_insert) - позволяет обрезать файл перед вставкой данных. По умолчанию отключена.
- [s3_create_new_file_on_insert](https://clickhouse.com/docs/ru/reference/settings/session-settings#s3_create_new_file_on_insert) - позволяет создавать новый файл при каждой вставке, если у формата есть суффикс. По умолчанию отключена.
- [s3_skip_empty_files](https://clickhouse.com/docs/ru/reference/settings/session-settings#s3_skip_empty_files) - позволяет пропускать пустые файлы при чтении. По умолчанию включена.

## Настройки, связанные с S3

- `s3_max_single_part_upload_size` — Максимальный размер объекта для загрузки в S3 с помощью singlepart upload. Значение по умолчанию — `32Mb`.
- `s3_min_upload_part_size` — Минимальный размер части, загружаемой при multipart-загрузке через [S3 Multipart upload](https://docs.aws.amazon.com/AmazonS3/latest/dev/uploadobjusingmpu.html). Значение по умолчанию — `16Mb`.
- `s3_max_redirects` — Максимально допустимое количество переходов при перенаправлениях S3. Значение по умолчанию — `10`.
- `s3_single_read_retries` — Максимальное количество попыток при одном чтении. Значение по умолчанию — `4`.
- `s3_max_put_rps` — Максимальная частота PUT-запросов в секунду до применения троттлинга. Значение по умолчанию — `0` (без ограничений).
- `s3_max_put_burst` — Максимальное количество запросов, которые можно отправить одновременно до достижения лимита запросов в секунду. По умолчанию (значение `0`) равно `s3_max_put_rps`.
- `s3_max_get_rps` — Максимальная частота GET-запросов в секунду до применения троттлинга. Значение по умолчанию — `0` (без ограничений).
- `s3_max_get_burst` — Максимальное количество запросов, которые можно отправить одновременно до достижения лимита запросов в секунду. По умолчанию (значение `0`) равно `s3_max_get_rps`.
- `s3_upload_part_size_multiply_factor` - Умножает `s3_min_upload_part_size` на этот коэффициент каждый раз, когда в рамках одной записи в S3 было загружено `s3_multiply_parts_count_threshold` частей. Значение по умолчанию — `2`.
- `s3_upload_part_size_multiply_parts_count_threshold` - Каждый раз, когда в S3 загружено такое количество частей, `s3_min_upload_part_size` умножается на `s3_upload_part_size_multiply_factor`. Значение по умолчанию — `500`.
- `s3_max_inflight_parts_for_one_file` - Ограничивает количество PUT-запросов, которые могут выполняться параллельно для одного объекта. Это число следует ограничивать. Значение `0` означает отсутствие ограничений. Значение по умолчанию — `20`. Для каждой части в процессе загрузки выделяется буфер размером `s3_min_upload_part_size` для первых `s3_upload_part_size_multiply_factor` частей и большего размера, если файл достаточно велик; см. `upload_part_size_multiply_factor`. При настройках по умолчанию загрузка одного файла размером менее `8G` потребляет не более `320Mb`. Для файлов большего размера потребление выше.

## Настройки для конечных точек

- `endpoint` — Задает префикс конечной точки. Обязательно.
- `access_key_id` и `secret_access_key` — Задают учетные данные, которые будут использоваться для данной конечной точки. Необязательно.
- `use_environment_credentials` — Если установлено значение `true`, клиент S3 попытается получить учетные данные из переменных окружения и метаданных [Amazon EC2](https://en.wikipedia.org/wiki/Amazon_Elastic_Compute_Cloud) для данной конечной точки. Необязательно, значение по умолчанию — `false`.
- `region` — Задает имя региона S3. Необязательно.
- `use_insecure_imds_request` — Если установлено значение `true`, клиент S3 будет использовать небезопасный запрос IMDS при получении учетных данных из метаданных Amazon EC2. Необязательно, значение по умолчанию — `false`.
- `expiration_window_seconds` — Льготный период для проверки того, не истек ли срок действия учетных данных. Необязательно, значение по умолчанию — `120`.
- `no_sign_request` - Игнорирует все учетные данные, чтобы запросы не подписывались. Полезно для доступа к публичным бакетам.
- `header` — Добавляет указанный HTTP-заголовок в запрос к данной конечной точке. Необязательно, можно указывать несколько раз.
- `access_header` - Добавляет указанный HTTP-заголовок в запрос к данной конечной точке в случаях, когда отсутствуют другие учетные данные из другого источника.
- `server_side_encryption_customer_key_base64` — Если указано, будут установлены необходимые заголовки для доступа к объектам S3 с шифрованием SSE-C. Необязательно.
- `server_side_encryption_kms_key_id` - Если указано, будут установлены необходимые заголовки для доступа к объектам S3 с [шифрованием SSE-KMS](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html). Если указана пустая строка, будет использоваться ключ S3 под управлением AWS. Необязательно.
- `server_side_encryption_kms_encryption_context` - Если указано вместе с `server_side_encryption_kms_key_id`, будет установлен указанный заголовок контекста шифрования для SSE-KMS. Необязательно.
- `server_side_encryption_kms_bucket_key_enabled` - Если указано вместе с `server_side_encryption_kms_key_id`, будет установлен заголовок для включения ключей S3 бакета для SSE-KMS. Необязательно, может быть `true` или `false`, по умолчанию не задано (соответствует настройке на уровне бакета).
- `max_single_read_retries` — Максимальное количество попыток в ходе одного чтения. Значение по умолчанию — `4`. Необязательно.
- `max_put_rps`, `max_put_burst`, `max_get_rps` и `max_get_burst` - Настройки ограничения скорости (см. описание выше), используемые для конкретной конечной точки вместо настроек на уровне запроса. Необязательно.

```
<s3>
    <endpoint-name>
        <endpoint>https://clickhouse-public-datasets.s3.amazonaws.com/my-test-bucket-768/</endpoint>
        <!-- <access_key_id>ACCESS_KEY_ID</access_key_id> -->
        <!-- <secret_access_key>SECRET_ACCESS_KEY</secret_access_key> -->
        <!-- <region>us-west-1</region> -->
        <!-- <use_environment_credentials>false</use_environment_credentials> -->
        <!-- <use_insecure_imds_request>false</use_insecure_imds_request> -->
        <!-- <expiration_window_seconds>120</expiration_window_seconds> -->
        <!-- <no_sign_request>false</no_sign_request> -->
        <!-- <header>Authorization: Bearer SOME-TOKEN</header> -->
        <!-- <server_side_encryption_customer_key_base64>BASE64-ENCODED-KEY</server_side_encryption_customer_key_base64> -->
        <!-- <server_side_encryption_kms_key_id>KMS_KEY_ID</server_side_encryption_kms_key_id> -->
        <!-- <server_side_encryption_kms_encryption_context>KMS_ENCRYPTION_CONTEXT</server_side_encryption_kms_encryption_context> -->
        <!-- <server_side_encryption_kms_bucket_key_enabled>true</server_side_encryption_kms_bucket_key_enabled> -->
        <!-- <max_single_read_retries>4</max_single_read_retries> -->
    </endpoint-name>
</s3>

```


## Работа с архивами

- ‘[https://s3-us-west-1.amazonaws.com/umbrella-static/top-1m-2018-01-10.csv.zip&#39](https://s3-us-west-1.amazonaws.com/umbrella-static/top-1m-2018-01-10.csv.zip&#39);
- ‘[https://s3-us-west-1.amazonaws.com/umbrella-static/top-1m-2018-01-11.csv.zip&#39](https://s3-us-west-1.amazonaws.com/umbrella-static/top-1m-2018-01-11.csv.zip&#39);
- ‘[https://s3-us-west-1.amazonaws.com/umbrella-static/top-1m-2018-01-12.csv.zip&#39](https://s3-us-west-1.amazonaws.com/umbrella-static/top-1m-2018-01-12.csv.zip&#39);

```
SELECT *
FROM s3(
   'https://s3-us-west-1.amazonaws.com/umbrella-static/top-1m-2018-01-1{0..2}.csv.zip :: *.csv'
);

```


## Доступ к публичным бакетам


```
CREATE TABLE big_table (name String, value UInt32)
    ENGINE = S3('https://datasets-documentation.s3.eu-west-3.amazonaws.com/aapl_stock.csv', NOSIGN, 'CSVWithNames');

```


## Оптимизация производительности


## Ролевой доступ


```
CREATE TABLE my_s3_table(name String, value UInt32)
ENGINE = S3('https://my-bucket.s3.amazonaws.com/data/*.csv', extra_credentials(role_arn = 'arn:aws:iam::111111111111:role/ClickHouseAccessRole-001'), 'CSV')

```


```
CREATE TABLE my_s3_table(name String, value UInt32)
ENGINE = S3('https://my-bucket.s3.amazonaws.com/data/*.csv', extra_credentials(role_arn = 'arn:aws:iam::111111111111:role/ClickHouseAccessRole-001', external_id = 'my-external-id'), 'CSV')

```


## См. также

- [табличная функция S3](https://clickhouse.com/docs/ru/reference/functions/table-functions/s3)
- [Интеграция S3 с ClickHouse](https://clickhouse.com/docs/ru/integrations/connectors/data-ingestion/AWS/integrating-s3-with-clickhouse)
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
