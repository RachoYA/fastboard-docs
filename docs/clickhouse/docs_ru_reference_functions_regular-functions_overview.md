# Обычные функции - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/functions/regular-functions/overview


## Строгая типизация


## Устранение общих подвыражений


## Типы результатов


## Константы


## Обработка NULL

- Если хотя бы один из аргументов функции равен `NULL`, результат функции также будет `NULL`.
- Особое поведение, которое отдельно указывается в описании каждой функции. В исходном коде ClickHouse для таких функций задано `UseDefaultImplementationForNulls=false`.

## Константность


## Функции высшего порядка


### оператор `->` и функции lambda(params, expr)


```
x -> 2 * x
str -> str != Referer

```


### Имена функций как лямбда-выражения


```
SELECT arrayMap(negate, [1, 2, 3]);            -- [-1, -2, -3]
SELECT arrayMap(x -> negate(x), [1, 2, 3]);    -- [-1, -2, -3]

SELECT arrayMap(plus, [1, 2, 3], [10, 20, 30]);            -- [11, 22, 33]
SELECT arrayMap((x, y) -> plus(x, y), [1, 2, 3], [10, 20, 30]); -- [11, 22, 33]

SELECT arrayFilter(isNotNull, [1, NULL, 3, NULL, 5]);            -- [1, 3, 5]
SELECT arrayFilter(x -> isNotNull(x), [1, NULL, 3, NULL, 5]);    -- [1, 3, 5]

SELECT arrayFold(plus, [1, 2, 3, 4, 5], toUInt64(0));                      -- 15
SELECT arrayFold((acc, x) -> plus(acc, x), [1, 2, 3, 4, 5], toUInt64(0));  -- 15

```


## Пользовательские функции (UDF)

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
