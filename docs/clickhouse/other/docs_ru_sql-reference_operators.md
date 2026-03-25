# Операторы | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/sql-reference/operators

ClickHouse преобразует операторы в соответствующие функции при разборе запроса в соответствии с их приоритетом, порядком вычисления и ассоциативностью.


## Операторы доступа​

a[N]– доступ к элементу массива. ФункцияarrayElement(a, N).

a.N– доступ к элементу кортежа. ФункцияtupleElement(a, N).


## Оператор числового отрицания​

-a– Функцияnegate(a).

Для отрицания кортежей:tupleNegate.


## Операторы умножения и деления​

a * b– Функцияmultiply(a, b).

Для умножения кортежа на число используйте функциюtupleMultiplyByNumber, для вычисления скалярного произведения –dotProduct.

a / b– Функцияdivide(a, b).

Для деления кортежа на число используйте функциюtupleDivideByNumber.

a % b– Функцияmodulo(a, b).


## Операторы сложения и вычитания​

a + b– Функцияplus(a, b).

Для сложения кортежей:tuplePlus.

a - b– Функцияminus(a, b).

Для вычитания кортежей:tupleMinus.


## Операторы сравнения​


### Функция equals​

a = b– Функцияequals(a, b).

a == b– Функцияequals(a, b).


### Функция notEquals​

a != b– ФункцияnotEquals(a, b).

a <> b– ФункцияnotEquals(a, b).


### Функция lessOrEquals​

a <= b– ФункцияlessOrEquals(a, b).


### Функция greaterOrEquals​

a >= b– ФункцияgreaterOrEquals(a, b).


### Функция less​

a < b– Функцияless(a, b).


### Функция greater​

a > b– Функцияgreater(a, b).


### Функция like​

a LIKE b– Функцияlike(a, b).


### Функция notLike​

a NOT LIKE b– функцияnotLike(a, b).


### Функция ilike​

a ILIKE b– Функцияilike(a, b).


### Функция BETWEEN​

a BETWEEN b AND c– эквивалентноa >= b AND a <= c.

a NOT BETWEEN b AND c– эквивалентноa < b OR a > c.


### операторIS NOT DISTINCT FROM(<=>)​

Начиная с версии 25.10 вы можете использовать<=>так же, как и любой другой оператор.
До версии 25.10 его можно было использовать только в выражениях JOIN, например:CREATE TABLE a (x String) ENGINE = Memory;
INSERT INTO a VALUES ('ClickHouse');

SELECT * FROM a AS a1 JOIN a AS a2 ON a1.x <=> a2.x;

┌─x──────────┬─a2.x───────┐
│ ClickHouse │ ClickHouse │
└────────────┴────────────┘


```
CREATE TABLE a (x String) ENGINE = Memory;
INSERT INTO a VALUES ('ClickHouse');

SELECT * FROM a AS a1 JOIN a AS a2 ON a1.x <=> a2.x;

┌─x──────────┬─a2.x───────┐
│ ClickHouse │ ClickHouse │
└────────────┴────────────┘

```

Оператор<=>— оператор проверки равенства с учетомNULL, эквивалентныйIS NOT DISTINCT FROM.
Он работает как обычный оператор равенства (=), но рассматривает значенияNULLкак сравнимые между собой.
Два значенияNULLсчитаются равными, а сравнениеNULLс любым ненулевым (non-NULL) значением возвращает 0 (ложь), а неNULL.

:::


```
SELECT
  'ClickHouse' <=> NULL,
  NULL <=> NULL

```


```
┌─isNotDistinc⋯use', NULL)─┬─isNotDistinc⋯NULL, NULL)─┐
│                        0 │                        1 │
└──────────────────────────┴──────────────────────────┘

```


## Операторы для работы с наборами данных​

См.операторы INи операторEXISTS.


### Функция in​

a IN ...– Функцияin(a, b).


### Функция notIn​

a NOT IN ...– ФункцияnotIn(a, b).


### Функция globalIn​

a GLOBAL IN ...– ФункцияglobalIn(a, b).


### Функция globalNotIn​

a GLOBAL NOT IN ...– ФункцияglobalNotIn(a, b).


### функция in с подзапросом​

a = ANY (subquery)– Функцияin(a, subquery).


### функция notIn с подзапросом​

a != ANY (subquery)– эквивалентноa NOT IN (SELECT singleValueOrNull(*) FROM subquery).


### функция IN с подзапросом​

a = ALL (subquery)– Функцияa IN (SELECT singleValueOrNull(*) FROM subquery).


### Функция подзапроса notIn​

a != ALL (subquery)– ФункцияnotIn(a, subquery).

Примеры

Запрос с ALL:


```
SELECT number AS a FROM numbers(10) WHERE a > ALL (SELECT number FROM numbers(3, 3));

```

Результат:


```
┌─a─┐
│ 6 │
│ 7 │
│ 8 │
│ 9 │
└───┘

```

Запрос с использованием ANY:


```
SELECT number AS a FROM numbers(10) WHERE a > ANY (SELECT number FROM numbers(3, 3));

```

