# Движки таблиц Replicated* - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/replication


```
ENGINE = ReplicatedMergeTree(
    '/clickhouse/tables/{shard}/table_name',
    '{replica}'
)

```


```
ENGINE = ReplicatedMergeTree

```

- ReplicatedSummingMergeTree
- ReplicatedCoalescingMergeTree
- ReplicatedVersionedCollapsingMergeTree
- ReplicatedCollapsingMergeTree
- ReplicatedGraphiteMergeTree
- ReplicatedMergeTree
- ReplicatedReplacingMergeTree
- ReplicatedAggregatingMergeTree
- Запрос `CREATE TABLE` создает новую реплицируемую таблицу на сервере, где он выполняется. Если эта таблица уже существует на других серверах, добавляется новая реплика.
- Запрос `DROP TABLE` удаляет реплику, расположенную на сервере, где он выполняется.
- Запрос `RENAME` переименовывает таблицу на одной из реплик. Иными словами, реплицируемые таблицы могут иметь разные имена на разных репликах.

```
<zookeeper>
    <node>
        <host>example1</host>
        <port>2181</port>
    </node>
    <node>
        <host>example2</host>
        <port>2181</port>
    </node>
    <node>
        <host>example3</host>
        <port>2181</port>
    </node>
</zookeeper>

```


```
<auxiliary_zookeepers>
    <zookeeper2>
        <node>
            <host>example_2_1</host>
            <port>2181</port>
        </node>
        <node>
            <host>example_2_2</host>
            <port>2181</port>
        </node>
        <node>
            <host>example_2_3</host>
            <port>2181</port>
        </node>
    </zookeeper2>
    <zookeeper3>
        <node>
            <host>example_3_1</host>
            <port>2181</port>
        </node>
    </zookeeper3>
</auxiliary_zookeepers>

```


```
CREATE TABLE table_name ( ... ) ENGINE = ReplicatedMergeTree('zookeeper_name_configured_in_auxiliary_zookeepers:path', 'replica_name') ...

```


## Создание таблиц с репликацией


### Параметры Replicated*MergeTree


| Параметр | Описание |
| --- | --- |
| `zoo_path` | Путь к таблице в ClickHouse Keeper. |
| `replica_name` | Имя реплики в ClickHouse Keeper. |
| `other_parameters` | Параметры движка, используемого для создания реплицируемой версии, например версия в `ReplacingMergeTree`. |


```
CREATE TABLE table_name
(
    EventDate DateTime,
    CounterID UInt32,
    UserID UInt32,
    ver UInt16
)
ENGINE = ReplicatedReplacingMergeTree('/clickhouse/tables/{layer}-{shard}/table_name', '{replica}', ver)
PARTITION BY toYYYYMM(EventDate)
ORDER BY (CounterID, EventDate, intHash32(UserID))
SAMPLE BY intHash32(UserID);

```


```
<macros>
    <shard>02</shard>
    <replica>example05-02-1</replica>
</macros>

```


```
<default_replica_path>/clickhouse/tables/{shard}/{database}/{table}</default_replica_path>
<default_replica_name>{replica}</default_replica_name>

```


```
CREATE TABLE table_name (
    x UInt32
) ENGINE = ReplicatedMergeTree
ORDER BY x;

```


```
CREATE TABLE table_name (
    x UInt32
) ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/{database}/table_name', '{replica}')
ORDER BY x;

```


## Восстановление после сбоев


```
sudo -u clickhouse touch /var/lib/clickhouse/flags/force_restore_data

```


## Восстановление после полной потери данных

- Установите ClickHouse на сервер. Если вы используете подстановки, правильно задайте их в config-файле, содержащем идентификаторы сегмента и реплики.
- Если у вас были нереплицируемые таблицы, данные которых нужно вручную скопировать на серверы, скопируйте их с реплики (из каталога `/var/lib/clickhouse/data/db_name/table_name/`).
- Скопируйте с реплики определения таблиц, расположенные в `/var/lib/clickhouse/metadata/`. Если идентификатор сегмента или реплики явно указан в определениях таблиц, исправьте его так, чтобы он соответствовал этой реплике. (Либо запустите сервер и выполните все запросы `ATTACH TABLE`, которые должны были находиться в .sql-файлах в `/var/lib/clickhouse/metadata/`.)
- Чтобы начать восстановление, создайте узел ClickHouse Keeper `/path_to_table/replica_name/flags/force_restore_data` с любым содержимым или выполните команду для восстановления всех реплицируемых таблиц: `sudo -u clickhouse touch /var/lib/clickhouse/flags/force_restore_data`

## Преобразование из MergeTree в ReplicatedMergeTree


```
SELECT data_paths FROM system.tables WHERE table = 'table_name' AND database = 'database_name';

```


```
SELECT zookeeper_path FROM system.replicas WHERE table = 'table_name';

```


## Преобразование ReplicatedMergeTree в MergeTree

- Удалите соответствующий файл `.sql` в каталоге метаданных (`/var/lib/clickhouse/metadata/`).
- Удалите соответствующий путь в ClickHouse Keeper (`/path_to_table/replica_name`).

## Восстановление при потере или повреждении метаданных в кластере ClickHouse Keeper

- [background_schedule_pool_size](https://clickhouse.com/docs/ru/reference/settings/server-settings/settings#background_schedule_pool_size)
- [background_fetches_pool_size](https://clickhouse.com/docs/ru/reference/settings/server-settings/settings#background_fetches_pool_size)
- [execute_merges_on_single_replica_time_threshold](https://clickhouse.com/docs/ru/reference/settings/merge-tree-settings#execute_merges_on_single_replica_time_threshold)
- [max_replicated_fetches_network_bandwidth](https://clickhouse.com/docs/ru/reference/settings/merge-tree-settings#max_replicated_fetches_network_bandwidth)
- [max_replicated_sends_network_bandwidth](https://clickhouse.com/docs/ru/reference/settings/merge-tree-settings#max_replicated_sends_network_bandwidth)
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
