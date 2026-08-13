# system.aggregated_zookeeper_log - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/system-tables/aggregated_zookeeper_log


## Описание


## Столбцы

- `hostname` ([LowCardinality(String)](https://clickhouse.com/docs/ru/reference/data-types/lowcardinality)) — Имя хоста сервера.
- `event_date` ([Date](https://clickhouse.com/docs/ru/reference/data-types/date)) — Дата сброса группы на диск.
- `event_time` ([DateTime](https://clickhouse.com/docs/ru/reference/data-types/datetime)) — Время сброса группы на диск.
- `session_id` ([Int64](https://clickhouse.com/docs/ru/reference/data-types/int-uint)) — Идентификатор сеанса.
- `parent_path` ([String](https://clickhouse.com/docs/ru/reference/data-types/string)) — Префикс пути.
- `operation` ([Enum16(‘Close’ = -11, ‘Error’ = -1, ‘Watch’ = 0, ‘Create’ = 1, ‘Remove’ = 2, ‘Exists’ = 3, ‘Get’ = 4, ‘Set’ = 5, ‘GetACL’ = 6, ‘SetACL’ = 7, ‘SimpleList’ = 8, ‘Sync’ = 9, ‘Heartbeat’ = 11, ‘List’ = 12, ‘Check’ = 13, ‘Multi’ = 14, ‘Create2’ = 15, ‘Reconfig’ = 16, ‘CheckWatch’ = 17, ‘RemoveWatch’ = 18, ‘MultiRead’ = 22, ‘Auth’ = 100, ‘SetWatch’ = 101, ‘SetWatch2’ = 105, ‘AddWatch’ = 106, ‘FilteredList’ = 500, ‘CheckNotExists’ = 501, ‘CreateIfNotExists’ = 502, ‘RemoveRecursive’ = 503, ‘CheckStat’ = 504, ‘TryRemove’ = 505, ‘FilteredListWithStatsAndData’ = 506, ‘ListRecursive’ = 507, ‘SessionID’ = 997)](https://clickhouse.com/docs/ru/reference/data-types/enum)) — Тип операции ZooKeeper.
- `is_subrequest` ([UInt8](https://clickhouse.com/docs/ru/reference/data-types/int-uint)) — Является ли эта операция подзапросом в рамках операции Multi или MultiRead.
- `count` ([UInt32](https://clickhouse.com/docs/ru/reference/data-types/int-uint)) — Количество операций в группе (session_id, parent_path, operation, component, is_subrequest).
- `errors` ([Map(Enum8(‘ZNOWATCHER’ = -121, ‘ZNOTREADONLY’ = -119, ‘ZSESSIONMOVED’ = -118, ‘ZNOTHING’ = -117, ‘ZCLOSING’ = -116, ‘ZAUTHFAILED’ = -115, ‘ZINVALIDACL’ = -114, ‘ZINVALIDCALLBACK’ = -113, ‘ZSESSIONEXPIRED’ = -112, ‘ZNOTEMPTY’ = -111, ‘ZNODEEXISTS’ = -110, ‘ZNOCHILDRENFOREPHEMERALS’ = -108, ‘ZBADVERSION’ = -103, ‘ZNOAUTH’ = -102, ‘ZNONODE’ = -101, ‘ZAPIERROR’ = -100, ‘ZOUTOFMEMORY’ = -10, ‘ZINVALIDSTATE’ = -9, ‘ZBADARGUMENTS’ = -8, ‘ZOPERATIONTIMEOUT’ = -7, ‘ZUNIMPLEMENTED’ = -6, ‘ZMARSHALLINGERROR’ = -5, ‘ZCONNECTIONLOSS’ = -4, ‘ZDATAINCONSISTENCY’ = -3, ‘ZRUNTIMEINCONSISTENCY’ = -2, ‘ZSYSTEMERROR’ = -1, ‘ZOK’ = 0), UInt32)](https://clickhouse.com/docs/ru/reference/data-types/map)) — Ошибки в группе (session_id, parent_path, operation, component, is_subrequest).
- `average_latency` ([Float64](https://clickhouse.com/docs/ru/reference/data-types/float)) — Средняя задержка по всем операциям в группе (session_id, parent_path, operation, component, is_subrequest), в микросекундах. Для подзапросов задержка равна нулю, поскольку она относится к внешней операции Multi или MultiRead.
- `component` ([LowCardinality(String)](https://clickhouse.com/docs/ru/reference/data-types/lowcardinality)) — Компонент, вызвавший это событие.

## См. также

- [system.zookeeper_log](https://clickhouse.com/docs/ru/reference/system-tables/zookeeper_log) — Подробный журнал ZooKeeper для каждого запроса.
- [ZooKeeper](https://clickhouse.com/docs/ru/guides/oss/best-practices/tips#zookeeper)
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
