# Функции для работы с массивами - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/functions/regular-functions/array-functions


## array


```
array(x1 [, x2, ..., xN])

```

- `x1` — Константное значение любого типа T. Если указан только этот аргумент, массив будет иметь тип T. - `[, x2, ..., xN]` — Дополнительные N константных значений с общим супертипом с `x1`

```
SELECT array(toInt32(1), toUInt16(2), toInt8(3)) AS a, toTypeName(a)

```


```
┌─a───────┬─toTypeName(a)─┐
│ [1,2,3] │ Array(Int32)  │
└─────────┴───────────────┘

```


```
SELECT array(toInt32(5), toDateTime('1998-06-16'), toInt8(5)) AS a, toTypeName(a)

```


```
Received exception from server (version 25.4.3):
Code: 386. DB::Exception: Received from localhost:9000. DB::Exception:
There is no supertype for types Int32, DateTime, Int8 ...

```


## arrayAUCPR


```
arrayAUCPR(scores, labels[, partial_offsets])

```

- `cores` — Оценки, выдаваемые моделью предсказания. [`Array((U)Int*)`](https://clickhouse.com/docs/ru/reference/data-types/array) или [`Array(Float*)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `labels` — Метки примеров: обычно 1 для положительного примера и 0 для отрицательного. [`Array((U)Int*)`](https://clickhouse.com/docs/ru/reference/data-types/array) или [`Array(Enum)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `partial_offsets` —
- Необязательно. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array) из трёх неотрицательных целых чисел для вычисления частичной площади под PR-кривой (что эквивалентно вертикальной полосе в PR-пространстве) вместо полного AUC. Этот параметр полезен при распределённом вычислении PR AUC. Массив должен содержать следующие элементы [`higher_partitions_tp`, `higher_partitions_fp`, `total_positives`].
- `higher_partitions_tp`: Количество положительных меток в партициях с более высокими оценками.
- `higher_partitions_fp`: Количество отрицательных меток в партициях с более высокими оценками.
- `total_positives`: Общее количество положительных примеров во всём наборе данных.
- Одна партиция может содержать все оценки в диапазоне [0, 0.5).
- Другая партиция может содержать оценки в диапазоне [0.5, 1.0].

```
SELECT arrayAUCPR([0.1, 0.4, 0.35, 0.8], [0, 0, 1, 1]);

```


```
┌─arrayAUCPR([0.1, 0.4, 0.35, 0.8], [0, 0, 1, 1])─┐
│                              0.8333333333333333 │
└─────────────────────────────────────────────────┘

```


## arrayAll


```
arrayAll(func(x[, y1, ..., yN]), source_arr[, cond1_arr, ... , condN_arr])

```

