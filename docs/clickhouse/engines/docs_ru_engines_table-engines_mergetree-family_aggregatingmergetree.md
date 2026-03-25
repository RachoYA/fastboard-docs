# Движок таблицы AggregatingMergeTree | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/engines/table-engines/mergetree-family/aggregatingmergetree

Движок наследуется отMergeTreeи изменяет логику слияния частей данных. ClickHouse заменяет все строки с одинаковым первичным ключом (или, точнее, с одинаковымключом сортировки) одной строкой (в пределах одной части данных), которая хранит комбинацию состояний агрегатных функций.

Вы можете использовать таблицыAggregatingMergeTreeдля инкрементальной агрегации данных, в том числе для материализованных представлений с агрегированными данными.

Пример использования AggregatingMergeTree и агрегатных функций показан в видео ниже:

Движок обрабатывает все столбцы со следующими типами:

- AggregateFunction
- SimpleAggregateFunction
Имеет смысл использоватьAggregatingMergeTree, если он уменьшает число строк на несколько порядков.


## Создание таблицы​


```
CREATE TABLE [IF NOT EXISTS] [db.]table_name [ON CLUSTER cluster]
(
    name1 [type1] [DEFAULT|MATERIALIZED|ALIAS expr1],
    name2 [type2] [DEFAULT|MATERIALIZED|ALIAS expr2],
    ...
) ENGINE = AggregatingMergeTree()
[PARTITION BY expr]
[ORDER BY expr]
[SAMPLE BY expr]
[TTL expr]
[SETTINGS name=value, ...]

```

Для описания параметров запроса см.описание запроса.

Части запроса

При создании таблицыAggregatingMergeTreeтребуются те жечасти запроса, что и при создании таблицыMergeTree.

Не используйте этот способ в новых проектах и по возможности переведите старые проекты на метод, описанный выше.


```
CREATE TABLE [IF NOT EXISTS] [db.]table_name [ON CLUSTER cluster]
(
  name1 [type1] [DEFAULT|MATERIALIZED|ALIAS expr1],
  name2 [type2] [DEFAULT|MATERIALIZED|ALIAS expr2],
  ...
) ENGINE [=] AggregatingMergeTree(date-column [, sampling_expression], (primary, key), index_granularity)

```

Все параметры имеют то же значение, что и вMergeTree.


## SELECT и INSERT​

Для вставки данных используйте запросINSERT SELECTс агрегирующими функциями с суффиксом-State.
При выборке данных из таблицыAggregatingMergeTreeиспользуйте предложениеGROUP BYи те же агрегирующие функции, что и при вставке данных, но с суффиксом-Merge.

В результатах запросаSELECTзначения типаAggregateFunctionимеют двоичное представление, зависящее от реализации, для всех форматов вывода ClickHouse. Например, если вы выгружаете данные в форматеTabSeparatedс помощью запросаSELECT, то этот дамп можно загрузить обратно с помощью запросаINSERT.


## Пример агрегированного материализованного представления​

В этом примере предполагается, что у вас есть база данных под названиемtest. Создайте её, если она ещё не существует, с помощью приведённой ниже команды:


```
CREATE DATABASE test;

```

Теперь создайте таблицуtest.visits, которая содержит сырые данные:


```
CREATE TABLE test.visits
 (
    StartDate DateTime64 NOT NULL,
    CounterID UInt64,
    Sign Nullable(Int32),
    UserID Nullable(Int32)
) ENGINE = MergeTree ORDER BY (StartDate, CounterID);

```

Далее необходимо создать таблицуAggregatingMergeTree, которая будет хранить агрегирующие функцииAggregationFunction, отслеживающие общее количество посещений и количество уникальных пользователей.

Создайте материализованное представление с движкомAggregatingMergeTree, которое отслеживает таблицуtest.visitsи использует типAggregateFunction:


```
CREATE TABLE test.agg_visits (
    StartDate DateTime64 NOT NULL,
    CounterID UInt64,
    Visits AggregateFunction(sum, Nullable(Int32)),
    Users AggregateFunction(uniq, Nullable(Int32))
)
ENGINE = AggregatingMergeTree() ORDER BY (StartDate, CounterID);

```

Создайте материализованное представление, которое заполняет таблицуtest.agg_visitsданными изtest.visits:


```
CREATE MATERIALIZED VIEW test.visits_mv TO test.agg_visits
AS SELECT
    StartDate,
    CounterID,
    sumState(Sign) AS Visits,
    uniqState(UserID) AS Users
FROM test.visits
GROUP BY StartDate, CounterID;

```

Добавьте данные в таблицуtest.visits:


```
INSERT INTO test.visits (StartDate, CounterID, Sign, UserID)
 VALUES (1667446031000, 1, 3, 4), (1667446031000, 1, 6, 3);

```

Данные вставляются как вtest.visits, так и вtest.agg_visits.

Чтобы получить агрегированные данные, выполните запрос видаSELECT ... GROUP BY ...к материализованному представлениюtest.visits_mv:


```
SELECT
    StartDate,
    sumMerge(Visits) AS Visits,
    uniqMerge(Users) AS Users
FROM test.visits_mv
GROUP BY StartDate
ORDER BY StartDate;

```


```
┌───────────────StartDate─┬─Visits─┬─Users─┐
│ 2022-11-03 03:27:11.000 │      9 │     2 │
└─────────────────────────┴────────┴───────┘

```

Добавьте ещё пару записей вtest.visits, но на этот раз попробуйте использовать другое значение временной метки для одной из записей:


```
INSERT INTO test.visits (StartDate, CounterID, Sign, UserID)
 VALUES (1669446031000, 2, 5, 10), (1667446031000, 3, 7, 5);

```

Выполните запросSELECTещё раз — будет выведен следующий результат:


```
┌───────────────StartDate─┬─Visits─┬─Users─┐
│ 2022-11-03 03:27:11.000 │     16 │     3 │
│ 2022-11-26 07:00:31.000 │      5 │     1 │
└─────────────────────────┴────────┴───────┘

```

В некоторых случаях вы можете захотеть избежать предварительной агрегации строк во время вставки, чтобы перенести нагрузку агрегации с момента вставки
на момент слияния. Обычно необходимо включать столбцы, которые не участвуют в агрегации, в операторGROUP BYв определении материализованного представления, чтобы избежать ошибки. Однако вы можете воспользоваться функциейinitializeAggregationс настройкойoptimize_on_insert = 0(по умолчанию она включена), чтобы добиться этого. ИспользованиеGROUP BYв этом случае больше не требуется:


```
CREATE MATERIALIZED VIEW test.visits_mv TO test.agg_visits
AS SELECT
    StartDate,
    CounterID,
    initializeAggregation('sumState', Sign) AS Visits,
    initializeAggregation('uniqState', UserID) AS Users
FROM test.visits;

```

При использованииinitializeAggregationагрегатное состояние создаётся для каждой отдельной строки без группировки.
Каждая исходная строка даёт одну строку в материализованном представлении, а фактическая агрегация происходит позже, когдаAggregatingMergeTreeобъединяет части. Это верно только в том случае, еслиoptimize_on_insert = 0.


## Связанные материалы​

- Блог:Использование комбинаторов агрегатных функций в ClickHouse