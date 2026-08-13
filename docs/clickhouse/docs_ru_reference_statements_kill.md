# Операторы KILL - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/statements/kill


## KILL QUERY


```
KILL QUERY [ON CLUSTER cluster]
  WHERE <where expression to SELECT FROM system.processes query>
  [SYNC|ASYNC|TEST]
  [FORMAT format]

```


```
SELECT
  initial_query_id,
  query_id,
  formatReadableTimeDelta(elapsed) AS time_delta,
  query,
  *
  FROM system.processes
  WHERE query ILIKE 'SELECT%'
  ORDER BY time_delta DESC;

```


```
SELECT
  initial_query_id,
  query_id,
  formatReadableTimeDelta(elapsed) AS time_delta,
  query,
  *
  FROM clusterAllReplicas(default, system.processes)
  WHERE query ILIKE 'SELECT%'
  ORDER BY time_delta DESC;

```


```
-- Принудительно завершает все запросы с указанным query_id:
KILL QUERY WHERE query_id='2-857d-4a57-9ee0-327da5d60a90'

-- Синхронно завершает все запросы, запущенные пользователем 'username':
KILL QUERY WHERE user='username' SYNC

```

- `finished` – Запрос был успешно завершён.
- `waiting` – Ожидание завершения запроса после отправки ему сигнала на завершение.
- Другие значения объясняют, почему запрос не удаётся остановить.

## KILL MUTATION

- Приостановить все новые мутации, `INSERT`ы и `SELECT`ы и дождаться обработки очереди мутаций.
- Или вручную завершить некоторые из этих мутаций, отправив команду `KILL`.

```
KILL MUTATION
  WHERE <where expression to SELECT FROM system.mutations query>
  [TEST]
  [FORMAT format]

```


```
SELECT count(*)
FROM system.mutations
WHERE is_done = 0;

```


```
SELECT count(*)
FROM clusterAllReplicas('default', system.mutations)
WHERE is_done = 0;

```


```
SELECT mutation_id, *
FROM system.mutations
WHERE is_done = 0;

```


```
SELECT mutation_id, *
FROM clusterAllReplicas('default', system.mutations)
WHERE is_done = 0;

```


```
-- Cancel and remove all mutations of the single table:
KILL MUTATION WHERE database = 'default' AND table = 'table'

-- Cancel the specific mutation:
KILL MUTATION WHERE database = 'default' AND table = 'table' AND mutation_id = 'mutation_3.txt'

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