Результат:


```
┌─a─┐
│ 4 │
│ 5 │
│ 6 │
│ 7 │
│ 8 │
│ 9 │
└───┘

```


## Операторы для работы с датами и временем​


### EXTRACT​


```
EXTRACT(part FROM date);

```

Извлекает части даты из заданного значения. Например, вы можете получить месяц из указанной даты или секунду из времени.

Параметрpartуказывает, какую часть даты нужно извлечь. Доступны следующие значения:

- SECOND— секунда. Возможные значения: 0–59.
- MINUTE— минута. Возможные значения: 0–59.
- HOUR— час. Возможные значения: 0–23.
- DAY— день месяца. Возможные значения: 1–31.
- WEEK— номер недели по ISO 8601. Возможные значения: 1–53.
- MONTH— номер месяца. Возможные значения: 1–12.
- QUARTER— квартал. Возможные значения: 1–4.
- YEAR— год.
- EPOCH— временная метка Unix (секунды с 1970-01-01 00:00:00 UTC). Примечание: дляDateTime64дробная часть секунды отбрасывается.
- DOW— день недели (совместимо с PostgreSQL). 0 = воскресенье, 6 = суббота.
- DOY— день года. Возможные значения: 1–366.
- ISODOW— день недели по ISO. 1 = понедельник, 7 = воскресенье.
- ISOYEAR— год нумерации недель по ISO 8601.
- CENTURY— век. Например, 2024 год относится к 21-му веку.
- DECADE— десятилетие (год, делённый на 10). Например, для 2024 года десятилетие равно 202.
- MILLENNIUM— тысячелетие. Например, 2024 год относится к 3-му тысячелетию.
Параметрpartне зависит от регистра.

Параметрdateзадает дату или время, которое нужно обработать. Поддерживаются типыDate,Date32,DateTimeиDateTime64.

Примеры:


```
SELECT EXTRACT(DAY FROM toDate('2017-06-15'));
SELECT EXTRACT(MONTH FROM toDate('2017-06-15'));
SELECT EXTRACT(YEAR FROM toDate('2017-06-15'));
SELECT EXTRACT(EPOCH FROM toDateTime('2024-01-15 12:30:45', 'UTC'));
SELECT EXTRACT(DOW FROM toDate('2024-01-15'));
SELECT EXTRACT(CENTURY FROM toDate('2024-01-01'));

```

В следующем примере создается таблица, и в неё вставляется значение типаDateTime.


```
CREATE TABLE test.Orders
(
    OrderId UInt64,
    OrderName String,
    OrderDate DateTime
) ENGINE = MergeTree
ORDER BY ();

```


```
INSERT INTO test.Orders VALUES (1, 'Jarlsberg Cheese', toDateTime('2008-10-11 13:23:44'));

```


```
SELECT
    toYear(OrderDate) AS OrderYear,
    toMonth(OrderDate) AS OrderMonth,
    toDayOfMonth(OrderDate) AS OrderDay,
    toHour(OrderDate) AS OrderHour,
    toMinute(OrderDate) AS OrderMinute,
    toSecond(OrderDate) AS OrderSecond
FROM test.Orders;

```


```
┌─OrderYear─┬─OrderMonth─┬─OrderDay─┬─OrderHour─┬─OrderMinute─┬─OrderSecond─┐
│      2008 │         10 │       11 │        13 │          23 │          44 │
└───────────┴────────────┴──────────┴───────────┴─────────────┴─────────────┘

```

Дополнительные примеры можно найти вtests.


### INTERVAL​

Создает значение типаInterval, которое следует использовать в арифметических операциях со значениями типовDateиDateTime.

Типы интервалов:

- SECOND
- MINUTE
- HOUR
- DAY
- WEEK
- MONTH
- QUARTER
- YEAR
Вы также можете использовать строковый литерал при задании значенияINTERVAL. Например,INTERVAL 1 HOURидентиченINTERVAL '1 hour'илиINTERVAL '1' hour.

Интервалы разных типов нельзя комбинировать. Нельзя использовать выражения видаINTERVAL 4 DAY 1 HOUR. Указывайте интервалы в единицах, которые меньше или равны наименьшей единице интервала, напримерINTERVAL 25 HOUR. Вы можете использовать последовательные операции, как в примере ниже.

Примеры:


```
SELECT now() AS current_date_time, current_date_time + INTERVAL 4 DAY + INTERVAL 3 HOUR;

```


```
┌───current_date_time─┬─plus(plus(now(), toIntervalDay(4)), toIntervalHour(3))─┐
│ 2020-11-03 22:09:50 │                                    2020-11-08 01:09:50 │
└─────────────────────┴────────────────────────────────────────────────────────┘

```


```
SELECT now() AS current_date_time, current_date_time + INTERVAL '4 day' + INTERVAL '3 hour';

```


```
┌───current_date_time─┬─plus(plus(now(), toIntervalDay(4)), toIntervalHour(3))─┐
│ 2020-11-03 22:12:10 │                                    2020-11-08 01:12:10 │
└─────────────────────┴────────────────────────────────────────────────────────┘

```


