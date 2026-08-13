# Values - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/formats/Values


| Ввод | Вывод | Псевдоним |
| --- | --- | --- |
| ✔ | ✔ |  |


## Описание

- Строки разделяются запятыми, без запятой после последней строки.
- Значения внутри скобок также разделяются запятыми.
- Числа выводятся в десятичном формате без кавычек.
- Массивы выводятся в `[]`.
- Строки, даты, а также значения даты и времени выводятся в кавычках.
- Правила экранирования и парсинга аналогичны формату [TabSeparated](https://clickhouse.com/docs/ru/reference/formats/TabSeparated/TabSeparated).
- одинарные кавычки
- обратные косые черты

## Пример использования


### Вставка данных


```
CREATE TABLE t (id UInt32, name String, values Array(UInt32)) ENGINE = Memory;

INSERT INTO t FORMAT Values (1, 'a', [10, 20]), (2, 'b', [30]);

SELECT * FROM t ORDER BY id;

```


```
┌─id─┬─name─┬─values──┐
│  1 │ a    │ [10,20] │
│  2 │ b    │ [30]    │
└────┴──────┴─────────┘

```


### Использование выражений во входных данных


```
CREATE TABLE prices (item String, total UInt32) ENGINE = Memory;

INSERT INTO prices FORMAT Values ('apple', 3 * 4), ('pear', length('hello') + 10);

SELECT * FROM prices ORDER BY total;

```


```
┌─item──┬─total─┐
│ apple │    12 │
│ pear  │    15 │
└───────┴───────┘

```


### Выборка данных


```
SELECT 1 AS a, 'O''Reilly' AS b, NULL::Nullable(String) AS c FORMAT Values;

```


```
(1,'O\'Reilly',NULL)

```


## Настройки формата


| Настройка | Описание | По умолчанию |
| --- | --- | --- |
| [`input_format_values_interpret_expressions`](https://clickhouse.com/docs/ru/reference/settings/formats#input_format_values_interpret_expressions) | если поле не удалось разобрать с помощью стримингового парсера, запустить SQL-парсер и попытаться интерпретировать его как SQL-выражение. | `true` |
| [`input_format_values_deduce_templates_of_expressions`](https://clickhouse.com/docs/ru/reference/settings/formats#input_format_values_deduce_templates_of_expressions) | если поле не удалось разобрать с помощью стримингового парсера, запустить SQL-парсер, определить шаблон SQL-выражения, попытаться разобрать по этому шаблону все строки, а затем интерпретировать выражение для всех строк. | `true` |
| [`input_format_values_accurate_types_of_literals`](https://clickhouse.com/docs/ru/reference/settings/formats#input_format_values_accurate_types_of_literals) | при разборе и интерпретации выражений с использованием шаблона проверять фактический тип литерала, чтобы избежать возможных проблем с переполнением и потерей точности. | `true` |

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
