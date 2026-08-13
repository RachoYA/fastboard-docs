# Движок таблицы AzureBlobStorage - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/azureBlobStorage


## CREATE TABLE


```
CREATE TABLE azure_blob_storage_table (name String, value UInt32)
    ENGINE = AzureBlobStorage(connection_string|storage_account_url, container_name, blobpath, [account_name, account_key, format, compression, partition_strategy, partition_columns_in_data_file, extra_credentials(client_id=, tenant_id=)])
    [PARTITION BY expr]
    [SETTINGS ...]

```


### Параметры движка

- `endpoint` — URL конечной точки AzureBlobStorage с контейнером и префиксом. При необходимости также может содержать account_name, если этого требует используемый метод аутентификации. (`http://azurite1:{port}/[account_name]{container_name}/{data_prefix}`) Либо эти параметры можно передать отдельно через storage_account_url, account_name и container. Для указания префикса следует использовать endpoint.
- `endpoint_contains_account_name` - Этот флаг указывает, содержит ли endpoint account_name, так как он нужен только для некоторых методов аутентификации. (По умолчанию: true)
- `connection_string|storage_account_url` — connection_string включает имя учётной записи и ключ ([Create connection string](https://learn.microsoft.com/en-us/azure/storage/common/storage-configure-connection-string?toc=%2Fazure%2Fstorage%2Fblobs%2Ftoc.json&bc=%2Fazure%2Fstorage%2Fblobs%2Fbreadcrumb%2Ftoc.json#configure-a-connection-string-for-an-azure-storage-account)), либо здесь можно указать URL учётной записи хранилища, а имя учётной записи и ключ учётной записи передать отдельными параметрами (см. параметры account_name и account_key)
- `container_name` - Имя контейнера
- `blobpath` - путь к файлу. В режиме только для чтения поддерживаются следующие подстановочные шаблоны: `*`, `**`, `?`, `{abc,def}` и `{N..M}`, где `N`, `M` — числа, `'abc'`, `'def'` — строки.
- `account_name` - если используется storage_account_url, здесь можно указать имя учётной записи
- `account_key` - если используется storage_account_url, здесь можно указать ключ учётной записи
- `format` — [Формат](https://clickhouse.com/docs/ru/reference/formats/index) файла.
- `compression` — Поддерживаемые значения: `none`, `gzip/gz`, `brotli/br`, `xz/LZMA`, `zstd/zst`. По умолчанию сжатие определяется автоматически по расширению файла. (то же самое, что установить `auto`).
- `partition_strategy` – Варианты: `wildcard` или `hive`. Для `wildcard` требуется `{_partition_id}` в пути, который заменяется ключом партиционирования. `hive` не допускает подстановочных шаблонов, предполагает, что путь является корнем таблицы, и создаёт каталоги партиций в стиле Hive, где в качестве имён файлов используются Snowflake ID, а в качестве расширения — формат файла. По умолчанию используется настройка `file_like_engine_default_partition_strategy` (`wildcard` при настройках `compatibility` старее `26.6`, иначе `hive`).
- `partition_columns_in_data_file` - Используется только со стратегией партиционирования `hive`. Указывает ClickHouse, следует ли ожидать, что столбцы партиции будут записаны в файл данных. По умолчанию `false`.
- `extra_credentials` - Используйте `client_id` и `tenant_id` для аутентификации. Если указаны extra_credentials, они имеют приоритет над `account_name` и `account_key`.

```
CREATE TABLE test_table (key UInt64, data String)
    ENGINE = AzureBlobStorage('DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://azurite1:10000/devstoreaccount1/;', 'testcontainer', 'test_table', 'CSV');

INSERT INTO test_table VALUES (1, 'a'), (2, 'b'), (3, 'c');

SELECT * FROM test_table;

```


```
┌─key──┬─data──┐
│  1   │   a   │
│  2   │   b   │
│  3   │   c   │
└──────┴───────┘

```


## Виртуальные столбцы

- `_path` — Путь к файлу. Тип: `LowCardinality(String)`.
- `_file` — Имя файла. Тип: `LowCardinality(String)`.
- `_size` — Размер файла в байтах. Тип: `Nullable(UInt64)`. Если размер неизвестен, значение — `NULL`.
- `_time` — Время последнего изменения файла. Тип: `Nullable(DateTime)`. Если время неизвестно, значение — `NULL`.

## Аутентификация

- `Managed Identity` — можно использовать, указав `endpoint`, `connection_string` или `storage_account_url`.
- `SAS Token` — можно использовать, указав `endpoint`, `connection_string` или `storage_account_url`. Определяется по наличию символа `?` в URL. Примеры см. в [azureBlobStorage](https://clickhouse.com/docs/ru/reference/functions/table-functions/azureBlobStorage#using-shared-access-signatures-sas-sas-tokens).
- `Workload Identity` — можно использовать, указав `endpoint` или `storage_account_url`. Если в конфигурации задан параметр `use_workload_identity`, для аутентификации используется [workload identity](https://github.com/Azure/azure-sdk-for-cpp/tree/main/sdk/identity/azure-identity#authenticate-azure-hosted-applications).

### Кэш данных


```
SELECT *
FROM azureBlobStorage('DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://azurite1:10000/devstoreaccount1/;', 'testcontainer', 'test_table', 'CSV')
SETTINGS filesystem_cache_name = 'cache_for_azure', enable_filesystem_cache = 1;

```

- добавьте в файл конфигурации ClickHouse следующий раздел:

```
<clickhouse>
    <filesystem_caches>
        <cache_for_azure>
            <path>path to cache directory</path>
            <max_size>10Gi</max_size>
        </cache_for_azure>
    </filesystem_caches>
</clickhouse>

```

- повторно использовать конфигурацию кэша (и, следовательно, хранилище кэша) из раздела `storage_configuration` ClickHouse, [описанного здесь](https://clickhouse.com/docs/ru/concepts/features/configuration/server-config/storing-data#using-local-cache)

### PARTITION BY


#### Стратегия партиционирования


```
create table azure_table (year UInt16, country String, counter UInt8) ENGINE=AzureBlobStorage(account_name='devstoreaccount1', account_key='Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==', storage_account_url = 'http://localhost:30000/devstoreaccount1', container='cont', blob_path='hive_partitioned', format='Parquet', compression='auto', partition_strategy='hive') PARTITION BY (year, country);

insert into azure_table values (2020, 'Russia', 1), (2021, 'Brazil', 2);

select _path, * from azure_table;

```


```
┌─_path──────────────────────────────────────────────────────────────────────┬─year─┬─country─┬─counter─┐
│ cont/hive_partitioned/year=2020/country=Russia/7351305360873664512.parquet │ 2020 │ Russia  │       1 │
│ cont/hive_partitioned/year=2021/country=Brazil/7351305360894636032.parquet │ 2021 │ Brazil  │       2 │
└────────────────────────────────────────────────────────────────────────────┴──────┴─────────┴─────────┘

```


## См. также

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