```
SELECT now() AS current_date_time, current_date_time + INTERVAL '4' day + INTERVAL '3' hour;

```


```
┌───current_date_time─┬─plus(plus(now(), toIntervalDay('4')), toIntervalHour('3'))─┐
│ 2020-11-03 22:33:19 │                                        2020-11-08 01:33:19 │
└─────────────────────┴────────────────────────────────────────────────────────────┘

```

Рекомендуется всегда использовать синтаксисINTERVALили функциюaddDays. Простое сложение или вычитание (синтаксис видаnow() + ...) не учитывает настройки времени, например переход на летнее время.

Примеры:


```
SELECT toDateTime('2014-10-26 00:00:00', 'Asia/Istanbul') AS time, time + 60 * 60 * 24 AS time_plus_24_hours, time + toIntervalDay(1) AS time_plus_1_day;

```


```
┌────────────────time─┬──time_plus_24_hours─┬─────time_plus_1_day─┐
│ 2014-10-26 00:00:00 │ 2014-10-26 23:00:00 │ 2014-10-27 00:00:00 │
└─────────────────────┴─────────────────────┴─────────────────────┘

```

См. также

- Interval— тип данных
- функции преобразования типовtoInterval

## Оператор логического AND​

СинтаксисSELECT a AND b— вычисляет логическую конъюнкцию выраженийaиbс помощью функцииand.


## Оператор логического ИЛИ​

СинтаксисSELECT a OR b— вычисляет логическую операцию ИЛИ надaиbс помощью функцииor.


## Оператор логического отрицания​

СинтаксисSELECT NOT a— вычисляет логическое отрицание выраженияaс помощью функцииnot.


## Условный оператор​

a ? b : c– функцияif(a, b, c).

Примечание:

Условный оператор вычисляет значенияbиc, затем проверяет, выполняется ли условиеa, и возвращает соответствующее значение. ЕслиbилиC– функцияarrayJoin(), каждая строка будет реплицирована независимо от условияa.


## Условное выражение​


```
CASE [x]
    WHEN a THEN b
    [WHEN ... THEN ...]
    [ELSE c]
END

```

Если указанx, используется функцияtransform(x, [a, ...], [b, ...], c). В противном случае используетсяmultiIf(a, b, ..., c).

Если в выражении отсутствует конструкцияELSE c, значением по умолчанию являетсяNULL.

Функцияtransformне поддерживает значениеNULL.


## Оператор конкатенации​

s1 || s2– Функцияconcat(s1, s2).


## Оператор создания лямбда-выражения​

x -> expr– Функцияlambda(x, expr).

Следующие операторы не имеют приоритета, так как являются скобками:


## Оператор создания массива​

[x1, ...]– Функцияarray(x1, ...).


## Оператор создания кортежей​

(x1, x2, ...)– Функцияtuple(x1, x2, ...).


## Оператор создания кортежа​

Все бинарные операторы являются левоассоциативными. Например,1 + 2 + 3преобразуется вplus(plus(1, 2), 3).
Иногда всё работает не так, как вы ожидаете. Например,SELECT 4 > 2 > 3вернёт 0.

Для повышения эффективности функцииandиorпринимают произвольное количество аргументов. Соответствующие цепочки операторовANDиORпреобразуются в один вызов этих функций.


## Проверка наNULL​

ClickHouse поддерживает операторыIS NULLиIS NOT NULL.


### IS NULL​

- Для значений типаNullableоператорIS NULLвозвращает:1, если значение равноNULL;0в остальных случаях.
- 1, если значение равноNULL;
- 0в остальных случаях.
- Для значений других типов операторIS NULLвсегда возвращает0.
Работу можно оптимизировать, включив настройкуoptimize_functions_to_subcolumns. Приoptimize_functions_to_subcolumns = 1функция читает только подстолбецnullвместо чтения и обработки всего столбца. ЗапросSELECT n IS NULL FROM tableпреобразуется вSELECT n.null FROM TABLE.


```
SELECT x+100 FROM t_null WHERE y IS NULL

```


```
┌─plus(x, 100)─┐
│          101 │
└──────────────┘

```


### IS NOT NULL​

- Для значений типаNullableоператорIS NOT NULLвозвращает:0, если значение равноNULL;1в противном случае.
- 0, если значение равноNULL;
- 1в противном случае.
- Для значений других типов операторIS NOT NULLвсегда возвращает1.

```
SELECT * FROM t_null WHERE y IS NOT NULL

```


```
┌─x─┬─y─┐
│ 2 │ 3 │
└───┴───┘

```

Оптимизацию можно выполнить, включив настройкуoptimize_functions_to_subcolumns. Приoptimize_functions_to_subcolumns = 1функция читает только подстолбецnullвместо чтения и обработки данных всего столбца. ЗапросSELECT n IS NOT NULL FROM tableпреобразуется вSELECT NOT n.null FROM table.
