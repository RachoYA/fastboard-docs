# system.asynchronous_loader - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/system-tables/asynchronous_loader


## Описание


## Столбцы

- `job` ([String](https://clickhouse.com/docs/ru/reference/data-types/index)) — Имя задачи (может быть неуникальным).
- `job_id` ([UInt64](https://clickhouse.com/docs/ru/reference/data-types/index)) — Уникальный ID задачи.
- `dependencies` ([Array(UInt64)](https://clickhouse.com/docs/ru/reference/data-types/index)) — Список ID задач, которые должны быть выполнены до этой задачи.
- `dependencies_left` ([UInt64](https://clickhouse.com/docs/ru/reference/data-types/index)) — Текущее количество зависимостей, которые ещё предстоит выполнить.
- `status` ([Enum8(‘PENDING’ = 0, ‘OK’ = 1, ‘FAILED’ = 2, ‘CANCELED’ = 3)](https://clickhouse.com/docs/ru/reference/data-types/index)) — Текущий статус загрузки задачи: PENDING: задача загрузки ещё не запущена. OK: задача загрузки выполнена успешно. FAILED: задача загрузки завершилась с ошибкой. CANCELED: задача загрузки не будет выполнена из-за удаления или сбоя зависимости.
- `is_executing` ([UInt8](https://clickhouse.com/docs/ru/reference/data-types/index)) — Задача в данный момент выполняется воркером.
- `is_blocked` ([UInt8](https://clickhouse.com/docs/ru/reference/data-types/index)) — Задача ожидает выполнения своих зависимостей.
- `is_ready` ([UInt8](https://clickhouse.com/docs/ru/reference/data-types/index)) — Задача готова к выполнению и ожидает воркера.
- `elapsed` ([Float64](https://clickhouse.com/docs/ru/reference/data-types/index)) — Количество секунд, прошедших с начала выполнения. Ноль, если задача ещё не запущена. Общее время выполнения, если задача завершена.
- `pool_id` ([UInt64](https://clickhouse.com/docs/ru/reference/data-types/index)) — ID пула, в данный момент назначенного задаче.
- `pool` ([String](https://clickhouse.com/docs/ru/reference/data-types/index)) — Имя пула `pool_id`.
- `priority` ([Int64](https://clickhouse.com/docs/ru/reference/data-types/index)) — Приоритет пула `pool_id`.
- `execution_pool_id` ([UInt64](https://clickhouse.com/docs/ru/reference/data-types/index)) — ID пула, в котором выполняется задача. До начала выполнения совпадает с изначально назначенным пулом.
- `execution_pool` ([String](https://clickhouse.com/docs/ru/reference/data-types/index)) — Имя пула `execution_pool_id`.
- `execution_priority` ([Int64](https://clickhouse.com/docs/ru/reference/data-types/index)) — Приоритет пула `execution_pool_id`.
- `ready_seqno` ([Nullable(UInt64)](https://clickhouse.com/docs/ru/reference/data-types/index)) — Не NULL для готовых задач. Воркер берёт следующую задачу для выполнения из очереди готовых задач своего пула. Если готовых задач несколько, выбирается задача с наименьшим значением `ready_seqno`.
- `waiters` ([UInt64](https://clickhouse.com/docs/ru/reference/data-types/index)) — Количество потоков, ожидающих эту задачу.
- `exception` ([Nullable(String)](https://clickhouse.com/docs/ru/reference/data-types/index)) — Не NULL для задач, завершившихся с ошибкой или отменённых. Содержит сообщение об ошибке, возникшей во время выполнения запроса, либо ошибку, приведшую к отмене этой задачи, вместе с цепочкой отказов зависимостей по именам задач.
- `schedule_time` ([DateTime64(6)](https://clickhouse.com/docs/ru/reference/data-types/index)) — Время, когда задача была создана и запланирована к выполнению (обычно вместе со всеми своими зависимостями).
- `enqueue_time` ([Nullable(DateTime64(6))](https://clickhouse.com/docs/ru/reference/data-types/index)) — Время, когда задача стала готовой и была помещена в очередь готовых задач своего пула. NULL, если задача ещё не готова.
- `start_time` ([Nullable(DateTime64(6))](https://clickhouse.com/docs/ru/reference/data-types/index)) — Время, когда воркер извлекает задачу из очереди готовых задач и начинает её выполнение. NULL, если задача ещё не запущена.
- `finish_time` ([Nullable(DateTime64(6))](https://clickhouse.com/docs/ru/reference/data-types/index)) — Время завершения выполнения задачи. NULL, если задача ещё не завершена.
- `is_executing` (`UInt8`) - Задача в данный момент выполняется воркером.
- `is_blocked` (`UInt8`) - Задача ожидает завершения зависимостей.
- `is_ready` (`UInt8`) - Задача готова к выполнению и ожидает свободного воркера.
- `elapsed` (`Float64`) - Количество секунд, прошедших с начала выполнения. Ноль, если задача ещё не запущена. Общее время выполнения, если задача завершена.
- `pool_id` (`UInt64`) - ID пула, в данный момент назначенного задаче.
- `pool` (`String`) - Имя пула `pool_id`.
- `priority` (`Int64`) - Приоритет пула `pool_id`.
- `execution_pool_id` (`UInt64`) - ID пула, в котором выполняется задача. До начала выполнения совпадает с изначально назначенным пулом.
- `execution_pool` (`String`) - Имя пула `execution_pool_id`.
- `execution_priority` (`Int64`) - Приоритет пула `execution_pool_id`.
- `ready_seqno` (`Nullable(UInt64)`) - Не NULL для готовых задач. Воркер берёт следующую задачу для выполнения из очереди готовых задач своего пула. Если готовых задач несколько, выбирается задача с наименьшим значением `ready_seqno`.
- `waiters` (`UInt64`) - Число потоков, ожидающих эту задачу.
- `exception` (`Nullable(String)`) - Не NULL для задач, завершившихся с ошибкой или отменённых. Содержит сообщение об ошибке, возникшей при выполнении запроса, либо ошибку, приведшую к отмене этой задачи, вместе с цепочкой отказов зависимостей в виде имён задач.
- `schedule_time` (`DateTime64`) - Время, когда задача была создана и запланирована к выполнению (обычно вместе со всеми её зависимостями).
- `enqueue_time` (`Nullable(DateTime64)`) - Время, когда задача стала готовой и была помещена в очередь готовых задач своего пула. NULL, если задача ещё не готова.
- `start_time` (`Nullable(DateTime64)`) - Время, когда воркер извлекает задачу из очереди готовых задач и начинает её выполнение. NULL, если задача ещё не запущена.
- `finish_time` (`Nullable(DateTime64)`) - Время, когда выполнение задачи завершилось. NULL, если задача ещё не завершена.

## Пример


```
SELECT *
FROM system.asynchronous_loader
LIMIT 1
FORMAT Vertical

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
