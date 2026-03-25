# Табличный движок SummingMergeTree | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/engines/table-engines/mergetree-family/summingmergetree

Этот движок наследуется отMergeTree. Разница в том, что при слиянии частей данных для таблицSummingMergeTreeClickHouse заменяет все строки с одинаковым первичным ключом (или, точнее, с одинаковымключом сортировки) одной строкой, которая содержит суммы значений для столбцов с числовым типом данных. Если ключ сортировки построен таким образом, что одному значению ключа соответствует большое количество строк, это существенно уменьшает объем хранимых данных и ускоряет выборку.

Мы рекомендуем использовать этот движок совместно сMergeTree. Храните полные данные в таблицеMergeTree, аSummingMergeTreeиспользуйте для хранения агрегированных данных, например при подготовке отчетов. Такой подход поможет избежать потери ценных данных из-за некорректно составленного первичного ключа.


## Создание таблицы​


```
CREATE TABLE [IF NOT EXISTS] [db.]table_name [ON CLUSTER cluster]
(
    name1 [type1] [DEFAULT|MATERIALIZED|ALIAS expr1],
    name2 [type2] [DEFAULT|MATERIALIZED|ALIAS expr2],
    ...
) ENGINE = SummingMergeTree([columns])
[PARTITION BY expr]
[ORDER BY expr]
[SAMPLE BY expr]
[SETTINGS name=value, ...]

```

Описание параметров запроса см. вописании запроса.


### Параметры SummingMergeTree​


#### Столбцы​

columns— кортеж с именами столбцов, значения в которых будут суммироваться. Необязательный параметр.
Столбцы должны иметь числовой тип и не должны входить в ключ партиционирования или сортировки.

Еслиcolumnsне указан, ClickHouse суммирует значения во всех столбцах с числовым типом данных, которые не входят в ключ сортировки.


### Части запроса​

При создании таблицыSummingMergeTreeтребуются те жечасти запроса, что и при создании таблицыMergeTree.

Не используйте этот метод в новых проектах и, по возможности, переведите старые проекты на метод, описанный выше.


```
CREATE TABLE [IF NOT EXISTS] [db.]table_name [ON CLUSTER cluster]
(
    name1 [type1] [DEFAULT|MATERIALIZED|ALIAS expr1],
    name2 [type2] [DEFAULT|MATERIALIZED|ALIAS expr2],
    ...
) ENGINE [=] SummingMergeTree(date-column [, sampling_expression], (primary, key), index_granularity, [columns])

```

Все параметры, кромеcolumns, имеют то же значение, что и вMergeTree.columns— кортеж с именами столбцов, значения в которых будут суммироваться. Необязательный параметр. Для описания см. текст выше.

- columns— кортеж с именами столбцов, значения в которых будут суммироваться. Необязательный параметр. Для описания см. текст выше.

## Пример использования​

Рассмотрим следующую таблицу:


```
CREATE TABLE summtt
(
    key UInt32,
    value UInt32
)
ENGINE = SummingMergeTree()
ORDER BY key

```

Запишите в неё данные:


```
INSERT INTO summtt VALUES(1,1),(1,2),(2,1)

```

ClickHouse может суммировать строки не полностью (см. ниже), поэтому в запросе мы используем агрегатную функциюsumи предложениеGROUP BY.


```
SELECT key, sum(value) FROM summtt GROUP BY key

```


```
┌─key─┬─sum(value)─┐
│   2 │          1 │
│   1 │          3 │
└─────┴────────────┘

```


## Обработка данных​

Когда данные вставляются в таблицу, они сохраняются как есть. ClickHouse периодически сливает вставленные части данных, и именно в этот момент строки с одинаковым первичным ключом суммируются и заменяются одной строкой для каждой получившейся части данных.

ClickHouse может сливать части данных таким образом, что разные получившиеся части данных могут содержать строки с одинаковым первичным ключом, т. е. суммирование будет неполным. Поэтому при выполнении запроса (SELECT) следует использовать агрегатную функциюsum()и предложениеGROUP BY, как описано в примере выше.


### Общие правила суммирования​

Значения в столбцах с числовым типом данных суммируются. Набор столбцов определяется параметромcolumns.

Если значения были равны 0 во всех столбцах для суммирования, строка удаляется.

Если столбец не входит в первичный ключ и не суммируется, из существующих значений выбирается произвольное.

Значения не суммируются для столбцов, входящих в первичный ключ.


### Суммирование в столбцах AggregateFunction​

Для столбцов типаAggregateFunctionClickHouse ведёт себя как движокAggregatingMergeTree, агрегируя в соответствии с функцией.


### Вложенные структуры​

Таблица может содержать вложенные структуры данных, которые обрабатываются особым образом.

Если имя вложенной таблицы оканчивается наMapи она содержит как минимум два столбца, удовлетворяющих следующим критериям:

- первый столбец — числовой(*Int*, Date, DateTime)или строковый(String, FixedString), назовём егоkey,
- остальные столбцы — арифметические(*Int*, Float32/64), назовём их(values...),
то такая вложенная таблица интерпретируется как отображениеkey => (values...), и при слиянии её строк элементы двух наборов данных объединяются поkeyс суммированием соответствующих(values...).

Примеры:


```
DROP TABLE IF EXISTS nested_sum;
CREATE TABLE nested_sum
(
    date Date,
    site UInt32,
    hitsMap Nested(
        browser String,
        imps UInt32,
        clicks UInt32
    )
) ENGINE = SummingMergeTree
PRIMARY KEY (date, site);

INSERT INTO nested_sum VALUES ('2020-01-01', 12, ['Firefox', 'Opera'], [10, 5], [2, 1]);
INSERT INTO nested_sum VALUES ('2020-01-01', 12, ['Chrome', 'Firefox'], [20, 1], [1, 1]);
INSERT INTO nested_sum VALUES ('2020-01-01', 12, ['IE'], [22], [0]);
INSERT INTO nested_sum VALUES ('2020-01-01', 10, ['Chrome'], [4], [3]);

OPTIMIZE TABLE nested_sum FINAL; -- emulate merge 

SELECT * FROM nested_sum;
┌───────date─┬─site─┬─hitsMap.browser───────────────────┬─hitsMap.imps─┬─hitsMap.clicks─┐
│ 2020-01-01 │   10 │ ['Chrome']                        │ [4]          │ [3]            │
│ 2020-01-01 │   12 │ ['Chrome','Firefox','IE','Opera'] │ [20,11,22,5] │ [1,3,0,1]      │
└────────────┴──────┴───────────────────────────────────┴──────────────┴────────────────┘

SELECT
    site,
    browser,
    impressions,
    clicks
FROM
(
    SELECT
        site,
        sumMap(hitsMap.browser, hitsMap.imps, hitsMap.clicks) AS imps_map
    FROM nested_sum
    GROUP BY site
)
ARRAY JOIN
    imps_map.1 AS browser,
    imps_map.2 AS impressions,
    imps_map.3 AS clicks;

┌─site─┬─browser─┬─impressions─┬─clicks─┐
│   12 │ Chrome  │          20 │      1 │
│   12 │ Firefox │          11 │      3 │
│   12 │ IE      │          22 │      0 │
│   12 │ Opera   │           5 │      1 │
│   10 │ Chrome  │           4 │      3 │
└──────┴─────────┴─────────────┴────────┘

```

При запросе данных используйте функциюsumMap(key, value)для агрегацииMap.

Для вложенной структуры данных не нужно указывать её столбцы в кортеже столбцов, по которым выполняется суммирование.


## Связанные материалы​

- Блог:Использование агрегатных комбинаторов в ClickHouse