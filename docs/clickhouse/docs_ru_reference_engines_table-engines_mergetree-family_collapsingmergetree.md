# Движок таблицы CollapsingMergeTree - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/collapsingmergetree


## Описание


## Параметры

- `Sign` — имя столбца, указывающего тип строки: `1` — «строка состояния», `-1` — «строка отмены». Тип: [Int8](https://clickhouse.com/docs/ru/reference/data-types/int-uint).

## Создание таблицы


```
CREATE TABLE [IF NOT EXISTS] [db.]table_name [ON CLUSTER cluster]
(
    name1 [type1] [DEFAULT|MATERIALIZED|ALIAS expr1],
    name2 [type2] [DEFAULT|MATERIALIZED|ALIAS expr2],
    ...
)
ENGINE = CollapsingMergeTree(Sign)
[PARTITION BY expr]
[ORDER BY expr]
[SAMPLE BY expr]
[SETTINGS name=value, ...]

```

- Описание параметров запроса см. в разделе [описание запроса](https://clickhouse.com/docs/ru/reference/statements/create/table).
- При создании таблицы `CollapsingMergeTree` требуются те же [секции запроса](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/mergetree#table_engine-mergetree-creating-a-table), что и при создании таблицы `MergeTree`.

## Схлопывание


### Данные

- Если `Sign` = `1`, это означает, что строка является строкой состояния: *строкой, содержащей поля, которые представляют текущее корректное состояние*.
- Если `Sign` = `-1`, это означает, что строка является строкой отмены: *строкой, используемой для отмены состояния объекта с теми же атрибутами*.

```
┌──────────────UserID─┬─PageViews─┬─Duration─┬─Sign─┐
│ 4324182021466249494 │         5 │      146 │    1 │
└─────────────────────┴───────────┴──────────┴──────┘

```


```
┌──────────────UserID─┬─PageViews─┬─Duration─┬─Sign─┐
│ 4324182021466249494 │         5 │      146 │   -1 │
│ 4324182021466249494 │         6 │      185 │    1 │
└─────────────────────┴───────────┴──────────┴──────┘

```


```
┌──────────────UserID─┬─PageViews─┬─Duration─┬─Sign─┐
│ 4324182021466249494 │         5 │      146 │    1 │ -- old "state" row can be deleted
│ 4324182021466249494 │         5 │      146 │   -1 │ -- "cancel" row can be deleted
│ 4324182021466249494 │         6 │      185 │    1 │ -- new "state" row remains
└─────────────────────┴───────────┴──────────┴──────┘

```

- Программа, записывающая данные, должна хранить состояние объекта, чтобы иметь возможность отменить его. Строка отмены должна содержать копии полей ключа сортировки строки состояния и противоположное значение `Sign`. Это увеличивает первоначальный объем хранилища, но позволяет быстро записывать данные.
- Длинные, постоянно растущие массивы в столбцах снижают эффективность движка из-за повышенной нагрузки при записи. Чем проще данные, тем выше эффективность.
- Результаты `SELECT` сильно зависят от согласованности истории изменений объекта. Будьте внимательны при подготовке данных для вставки. Если данные несогласованы, результаты могут быть непредсказуемыми. Например, отрицательные значения у неотрицательных метрик, таких как глубина сеанса.

### Алгоритм


|  |  |
| --- | --- |
| 1. | Первую «строку отмены» и последнюю «строку состояния», если количество «строк состояния» и «строк отмены» совпадает и последняя строка — это «строка состояния». |
| 2. | Последнюю «строку состояния», если «строк состояния» больше, чем «строк отмены». |
| 3. | Первую «строку отмены», если «строк отмены» больше, чем «строк состояния». |
| 4. | Ни одной строки, во всех остальных случаях. |


## Примеры


### Пример использования


```
┌──────────────UserID─┬─PageViews─┬─Duration─┬─Sign─┐
│ 4324182021466249494 │         5 │      146 │    1 │
│ 4324182021466249494 │         5 │      146 │   -1 │
│ 4324182021466249494 │         6 │      185 │    1 │
└─────────────────────┴───────────┴──────────┴──────┘

```


```
CREATE TABLE UAct
(
    UserID UInt64,
    PageViews UInt8,
    Duration UInt8,
    Sign Int8
)
ENGINE = CollapsingMergeTree(Sign)
ORDER BY UserID

```


```
INSERT INTO UAct VALUES (4324182021466249494, 5, 146, 1)

```


```
INSERT INTO UAct VALUES (4324182021466249494, 5, 146, -1),(4324182021466249494, 6, 185, 1)

```


```
SELECT * FROM UAct

```


```
┌──────────────UserID─┬─PageViews─┬─Duration─┬─Sign─┐
│ 4324182021466249494 │         5 │      146 │   -1 │
│ 4324182021466249494 │         6 │      185 │    1 │
└─────────────────────┴───────────┴──────────┴──────┘
┌──────────────UserID─┬─PageViews─┬─Duration─┬─Sign─┐
│ 4324182021466249494 │         5 │      146 │    1 │
└─────────────────────┴───────────┴──────────┴──────┘

```


```
SELECT
    UserID,
    sum(PageViews * Sign) AS PageViews,
    sum(Duration * Sign) AS Duration
FROM UAct
GROUP BY UserID
HAVING sum(Sign) > 0

```


```
┌──────────────UserID─┬─PageViews─┬─Duration─┐
│ 4324182021466249494 │         6 │      185 │
└─────────────────────┴───────────┴──────────┘

```


```
SELECT * FROM UAct FINAL

```


```
┌──────────────UserID─┬─PageViews─┬─Duration─┬─Sign─┐
│ 4324182021466249494 │         6 │      185 │    1 │
└─────────────────────┴───────────┴──────────┴──────┘

```


### Пример другого подхода


```
┌──────────────UserID─┬─PageViews─┬─Duration─┬─Sign─┐
│ 4324182021466249494 │         5 │      146 │    1 │
│ 4324182021466249494 │        -5 │     -146 │   -1 │
│ 4324182021466249494 │         6 │      185 │    1 │
└─────────────────────┴───────────┴──────────┴──────┘

```


```
CREATE TABLE UAct
(
    UserID UInt64,
    PageViews Int16,
    Duration Int16,
    Sign Int8
)
ENGINE = CollapsingMergeTree(Sign)
ORDER BY UserID

```


```
INSERT INTO UAct VALUES(4324182021466249494,  5,  146,  1);
INSERT INTO UAct VALUES(4324182021466249494, -5, -146, -1);
INSERT INTO UAct VALUES(4324182021466249494,  6,  185,  1);

SELECT * FROM UAct FINAL;

```


```
┌──────────────UserID─┬─PageViews─┬─Duration─┬─Sign─┐
│ 4324182021466249494 │         6 │      185 │    1 │
└─────────────────────┴───────────┴──────────┴──────┘

```


```
SELECT
    UserID,
    sum(PageViews) AS PageViews,
    sum(Duration) AS Duration
FROM UAct
GROUP BY UserID

```


```
┌──────────────UserID─┬─PageViews─┬─Duration─┐
│ 4324182021466249494 │         6 │      185 │
└─────────────────────┴───────────┴──────────┘

```


```
SELECT COUNT() FROM UAct

```


```
┌─count()─┐
│       3 │
└─────────┘

```


```
OPTIMIZE TABLE UAct FINAL;

SELECT * FROM UAct

```


```
┌──────────────UserID─┬─PageViews─┬─Duration─┬─Sign─┐
│ 4324182021466249494 │         6 │      185 │    1 │
└─────────────────────┴───────────┴──────────┴──────┘

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
