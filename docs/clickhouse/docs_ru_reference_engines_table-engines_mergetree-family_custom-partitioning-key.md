# Пользовательский ключ партиционирования - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/custom-partitioning-key


```
CREATE TABLE visits
(
    VisitDate Date,
    Hour UInt8,
    ClientID UUID
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(VisitDate)
ORDER BY Hour;

```


```
ENGINE = ReplicatedCollapsingMergeTree('/clickhouse/tables/name', 'replica1', Sign)
PARTITION BY (toMonday(StartDate), EventType)
ORDER BY (CounterID, StartDate, intHash32(UserID));

```


```
SELECT
    partition,
    name,
    active
FROM system.parts
WHERE table = 'visits'

```


```
┌─partition─┬─name──────────────┬─active─┐
│ 201901    │ 201901_1_3_1      │      0 │
│ 201901    │ 201901_1_9_2_11   │      1 │
│ 201901    │ 201901_8_8_0      │      0 │
│ 201901    │ 201901_9_9_0      │      0 │
│ 201902    │ 201902_4_6_1_11   │      1 │
│ 201902    │ 201902_10_10_0_11 │      1 │
│ 201902    │ 201902_11_11_0_11 │      1 │
└───────────┴───────────────────┴────────┘

```

- `201901` — это имя партиции.
- `1` — это минимальный номер блока данных.
- `9` — это максимальный номер блока данных.
- `2` — это уровень фрагмента (глубина дерева слияния, из которого он образован).
- `11` — это версия мутации (если к части была применена мутация)

```
OPTIMIZE TABLE visits PARTITION 201902;

```


```
┌─partition─┬─name─────────────┬─active─┐
│ 201901    │ 201901_1_3_1     │      0 │
│ 201901    │ 201901_1_9_2_11  │      1 │
│ 201901    │ 201901_8_8_0     │      0 │
│ 201901    │ 201901_9_9_0     │      0 │
│ 201902    │ 201902_4_6_1     │      0 │
│ 201902    │ 201902_4_11_2_11 │      1 │
│ 201902    │ 201902_10_10_0   │      0 │
│ 201902    │ 201902_11_11_0   │      0 │
└───────────┴──────────────────┴────────┘

```


```
/var/lib/clickhouse/data/default/visits$ ls -l
total 40
drwxr-xr-x 2 clickhouse clickhouse 4096 Feb  1 16:48 201901_1_3_1
drwxr-xr-x 2 clickhouse clickhouse 4096 Feb  5 16:17 201901_1_9_2_11
drwxr-xr-x 2 clickhouse clickhouse 4096 Feb  5 15:52 201901_8_8_0
drwxr-xr-x 2 clickhouse clickhouse 4096 Feb  5 15:52 201901_9_9_0
drwxr-xr-x 2 clickhouse clickhouse 4096 Feb  5 16:17 201902_10_10_0
drwxr-xr-x 2 clickhouse clickhouse 4096 Feb  5 16:17 201902_11_11_0
drwxr-xr-x 2 clickhouse clickhouse 4096 Feb  5 16:19 201902_4_11_2_11
drwxr-xr-x 2 clickhouse clickhouse 4096 Feb  5 12:09 201902_4_6_1
drwxr-xr-x 2 clickhouse clickhouse 4096 Feb  1 16:48 detached

```


## Оптимизация Group By с использованием ключа партиционирования


```
CREATE TABLE session_log
(
    UserID UInt64,
    SessionID UUID
)
ENGINE = MergeTree
PARTITION BY sipHash64(UserID) % 16
ORDER BY tuple();

SELECT
    UserID,
    COUNT()
FROM session_log
GROUP BY UserID;

```

- число партиций, задействованных в запросе, должно быть достаточно большим (более `max_threads / 2`), иначе запрос не будет в полной мере использовать ресурсы машины
- партиции не должны быть слишком маленькими, чтобы батчевая обработка не выродилась в построчную
- партиции должны быть сопоставимы по размеру, чтобы все потоки выполняли примерно одинаковый объём работы
- `allow_aggregate_partitions_independently` - управляет тем, включено ли использование этой оптимизации
- `force_aggregate_partitions_independently` - принудительно включает её использование, когда это допустимо с точки зрения корректности, но она отключается внутренней логикой, оценивающей целесообразность её применения
- `max_number_of_partitions_for_independent_aggregation` - жёсткое ограничение на максимальное число партиций, которое может быть у таблицы
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
