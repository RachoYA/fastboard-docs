# aggregate_* настройки сеанса - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/settings/session-settings/aggregate


## aggregate_function_input_format

- `state` — Двоичная строка с сериализованным состоянием (по умолчанию). Это стандартное поведение, при котором значения AggregateFunction должны передаваться как двоичные данные.
- `value` — Формат ожидает одно значение аргумента агрегатной функции или, в случае нескольких аргументов, их кортеж. Они будут десериализованы с помощью соответствующего IDataType или DataTypeTuple, а затем агрегированы для формирования состояния.
- `array` — Формат ожидает `Array` значений, как описано выше для варианта `value`. Все элементы массива будут агрегированы для формирования состояния.

```
CREATE TABLE example (
    user_id UInt64,
    avg_session_length AggregateFunction(avg, UInt32)
);

```


```
INSERT INTO example FORMAT CSV
123,456

```


```
INSERT INTO example FORMAT CSV
123,"[456,789,101]"

```


## aggregate_functions_null_for_empty

- 0 — Отключено.
- 1 — Включено.

```
SELECT SUM(-1), MAX(0) FROM system.one WHERE 0;

```


```
┌─SUM(-1)─┬─MAX(0)─┐
│       0 │      0 │
└─────────┴────────┘

```


```
┌─SUMOrNull(-1)─┬─MAXOrNull(0)─┐
│          NULL │         NULL │
└───────────────┴──────────────┘

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
