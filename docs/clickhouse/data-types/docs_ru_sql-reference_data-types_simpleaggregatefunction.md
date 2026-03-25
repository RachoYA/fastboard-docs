# Тип данных SimpleAggregateFunction | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/sql-reference/data-types/simpleaggregatefunction


## Описание​

Тип данныхSimpleAggregateFunctionхранит промежуточное состояние
агрегатной функции, но не её полное состояние, как это делает типAggregateFunction.

Эта оптимизация может быть применена к функциям, для которых выполняется
следующее свойство:

результат применения функцииfк набору строкS1 UNION ALL S2может быть
получен путём раздельного примененияfк частям набора строк, а затем
повторного примененияfк результатам:f(S1 UNION ALL S2) = f(f(S1) UNION ALL f(S2)).

Это свойство гарантирует, что частичных результатов агрегации достаточно для
вычисления объединённого результата, поэтому нам не нужно хранить и обрабатывать
избыточные данные. Например, результат функцийminилиmaxне требует
дополнительных шагов для вычисления окончательного результата из
промежуточных шагов, тогда как функцияavgтребует хранения суммы и
количества, которые затем делятся для получения среднего значения
на заключительном шагеMerge, объединяющем промежуточные состояния.

Значения агрегатных функций обычно получаются путём вызова агрегатной функции
с комбинатором-SimpleState, добавленным к имени функции.


## Синтаксис​


```
SimpleAggregateFunction(aggregate_function_name, types_of_arguments...)

```

Параметры

- aggregate_function_name— имя агрегатной функции.
- Type— типы аргументов агрегатной функции.

## Поддерживаемые функции​

Поддерживаются следующие агрегатные функции:

- any
- any_respect_nulls
- anyLast
- anyLast_respect_nulls
- min
- max
- sum
- sumWithOverflow
- groupBitAnd
- groupBitOr
- groupBitXor
- groupArrayArray
- groupUniqArrayArray
- groupUniqArrayArrayMap
- sumMap(sumMappedArrays)
- minMap(minMappedArrays)
- maxMap(maxMappedArrays)
Значения типаSimpleAggregateFunction(func, Type)имеют тот же типType,
поэтому, в отличие от типаAggregateFunction, нет необходимости применять
комбинаторы-Merge/-State.ТипSimpleAggregateFunctionобеспечивает более высокую производительность, чем типAggregateFunctionдля одних и тех же агрегатных функций.

ТипSimpleAggregateFunctionобеспечивает более высокую производительность, чем типAggregateFunctionдля одних и тех же агрегатных функций.


## Пример​


```
CREATE TABLE simple (id UInt64, val SimpleAggregateFunction(sum, Double)) ENGINE=AggregatingMergeTree ORDER BY id;

```


## Связанные материалы​

- Блог:Использование агрегатных комбинаторов в ClickHouse- Блог:Использование агрегатных комбинаторов в ClickHouse
- Тип данныхAggregateFunction.