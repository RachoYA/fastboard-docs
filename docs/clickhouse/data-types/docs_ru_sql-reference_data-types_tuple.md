# Tuple(T1, T2, ...) | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/sql-reference/data-types/tuple

Кортеж элементов, каждый из которых имеет собственныйтип. Кортеж должен содержать как минимум один элемент.

Кортежи используются для временной группировки столбцов. Столбцы могут быть сгруппированы при использовании выражения IN в запросе, а также при указании некоторых формальных параметров лямбда-функций. Дополнительную информацию см. в разделахОператоры INиФункции высшего порядка.

Кортежи могут быть результатом запроса. В этом случае в текстовых форматах, отличных от JSON, значения перечисляются через запятую в(). В форматах JSON кортежи выводятся как массивы (в[]).


## Создание кортежей​

Вы можете использовать функцию для создания кортежа:


```
tuple(T1, T2, ...)

```

Пример создания кортежа:


```
SELECT tuple(1, 'a') AS x, toTypeName(x)

```


```
┌─x───────┬─toTypeName(tuple(1, 'a'))─┐
│ (1,'a') │ Tuple(UInt8, String)      │
└─────────┴───────────────────────────┘

```

Кортеж может содержать один элемент

Пример:


```
SELECT tuple('a') AS x;

```


```
┌─x─────┐
│ ('a') │
└───────┘

```

Синтаксис(tuple_element1, tuple_element2)можно использовать для создания кортежа из нескольких элементов без вызова функцииtuple().

Пример:


```
SELECT (1, 'a') AS x, (today(), rand(), 'someString') AS y, ('a') AS not_a_tuple;

```


```
┌─x───────┬─y──────────────────────────────────────┬─not_a_tuple─┐
│ (1,'a') │ ('2022-09-21',2006973416,'someString') │ a           │
└─────────┴────────────────────────────────────────┴─────────────┘

```


## Определение типов данных​

При создании кортежей на лету ClickHouse определяет тип аргументов кортежа как наименьший возможный тип, который может вместить переданное значение аргумента. Если значение —NULL, определённый тип —Nullable.

Пример автоматического определения типа данных:


```
SELECT tuple(1, NULL) AS x, toTypeName(x)

```


```
┌─x─────────┬─toTypeName(tuple(1, NULL))──────┐
│ (1, NULL) │ Tuple(UInt8, Nullable(Nothing)) │
└───────────┴─────────────────────────────────┘

```


## Обращение к элементам кортежа (Tuple)​

К элементам кортежа (Tuple) можно обращаться по имени или по индексу:


```
CREATE TABLE named_tuples (`a` Tuple(s String, i Int64)) ENGINE = Memory;
INSERT INTO named_tuples VALUES (('y', 10)), (('x',-10));

SELECT a.s FROM named_tuples; -- by name
SELECT a.2 FROM named_tuples; -- by index

```

Результат:


```
┌─a.s─┐
│ y   │
│ x   │
└─────┘

┌─tupleElement(a, 2)─┐
│                 10 │
│                -10 │
└────────────────────┘

```


## Операции сравнения для Tuple​

Два кортежа сравниваются последовательным сравнением их элементов слева направо. Если первый элемент кортежа больше (меньше) соответствующего элемента второго кортежа, то первый кортеж больше (меньше) второго; иначе (если оба элемента равны) сравнивается следующий элемент.

Пример:


```
SELECT (1, 'z') > (1, 'a') c1, (2022, 01, 02) > (2023, 04, 02) c2, (1,2,3) = (3,2,1) c3;

```


```
┌─c1─┬─c2─┬─c3─┐
│  1 │  0 │  0 │
└────┴────┴────┘

```

Практические примеры:


```
CREATE TABLE test
(
    `year` Int16,
    `month` Int8,
    `day` Int8
)
ENGINE = Memory AS
SELECT *
FROM values((2022, 12, 31), (2000, 1, 1));

SELECT * FROM test;

┌─year─┬─month─┬─day─┐
│ 2022 │    12 │  31 │
│ 2000 │     1 │   1 │
└──────┴───────┴─────┘

SELECT *
FROM test
WHERE (year, month, day) > (2010, 1, 1);

┌─year─┬─month─┬─day─┐
│ 2022 │    12 │  31 │
└──────┴───────┴─────┘
CREATE TABLE test
(
    `key` Int64,
    `duration` UInt32,
    `value` Float64
)
ENGINE = Memory AS
SELECT *
FROM values((1, 42, 66.5), (1, 42, 70), (2, 1, 10), (2, 2, 0));

SELECT * FROM test;

┌─key─┬─duration─┬─value─┐
│   1 │       42 │  66.5 │
│   1 │       42 │    70 │
│   2 │        1 │    10 │
│   2 │        2 │     0 │
└─────┴──────────┴───────┘

-- Let's find a value for each key with the biggest duration, if durations are equal, select the biggest value

SELECT
    key,
    max(duration),
    argMax(value, (duration, value))
FROM test
GROUP BY key
ORDER BY key ASC;

┌─key─┬─max(duration)─┬─argMax(value, tuple(duration, value))─┐
│   1 │            42 │                                    70 │
│   2 │             2 │                                     0 │
└─────┴───────────────┴───────────────────────────────────────┘

```


## Nullable(Tuple(T1, T2, ...))​

ТребуетсяSET allow_experimental_nullable_tuple_type = 1Это экспериментальная возможность, и она может измениться в будущих версиях.

Позволяет всему кортежу бытьNULLв отличие отTuple(Nullable(T1), Nullable(T2), ...), гдеNULLмогут быть только отдельные элементы.

Пример:


```
SET allow_experimental_nullable_tuple_type = 1;

CREATE TABLE test (
    id UInt32,
    data Nullable(Tuple(String, Int64))
) ENGINE = Memory;

INSERT INTO test VALUES (1, ('hello', 42)), (2, NULL);

SELECT * FROM test WHERE data IS NULL;

```


```
 ┌─id─┬─data─┐
 │  2 │ ᴺᵁᴸᴸ │
 └────┴──────┘

```
