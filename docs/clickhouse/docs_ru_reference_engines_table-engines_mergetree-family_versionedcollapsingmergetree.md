# Движок таблицы VersionedCollapsingMergeTree - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/versionedcollapsingmergetree

- Позволяет быстро записывать состояния объектов, которые постоянно меняются.
- Удаляет старые состояния объектов в фоновом режиме. Это значительно сокращает объем хранимых данных.

## Создание таблицы


```
CREATE TABLE [IF NOT EXISTS] [db.]table_name [ON CLUSTER cluster]
(
    name1 [type1] [DEFAULT|MATERIALIZED|ALIAS expr1],
    name2 [type2] [DEFAULT|MATERIALIZED|ALIAS expr2],
    ...
) ENGINE = VersionedCollapsingMergeTree(sign, version)
[PARTITION BY expr]
[ORDER BY expr]
[SAMPLE BY expr]
[SETTINGS name=value, ...]

```


### Параметры движка


```
VersionedCollapsingMergeTree(sign, version)

```


| Параметр | Описание | Тип |
| --- | --- | --- |
| `sign` | Имя столбца с типом строки: `1` — это строка состояния, `-1` — это строка отмены. | [`Int8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) |
| `version` | Имя столбца с версией состояния объекта. | [`Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint), [`UInt*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint), [`Date`](https://clickhouse.com/docs/ru/reference/data-types/date), [`Date32`](https://clickhouse.com/docs/ru/reference/data-types/date32), [`DateTime`](https://clickhouse.com/docs/ru/reference/data-types/datetime) или [`DateTime64`](https://clickhouse.com/docs/ru/reference/data-types/datetime64) |


### Секции запроса


## Схлопывание


### Данные


```
┌──────────────UserID─┬─PageViews─┬─Duration─┬─Sign─┬─Version─┐
│ 4324182021466249494 │         5 │      146 │    1 │       1 |
└─────────────────────┴───────────┴──────────┴──────┴─────────┘

```


```
┌──────────────UserID─┬─PageViews─┬─Duration─┬─Sign─┬─Version─┐
│ 4324182021466249494 │         5 │      146 │   -1 │       1 |
│ 4324182021466249494 │         6 │      185 │    1 │       2 |
└─────────────────────┴───────────┴──────────┴──────┴─────────┘

```


```
┌──────────────UserID─┬─PageViews─┬─Duration─┬─Sign─┬─Version─┐
│ 4324182021466249494 │         5 │      146 │    1 │       1 |
│ 4324182021466249494 │         5 │      146 │   -1 │       1 |
└─────────────────────┴───────────┴──────────┴──────┴─────────┘

```

- Программа, которая записывает данные, должна помнить состояние объекта, чтобы можно было его отменить. Строка “Cancel” должна содержать копии полей первичного ключа, версию строки “state” и противоположный `Sign`. Это увеличивает начальный объем хранилища, но позволяет быстро записывать данные.
- Длинные растущие массивы в столбцах снижают эффективность движка из-за нагрузки при записи. Чем проще данные, тем выше эффективность.
- Результаты `SELECT` сильно зависят от согласованности истории изменений объекта. Будьте внимательны при подготовке данных для вставки. Несогласованные данные могут приводить к непредсказуемым результатам, например к отрицательным значениям для неотрицательных метрик, таких как глубина сеанса.

### Алгоритм


## Выборка данных


## Пример использования


```
┌──────────────UserID─┬─PageViews─┬─Duration─┬─Sign─┬─Version─┐
│ 4324182021466249494 │         5 │      146 │    1 │       1 |
│ 4324182021466249494 │         5 │      146 │   -1 │       1 |
│ 4324182021466249494 │         6 │      185 │    1 │       2 |
└─────────────────────┴───────────┴──────────┴──────┴─────────┘

```


```
CREATE TABLE UAct
(
    UserID UInt64,
    PageViews UInt8,
    Duration UInt8,
    Sign Int8,
    Version UInt8
)
ENGINE = VersionedCollapsingMergeTree(Sign, Version)
ORDER BY UserID

```


```
INSERT INTO UAct VALUES (4324182021466249494, 5, 146, 1, 1)

```


```
INSERT INTO UAct VALUES (4324182021466249494, 5, 146, -1, 1),(4324182021466249494, 6, 185, 1, 2)

```


```
SELECT * FROM UAct

```


```
┌──────────────UserID─┬─PageViews─┬─Duration─┬─Sign─┬─Version─┐
│ 4324182021466249494 │         5 │      146 │    1 │       1 │
└─────────────────────┴───────────┴──────────┴──────┴─────────┘
┌──────────────UserID─┬─PageViews─┬─Duration─┬─Sign─┬─Version─┐
│ 4324182021466249494 │         5 │      146 │   -1 │       1 │
│ 4324182021466249494 │         6 │      185 │    1 │       2 │
└─────────────────────┴───────────┴──────────┴──────┴─────────┘

```


```
SELECT
    UserID,
    sum(PageViews * Sign) AS PageViews,
    sum(Duration * Sign) AS Duration,
    Version
FROM UAct
GROUP BY UserID, Version
HAVING sum(Sign) > 0

```


```
┌──────────────UserID─┬─PageViews─┬─Duration─┬─Version─┐
│ 4324182021466249494 │         6 │      185 │       2 │
└─────────────────────┴───────────┴──────────┴─────────┘

```


```
SELECT * FROM UAct FINAL

```


```
┌──────────────UserID─┬─PageViews─┬─Duration─┬─Sign─┬─Version─┐
│ 4324182021466249494 │         6 │      185 │    1 │       2 │
└─────────────────────┴───────────┴──────────┴──────┴─────────┘

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
