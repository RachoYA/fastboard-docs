# Типы Float32 | Float64 | BFloat16 - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/data-types/float


```
CREATE TABLE IF NOT EXISTS float_vs_decimal
(
my_float Float64,
my_decimal Decimal64(3)
)
ENGINE=MergeTree
ORDER BY tuple();

# Сгенерировать 1 000 000 случайных чисел с 2 знаками после запятой и сохранить их как float и как decimal
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

- `Float32` — `float`.
- `Float64` — `double`.
- `Float32` — `FLOAT`, `REAL`, `SINGLE`.
- `Float64` — `DOUBLE`, `DOUBLE PRECISION`.

## Использование чисел с плавающей запятой

- При вычислениях с числами с плавающей запятой может возникать ошибка округления.

```
SELECT 1 - 0.9

┌───────minus(1, 0.9)─┐
│ 0.09999999999999998 │
└─────────────────────┘

```

- Результат вычислений зависит от способа вычислений (типа процессора и архитектуры компьютерной системы).
- Вычисления с числами с плавающей запятой могут давать такие значения, как бесконечность (`Inf`) и «не число» (`NaN`). Это следует учитывать при обработке результатов вычислений.
- При разборе чисел с плавающей запятой из текста результат может не быть ближайшим числом, представимым в машинном формате.

## NaN и Inf

- `Inf` — бесконечность.

```
SELECT 0.5 / 0

┌─divide(0.5, 0)─┐
│            inf │
└────────────────┘

```

- `-Inf` — Отрицательная бесконечность.

```
SELECT -0.5 / 0

┌─divide(-0.5, 0)─┐
│            -inf │
└─────────────────┘

```

- `NaN` — не является числом.

```
SELECT 0 / 0

┌─divide(0, 0)─┐
│          nan │
└──────────────┘

```


## Значения NaN в семантике множеств

- `0./0.` даёт `NaN`, у которого на большинстве платформ x86 знаковый бит равен 1.
- Литерал `nan` даёт `NaN`, у которого знаковый бит равен 0.
- После [PR #98230](https://github.com/ClickHouse/ClickHouse/pull/98230) путь AArch64 NEON для `log` возвращает `NaN`, у которого знаковый бит отличается от скалярного `log` из glibc для отрицательных входных значений.

```
SELECT countDistinct(arrayJoin([0./0., nan, log(-1.)]));
-- May return 2 or 3 depending on architecture and build, even though all three inputs are NaN.

```


```
-- Replace every NaN with a single canonical NaN value
SELECT countDistinct(if(isNaN(x), CAST('nan' AS Float64), x))
FROM (SELECT arrayJoin([0./0., nan, log(-1.)]) AS x);
-- Returns 1.

-- Or exclude NaN values from the set entirely
SELECT countDistinct(if(isNaN(x), NULL, x))
FROM (SELECT arrayJoin([0./0., nan, log(-1.)]) AS x);
-- Returns 0.

```


## BFloat16

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
