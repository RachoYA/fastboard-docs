# Decimal, Decimal(P), Decimal(P, S), Decimal32(S), Decimal64(S), Decimal128(S), Decimal256(S) - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/data-types/decimal


## Параметры

- P — точность. Допустимый диапазон: [ 1 : 76 ]. Определяет, сколько десятичных знаков может содержать число (включая дробную часть). По умолчанию точность равна 10.
- S — масштаб. Допустимый диапазон: [ 0 : P ]. Определяет, сколько десятичных знаков может содержать дробная часть.
- при P в диапазоне [ 1 : 9 ] — для Decimal32(S)
- при P в диапазоне [ 10 : 18 ] — для Decimal64(S)
- при P в диапазоне [ 19 : 38 ] — для Decimal128(S)
- при P в диапазоне [ 39 : 76 ] — для Decimal256(S)

## Диапазоны значений Decimal

- Decimal(P, S) - (-1 * 10^(P - S), 1 * 10^(P - S))
- Decimal32(S) - (-1 * 10^(9 - S), 1 * 10^(9 - S))
- Decimal64(S) - (-1 * 10^(18 - S), 1 * 10^(18 - S))
- Decimal128(S) - (-1 * 10^(38 - S), 1 * 10^(38 - S))
- Decimal256(S) - (-1 * 10^(76 - S), 1 * 10^(76 - S))

## Внутреннее представление


## Операции и тип результата

- `Decimal64(S1) <op> Decimal32(S2) -> Decimal64(S)`
- `Decimal128(S1) <op> Decimal32(S2) -> Decimal128(S)`
- `Decimal128(S1) <op> Decimal64(S2) -> Decimal128(S)`
- `Decimal256(S1) <op> Decimal<32|64|128>(S2) -> Decimal256(S)`
- сложение, вычитание: S = max(S1, S2).
- умножение: S = S1 + S2.
- деление: S = S1.

## Проверка переполнения


```
SELECT toDecimal32(2, 4) AS x, x / 3

```


```
┌──────x─┬─divide(toDecimal32(2, 4), 3)─┐
│ 2.0000 │                       0.6666 │
└────────┴──────────────────────────────┘

```


```
SELECT toDecimal32(4.2, 8) AS x, x * x

```


```
DB::Exception: Scale is out of bounds.

```


```
SELECT toDecimal32(4.2, 8) AS x, 6 * x

```


```
DB::Exception: Decimal math overflow.

```


```
SET decimal_check_overflow = 0;
SELECT toDecimal32(4.2, 8) AS x, 6 * x

```


```
┌──────────x─┬─multiply(6, toDecimal32(4.2, 8))─┐
│ 4.20000000 │                     -17.74967296 │
└────────────┴──────────────────────────────────┘

```


```
SELECT toDecimal32(1, 8) < 100

```


```
DB::Exception: Can't compare.

```

- [isDecimalOverflow](https://clickhouse.com/docs/ru/reference/functions/regular-functions/other-functions#isDecimalOverflow)
- [countDigits](https://clickhouse.com/docs/ru/reference/functions/regular-functions/other-functions#countDigits)
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
