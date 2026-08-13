# system.asynchronous_metric_log - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/system-tables/asynchronous_metric_log


## Описание


## Столбцы

- `hostname` ([LowCardinality(String)](https://clickhouse.com/docs/ru/reference/data-types/lowcardinality)) — Имя хоста сервера, выполняющего запрос.
- `event_date` ([Date](https://clickhouse.com/docs/ru/reference/data-types/date)) — Дата события.
- `event_time` ([DateTime](https://clickhouse.com/docs/ru/reference/data-types/datetime)) — Время события.
- `metric` ([LowCardinality(String)](https://clickhouse.com/docs/ru/reference/data-types/lowcardinality)) — Название метрики.
- `value` ([Float64](https://clickhouse.com/docs/ru/reference/data-types/float)) — Значение метрики.

## Пример


```
SELECT * FROM system.asynchronous_metric_log LIMIT 3 \G

```


```
Row 1:
──────
hostname:   clickhouse.eu-central1.internal
event_date: 2023-11-14
event_time: 2023-11-14 14:39:07
metric:     AsynchronousHeavyMetricsCalculationTimeSpent
value:      0.001

Row 2:
──────
hostname:   clickhouse.eu-central1.internal
event_date: 2023-11-14
event_time: 2023-11-14 14:39:08
metric:     AsynchronousHeavyMetricsCalculationTimeSpent
value:      0

Row 3:
──────
hostname:   clickhouse.eu-central1.internal
event_date: 2023-11-14
event_time: 2023-11-14 14:39:09
metric:     AsynchronousHeavyMetricsCalculationTimeSpent
value:      0

```

- [настройка asynchronous_metric_log](https://clickhouse.com/docs/ru/reference/settings/server-settings/settings#asynchronous_metric_log) — Включение и отключение настройки.
- [system.asynchronous_metrics](https://clickhouse.com/docs/ru/reference/system-tables/asynchronous_metrics) — Содержит метрики, периодически вычисляемые в фоновом режиме.
- [system.metric_log](https://clickhouse.com/docs/ru/reference/system-tables/metric_log) — Содержит историю значений метрик из таблиц `system.metrics` и `system.events`, которая периодически сбрасывается на диск.
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