- `func(x[, y1, ..., yN])` — лямбда-функция, которая работает с элементами исходного массива (`x`) и массивов условий (`y`). [`Лямбда-функция`](https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview#arrow-operator-and-lambda)
- `source_arr` — исходный массив для обработки. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `cond1_arr, ...` — Необязательно. N массивов условий, передающих дополнительные аргументы в лямбда-функцию. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayAll(x, y -> x=y, [1, 2, 3], [1, 2, 3])

```


```
1

```


```
SELECT arrayAll(x, y -> x=y, [1, 2, 3], [1, 1, 1])

```


```
0

```


## arrayAutocorrelation


```
arrayAutocorrelation(arr, [max_lag])

```

- `arr` — Массив чисел. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `max_lag` — Необязательный параметр. Максимальное число вычисляемых лагов. Должен быть неотрицательным целым числом. [`Integer`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT arrayAutocorrelation([1, 2, 3, 4, 5]);

```


```
[1, 0.4, -0.1, -0.4, -0.4]

```


```
SELECT arrayAutocorrelation([10, 20, 10]);

```


```
[1, -0.6666666666666669, 0.16666666666666674]

```


```
SELECT arrayAutocorrelation([5, 5, 5]);

```


```
[nan, nan, nan]

```


```
SELECT arrayAutocorrelation([1, 2, 3, 4, 5], 2);

```


```
[1, 0.4]

```


## arrayAvg


```
arrayAvg([func(x[, y1, ..., yN])], source_arr[, cond1_arr, ... , condN_arr])

```

- `func(x[, y1, ..., yN])` — Необязательно. Лямбда-функция, применяемая к элементам исходного массива (`x`) и массивов условий (`y`). [`Лямбда-функция`](https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview#arrow-operator-and-lambda)
- `source_arr` — Исходный массив для обработки. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `[, cond1_arr, ... , condN_arr]` — Необязательно. N массивов условий, которые передают дополнительные аргументы в лямбда-функцию. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayAvg([1, 2, 3, 4]);

```


```
2.5

```


```
SELECT arrayAvg(x, y -> x*y, [2, 3], [2, 3]) AS res;

```


```
6.5

```


## arrayBottomK

- `arrayTopK`, которая возвращает K наибольших элементов.
- `arrayPartialSort`, которая помещает те же K элементов в позиции `[1..K]`, но также сохраняет остальные элементы в неопределённом порядке и не пропускает значения `NULL`.

```
arrayBottomK([f,] K, arr [, arr1, ... ,arrN])

```

- `f(arr[, arr1, ... ,arrN])` — Необязательно. Лямбда-функция для вычисления ключа сортировки для каждого элемента. [`Лямбда-функция`](https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview#arrow-operator-and-lambda)
- `K` — Число наименьших элементов, которые нужно вернуть. [`(U)Int8/16/32/64`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `arr` — Массив. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `arr1, ... ,arrN` — N дополнительных массивов, если `f` принимает несколько аргументов. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayBottomK(3, [1, 5, 2, 7, 3])

```


```
[1,2,3]

```


```
SELECT arrayBottomK(3, [1, NULL, 5, 2, NULL, 7])

```


```
[1,2,5]

```


```
SELECT arrayBottomK(5, [1, NULL, 2])

```


```
[1,2]

```


```
SELECT arrayBottomK((x) -> -x, 2, [5, 9, 1, 3])

```


```
[9,5]

```


```
SELECT arrayBottomK((x, y) -> y, 2, ['a', 'b', 'c'], [3, 1, 2])

```


```
['b','c']

```


## arrayCompact


```
arrayCompact(arr)

```

- `arr` — Массив, из которого удаляются дубликаты. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayCompact([1, 1, nan, nan, 2, 3, 3, 3]);

```


```
[1,nan,2,3]

```


## arrayConcat


```
arrayConcat(arr1 [, arr2, ... , arrN])

```

- `arr1 [, arr2, ... , arrN]` — N массивов, которые нужно объединить. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayConcat([1, 2], [3, 4], [5, 6]) AS res

```


```
[1, 2, 3, 4, 5, 6]

```


## arrayCount


```
arrayCount([func, ] arr1, ...)

```

- `func` — Необязательный. Функция, применяемая к каждому элементу массива (массивов). [`Лямбда-функция`](https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview#arrow-operator-and-lambda)
- `arr1, ..., arrN` — N массивов. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayCount(x -> (x % 2), groupArray(number)) FROM numbers(10)

```


```
5

```


## arrayCumSum


```
arrayCumSum([func,] arr1[, arr2, ... , arrN])

```

- `func` — Необязательно. Лямбда-функция, применяемая к элементам массива на каждой позиции. [`Лямбда-функция`](https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview#arrow-operator-and-lambda)
- `arr1` — Исходный массив числовых значений. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `[arr2, ..., arrN]` — Необязательно. Дополнительные массивы того же размера, передаваемые в качестве аргументов лямбда-функции, если она указана. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayCumSum([1, 1, 1, 1]) AS res

```


```
[1, 2, 3, 4]

```


```
SELECT arrayCumSum(x -> x * 2, [1, 2, 3]) AS res

```


```
[2, 6, 12]

```


## arrayCumSumNonNegative


```
arrayCumSumNonNegative([func,] arr1[, arr2, ... , arrN])

```

- `func` — Необязательно. Лямбда-функция, применяемая к элементам массива в каждой позиции. [`Лямбда-функция`](https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview#arrow-operator-and-lambda)
- `arr1` — Исходный массив числовых значений. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `[arr2, ..., arrN]` — Необязательно. Дополнительные массивы того же размера, передаваемые в лямбда-функцию в качестве аргументов, если она указана. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayCumSumNonNegative([1, 1, -4, 1]) AS res

```


```
[1, 2, 0, 1]

```


```
SELECT arrayCumSumNonNegative(x -> x * 2, [1, -2, 3]) AS res

```


```
[2, 0, 6]

```


## arrayDifference


```
arrayDifference(arr)

```

- `arr` — массив `Array`, для которого вычисляются разности между соседними элементами. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayDifference([1, 2, 3, 4]);

```


```
[0,1,1,1]

```


```
SELECT arrayDifference([0, 10000000000000000000]);

```


```
┌─arrayDifference([0, 10000000000000000000])─┐
│ [0,-8446744073709551616]                   │
└────────────────────────────────────────────┘

```


## arrayDistinct


```
arrayDistinct(arr)

```

- `arr` — Массив, из которого нужно извлечь уникальные элементы. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayDistinct([1, 2, 2, 3, 1]);

```


```
[1,2,3]

```


## arrayDotProduct


```
arrayDotProduct(v1, v2)

```

- `v1` — Первый вектор. [`Array((U)Int* | Float* | BFloat16 | Decimal)`](https://clickhouse.com/docs/ru/reference/data-types/array) или [`Tuple((U)Int* | Float* | Decimal)`](https://clickhouse.com/docs/ru/reference/data-types/tuple)
- `v2` — Второй вектор. [`Array((U)Int* | Float* | BFloat16 | Decimal)`](https://clickhouse.com/docs/ru/reference/data-types/array) или [`Tuple((U)Int* | Float* | Decimal)`](https://clickhouse.com/docs/ru/reference/data-types/tuple)

```
SELECT arrayDotProduct([1, 2, 3], [4, 5, 6]) AS res, toTypeName(res);

```


```
32    UInt16

```


```
SELECT dotProduct((1::UInt16, 2::UInt8, 3::Float32),(4::Int16, 5::Float32, 6::UInt8)) AS res, toTypeName(res);

```


```
32    Float64

```


## arrayElement


```
arrayElement(arr, n)

```

- `arr` — Массив, в котором выполняется поиск. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array). - `n` — Позиция элемента, который требуется получить. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint).

```
SELECT arrayElement(arr, 2) FROM (SELECT [1, 2, 3] AS arr)

```


```
2

```


```
SELECT arrayElement(arr, -1) FROM (SELECT [1, 2, 3] AS arr)

```


```
3

```


```
SELECT arr[2] FROM (SELECT [1, 2, 3] AS arr)

```


```
2

```


```
SELECT arrayElement(arr, 4) FROM (SELECT [1, 2, 3] AS arr)

```


```
0

```


## arrayElementOrNull


```
arrayElementOrNull(arrays)

```

- `arrays` — Произвольное количество аргументов типа массив. [`Array`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayElementOrNull(arr, 2) FROM (SELECT [1, 2, 3] AS arr)

```


```
2

```


```
SELECT arrayElementOrNull(arr, -1) FROM (SELECT [1, 2, 3] AS arr)

```


```
3

```


```
SELECT arrayElementOrNull(arr, 4) FROM (SELECT [1, 2, 3] AS arr)

```


```
NULL

```


## arrayEnumerate


```
arrayEnumerate(arr)

```

- `arr` — массив, который нужно пронумеровать. [`Array`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
CREATE TABLE test
(
    `id` UInt8,
    `tag` Array(String),
    `version` Array(String)
)
ENGINE = MergeTree
ORDER BY id;

INSERT INTO test VALUES (1, ['release-stable', 'dev', 'security'], ['2.4.0', '2.6.0-alpha', '2.4.0-sec1']);

SELECT
    id,
    tag,
    version,
    seq
FROM test
ARRAY JOIN
    tag,
    version,
    arrayEnumerate(tag) AS seq

```


```
┌─id─┬─tag────────────┬─version─────┬─seq─┐
│  1 │ release-stable │ 2.4.0       │   1 │
│  1 │ dev            │ 2.6.0-alpha │   2 │
│  1 │ security       │ 2.4.0-sec1  │   3 │
└────┴────────────────┴─────────────┴─────┘

```


## arrayEnumerateDense


```
arrayEnumerateDense(arr)

```

- `arr` — Массив, который нужно пронумеровать. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayEnumerateDense([10, 20, 10, 30])

```


```
[1,2,1,3]

```


## arrayEnumerateDenseRanked


```
arrayEnumerateDenseRanked(clear_depth, arr, max_array_depth)

```

- `clear_depth` — Отдельно нумерует элементы на указанном уровне. Должен быть меньше или равен `max_arr_depth`. [`UInt*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `arr` — N-мерный массив, элементы которого нужно пронумеровать. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `max_array_depth` — Максимальная эффективная глубина. Должна быть меньше или равна глубине `arr`. [`UInt*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
-- При clear_depth=1 и max_array_depth=1 результат идентичен результату arrayEnumerateDense.

SELECT arrayEnumerateDenseRanked(1,[10, 20, 10, 30],1);

```


```
[1,2,1,3]

```


```
-- В этом примере arrayEnumerateDenseRanked используется для получения массива, указывающего для каждого элемента
-- многомерного массива его порядковый номер среди элементов с одинаковым значением.
-- Для первой строки переданного массива [10, 10, 30, 20] соответствующая первая строка результата равна [1, 1, 2, 3]:
-- 10 — первое встреченное число (позиции 1 и 2), 30 — второе встреченное число (позиция 3),
-- 20 — третье встреченное число (позиция 4).
-- Для второй строки [40, 50, 10, 30] соответствующая вторая строка результата равна [4,5,1,2]: 40
-- и 50 — четвёртое и пятое встреченные числа (позиции 1 и 2 этой строки), ещё одно 10
-- (первое встреченное число) находится в позиции 3, а 30 (второе встреченное число) — в последней позиции.

SELECT arrayEnumerateDenseRanked(1,[[10,10,30,20],[40,50,10,30]],2);

```


```
[[1,1,2,3],[4,5,1,2]]

```


```
-- При clear_depth=2 перечисление выполняется заново отдельно для каждой строки.

SELECT arrayEnumerateDenseRanked(2,[[10,10,30,20],[40,50,10,30]],2);

```


```
[[1, 1, 2, 3], [1, 2, 3, 4]]

```


## arrayEnumerateUniq


```
arrayEnumerateUniq(arr1[, arr2, ... , arrN])

```

- `arr1` — Первый массив для обработки. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `arr2, ...` — Необязательно. Дополнительные массивы того же размера для обеспечения уникальности кортежей. [`Array(UInt32)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayEnumerateUniq([10, 20, 10, 30]);

```


```
[1, 1, 2, 1]

```


```
SELECT arrayEnumerateUniq([1, 1, 1, 2, 2, 2], [1, 1, 2, 1, 1, 2]);

```


```
[1,2,1,1,2,1]

```


```
-- Для каждого идентификатора цели вычисляется количество конверсий (каждый элемент вложенной структуры данных Goals является достигнутой целью, которую мы называем конверсией)
-- и количество сеансов. Без ARRAY JOIN количество сеансов считалось бы как sum(Sign). Однако в данном случае
-- строки были умножены на вложенную структуру Goals, поэтому чтобы учесть каждый сеанс ровно один раз, применяется условие на
-- значение функции arrayEnumerateUniq(Goals.ID).

SELECT
    Goals.ID AS GoalID,
    sum(Sign) AS Reaches,
    sumIf(Sign, num = 1) AS Visits
FROM test.visits
ARRAY JOIN
    Goals,
    arrayEnumerateUniq(Goals.ID) AS num
WHERE CounterID = 160656
GROUP BY GoalID
ORDER BY Reaches DESC
LIMIT 10

```


```
┌──GoalID─┬─Reaches─┬─Visits─┐
│   53225 │    3214 │   1097 │
│ 2825062 │    3188 │   1097 │
│   56600 │    2803 │    488 │
│ 1989037 │    2401 │    365 │
│ 2830064 │    2396 │    910 │
│ 1113562 │    2372 │    373 │
│ 3270895 │    2262 │    812 │
│ 1084657 │    2262 │    345 │
│   56599 │    2260 │    799 │
│ 3271094 │    2256 │    812 │
└─────────┴─────────┴────────┘

```


## arrayEnumerateUniqRanked


```
arrayEnumerateUniqRanked(clear_depth, arr, max_array_depth)

```

- `clear_depth` — Отдельно нумерует элементы на указанном уровне. Положительное целое число, меньшее или равное `max_arr_depth`. [`UInt*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `arr` — N-мерный массив, элементы которого нужно пронумеровать. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `max_array_depth` — Максимальная эффективная глубина. Положительное целое число, меньшее или равное глубине `arr`. [`UInt*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
-- При clear_depth=1 и max_array_depth=1 результат arrayEnumerateUniqRanked
-- совпадает с результатом, который вернул бы arrayEnumerateUniq для того же массива.

SELECT arrayEnumerateUniqRanked(1, [1, 2, 1], 1);

```


```
[1, 1, 2]

```


```
-- При clear_depth=1 и max_array_depth=1 результат arrayEnumerateUniqRanked
-- идентичен результату, который дал бы arrayEnumerateUniq для того же массива.

SELECT arrayEnumerateUniqRanked(1, [[1, 2, 3], [2, 2, 1], [3]], 2);", "[[1, 1, 1], [2, 3, 2], [2]]

```


```
[1, 1, 2]

```


```
-- В этом примере arrayEnumerateUniqRanked используется для получения массива, указывающего,
-- для каждого элемента многомерного массива, какова его позиция среди элементов
-- с тем же значением. Для первой строки переданного массива [1, 2, 3] соответствующий
-- результат равен [1, 1, 1]: значения 1, 2 и 3 встречаются впервые.
-- Для второй строки переданного массива [2, 2, 1] соответствующий результат равен [2, 3, 3]:
-- значение 2 встречается второй и третий раз, а 1 — второй раз.
-- Аналогично, для третьей строки переданного массива [3]
-- соответствующий результат равен [2]: значение 3 встречается второй раз.

SELECT arrayEnumerateUniqRanked(1, [[1, 2, 3], [2, 2, 1], [3]], 2);

```


```
[[1, 1, 1], [2, 3, 2], [2]]

```


```
-- При clear_depth=2 элементы перечисляются отдельно для каждой строки.
SELECT arrayEnumerateUniqRanked(2,[[1, 2, 3],[2, 2, 1],[3]], 2);

```


```
[[1, 1, 1], [1, 2, 1], [1]]

```


## arrayExcept

- Порядок элементов из `source` сохраняется
- Дубликаты в `source` сохраняются, если их нет в `except`
- NULL обрабатывается как отдельное значение

```
arrayExcept(source, except)

```

- `source` — Исходный массив, содержащий элементы для фильтрации. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `except` — Массив, содержащий элементы, которые нужно исключить из результата. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayExcept([1, 2, 3, 2, 4], [3, 5])

```


```
[1, 2, 2, 4]

```


```
SELECT arrayExcept([1, NULL, 2, NULL], [2])

```


```
[1, NULL, NULL]

```


```
SELECT arrayExcept([1, NULL, 2, NULL], [NULL, 2, NULL])

```


```
[1]

```


```
SELECT arrayExcept(['apple', 'banana', 'cherry'], ['banana', 'date'])

```


```
['apple', 'cherry']

```


## arrayExists


```
arrayExists(func(x[, y1, ..., yN]), source_arr[, cond1_arr, ... , condN_arr])

```

- `func(x[, y1, ..., yN])` — Лямбда-функция, которая применяется к элементам исходного массива (`x`) и массивов условий (`y`). [`Лямбда-функция`](https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview#arrow-operator-and-lambda)
- `source_arr` — Исходный массив для обработки. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `[, cond1_arr, ... , condN_arr]` — Необязательно. N массивов условий, которые передают лямбда-функции дополнительные аргументы. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayExists(x, y -> x=y, [1, 2, 3], [0, 0, 0])

```


```
0

```


## arrayFill


```
arrayFill(func(x [, y1, ..., yN]), source_arr[, cond1_arr, ... , condN_arr])

```

- `func(x [, y1, ..., yN])` — лямбда-функция `func(x [, y1, y2, ... yN]) → F(x [, y1, y2, ... yN])`, которая применяется к элементам исходного массива (`x`) и условных массивов (`y`). [`Лямбда-функция`](https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview#arrow-operator-and-lambda)
- `source_arr` — исходный массив для обработки. [`Лямбда-функция`](https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview#arrow-operator-and-lambda)
- `[, cond1_arr, ... , condN_arr]` — Необязательно. N условных массивов, которые передают дополнительные аргументы в лямбда-функцию. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayFill(x -> not isNull(x), [1, null, 2, null]) AS res

```


```
[1, 1, 2, 2]

```


```
SELECT arrayFill(x, y, z -> x > y AND x < z, [5, 3, 6, 2], [4, 7, 1, 3], [10, 2, 8, 5]) AS res

```


```
[5, 5, 6, 6]

```


## arrayFilter


```
arrayFilter(func(x[, y1, ..., yN]), source_arr[, cond1_arr, ... , condN_arr])]

```

- `func(x[, y1, ..., yN])` — лямбда-функция, применяемая к элементам исходного массива (`x`) и массивов условий (`y`). [`Лямбда-функция`](https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview#arrow-operator-and-lambda)
- `source_arr` — исходный массив для обработки. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `[, cond1_arr, ... , condN_arr]` — Необязательно. N массивов условий, передающих дополнительные аргументы в лямбда-функцию. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayFilter(x -> x LIKE '%World%', ['Hello', 'abc World']) AS res

```


```
['abc World']

```


```
SELECT
    arrayFilter(
        (i, x) -> x LIKE '%World%',
        arrayEnumerate(arr),
        ['Hello', 'abc World'] AS arr)
    AS res

```


```
[2]

```


## arrayFirst


```
arrayFirst(func(x[, y1, ..., yN]), source_arr[, cond1_arr, ... , condN_arr])

```

- `func(x[, y1, ..., yN])` — Лямбда-функция, применяемая к элементам исходного массива (`x`) и массивов условий (`y`). [Лямбда-функция](https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview#arrow-operator-and-lambda). - `source_arr` — Исходный массив для обработки. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array). - `[, cond1_arr, ... , condN_arr]` — Необязательно. N массивов условий, передающих дополнительные аргументы в лямбда-функцию. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array).

```
SELECT arrayFirst(x, y -> x=y, ['a', 'b', 'c'], ['c', 'b', 'a'])

```


```
b

```


```
SELECT arrayFirst(x, y -> x=y, [0, 1, 2], [3, 3, 3]) AS res, toTypeName(res)

```


```
0 UInt8

```


## arrayFirstIndex


```
arrayFirstIndex(func(x[, y1, ..., yN]), source_arr[, cond1_arr, ... , condN_arr])

```

- `func(x[, y1, ..., yN])` — Лямбда-функция, применяемая к элементам исходного массива (`x`) и массивов условий (`y`). [Лямбда-функция](https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview#arrow-operator-and-lambda). - `source_arr` — Исходный массив, который нужно обработать. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array). - `[, cond1_arr, ... , condN_arr]` — Необязательно. N массивов условий, передающих дополнительные аргументы в лямбда-функцию. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array).

```
SELECT arrayFirstIndex(x, y -> x=y, ['a', 'b', 'c'], ['c', 'b', 'a'])

```


```
2

```


```
SELECT arrayFirstIndex(x, y -> x=y, ['a', 'b', 'c'], ['d', 'e', 'f'])

```


```
0

```


## arrayFirstOrNull


```
arrayFirstOrNull(func(x[, y1, ..., yN]), source_arr[, cond1_arr, ... , condN_arr])

```

- `func(x[, y1, ..., yN])` — Лямбда-функция, применяемая к элементам исходного массива (`x`) и массивов условий (`y`). [`Лямбда-функция`](https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview#arrow-operator-and-lambda)
- `source_arr` — Исходный массив, который нужно обработать. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `[, cond1_arr, ... , condN_arr]` — Необязательно. N массивов условий, передающих дополнительные аргументы в лямбда-функцию. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayFirstOrNull(x, y -> x=y, ['a', 'b', 'c'], ['c', 'b', 'a'])

```


```
b

```


```
SELECT arrayFirstOrNull(x, y -> x=y, [0, 1, 2], [3, 3, 3]) AS res, toTypeName(res)

```


```
NULL Nullable(UInt8)

```


## arrayFlatten

- Работает с вложенными массивами любой глубины.
- Не изменяет массивы, которые уже являются плоскими.

```
arrayFlatten(arr)

```

- `arr` — Многомерный массив. [`Array(Array(T))`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayFlatten([[[1]], [[2], [3]]]);

```


```
[1, 2, 3]

```


## arrayFold


```
arrayFold(λ(acc, x1 [, x2, x3, ... xN]), arr1 [, arr2, arr3, ... arrN], acc)

```

- `λ(x, x1 [, x2, x3, ... xN])` — Лямбда-функция `λ(acc, x1 [, x2, x3, ... xN]) → F(acc, x1 [, x2, x3, ... xN])`, где `F` — операция, применяемая к `acc` и значениям массива `x`, а затем результат снова используется как `acc`. [`Лямбда-функция`](https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview#arrow-operator-and-lambda)
- `arr1 [, arr2, arr3, ... arrN]` — N массивов, над которыми выполняется операция. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `acc` — Значение аккумулятора того же типа, что и возвращаемое значение лямбда-функции.

```
SELECT arrayFold(acc,x -> acc + x*2, [1, 2, 3, 4], 3::Int64) AS res;

```


```
23

```


```
SELECT arrayFold(acc, x -> (acc.2, acc.2 + acc.1),range(number),(1::Int64, 0::Int64)).1 AS fibonacci FROM numbers(1,10);

```


```
┌─fibonacci─┐
│         0 │
│         1 │
│         1 │
│         2 │
│         3 │
│         5 │
│         8 │
│        13 │
│        21 │
│        34 │
└───────────┘

```


```
SELECT arrayFold(
(acc, x, y) -> acc + (x * y),
[1, 2, 3, 4],
[10, 20, 30, 40],
0::Int64
) AS res;

```


```
300

```


## arrayIntersect


```
arrayIntersect(arr, arr1, ..., arrN)

```

- `arrN` — N массивов, из которых составляется новый массив. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array).

```
SELECT
arrayIntersect([1, 2], [1, 3], [2, 3]) AS empty_intersection,
arrayIntersect([1, 2], [1, 3], [1, 4]) AS non_empty_intersection

```


```
┌─empty_intersection─┬─non_empty_intersection─┐
│ []                 │ [1]                    │
└────────────────────┴────────────────────────┘

```


## arrayJaccardIndex


```
arrayJaccardIndex(arr_x, arr_y)

```

- `arr_x` — Первый массив. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `arr_y` — Второй массив. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayJaccardIndex([1, 2], [2, 3]) AS res

```


```
0.3333333333333333

```


## arrayJoin


```
arrayJoin(arr)

```

- `arr` — Массив, который нужно развернуть. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayJoin([1, 2, 3] AS src) AS dst, 'Hello', src

```


```
┌─dst─┬─\'Hello\'─┬─src─────┐
│   1 │ Hello     │ [1,2,3] │
│   2 │ Hello     │ [1,2,3] │
│   3 │ Hello     │ [1,2,3] │
└─────┴───────────┴─────────┘

```


```
-- The arrayJoin function affects all sections of the query, including the WHERE section. Notice the result 2, even though the subquery returned 1 row.

SELECT sum(1) AS impressions
FROM
(
    SELECT ['Istanbul', 'Berlin', 'Bobruisk'] AS cities
)
WHERE arrayJoin(cities) IN ['Istanbul', 'Berlin'];

```


```
┌─impressions─┐
│           2 │
└─────────────┘

```


```
-- A query can use multiple arrayJoin functions. In this case, the transformation is performed multiple times and the rows are multiplied.

SELECT
    sum(1) AS impressions,
    arrayJoin(cities) AS city,
    arrayJoin(browsers) AS browser
FROM
(
    SELECT
        ['Istanbul', 'Berlin', 'Bobruisk'] AS cities,
        ['Firefox', 'Chrome', 'Chrome'] AS browsers
)
GROUP BY
    2,
    3
ORDER BY
    city,
    browser

```


```
┌─impressions─┬─city─────┬─browser─┐
│           2 │ Berlin   │ Chrome  │
│           1 │ Berlin   │ Firefox │
│           2 │ Bobruisk │ Chrome  │
│           1 │ Bobruisk │ Firefox │
│           2 │ Istanbul │ Chrome  │
│           1 │ Istanbul │ Firefox │
└─────────────┴──────────┴─────────┘

```


```
-- Using multiple arrayJoin with the same expression may not produce the expected result due to optimizations.
-- For these cases, consider modifying the repeated array expression with extra operations that do not affect join result.
-- e.g. arrayJoin(arraySort(arr)), arrayJoin(arrayConcat(arr, []))

SELECT
    arrayJoin(dice) as first_throw,
    /* arrayJoin(dice) as second_throw */ -- is technically correct, but will annihilate result set
    arrayJoin(arrayConcat(dice, [])) as second_throw -- intentionally changed expression to force re-evaluation
FROM (
    SELECT [1, 2, 3, 4, 5, 6] as dice
);

```


```
┌─first_throw─┬─second_throw─┐
│           1 │            1 │
│           1 │            2 │
│           1 │            3 │
│           1 │            4 │
│           1 │            5 │
│           1 │            6 │
│           2 │            1 │
│           2 │            2 │
│           2 │            3 │
│           2 │            4 │
│           2 │            5 │
│           2 │            6 │
│           3 │            1 │
│           3 │            2 │
│           3 │            3 │
│           3 │            4 │
│           3 │            5 │
│           3 │            6 │
│           4 │            1 │
│           4 │            2 │
│           4 │            3 │
│           4 │            4 │
│           4 │            5 │
│           4 │            6 │
│           5 │            1 │
│           5 │            2 │
│           5 │            3 │
│           5 │            4 │
│           5 │            5 │
│           5 │            6 │
│           6 │            1 │
│           6 │            2 │
│           6 │            3 │
│           6 │            4 │
│           6 │            5 │
│           6 │            6 │
└─────────────┴──────────────┘

```


```
-- Note the ARRAY JOIN syntax in the `SELECT` query below, which provides broader possibilities.
-- ARRAY JOIN allows you to convert multiple arrays with the same number of elements at a time.

SELECT
    sum(1) AS impressions,
    city,
    browser
FROM
(
    SELECT
        ['Istanbul', 'Berlin', 'Bobruisk'] AS cities,
        ['Firefox', 'Chrome', 'Chrome'] AS browsers
)
ARRAY JOIN
    cities AS city,
    browsers AS browser
GROUP BY
    2,
    3
ORDER BY
    2,
    3

```


```
┌─impressions─┬─city─────┬─browser─┐
│           1 │ Berlin   │ Chrome  │
│           1 │ Bobruisk │ Chrome  │
│           1 │ Istanbul │ Firefox │
└─────────────┴──────────┴─────────┘

```


```
-- You can also use Tuple

SELECT
    sum(1) AS impressions,
    (arrayJoin(arrayZip(cities, browsers)) AS t).1 AS city,
    t.2 AS browser
FROM
(
    SELECT
        ['Istanbul', 'Berlin', 'Bobruisk'] AS cities,
        ['Firefox', 'Chrome', 'Chrome'] AS browsers
)
GROUP BY
    2,
    3
ORDER BY
    2,
    3

```


```
┌─impressions─┬─city─────┬─browser─┐
│           1 │ Berlin   │ Chrome  │
│           1 │ Bobruisk │ Chrome  │
│           1 │ Istanbul │ Firefox │
└─────────────┴──────────┴─────────┘

```


## arrayLast


```
arrayLast(func(x[, y1, ..., yN]), source[, cond1, ... , condN_arr])

```

- `func(x[, y1, ..., yN])` — Лямбда-функция, применяемая к элементам исходного массива (`x`) и массивов условий (`y`). [Лямбда-функция](https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview#arrow-operator-and-lambda). - `source` — Исходный массив, который нужно обработать. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array). - `[, cond1, ... , condN]` — Необязательно. N массивов условий, передающих лямбда-функции дополнительные аргументы. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array).

```
SELECT arrayLast(x, y -> x=y, ['a', 'b', 'c'], ['a', 'b', 'c'])

```


```
c

```


```
SELECT arrayFirst(x, y -> x=y, [0, 1, 2], [3, 3, 3]) AS res, toTypeName(res)

```


```
0 UInt8

```


## arrayLastIndex


```
arrayLastIndex(func(x[, y1, ..., yN]), source_arr[, cond1_arr, ... , condN_arr])

```

- `func(x[, y1, ..., yN])` — Лямбда-функция, которая применяется к элементам исходного массива (`x`) и массивов условий (`y`). [`Лямбда-функция`](https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview#arrow-operator-and-lambda)
- `source_arr` — Исходный массив для обработки. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `[, cond1_arr, ... , condN_arr]` — Необязательно. N массивов условий, которые передают дополнительные аргументы в лямбда-функцию. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayLastIndex(x, y -> x=y, ['a', 'b', 'c'], ['a', 'b', 'c']);

```


```
3

```


```
SELECT arrayLastIndex(x, y -> x=y, ['a', 'b', 'c'], ['d', 'e', 'f']);

```


```
0

```


## arrayLastOrNull


```
arrayLastOrNull(func(x[, y1, ..., yN]), source_arr[, cond1_arr, ... , condN_arr])

```

- `func(x [, y1, ..., yN])` — лямбда-функция, применяемая к элементам исходного массива (`x`) и массивов условий (`y`). [Лямбда-функция](https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview#arrow-operator-and-lambda). - `source_arr` — исходный массив для обработки. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array). - `[, cond1_arr, ... , condN_arr]` — необязательно. N массивов условий, передающих дополнительные аргументы в лямбда-функцию. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array).

```
SELECT arrayLastOrNull(x, y -> x=y, ['a', 'b', 'c'], ['a', 'b', 'c'])

```


```
c

```


```
SELECT arrayLastOrNull(x, y -> x=y, [0, 1, 2], [3, 3, 3]) AS res, toTypeName(res)

```


```
NULL Nullable(UInt8)

```


## arrayLevenshteinDistance


```
arrayLevenshteinDistance(from, to)

```

- `from` — Первый массив. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array). - `to` — Второй массив. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array).

```
SELECT arrayLevenshteinDistance([1, 2, 4], [1, 2, 3])

```


```
1

```


## arrayLevenshteinDistanceWeighted


```
arrayLevenshteinDistanceWeighted(from, to, from_weights, to_weights)

```

- `from` — первый массив. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array). - `to` — второй массив. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array). - `from_weights` — веса первого массива. [`Array((U)Int*|Float*)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `to_weights` — веса второго массива. [`Array((U)Int*|Float*)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayLevenshteinDistanceWeighted(['A', 'B', 'C'], ['A', 'K', 'L'], [1.0, 2, 3], [3.0, 4, 5])

```


```
14

```


## arrayMap


```
arrayMap(func, arr)

```

- `func` — Лямбда-функция, которая применяется к элементам исходного массива (`x`) и условных массивов (`y`). [`Лямбда-функция`](https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview#arrow-operator-and-lambda)
- `arr` — N массивов для обработки. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayMap(x -> (x + 2), [1, 2, 3]) as res;

```


```
[3, 4, 5]

```


```
SELECT arrayMap((x, y) -> (x, y), [1, 2, 3], [4, 5, 6]) AS res

```


```
[(1, 4),(2, 5),(3, 6)]

```


## arrayMax


```
arrayMax([func(x[, y1, ..., yN])], source_arr[, cond1_arr, ... , condN_arr])

```

- `func(x[, y1, ..., yN])` — Необязательно. Лямбда-функция, применяемая к элементам исходного массива (`x`) и массивов условий (`y`). [`Лямбда-функция`](https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview#arrow-operator-and-lambda)
- `source_arr` — Исходный массив для обработки. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `[, cond1_arr, ... , condN_arr]` — Необязательно. N массивов условий, передающих дополнительные аргументы в лямбда-функцию. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayMax([5, 3, 2, 7]);

```


```
7

```


```
SELECT arrayMax(x, y -> x/y, [4, 8, 12, 16], [1, 2, 1, 2]);

```


```
12

```


## arrayMin


```
arrayMin([func(x[, y1, ..., yN])], source_arr[, cond1_arr, ... , condN_arr])

```

- `func(x[, y1, ..., yN])` — Необязательно. Лямбда-функция, применяемая к элементам исходного массива (`x`) и массивов условий (`y`). [`Лямбда-функция`](https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview#arrow-operator-and-lambda)
- `source_arr` — Исходный массив для обработки. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `cond1_arr, ...` — Необязательно. N массивов условий, передающих в лямбда-функцию дополнительные аргументы. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayMin([5, 3, 2, 7]);

```


```
2

```


```
SELECT arrayMin(x, y -> x/y, [4, 8, 12, 16], [1, 2, 1, 2]);

```


```
4

```


## arrayNormalizedGini


```
arrayNormalizedGini(predicted, label)

```

- `predicted` — Предсказанное значение. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `label` — Фактическое значение. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayNormalizedGini([0.9, 0.3, 0.8, 0.7],[6, 1, 0, 2]);

```


```
(0.18055555555555558, 0.2638888888888889, 0.6842105263157896)

```


## arrayPartialReverseSort


```
arrayPartialReverseSort([f,] limit, arr [, arr1, ... ,arrN])

```

- `f(arr[, arr1, ... ,arrN])` — Лямбда-функция, применяемая к элементам массива `arr`. [`Лямбда-функция`](https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview#arrow-operator-and-lambda)
- `limit` — Значение индекса, до которого выполняется сортировка. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `arr` — Массив для сортировки. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `arr1, ... ,arrN` — N дополнительных массивов, если `f` принимает несколько аргументов. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayPartialReverseSort(2, [5, 9, 1, 3])

```


```
[9, 5, 1, 3]

```


```
SELECT arrayPartialReverseSort(2, ['expenses','lasso','embolism','gladly'])

```


```
['lasso','gladly','expenses','embolism']

```


```
SELECT arrayResize(arrayPartialReverseSort(2, [5, 9, 1, 3]), 2)

```


```
[9, 5]

```


```
SELECT arrayPartialReverseSort((x) -> -x, 2, [5, 9, 1, 3])

```


```
[1, 3, 5, 9]

```


```
SELECT arrayPartialReverseSort((x, y) -> -y, 1, [0, 1, 2], [1, 2, 3]) as res

```


```
[0, 1, 2]

```


## arrayPartialShuffle


```
arrayPartialShuffle(arr [, limit[, seed]])

```

- `arr` — Массив, который нужно перемешать. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `seed` — Необязательно. Seed, используемый при генерации случайных чисел. Если не указан, используется случайное значение. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `limit` — Необязательно. Число, ограничивающее количество перестановок элементов, в диапазоне `[1..N]`. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT arrayPartialShuffle([1, 2, 3, 4], 0)

```


```
[2, 4, 3, 1]

```


```
SELECT arrayPartialShuffle([1, 2, 3, 4])

```


```
[4, 1, 3, 2]

```


```
SELECT arrayPartialShuffle([1, 2, 3, 4], 2)

```


```
[3, 4, 1, 2]

```


```
SELECT arrayPartialShuffle([1, 2, 3, 4], 2, 41)

```


```
[3, 2, 1, 4]

```


```
SELECT arrayPartialShuffle(materialize([1, 2, 3, 4]), 2, 42), arrayPartialShuffle([1, 2, 3], 2, 42) FROM numbers(10)

```


```
┌─arrayPartial⋯4]), 2, 42)─┬─arrayPartial⋯ 3], 2, 42)─┐
│ [3,2,1,4]                │ [3,2,1]                  │
│ [3,2,1,4]                │ [3,2,1]                  │
│ [4,3,2,1]                │ [3,2,1]                  │
│ [1,4,3,2]                │ [3,2,1]                  │
│ [3,4,1,2]                │ [3,2,1]                  │
│ [1,2,3,4]                │ [3,2,1]                  │
│ [1,4,3,2]                │ [3,2,1]                  │
│ [1,4,3,2]                │ [3,2,1]                  │
│ [3,1,2,4]                │ [3,2,1]                  │
│ [1,3,2,4]                │ [3,2,1]                  │
└──────────────────────────┴──────────────────────────┘

```


## arrayPartialSort


```
arrayPartialSort([f,] limit, arr [, arr1, ... ,arrN])

```

- `f(arr[, arr1, ... ,arrN])` — Лямбда-функция, применяемая к элементам массива `x`. [`Лямбда-функция`](https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview#arrow-operator-and-lambda)
- `limit` — Значение индекса, до которого будет выполняться сортировка. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `arr` — Массив, который нужно отсортировать. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `arr1, ... ,arrN` — N дополнительных массивов, если `f` принимает несколько аргументов. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayPartialSort(2, [5, 9, 1, 3])

```


```
[1, 3, 5, 9]

```


```
SELECT arrayPartialSort(2, ['expenses', 'lasso', 'embolism', 'gladly'])

```


```
['embolism', 'expenses', 'gladly', 'lasso']

```


```
SELECT arrayResize(arrayPartialSort(2, [5, 9, 1, 3]), 2)

```


```
[1, 3]

```


```
SELECT arrayPartialSort((x) -> -x, 2, [5, 9, 1, 3])

```


```
[9, 5, 1, 3]

```


```
SELECT arrayPartialSort((x, y) -> -y, 1, [0, 1, 2], [1, 2, 3]) as res

```


```
[2, 1, 0]

```


## arrayPopBack


```
arrayPopBack(arr)

```

- `arr` — Массив, из которого нужно удалить последний элемент. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayPopBack([1, 2, 3]) AS res;

```


```
[1, 2]

```


## arrayPopFront


```
arrayPopFront(arr)

```

- `arr` — массив, из которого нужно удалить первый элемент. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayPopFront([1, 2, 3]) AS res;

```


```
[2, 3]

```


## arrayProduct


```
arrayProduct([func(x[, y1, ..., yN])], source_arr[, cond1_arr, ... , condN_arr])

```

- `func(x[, y1, ..., yN])` — Необязательно. Лямбда-функция, применяемая к элементам исходного массива (`x`) и массивов условий (`y`). [`Лямбда-функция`](https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview#arrow-operator-and-lambda)
- `source_arr` — Исходный массив для обработки. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `[, cond1_arr, ... , condN_arr]` — Необязательно. N массивов условий, передающих дополнительные аргументы в лямбда-функцию. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayProduct([1, 2, 3, 4]);

```


```
24

```


```
SELECT arrayProduct(x, y -> x+y, [2, 2], [2, 2]) AS res;

```


```
16

```


## arrayPushBack


```
arrayPushBack(arr, x)

```

- `arr` — Массив, в конец которого добавляется значение `x`. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `x` —
- Одно значение, добавляемое в конец массива. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array).
- В массив чисел можно добавлять только числа, а в массив строк — только строки.
- При добавлении чисел ClickHouse автоматически приводит тип `x` к типу данных массива.
- Может быть `NULL`. Функция добавляет в массив элемент `NULL`, а тип элементов массива преобразуется в `Nullable`.

```
SELECT arrayPushBack(['a'], 'b') AS res;

```


```
['a','b']

```


## arrayPushFront


```
arrayPushFront(arr, x)

```

- `arr` — Массив, в конец которого добавляется значение `x`. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array). - `x` —
- Одно значение, добавляемое в начало массива. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array).
- В массив чисел можно добавлять только числа, а в массив строк — только строки.
- При добавлении чисел ClickHouse автоматически приводит тип `x` к типу данных массива.
- Может быть `NULL`. Функция добавляет в массив элемент `NULL`, а тип элементов массива преобразуется в `Nullable`.

```
SELECT arrayPushFront(['b'], 'a') AS res;

```


```
['a','b']

```


## arrayROCAUC


```
arrayROCAUC(scores, labels[, scale[, partial_offsets]])

```

- `scores` — Оценки, которые выдаёт модель. [`Array((U)Int*)`](https://clickhouse.com/docs/ru/reference/data-types/array) или [`Array(Float*)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `labels` — Метки объектов, обычно 1 для положительного примера и 0 для отрицательного. [`Array((U)Int*)`](https://clickhouse.com/docs/ru/reference/data-types/array) или [`Enum`](https://clickhouse.com/docs/ru/reference/data-types/enum)
- `scale` — Необязательно. Определяет, нужно ли возвращать нормализованную площадь. Если false, вместо этого возвращается площадь под кривой TP (true positives) x FP (false positives). Значение по умолчанию: true. [`Bool`](https://clickhouse.com/docs/ru/reference/data-types/boolean)
- `partial_offsets` —
- Массив из четырёх неотрицательных целых чисел для вычисления частичной площади под ROC-кривой (эквивалентной вертикальной полосе в пространстве ROC) вместо полного AUC. Эта опция полезна для распределённого вычисления ROC AUC. Массив должен содержать следующие элементы [`higher_partitions_tp`, `higher_partitions_fp`, `total_positives`, `total_negatives`]. [Array](https://clickhouse.com/docs/ru/reference/data-types/array) из неотрицательных [Integers](https://clickhouse.com/docs/ru/reference/data-types/int-uint). Необязательно.
- `higher_partitions_tp`: Количество положительных меток в партициях с более высокими оценками.
- `higher_partitions_fp`: Количество отрицательных меток в партициях с более высокими оценками.
- `total_positives`: Общее количество положительных примеров во всём наборе данных.
- `total_negatives`: Общее количество отрицательных примеров во всём наборе данных.
- Одна партиция может содержать все оценки в диапазоне [0, 0.5).
- Другая партиция может содержать оценки в диапазоне [0.5, 1.0].

```
SELECT arrayROCAUC([0.1, 0.4, 0.35, 0.8], [0, 0, 1, 1]);

```


```
0.75

```


## arrayRandomSample


```
arrayRandomSample(arr, samples)

```

- `arr` — Входной массив или многомерный массив, из которого производится выборка элементов. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `samples` — Количество элементов, которые нужно включить в случайную выборку. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT arrayRandomSample(['apple', 'banana', 'cherry', 'date'], 2) as res;

```


```
['cherry','apple']

```


```
SELECT arrayRandomSample([[1, 2], [3, 4], [5, 6]], 2) as res;

```


```
[[3,4],[5,6]]

```


## arrayReduce


```
arrayReduce(agg_f, arr1[, arr2, ... , arrN])

```

- `agg_f` — имя агрегатной функции; должно быть константой. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `arr1[, arr2, ... , arrN]` — N массивов, соответствующих аргументам `agg_f`. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayReduce('max', [1, 2, 3]);

```


```
┌─arrayReduce('max', [1, 2, 3])─┐
│                             3 │
└───────────────────────────────┘

```


```
--Если агрегатная функция принимает несколько аргументов, она должна применяться к нескольким массивам одинакового размера.

SELECT arrayReduce('maxIf', [3, 5], [1, 0]);

```


```
┌─arrayReduce('maxIf', [3, 5], [1, 0])─┐
│                                    3 │
└──────────────────────────────────────┘

```


```
SELECT arrayReduce('uniqUpTo(3)', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

```


```
┌─arrayReduce('uniqUpTo(3)', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])─┐
│                                                           4 │
└─────────────────────────────────────────────────────────────┘

```


## arrayReduceInRanges


```
arrayReduceInRanges(agg_f, ranges, arr1[, arr2, ... ,arrN])

```

- `agg_f` — Имя используемой агрегатной функции. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `ranges` — Диапазон, по которому выполняется агрегирование. Массив кортежей `(i, r)`, содержащих индекс `i`, с которого следует начинать, и диапазон `r`, по которому выполняется агрегирование. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array) или [`Tuple(T)`](https://clickhouse.com/docs/ru/reference/data-types/tuple)
- `arr1[, arr2, ... ,arrN]` — N массивов в качестве аргументов агрегатной функции. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayReduceInRanges(
    'sum',
    [(1, 5), (2, 3), (3, 4), (4, 4)],
    [1000000, 200000, 30000, 4000, 500, 60, 7]
) AS res

```


```
┌─res─────────────────────────┐
│ [1234500,234000,34560,4567] │
└─────────────────────────────┘

```


## arrayRemove


```
arrayRemove(arr, elem)

```

- `arr` — Array(T) - `elem` — T

```
SELECT arrayRemove([1, 2, 2, 3], 2)

```


```
[1, 3]

```


```
SELECT arrayRemove(['a', NULL, 'b', NULL], NULL)

```


```
['a', 'b']

```


## arrayResize


```
arrayResize(arr, size[, extender])

```

- `arr` — Массив, размер которого нужно изменить. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `size` — -Новая длина массива. Если `size` меньше исходного размера массива, массив обрезается справа. Если `size` больше исходного размера массива, массив расширяется вправо значениями `extender` или значениями по умолчанию для типа данных элементов массива.
- `extender` — Значение, используемое для расширения массива. Может быть `NULL`.

```
SELECT arrayResize([1], 3);

```


```
[1,0,0]

```


```
SELECT arrayResize([1], 3, NULL);

```


```
[1,NULL,NULL]

```


## arrayReverse


```
arrayReverse(arr)

```

- `arr` — Массив, который нужно развернуть. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayReverse([1, 2, 3])

```


```
[3,2,1]

```


## arrayReverseFill


```
arrayReverseFill(func(x[, y1, ..., yN]), source_arr[, cond1_arr, ... , condN_arr])

```

- `func(x[, y1, ..., yN])` — Лямбда-функция, применяемая к элементам исходного массива (`x`) и условных массивов (`y`). [`Лямбда-функция`](https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview#arrow-operator-and-lambda)
- `source_arr` — Исходный массив для обработки. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `[, cond1_arr, ... , condN_arr]` — Необязательно. N условных массивов, передающих дополнительные аргументы в лямбда-функцию. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayReverseFill(x -> not isNull(x), [1, null, 2, null]) AS res

```


```
[1, 2, 2, NULL]

```


```
SELECT arrayReverseFill(x, y, z -> x > y AND x < z, [5, 3, 6, 2], [4, 7, 1, 3], [10, 2, 8, 5]) AS res;

```


```
[5, 6, 6, 2]

```


## arrayReverseSort

- `-Inf`
- `Inf`
- `NaN`
- `NULL`

```
arrayReverseSort([f,] arr [, arr1, ... ,arrN])

```

- `f(y1[, y2 ... yN])` — лямбда-функция, применяемая к элементам массива `x`. - `arr` — массив, который нужно отсортировать. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array) - `arr1, ..., arrN` — необязательно. N дополнительных массивов, если `f` принимает несколько аргументов.

```
SELECT arrayReverseSort((x, y) -> y, [4, 3, 5], ['a', 'b', 'c']) AS res;

```


```
[5,3,4]

```


```
SELECT arrayReverseSort((x, y) -> -y, [4, 3, 5], [1, 2, 3]) AS res;

```


```
[4,3,5]

```


## arrayReverseSplit


```
arrayReverseSplit(func(x[, y1, ..., yN]), source_arr[, cond1_arr, ... , condN_arr])

```

- `func(x[, y1, ..., yN])` — Лямбда-функция, применяемая к элементам исходного массива (`x`) и массивов условий (`y`). [`Лямбда-функция`](https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview#arrow-operator-and-lambda)
- `source_arr` — Исходный массив для обработки. [`Лямбда-функция`](https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview#arrow-operator-and-lambda)
- `[, cond1_arr, ... , condN_arr]` — Необязательно. N массивов условий, предоставляющих лямбда-функции дополнительные аргументы. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayReverseSplit((x, y) -> y, [1, 2, 3, 4, 5], [1, 0, 0, 1, 0]) AS res

```


```
[[1], [2, 3, 4], [5]]

```


## arrayRotateLeft


```
arrayRotateLeft(arr, n)

```

- `arr` — Массив, элементы которого нужно циклически сдвинуть.[`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array). - `n` — Количество элементов для циклического сдвига. [`(U)Int8/16/32/64`](https://clickhouse.com/docs/ru/reference/data-types/int-uint).

```
SELECT arrayRotateLeft([1,2,3,4,5,6], 2) as res;

```


```
[3,4,5,6,1,2]

```


```
SELECT arrayRotateLeft([1,2,3,4,5,6], -2) as res;

```


```
[5,6,1,2,3,4]

```


## arrayRotateRight


```
arrayRotateRight(arr, n)

```

- `arr` — Массив, элементы которого нужно циклически сдвинуть.[`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array). - `n` — Количество элементов, на которое выполняется циклический сдвиг. [`(U)Int8/16/32/64`](https://clickhouse.com/docs/ru/reference/data-types/int-uint).

```
SELECT arrayRotateRight([1,2,3,4,5,6], 2) as res;

```


```
[5,6,1,2,3,4]

```


```
SELECT arrayRotateRight([1,2,3,4,5,6], -2) as res;

```


```
[3,4,5,6,1,2]

```


## arrayShiftLeft


```
arrayShiftLeft(arr, n[, default])

```

- `arr` — Массив, элементы которого нужно сдвинуть.[`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array). - `n` — Количество элементов, на которое нужно выполнить сдвиг.[`(U)Int8/16/32/64`](https://clickhouse.com/docs/ru/reference/data-types/int-uint). - `default` — Необязательно. Значение по умолчанию для новых элементов.

```
SELECT arrayShiftLeft([1,2,3,4,5,6], 2) as res;

```


```
[3,4,5,6,0,0]

```


```
SELECT arrayShiftLeft([1,2,3,4,5,6], -2) as res;

```


```
[0,0,1,2,3,4]

```


```
SELECT arrayShiftLeft([1,2,3,4,5,6], 2, 42) as res;

```


```
[3,4,5,6,42,42]

```


## arrayShiftRight


```
arrayShiftRight(arr, n[, default])

```

- `arr` — Массив, элементы которого нужно сдвинуть. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `n` — Количество элементов, на которое нужно выполнить сдвиг. [`(U)Int8/16/32/64`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `default` — Необязательно. Значение по умолчанию для новых элементов.

```
SELECT arrayShiftRight([1, 2, 3, 4, 5, 6], 2) as res;

```


```
[0, 0, 1, 2, 3, 4]

```


```
SELECT arrayShiftRight([1, 2, 3, 4, 5, 6], -2) as res;

```


```
[3, 4, 5, 6, 0, 0]

```


```
SELECT arrayShiftRight([1, 2, 3, 4, 5, 6], 2, 42) as res;

```


```
[42, 42, 1, 2, 3, 4]

```


## arrayShingles


```
arrayShingles(arr, l)

```

- `arr` — массив, для которого нужно сгенерировать массив шинглов. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `l` — длина каждого шингла. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT arrayShingles([1, 2, 3, 4], 3) as res;

```


```
[[1, 2, 3], [2, 3, 4]]

```


## arrayShuffle


```
arrayShuffle(arr [, seed])

```

- `arr` — Массив, который нужно перемешать. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `seed (optional)` — Необязательно. Значение seed, используемое для генерации случайных чисел. Если не указано, используется случайное значение. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT arrayShuffle([1, 2, 3, 4]);

```


```
[1,4,2,3]

```


```
SELECT arrayShuffle([1, 2, 3, 4], 41);

```


```
[3,2,1,4]

```


## arraySimilarity


```
arraySimilarity(from, to, from_weights, to_weights)

```

- `from` — первый массив [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `to` — второй массив [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `from_weights` — веса первого массива. [`Array((U)Int*|Float*)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `to_weights` — веса второго массива. [`Array((U)Int*|Float*)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arraySimilarity(['A', 'B', 'C'], ['A', 'K', 'L'], [1.0, 2, 3], [3.0, 4, 5]);

```


```
0.2222222222222222

```


## arraySlice


```
arraySlice(arr, offset [, length])

```

- `arr` — Массив, из которого берётся срез. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `offset` — Отступ от края массива. Положительное значение указывает на смещение слева, а отрицательное — на отступ справа. Нумерация элементов массива начинается с `1`. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `length` — Длина требуемого среза. Если указать отрицательное значение, функция возвращает открытый срез `[offset, array_length - length]`. Если не указывать это значение, функция возвращает срез `[offset, the_end_of_array]`. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT arraySlice([1, 2, NULL, 4, 5], 2, 3) AS res;

```


```
[2, NULL, 4]

```


## arraySort

- `-Inf`
- `Inf`
- `NaN`
- `NULL`

```
arraySort([f,] arr [, arr1, ... ,arrN])

```

- `f(y1[, y2 ... yN])` — лямбда-функция, применяемая к элементам массива `x`. - `arr` — массив, который необходимо отсортировать. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array) - `arr1, ..., arrN` — Необязательно. N дополнительных массивов, если `f` принимает несколько аргументов.

```
SELECT arraySort([1, 3, 3, 0]);

```


```
[0,1,3,3]

```


```
SELECT arraySort(['hello', 'world', '!']);

```


```
['!','hello','world']

```


```
SELECT arraySort([1, nan, 2, NULL, 3, nan, -4, NULL, inf, -inf]);

```


```
[-inf,-4,1,2,3,inf,nan,nan,NULL,NULL]

```


## arraySplit


```
arraySplit(func(x[, y1, ..., yN]), source_arr[, cond1_arr, ... , condN_arr])

```

- `func(x[, y1, ..., yN])` — Лямбда-функция, применяемая к элементам исходного массива (`x`) и условных массивов (`y`). [Лямбда-функция](https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview#arrow-operator-and-lambda). - `source_arr` — Исходный массив, который нужно разбить [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array). - `[, cond1_arr, ... , condN_arr]` — Необязательно. N условных массивов, передающих лямбда-функции дополнительные аргументы. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array).

```
SELECT arraySplit((x, y) -> y, [1, 2, 3, 4, 5], [1, 0, 0, 1, 0]) AS res

```


```
[[1, 2, 3], [4, 5]]

```


## arraySum


```
arraySum([func(x[, y1, ..., yN])], source_arr[, cond1_arr, ... , condN_arr])

```

- `func(x[, y1, ..., yN])` — Необязательно. Лямбда-функция, применяемая к элементам исходного массива (`x`) и массивов условий (`y`). [`Лямбда-функция`](https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview#arrow-operator-and-lambda)
- `source_arr` — Исходный массив для обработки. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `, cond1_arr, ... , condN_arr]` — Необязательно. N массивов условий, которые передают дополнительные аргументы в лямбда-функцию. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arraySum([1, 2, 3, 4]);

```


```
10

```


```
SELECT arraySum(x, y -> x+y, [1, 1, 1, 1], [1, 1, 1, 1]);

```


```
8

```


## arraySymmetricDifference


```
arraySymmetricDifference(arr1, arr2, ... , arrN)

```

- `arrN` — N массивов, из которых создаётся новый массив. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array).

```
SELECT
arraySymmetricDifference([1, 2], [1, 2], [1, 2]) AS empty_symmetric_difference,
arraySymmetricDifference([1, 2], [1, 2], [1, 3]) AS non_empty_symmetric_difference;

```


```
┌─empty_symmetric_difference─┬─non_empty_symmetric_difference─┐
│ []                         │ [3,2]                          │
└────────────────────────────┴────────────────────────────────┘

```


## arrayTopK


```
arrayTopK([f,] K, arr [, arr1, ... ,arrN])

```

- `f(arr[, arr1, ... ,arrN])` — Необязательно. Лямбда-функция для вычисления ключа сортировки для каждого элемента. [`Лямбда-функция`](https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview#arrow-operator-and-lambda)
- `K` — Количество наибольших элементов, которые нужно вернуть. [`(U)Int8/16/32/64`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `arr` — Массив. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `arr1, ... ,arrN` — N дополнительных массивов, если `f` принимает несколько аргументов. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayTopK(3, [1, 5, 2, 7, 3])

```


```
[7,5,3]

```


```
SELECT arrayTopK(3, [1, NULL, 5, 2, NULL, 7])

```


```
[7,5,2]

```


```
SELECT arrayTopK(5, [1, NULL, 2])

```


```
[2,1]

```


```
SELECT arrayTopK((x) -> -x, 2, [5, 9, 1, 3])

```


```
[1,3]

```


```
SELECT arrayTopK((x, y) -> y, 2, ['a', 'b', 'c'], [3, 1, 2])

```


```
['a','c']

```


## arrayTranspose


```
arrayTranspose(arr)

```

- `arr` — двумерный массив для транспонирования. Все внутренние массивы должны иметь одинаковую длину. [`Array(Array(T))`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayTranspose([[1, 2], [3, 4]])

```


```
[[1, 3], [2, 4]]

```


```
SELECT arrayTranspose([[1, 2, 3], [4, 5, 6]])

```


```
[[1, 4], [2, 5], [3, 6]]

```


```
SELECT arrayTranspose([['a', 'b'], ['c', 'd']])

```


```
[['a', 'c'], ['b', 'd']]

```


## arrayUnion


```
arrayUnion(arr1, arr2, ..., arrN)

```

- `arrN` — N массивов, из которых создаётся новый массив. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT
arrayUnion([-2, 1], [10, 1], [-2], []) as num_example,
arrayUnion(['hi'], [], ['hello', 'hi']) as str_example,
arrayUnion([1, 3, NULL], [2, 3, NULL]) as null_example

```


```
┌─num_example─┬─str_example────┬─null_example─┐
│ [10,-2,1]   │ ['hello','hi'] │ [3,2,1,NULL] │
└─────────────┴────────────────┴──────────────┘

```


## arrayUniq

- Позиция 1: (1,3,5)
- Позиция 2: (2,4,6)

```
arrayUniq(arr1[, arr2, ..., arrN])

```

- `arr1` — Массив, для которого подсчитывается количество уникальных элементов. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `[, arr2, ..., arrN]` — Необязательно. Дополнительные массивы, используемые для подсчета количества уникальных кортежей из элементов, находящихся на соответствующих позициях в нескольких массивах. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayUniq([1, 1, 2, 2])

```


```
2

```


```
SELECT arrayUniq([1, 2, 3, 1], [4, 5, 6, 4])

```


```
3

```


## arrayWithConstant


```
arrayWithConstant(N, x)

```

- `length` — Количество элементов в массиве. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `x` — Значение для `N` элементов массива, любого типа.

```
SELECT arrayWithConstant(3, 1)

```


```
[1, 1, 1]

```


## arrayZip


```
arrayZip(arr1, arr2, ... , arrN)

```

- `arr1, arr2, ... , arrN` — N массивов, объединяемых в один массив. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayZip(['a', 'b', 'c'], [5, 2, 1]);

```


```
[('a', 5), ('b', 2), ('c', 1)]

```


## arrayZipUnaligned


```
arrayZipUnaligned(arr1, arr2, ..., arrN)

```

- `arr1, arr2, ..., arrN` — N массивов, объединённых в один массив. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT arrayZipUnaligned(['a'], [1, 2, 3]);

```


```
[('a', 1),(NULL, 2),(NULL, 3)]

```


## countEqual


```
countEqual(arr, x)

```

- `arr` — Массив, в котором выполняется поиск. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `x` — Значение в массиве, количество вхождений которого нужно подсчитать. Любой тип.

```
SELECT countEqual([1, 2, NULL, NULL], NULL)

```


```
2

```


## empty


```
empty(arr)

```

- `arr` — Входной массив. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT empty([]);

```


```
1

```


## emptyArrayDate


```
emptyArrayDate()

```

- Отсутствуют.

```
SELECT emptyArrayDate()

```


```
[]

```


## emptyArrayDateTime


```
emptyArrayDateTime()

```

- Отсутствуют.

```
SELECT emptyArrayDateTime()

```


```
[]

```


## emptyArrayFloat32


```
emptyArrayFloat32()

```

- Отсутствуют.

```
SELECT emptyArrayFloat32()

```


```
[]

```


## emptyArrayFloat64


```
emptyArrayFloat64()

```

- Отсутствуют.

```
SELECT emptyArrayFloat64()

```


```
[]

```


## emptyArrayInt16


```
emptyArrayInt16()

```

- Отсутствуют.

```
SELECT emptyArrayInt16()

```


```
[]

```


## emptyArrayInt32


```
emptyArrayInt32()

```

- Нет аргументов.

```
SELECT emptyArrayInt32()

```


```
[]

```


## emptyArrayInt64


```
emptyArrayInt64()

```

- Нет.

```
SELECT emptyArrayInt64()

```


```
[]

```


## emptyArrayInt8


```
emptyArrayInt8()

```

- Отсутствуют.

```
SELECT emptyArrayInt8()

```


```
[]

```


## emptyArrayString


```
emptyArrayString()

```

- Отсутствуют.

```
SELECT emptyArrayString()

```


```
[]

```


## emptyArrayToSingle


```
emptyArrayToSingle(arr)

```

- `arr` — Пустой массив. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
CREATE TABLE test (
  a Array(Int32),
  b Array(String),
  c Array(DateTime)
)
ENGINE = MergeTree
ORDER BY tuple();

INSERT INTO test VALUES ([], [], []);

SELECT emptyArrayToSingle(a), emptyArrayToSingle(b), emptyArrayToSingle(c) FROM test;

```


```
┌─emptyArrayToSingle(a)─┬─emptyArrayToSingle(b)─┬─emptyArrayToSingle(c)───┐
│ [0]                   │ ['']                  │ ['1970-01-01 01:00:00'] │
└───────────────────────┴───────────────────────┴─────────────────────────┘

```


## emptyArrayUInt16


```
emptyArrayUInt16()

```

- Отсутствуют.

```
SELECT emptyArrayUInt16()

```


```
[]

```


## emptyArrayUInt32


```
emptyArrayUInt32()

```

- Отсутствуют.

```
SELECT emptyArrayUInt32()

```


```
[]

```


## emptyArrayUInt64


```
emptyArrayUInt64()

```

- Нет.

```
SELECT emptyArrayUInt64()

```


```
[]

```


## emptyArrayUInt8


```
emptyArrayUInt8()

```

- Отсутствуют.

```
SELECT emptyArrayUInt8()

```


```
[]

```


## has


```
has(haystack, needle)

```

- `haystack` — Исходный массив, map или JSON. [`Array`](https://clickhouse.com/docs/ru/reference/data-types/array) или [`Map`](https://clickhouse.com/docs/ru/reference/data-types/map) или [`JSON`](https://clickhouse.com/docs/ru/reference/data-types/newjson)
- `needle` — Искомое значение (элемент массива, ключ в map или строка path в JSON).

```
SELECT has([1, 2, 3], 2)

```


```
1

```


```
SELECT has([1, 2, 3], 4)

```


```
0

```


```
SELECT has(map('a', 1, 'b', 2), 'b')

```


```
1

```


```
SELECT has('{"a": {"b": 1}}'::JSON, 'a.b')

```


```
1

```


## hasAll

- Пустой массив является подмножеством любого массива.
- `Null` обрабатывается как значение.
- Порядок значений в обоих массивах не имеет значения.

```
hasAll(set, subset)

```

- `set` — массив любого типа с набором элементов. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `subset` — массив любого типа, элементы которого имеют с `set` общий супертип; используется для проверки того, что он является подмножеством `set`. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `1`, если `set` содержит все элементы из `subset`.
- `0` — в противном случае.

```
SELECT hasAll([], [])

```


```
1

```


```
SELECT hasAll([1, Null], [Null])

```


```
1

```


```
SELECT hasAll([1.0, 2, 3, 4], [1, 3])

```


```
1

```


```
SELECT hasAll(['a', 'b'], ['a'])

```


```
1

```


```
SELECT hasAll([1], ['a'])

```


```
Raises a NO_COMMON_TYPE exception

```


```
SELECT hasAll([[1, 2], [3, 4]], [[1, 2], [3, 5]])

```


```
0

```


## hasAny

- `Null` обрабатывается как значение.
- Порядок значений в обоих массивах не имеет значения.

```
hasAny(arr_x, arr_y)

```

- `arr_x` — Массив любого типа с элементами. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `arr_y` — Массив любого типа, имеющий общий супертип с массивом `arr_x`. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `1`, если `arr_x` и `arr_y` имеют хотя бы один общий элемент.
- `0` — в противном случае.

```
SELECT hasAny([1], [])

```


```
0

```


```
SELECT hasAny([Null], [Null, 1])

```


```
1

```


```
SELECT hasAny([-128, 1., 512], [1])

```


```
1

```


```
SELECT hasAny([[1, 2], [3, 4]], ['a', 'c'])

```


```
Вызывает исключение `NO_COMMON_TYPE`

```


```
SELECT hasAll([[1, 2], [3, 4]], [[1, 2], [1, 2]])

```


```
1

```


## hasSubstr

- Функция вернёт `1`, если `array2` пуст.
- `NULL` обрабатывается как значение. Иными словами, `hasSubstr([1, 2, NULL, 3, 4], [2,3])` вернёт `0`. Однако `hasSubstr([1, 2, NULL, 3, 4], [2,NULL,3])` вернёт `1`
- Порядок значений в обоих массивах важен.

```
hasSubstr(arr1, arr2)

```

- `arr1` — Массив любого типа с произвольным набором элементов. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `arr2` — Массив любого типа с произвольным набором элементов. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT hasSubstr([], [])

```


```
1

```


```
SELECT hasSubstr([1, Null], [Null])

```


```
1

```


```
SELECT hasSubstr([1.0, 2, 3, 4], [1, 3])

```


```
0

```


```
SELECT hasSubstr(['a', 'b'], ['a'])

```


```
1

```


```
SELECT hasSubstr(['a', 'b' , 'c'], ['a', 'b'])

```


```
1

```


```
SELECT hasSubstr(['a', 'b' , 'c'], ['a', 'c'])

```


```
0

```


```
SELECT hasSubstr([[1, 2], [3, 4], [5, 6]], [[1, 2], [3, 4]])

```


```
1

```


```
SELECT hasSubstr([1, 2, NULL, 3, 4], ['a'])

```


```
Вызывает исключение `NO_COMMON_TYPE`

```


## indexOf


```
indexOf(arr, x)

```

- `arr` — Массив, в котором выполняется поиск `x`. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `x` — Значение первого совпавшего элемента в `arr`, индекс которого нужно вернуть. [`UInt64`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT indexOf([5, 4, 1, 3], 3)

```


```
4

```


```
SELECT indexOf([1, 3, NULL, NULL], NULL)

```


```
3

```


## indexOfAssumeSorted


```
indexOfAssumeSorted(arr, x)

```

- `arr` — Отсортированный массив, в котором выполняется поиск. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `x` — Значение первого совпадающего элемента в отсортированном `arr`, индекс которого нужно вернуть. [`UInt64`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT indexOfAssumeSorted([1, 3, 3, 3, 4, 4, 5], 4)

```


```
5

```


## length

- Для аргументов String или FixedString: вычисляет число байтов в строке.
- Для аргументов Array: вычисляет число элементов в массиве.
- Для аргументов QBit: вычисляет размерность вектора.
- Если функция применяется к аргументу FixedString или QBit, она является константным выражением.

```
length(x)

```

- `x` — значение, для которого вычисляется число байтов (для `String`/`FixedString`), элементов (для `Array`) или размерность (для `QBit`). [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring) или [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array) или [`QBit`](https://clickhouse.com/docs/ru/reference/data-types/qbit)

```
SELECT length('Hello, world!')

```


```
13

```


```
SELECT length(['Hello', 'world'])

```


```
2

```


```
SELECT length([0, 0, 0, 0, 0, 0, 0, 0]::QBit(Float32, 8))

```


```
8

```


```
WITH 'hello' || toString(number) AS str
SELECT str,
isConstant(length(str)) AS str_length_is_constant,
isConstant(length(str::FixedString(6))) AS fixed_str_length_is_constant
FROM numbers(3)

```


```
┌─str────┬─str_length_is_constant─┬─fixed_str_length_is_constant─┐
│ hello0 │                      0 │                            1 │
│ hello1 │                      0 │                            1 │
│ hello2 │                      0 │                            1 │
└────────┴────────────────────────┴──────────────────────────────┘

```


```
SELECT 'ёлка' AS str1, length(str1), lengthUTF8(str1), normalizeUTF8NFKD(str1) AS str2, length(str2), lengthUTF8(str2)

```


```
┌─str1─┬─length(str1)─┬─lengthUTF8(str1)─┬─str2─┬─length(str2)─┬─lengthUTF8(str2)─┐
│ ёлка │            8 │                4 │ ёлка │           10 │                5 │
└──────┴──────────────┴──────────────────┴──────┴──────────────┴──────────────────┘

```


```
SELECT 'ábc' AS str, length(str), lengthUTF8(str)

```


```
┌─str─┬─length(str)──┬─lengthUTF8(str)─┐
│ ábc │            4 │               3 │
└─────┴──────────────┴─────────────────┘

```


## notEmpty


```
notEmpty(arr)

```

- `arr` — входной массив. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT notEmpty([1,2]);

```


```
1

```


## randomHadamardTransform

- степень двойки (обычное быстрое преобразование Уолша-Адамара);
- `2^k * m`, где `m` принадлежит `{12, 20}` (порядки, для которых существует матрица Адамара `+/-1`, например `768 = 64 * 12`, `1536 = 128 * 12`, `3072 = 256 * 12`, `2560 = 128 * 20`), применяется как точное преобразование Кронекера `H_(2^k) (x) H_m` (без умножений с плавающей запятой);
- `2^k * m`, где `m` — любое другое нечётное число до `64` (порядки, для которых матрицы Адамара `+/-1` не существует — они есть только для порядков `1`, `2` и чисел, кратных `4`), применяется как точное преобразование Кронекера `H_(2^k) (x) C_m`, где `C_m` — вещественная ортогональная матрица дискретного преобразования Хартли. Это покрывает оставшиеся семейства эмбеддингов, такие как `3584 = 512 * 7`, `1152 = 128 * 9`, `1408 = 128 * 11`.
- `seed` (необязательно, по умолчанию `0`): выбирает схему знаков; один и тот же seed всегда даёт одно и то же преобразование.
- `output_dims` (необязательно, по умолчанию длина преобразования): сохраняет только первые `output_dims` координат, превращая преобразование в случайную проекцию, которая принимает **любую** длину. Масштабирование `1/sqrt(output_dims)` сохраняет норму результата для полного преобразования и сохраняет её в математическом ожидании при усечении. Значение не должно превышать длину преобразования. Поскольку усечённый префикс фактора дискретного преобразования Хартли `C_m` не обладает такой же равномерностью leverage, как матрица Адамара `+/-1`, усечение через `output_dims` для длины из семейства Хартли (или для любой длины без точного разложения) использует дополненное нулями преобразование степени двойки, которое это свойство сохраняет.

```
randomHadamardTransform(vector[, seed[, output_dims]])

```

- `vector` — Вектор для преобразования. [`Array(BFloat16)`](https://clickhouse.com/docs/ru/reference/data-types/array) или [`Array(Float32)`](https://clickhouse.com/docs/ru/reference/data-types/array) или [`Array(Float64)`](https://clickhouse.com/docs/ru/reference/data-types/array)
- `seed` — Необязательно. seed для детерминированных знаков +/-1 (по умолчанию 0). [`UInt*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `output_dims` — Необязательно. Обрезает результат до указанного числа начальных координат (по умолчанию: полная длина преобразования, которая совпадает с длиной входного вектора для любой поддерживаемой размерности). Передача output_dims также включает преобразование для длин, у которых нет точной формы полного преобразования. [`UInt*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT length(randomHadamardTransform([1, 2, 3, 4]::Array(Float32)))

```


```
4

```


```
SELECT round(arraySum(x -> x * x, randomHadamardTransform([1, 2, 3, 4]::Array(Float32))) - 30, 4)

```


```
0

```


```
SELECT length(randomHadamardTransform([1, 2, 3, 4, 5, 6, 7, 8]::Array(Float32), 42, 3))

```


```
3

```


```
SELECT length(randomHadamardTransform(CAST(range(1152), 'Array(Float32)')))

```


```
1152

```


## range

- `UInt8/16/32/64`
- `Int8/16/32/64]`
- Все аргументы `start`, `end`, `step` должны относиться к одному из поддерживаемых выше типов. Элементы возвращаемого массива будут супертипом аргументов.
- Генерируется исключение, если функция возвращает массив, общая длина которого превышает количество элементов, заданное настройкой [`function_range_max_elements_in_block`](https://clickhouse.com/docs/ru/reference/settings/session-settings#function_range_max_elements_in_block).
- Возвращает `NULL`, если любой аргумент имеет тип Nullable(nothing). Генерируется исключение, если любой аргумент имеет значение `NULL` (тип Nullable(T)).

```
range([start, ] end [, step])

```

- `start` — Необязательный. Первый элемент массива. Обязателен, если используется `step`. Значение по умолчанию: `0`. - `end` — Обязательный. Число, до которого строится массив. - `step` — Необязательный. Определяет шаг между элементами массива. Значение по умолчанию: `1`.

```
SELECT range(5), range(1, 5), range(1, 5, 2), range(-1, 5, 2);

```


```
┌─range(5)────┬─range(1, 5)─┬─range(1, 5, 2)─┬─range(-1, 5, 2)─┐
│ [0,1,2,3,4] │ [1,2,3,4]   │ [1,3]          │ [-1,1,3]        │
└─────────────┴─────────────┴────────────────┴─────────────────┘

```


## replicate


```
replicate(x, arr)

```

- `x` — Значение, которым заполняется результирующий массив. [`Any`](https://clickhouse.com/docs/ru/reference/data-types/index)
- `arr` — Массив. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT replicate(1, ['a', 'b', 'c']);

```


```
┌─replicate(1, ['a', 'b', 'c'])───┐
│ [1, 1, 1]                       │
└─────────────────────────────────┘

```


## reverse


```
reverse(arr | str)

```

- `arr | str` — Исходный массив или строка. [`Array(T)`](https://clickhouse.com/docs/ru/reference/data-types/array) или [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT reverse([1, 2, 3, 4]);

```


```
[4, 3, 2, 1]

```


```
SELECT reverse('abcd');

```


```
'dcba'

```


## Функции расстояния

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
