# Операторы KILL | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/sql-reference/statements/kill

Существуют две разновидности операторов KILL: для завершения запроса и для завершения мутации


## KILL QUERY​


```
KILL QUERY [ON CLUSTER cluster]
  WHERE <where expression to SELECT FROM system.processes query>
  [SYNC|ASYNC|TEST]
  [FORMAT format]

```

Пытается принудительно завершить выполняющиеся в данный момент запросы.
Запросы для завершения отбираются из таблицы system.processes по критериям, заданным вWHERE-условии запросаKILL.

Примеры:

Сначала нужно получить список незавершённых запросов. Этот SQL-запрос выводит их, начиная с тех, что выполняются дольше всего:

Список с одного узла ClickHouse:


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

Список из кластера ClickHouse:


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

Прервать выполнение запроса:


```
-- Forcibly terminates all queries with the specified query_id:
KILL QUERY WHERE query_id='2-857d-4a57-9ee0-327da5d60a90'

-- Synchronously terminates all queries run by 'username':
KILL QUERY WHERE user='username' SYNC

```

Если вы завершаете запрос в ClickHouse Cloud или в самостоятельно управляемом кластере, обязательно используйте операторON CLUSTER [cluster-name], чтобы гарантировать, что запрос будет остановлен на всех репликах.

Пользователи с правами только на чтение могут останавливать только собственные запросы.

По умолчанию используется асинхронный режим (ASYNC), который не ожидает подтверждения остановки запросов.

Синхронный режим (SYNC) ожидает завершения всех запросов и отображает информацию о каждом процессе по мере его остановки.
Ответ содержит столбецkill_status, который может принимать следующие значения:

- finished– запрос был успешно завершён.
- waiting– ожидание завершения запроса после отправки ему сигнала на завершение.
- Другие значения объясняют, почему запрос не может быть остановлен.
Тестовый запрос (TEST) только проверяет права пользователя и отображает список запросов, подлежащих остановке.


## ОТМЕНА МУТАЦИИ​

Наличие долго выполняющихся или незавершённых мутаций часто указывает на некорректную работу сервиса ClickHouse. Асинхронная природа мутаций может привести к тому, что они будут потреблять все доступные ресурсы системы. Вам может потребоваться либо:

- Приостановить все новые мутации, операцииINSERTиSELECTи дать очереди мутаций полностью выполниться.
- Или вручную прервать выполнение некоторых из этих мутаций, отправив командуKILL.

```
KILL MUTATION
  WHERE <where expression to SELECT FROM system.mutations query>
  [TEST]
  [FORMAT format]

```

Пытается отменить и удалитьмутации, которые в данный момент выполняются. Мутации для отмены выбираются из таблицыsystem.mutationsс использованием фильтра, заданного в предложенииWHEREзапросаKILL.

Проверочный запрос (TEST) только проверяет права пользователя и выводит список мутаций для остановки.

Примеры:

Получитьcount()незавершённых мутаций:

Количество мутаций с одного узла ClickHouse:


```
SELECT count(*)
FROM system.mutations
WHERE is_done = 0;

```

Количество мутаций из кластера реплик ClickHouse:


```
SELECT count(*)
FROM clusterAllReplicas('default', system.mutations)
WHERE is_done = 0;

```

Выполните запрос для получения списка незавершённых мутаций:

Список мутаций на одном узле ClickHouse:


```
SELECT mutation_id, *
FROM system.mutations
WHERE is_done = 0;

```

Список мутаций в кластере ClickHouse:


```
SELECT mutation_id, *
FROM clusterAllReplicas('default', system.mutations)
WHERE is_done = 0;

```

При необходимости остановите мутации:


```
-- Cancel and remove all mutations of the single table:
KILL MUTATION WHERE database = 'default' AND table = 'table'

-- Cancel the specific mutation:
KILL MUTATION WHERE database = 'default' AND table = 'table' AND mutation_id = 'mutation_3.txt'

```

Этот запрос полезен, когда мутация «застряла» и не может завершиться (например, если какая‑то функция в запросе мутации выбрасывает исключение при применении к данным, содержащимся в таблице).

Изменения, уже выполненные мутацией, не откатываются.

Значениеis_killed=1в столбце (только в ClickHouse Cloud) в таблицеsystem.mutationsне обязательно означает, что мутация полностью завершена. Возможна ситуация, когда мутация остаётся в состоянии, гдеis_killed=1иis_done=0в течение продолжительного времени. Это может произойти, если «убитую» мутацию блокирует другая, долго выполняющаяся мутация. Это нормальная ситуация.
