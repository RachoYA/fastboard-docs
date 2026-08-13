# system.backup_log - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/system-tables/backup_log


## Описание


## Столбцы

- `hostname` ([LowCardinality(String)](https://clickhouse.com/docs/ru/reference/data-types/lowcardinality)) — Имя хоста сервера, выполняющего запрос.
- `event_date` ([Date](https://clickhouse.com/docs/ru/reference/data-types/date)) — Дата записи.
- `event_time` ([DateTime](https://clickhouse.com/docs/ru/reference/data-types/datetime)) — Время записи.
- `event_time_microseconds` ([DateTime64(6)](https://clickhouse.com/docs/ru/reference/data-types/datetime64)) — Время записи с точностью до микросекунд.
- `id` ([String](https://clickhouse.com/docs/ru/reference/data-types/string)) — Идентификатор операции резервного копирования или восстановления.
- `name` ([String](https://clickhouse.com/docs/ru/reference/data-types/string)) — Имя хранилища резервной копии (содержимое предложения `FROM` или `TO`).
- `base_backup_name` ([String](https://clickhouse.com/docs/ru/reference/data-types/string)) — Имя базовой резервной копии в случае инкрементной резервной копии.
- `query_id` ([String](https://clickhouse.com/docs/ru/reference/data-types/string)) — Идентификатор запроса, связанного с операцией резервного копирования.
- `status` ([Enum8(‘CREATING_BACKUP’ = 0, ‘BACKUP_CREATED’ = 1, ‘BACKUP_FAILED’ = 2, ‘RESTORING’ = 3, ‘RESTORED’ = 4, ‘RESTORE_FAILED’ = 5, ‘BACKUP_CANCELLED’ = 6, ‘RESTORE_CANCELLED’ = 7)](https://clickhouse.com/docs/ru/reference/data-types/enum)) — Статус операции.
- `error` ([String](https://clickhouse.com/docs/ru/reference/data-types/string)) — Сообщение об ошибке для неуспешной операции (пустая строка для успешных операций).
- `start_time` ([DateTime64(6)](https://clickhouse.com/docs/ru/reference/data-types/datetime64)) — Время начала операции.
- `end_time` ([DateTime64(6)](https://clickhouse.com/docs/ru/reference/data-types/datetime64)) — Время завершения операции.
- `num_files` ([UInt64](https://clickhouse.com/docs/ru/reference/data-types/int-uint)) — Количество файлов, сохранённых в резервной копии.
- `total_size` ([UInt64](https://clickhouse.com/docs/ru/reference/data-types/int-uint)) — Общий размер файлов, сохранённых в резервной копии.
- `num_entries` ([UInt64](https://clickhouse.com/docs/ru/reference/data-types/int-uint)) — Количество записей в резервной копии, то есть количество файлов в папке, если резервная копия хранится в виде папки, или количество файлов в архиве, если резервная копия хранится в виде архива. Это не то же самое, что `num_files`, если это инкрементная резервная копия или если она содержит пустые файлы либо дубликаты. Всегда верно следующее: `num_entries ≤ num_files`.
- `uncompressed_size` ([UInt64](https://clickhouse.com/docs/ru/reference/data-types/int-uint)) — Размер резервной копии в несжатом виде.
- `compressed_size` ([UInt64](https://clickhouse.com/docs/ru/reference/data-types/int-uint)) — Размер резервной копии в сжатом виде. Если резервная копия не хранится в виде архива, он равен `uncompressed_size`.
- `files_read` ([UInt64](https://clickhouse.com/docs/ru/reference/data-types/int-uint)) — Количество файлов, прочитанных в ходе операции восстановления.
- `bytes_read` ([UInt64](https://clickhouse.com/docs/ru/reference/data-types/int-uint)) — Общий размер файлов, прочитанных в ходе операции восстановления.
- `settings` ([Map(LowCardinality(String), String)](https://clickhouse.com/docs/ru/reference/data-types/map)) — Настройки резервного копирования/восстановления, фактически использованные для этой операции (из предложения `SETTINGS`, включая значения по умолчанию). Конфиденциальные настройки не раскрываются.
- `engine_settings` ([Map(LowCardinality(String), String)](https://clickhouse.com/docs/ru/reference/data-types/map)) — Настройки, фактически использованные средством чтения/записи движка резервного копирования (например, S3 `allow_native_copy`). Пусто, если в операции задействовано более одного движка и это нельзя представить в виде плоской map: инкрементные резервные копии и восстановления, восстановления легковесных снимков и невнутренние операции `ON CLUSTER`.

## Пример


```
BACKUP TABLE test_db.my_table TO Disk('backups_disk', '1.zip')

```


```
┌─id───────────────────────────────────┬─status─────────┐
│ e5b74ecb-f6f1-426a-80be-872f90043885 │ BACKUP_CREATED │
└──────────────────────────────────────┴────────────────┘

```


```
SELECT hostname, event_date, event_time_microseconds, id, name, status, error, start_time, end_time, num_files, total_size, num_entries, uncompressed_size, compressed_size, files_read, bytes_read FROM system.backup_log WHERE id = 'e5b74ecb-f6f1-426a-80be-872f90043885' ORDER BY event_date, event_time_microseconds \G

```


```
Row 1:
──────
hostname:                clickhouse.eu-central1.internal
event_date:              2023-08-19
event_time_microseconds: 2023-08-19 11:05:21.998566
id:                      e5b74ecb-f6f1-426a-80be-872f90043885
name:                    Disk('backups_disk', '1.zip')
status:                  CREATING_BACKUP
error:                   
start_time:              2023-08-19 11:05:21
end_time:                1970-01-01 03:00:00
num_files:               0
total_size:              0
num_entries:             0
uncompressed_size:       0
compressed_size:         0
files_read:              0
bytes_read:              0

Row 2:
──────
hostname:                clickhouse.eu-central1.internal
event_date:              2023-08-19
event_time:              2023-08-19 11:08:56
event_time_microseconds: 2023-08-19 11:08:56.916192
id:                      e5b74ecb-f6f1-426a-80be-872f90043885
name:                    Disk('backups_disk', '1.zip')
status:                  BACKUP_CREATED
error:                   
start_time:              2023-08-19 11:05:21
end_time:                2023-08-19 11:08:56
num_files:               57
total_size:              4290364870
num_entries:             46
uncompressed_size:       4290362365
compressed_size:         3525068304
files_read:              0
bytes_read:              0

```


```
RESTORE TABLE test_db.my_table FROM Disk('backups_disk', '1.zip')

```


```
┌─id───────────────────────────────────┬─status───┐
│ cdf1f731-52ef-42da-bc65-2e1bfcd4ce90 │ RESTORED │
└──────────────────────────────────────┴──────────┘

```


```
SELECT hostname, event_date, event_time_microseconds, id, name, status, error, start_time, end_time, num_files, total_size, num_entries, uncompressed_size, compressed_size, files_read, bytes_read FROM system.backup_log WHERE id = 'cdf1f731-52ef-42da-bc65-2e1bfcd4ce90' ORDER BY event_date, event_time_microseconds \G

```


```
Row 1:
──────
hostname:                clickhouse.eu-central1.internal
event_date:              2023-08-19
event_time_microseconds: 2023-08-19 11:09:19.718077
id:                      cdf1f731-52ef-42da-bc65-2e1bfcd4ce90
name:                    Disk('backups_disk', '1.zip')
status:                  RESTORING
error:                   
start_time:              2023-08-19 11:09:19
end_time:                1970-01-01 03:00:00
num_files:               0
total_size:              0
num_entries:             0
uncompressed_size:       0
compressed_size:         0
files_read:              0
bytes_read:              0

Row 2:
──────
hostname:                clickhouse.eu-central1.internal
event_date:              2023-08-19
event_time_microseconds: 2023-08-19 11:09:29.334234
id:                      cdf1f731-52ef-42da-bc65-2e1bfcd4ce90
name:                    Disk('backups_disk', '1.zip')
status:                  RESTORED
error:                   
start_time:              2023-08-19 11:09:19
end_time:                2023-08-19 11:09:29
num_files:               57
total_size:              4290364870
num_entries:             46
uncompressed_size:       4290362365
compressed_size:         4290362365
files_read:              57
bytes_read:              4290364870

```


```
SELECT id, name, status, error, start_time, end_time, num_files, total_size, num_entries, uncompressed_size, compressed_size, files_read, bytes_read FROM system.backups ORDER BY start_time

```


```
┌─id───────────────────────────────────┬─name──────────────────────────┬─status─────────┬─error─┬──────────start_time─┬────────────end_time─┬─num_files─┬─total_size─┬─num_entries─┬─uncompressed_size─┬─compressed_size─┬─files_read─┬─bytes_read─┐
│ e5b74ecb-f6f1-426a-80be-872f90043885 │ Disk('backups_disk', '1.zip') │ BACKUP_CREATED │       │ 2023-08-19 11:05:21 │ 2023-08-19 11:08:56 │        57 │ 4290364870 │          46 │        4290362365 │      3525068304 │          0 │          0 │
│ cdf1f731-52ef-42da-bc65-2e1bfcd4ce90 │ Disk('backups_disk', '1.zip') │ RESTORED       │       │ 2023-08-19 11:09:19 │ 2023-08-19 11:09:29 │        57 │ 4290364870 │          46 │        4290362365 │      4290362365 │         57 │ 4290364870 │
└──────────────────────────────────────┴───────────────────────────────┴────────────────┴───────┴─────────────────────┴─────────────────────┴───────────┴────────────┴─────────────┴───────────────────┴─────────────────┴────────────┴────────────┘

```


## См. также

- [Резервное копирование и восстановление](https://clickhouse.com/docs/ru/concepts/features/backup-restore/overview)
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
