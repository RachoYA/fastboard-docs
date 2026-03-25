# Типы Float32 | Float64 | BFloat16 | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/sql-reference/data-types/float

Если вам нужны точные вычисления, в частности, если вы работаете с финансовыми или бизнес-данными, требующими высокой точности, вам следует рассмотреть использованиеDecimal.Числа с плавающей запятоймогут приводить к неточным результатам, как показано ниже:CREATE TABLE IF NOT EXISTS float_vs_decimal
(
   my_float Float64,
   my_decimal Decimal64(3)
)
ENGINE=MergeTree
ORDER BY tuple();

# Generate 1 000 000 random numbers with 2 decimal places and store them as a float and as a decimal
INSERT INTO float_vs_decimal SELECT round(randCanonical(), 3) AS res, res FROM system.numbers LIMIT 1000000;SELECT sum(my_float), sum(my_decimal) FROM float_vs_decimal;

┌──────sum(my_float)─┬─sum(my_decimal)─┐
│ 499693.60500000004 │      499693.605 │
└────────────────────┴─────────────────┘

SELECT sumKahan(my_float), sumKahan(my_decimal) FROM float_vs_decimal;

┌─sumKahan(my_float)─┬─sumKahan(my_decimal)─┐
│         499693.605 │           499693.605 │
└────────────────────┴──────────────────────┘

Числа с плавающей запятоймогут приводить к неточным результатам, как показано ниже:CREATE TABLE IF NOT EXISTS float_vs_decimal
(
   my_float Float64,
   my_decimal Decimal64(3)
)
ENGINE=MergeTree
ORDER BY tuple();

# Generate 1 000 000 random numbers with 2 decimal places and store them as a float and as a decimal
INSERT INTO float_vs_decimal SELECT round(randCanonical(), 3) AS res, res FROM system.numbers LIMIT 1000000;SELECT sum(my_float), sum(my_decimal) FROM float_vs_decimal;

┌──────sum(my_float)─┬─sum(my_decimal)─┐
│ 499693.60500000004 │      499693.605 │
└────────────────────┴─────────────────┘

SELECT sumKahan(my_float), sumKahan(my_decimal) FROM float_vs_decimal;

┌─sumKahan(my_float)─┬─sumKahan(my_decimal)─┐
│         499693.605 │           499693.605 │
└────────────────────┴──────────────────────┘


```
CREATE TABLE IF NOT EXISTS float_vs_decimal
(
   my_float Float64,
   my_decimal Decimal64(3)
)
ENGINE=MergeTree
ORDER BY tuple();

# Generate 1 000 000 random numbers with 2 decimal places and store them as a float and as a decimal
INSERT INTO float_vs_decimal SELECT round(randCanonical(), 3) AS res, res FROM system.numbers LIMIT 1000000;

```


```
SELECT sum(my_float), sum(my_decimal) FROM float_vs_decimal;

┌──────sum(my_float)─┬─sum(my_decimal)─┐
│ 499693.60500000004 │      499693.605 │
└────────────────────┴─────────────────┘

SELECT sumKahan(my_float), sumKahan(my_decimal) FROM float_vs_decimal;

┌─sumKahan(my_float)─┬─sumKahan(my_decimal)─┐
│         499693.605 │           499693.605 │
└────────────────────┴──────────────────────┘

```

Эквивалентные типы в ClickHouse и в C приведены ниже:

- Float32—float.
- Float64—double.
Типы Float в ClickHouse имеют следующие алиасы:

- Float32—FLOAT,REAL,SINGLE.
- Float64—DOUBLE,DOUBLE PRECISION.
При создании таблиц можно устанавливать числовые параметры для чисел с плавающей точкой (например,FLOAT(12),FLOAT(15, 22),DOUBLE(12),DOUBLE(4, 18)), но ClickHouse игнорирует их.


## Использование чисел с плавающей точкой​

- Вычисления с числами с плавающей точкой могут привести к ошибке округления.

```
SELECT 1 - 0.9

┌───────minus(1, 0.9)─┐
│ 0.09999999999999998 │
└─────────────────────┘

```

- Результат вычисления зависит от метода вычисления (типа процессора и архитектуры компьютерной системы).
- Вычисления с плавающей точкой могут привести к таким числам, как бесконечность (Inf) и "не-число" (NaN). Это следует учитывать при обработке результатов вычислений.
- При разборе чисел с плавающей точкой из текста результат может не быть ближайшим машинно-представимым числом.

## NaN и Inf​

В отличие от стандартного SQL, ClickHouse поддерживает следующие категории чисел с плавающей точкой:

- Inf– Бесконечность.

```
SELECT 0.5 / 0

┌─divide(0.5, 0)─┐
│            inf │
└────────────────┘

```

- -Inf— Отрицательная бесконечность.

```
SELECT -0.5 / 0

┌─divide(-0.5, 0)─┐
│            -inf │
└─────────────────┘

```

- NaN— Не число.

```
SELECT 0 / 0

┌─divide(0, 0)─┐
│          nan │
└──────────────┘

```

См. правила сортировкиNaNв разделепредложение ORDER BY.


## BFloat16​

BFloat16— это 16-битный тип данных с плавающей точкой с 8-битной экспонентой, знаком и 7-битной мантиссой.
Он полезен для приложений машинного обучения и искусственного интеллекта.

ClickHouse поддерживает преобразования междуFloat32иBFloat16, которые
могут быть выполнены с использованием функцийtoFloat32()илиtoBFloat16.

Большинство других операций не поддерживаются.
