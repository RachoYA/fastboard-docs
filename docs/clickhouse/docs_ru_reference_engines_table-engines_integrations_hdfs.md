# Движок таблицы HDFS - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/hdfs


## Использование


```
ENGINE = HDFS(URI, format)

```

- `URI` — полный URI файла в HDFS. Часть пути в `URI` может содержать глоб-шаблоны. В этом случае таблица будет доступна только для чтения.
- `format` — задаёт один из доступных форматов файлов. Чтобы выполнять запросы `SELECT`, формат должен поддерживать ввод, а для выполнения запросов `INSERT` — вывод. Доступные форматы перечислены в разделе [Форматы](https://clickhouse.com/docs/ru/reference/formats/index#formats-overview).
- [PARTITION BY expr]

### PARTITION BY


```
CREATE TABLE hdfs_engine_table (name String, value UInt32) ENGINE=HDFS('hdfs://hdfs1:9000/other_storage', 'TSV')

```


```
INSERT INTO hdfs_engine_table VALUES ('one', 1), ('two', 2), ('three', 3)

```


```
SELECT * FROM hdfs_engine_table LIMIT 2

```


```
┌─name─┬─value─┐
│ one  │     1 │
│ two  │     2 │
└──────┴───────┘

```


## Подробности реализации

- Чтение и запись могут выполняться параллельно.
- Не поддерживаются:
- Операции `ALTER` и `SELECT...SAMPLE`.
- Индексы.
- [Репликация с нулевым копированием](https://clickhouse.com/docs/ru/concepts/features/configuration/server-config/storing-data#zero-copy) возможна, но не рекомендуется.
- `*` — Подставляет любое количество любых символов, кроме `/`, включая пустую строку.
- `?` — Подставляет любой одиночный символ.
- `{some_string,another_string,yet_another_one}` — Подставляет любую из строк `'some_string', 'another_string', 'yet_another_one'`.
- `{N..M}` — Подставляет любое число в диапазоне от N до M включительно.
- Предположим, у нас есть несколько файлов в формате TSV со следующими URI в HDFS:
- ‘hdfs://hdfs1:9000/some_dir/some_file_1’
- ‘hdfs://hdfs1:9000/some_dir/some_file_2’
- ‘hdfs://hdfs1:9000/some_dir/some_file_3’
- ‘hdfs://hdfs1:9000/another_dir/some_file_1’
- ‘hdfs://hdfs1:9000/another_dir/some_file_2’
- ‘hdfs://hdfs1:9000/another_dir/some_file_3’
- Существует несколько способов создать таблицу, включающую все шесть файлов:

```
CREATE TABLE table_with_range (name String, value UInt32) ENGINE = HDFS('hdfs://hdfs1:9000/{some,another}_dir/some_file_{1..3}', 'TSV')

```


```
CREATE TABLE table_with_question_mark (name String, value UInt32) ENGINE = HDFS('hdfs://hdfs1:9000/{some,another}_dir/some_file_?', 'TSV')

```


```
CREATE TABLE table_with_asterisk (name String, value UInt32) ENGINE = HDFS('hdfs://hdfs1:9000/{some,another}_dir/*', 'TSV')

```


```
CREATE TABLE big_table (name String, value UInt32) ENGINE = HDFS('hdfs://hdfs1:9000/big_dir/file{0..9}{0..9}{0..9}', 'CSV')

```


## Конфигурация


```
<!-- Global configuration options for HDFS engine type -->
<hdfs>
<hadoop_kerberos_keytab>/tmp/keytab/clickhouse.keytab</hadoop_kerberos_keytab>
<hadoop_kerberos_principal>clickuser@TEST.CLICKHOUSE.TECH</hadoop_kerberos_principal>
<hadoop_security_authentication>kerberos</hadoop_security_authentication>
</hdfs>

<!-- Configuration specific for user "root" -->
<hdfs_root>
<hadoop_kerberos_principal>root@TEST.CLICKHOUSE.TECH</hadoop_kerberos_principal>
</hdfs_root>

```


### Параметры конфигурации


#### Поддерживается в libhdfs3


| **параметр** | **значение по умолчанию** |
| --- | --- |
| rpc_client_connect_tcpnodelay | true |
| dfs_client_read_shortcircuit | true |
| output_replace-datanode-on-failure | true |
| input_notretry-another-node | false |
| input_localread_mappedfile | true |
| dfs_client_use_legacy_blockreader_local | false |
| rpc_client_ping_interval | 10 * 1000 |
| rpc_client_connect_timeout | 600 * 1000 |
| rpc_client_read_timeout | 3600 * 1000 |
| rpc_client_write_timeout | 3600 * 1000 |
| rpc_client_socket_linger_timeout | -1 |
| rpc_client_connect_retry | 10 |
| rpc_client_timeout | 3600 * 1000 |
| dfs_default_replica | 3 |
| input_connect_timeout | 600 * 1000 |
| input_read_timeout | 3600 * 1000 |
| input_write_timeout | 3600 * 1000 |
| input_localread_default_buffersize | 1 * 1024 * 1024 |
| dfs_prefetchsize | 10 |
| input_read_getblockinfo_retry | 3 |
| input_localread_blockinfo_cachesize | 1000 |
| input_read_max_retry | 60 |
| output_default_chunksize | 512 |
| output_default_packetsize | 64 * 1024 |
| output_default_write_retry | 10 |
| output_connect_timeout | 600 * 1000 |
| output_read_timeout | 3600 * 1000 |
| output_write_timeout | 3600 * 1000 |
| output_close_timeout | 3600 * 1000 |
| output_packetpool_size | 1024 |
| output_heartbeat_interval | 10 * 1000 |
| dfs_client_failover_max_attempts | 15 |
| dfs_client_read_shortcircuit_streams_cache_size | 256 |
| dfs_client_socketcache_expiryMsec | 3000 |
| dfs_client_socketcache_capacity | 16 |
| dfs_default_blocksize | 64 * 1024 * 1024 |
| dfs_default_uri | ”hdfs://localhost:9000” |
| hadoop_security_authentication | ”simple” |
| hadoop_security_kerberos_ticket_cache_path | "" |
| dfs_client_log_severity | ”INFO” |
| dfs_domain_socket_path | "" |


#### Дополнительные параметры ClickHouse


| **параметр** | **значение по умолчанию** |
| --- | --- |
| hadoop_kerberos_keytab | "" |
| hadoop_kerberos_principal | "" |
| libhdfs3_conf | "" |


### Ограничения

- `hadoop_security_kerberos_ticket_cache_path` и `libhdfs3_conf` могут быть только глобальными, а не пользовательскими

## Поддержка Kerberos


## Поддержка HA для NameNode в HDFS

- Скопируйте `hdfs-site.xml` с узла HDFS в `/etc/clickhouse-server/`.
- Добавьте следующий фрагмент в файл конфигурации ClickHouse:

```
<hdfs>
    <libhdfs3_conf>/etc/clickhouse-server/hdfs-site.xml</libhdfs3_conf>
</hdfs>

```

- Затем используйте значение тега `dfs.nameservices` из `hdfs-site.xml` в качестве адреса NameNode в URI HDFS. Например, замените `hdfs://appadmin@192.168.101.11:8020/abc/` на `hdfs://appadmin@my_nameservice/abc/`.

## Виртуальные столбцы

- `_path` — Путь к файлу. Тип: `LowCardinality(String)`.
- `_file` — Имя файла. Тип: `LowCardinality(String)`.
- `_size` — Размер файла в байтах. Тип: `Nullable(UInt64)`. Если размер неизвестен, значение — `NULL`.
- `_time` — Время последнего изменения файла. Тип: `Nullable(DateTime)`. Если время неизвестно, значение — `NULL`.

## Настройки хранилища

- [hdfs_truncate_on_insert](https://clickhouse.com/docs/ru/reference/settings/session-settings#hdfs_truncate_on_insert) - позволяет обрезать файл перед вставкой в него. По умолчанию отключено.
- [hdfs_create_new_file_on_insert](https://clickhouse.com/docs/ru/reference/settings/session-settings#hdfs_create_new_file_on_insert) - позволяет создавать новый файл при каждой вставке, если у формата есть суффикс. По умолчанию отключено.
- [hdfs_skip_empty_files](https://clickhouse.com/docs/ru/reference/settings/session-settings#hdfs_skip_empty_files) - позволяет пропускать пустые файлы при чтении. По умолчанию отключено.
- [Виртуальные столбцы](https://clickhouse.com/docs/ru/reference/engines/table-engines/index#table_engines-virtual_columns)
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
