# Date32 | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/sql-reference/data-types/date32

Дата. Поддерживает тот же диапазон дат, что иDateTime64. Хранится как знаковое 32-битное целое число в нативном порядке байтов, значение которого равно количеству дней, прошедших с1900-01-01.Важно!0 соответствует1970-01-01, а отрицательные значения — дням до1970-01-01.

Примеры

Создание таблицы со столбцом типаDate32и вставка данных в него:


```
CREATE TABLE dt32
(
    `timestamp` Date32,
    `event_id` UInt8
)
ENGINE = TinyLog;

```


```
-- Parse Date
-- - from string,
-- - from 'small' integer interpreted as number of days since 1970-01-01, and
-- - from 'big' integer interpreted as number of seconds since 1970-01-01.
INSERT INTO dt32 VALUES ('2100-01-01', 1), (47482, 2), (4102444800, 3);

SELECT * FROM dt32;

```


```
┌──timestamp─┬─event_id─┐
│ 2100-01-01 │        1 │
│ 2100-01-01 │        2 │
│ 2100-01-01 │        3 │
└────────────┴──────────┘

```

Смотрите также

- toDate32
- toDate32OrZero
- toDate32OrNull