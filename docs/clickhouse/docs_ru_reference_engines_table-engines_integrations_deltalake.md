# Движок таблицы DeltaLake - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/deltalake


## Создание таблицы DeltaLake


```
CREATE TABLE table_name
ENGINE = DeltaLake(url, [aws_access_key_id, aws_secret_access_key,] [extra_credentials])

```

- `url` — URL бакета с путём к существующей таблице Delta Lake.
- `aws_access_key_id`, `aws_secret_access_key` - Долговременные учётные данные пользователя аккаунта [AWS](https://aws.amazon.com/). Их можно использовать для аутентификации запросов. Параметр необязателен. Если учётные данные не указаны, они берутся из файла конфигурации.
- `extra_credentials` - Необязательный параметр. Используется для передачи `role_arn` при доступе на основе ролей в ClickHouse Cloud. Шаги по настройке см. в разделе [Secure S3](https://clickhouse.com/docs/ru/products/cloud/guides/data-sources/accessing-s3-data-securely).

```
CREATE TABLE deltalake
ENGINE = DeltaLake('http://mars-doc-test.s3.amazonaws.com/clickhouse-bucket-3/test_table/', 'ABC123', 'Abc+123')

```


```
<clickhouse>
    <named_collections>
        <deltalake_conf>
            <url>http://mars-doc-test.s3.amazonaws.com/clickhouse-bucket-3/</url>
            <access_key_id>ABC123</access_key_id>
            <secret_access_key>Abc+123</secret_access_key>
        </deltalake_conf>
    </named_collections>
</clickhouse>

```


```
CREATE TABLE deltalake
ENGINE = DeltaLake(deltalake_conf, filename = 'test_table')

```


```
-- Использование HTTPS URL (рекомендуется)
CREATE TABLE table_name
ENGINE = DeltaLake('https://storage.googleapis.com/<bucket>/<path>/', '<access_key_id>', '<secret_access_key>')

```

- `url` — URL GCS-бакета для таблицы Delta Lake. Должен использовать формат `https://storage.googleapis.com/<bucket>/<path>/` (конечная точка GCS XML API) или `gs://<bucket>/<path>/`, который автоматически преобразуется.
- `access_key_id` — ключ доступа GCS. Создаётся через Google Cloud Console → Cloud Storage → Settings → Interoperability.
- `secret_access_key` — секретный ключ GCS.

```
CREATE NAMED COLLECTION gcs_creds AS
access_key_id = '<access_key>',
secret_access_key = '<secret>';

CREATE TABLE gcpDeltaLake
ENGINE = DeltaLake(gcs_creds, url = 'https://storage.googleapis.com/<bucket>/<path>')

```


```
CREATE TABLE table_name
ENGINE = DeltaLake(connection_string|storage_account_url, container_name, blobpath, [account_name, account_key, format, compression])

```

- `connection_string` — строка подключения Azure
- `storage_account_url` — URL учётной записи хранилища Azure (например, [https://account.blob.core.windows.net](https://account.blob.core.windows.net))
- `container_name` — имя контейнера Azure
- `blobpath` — путь к таблице Delta Lake внутри контейнера
- `account_name` — имя учётной записи хранилища Azure
- `account_key` — ключ учётной записи хранилища Azure

## Запись данных с помощью таблицы DeltaLake


```
SET allow_delta_lake_writes = 1;

INSERT INTO deltalake(id, firstname, lastname, gender, age)
VALUES (1, 'John', 'Smith', 'M', 32);

```


### Кэширование данных


## См. также

- [Табличная функция deltaLake](https://clickhouse.com/docs/ru/reference/functions/table-functions/deltalake)
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
