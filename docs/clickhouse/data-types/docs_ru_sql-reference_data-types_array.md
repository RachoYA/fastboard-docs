# Array(T) | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/sql-reference/data-types/array

Массив элементов типаTс индексацией, начинающейся с 1.Tможет быть любым типом данных, включая массив.


## Создание массива​

Для создания массива можно использовать функцию:


```
array(T)

```

Можно также использовать[].


```
[]

```

Пример создания массива:


```
SELECT array(1, 2) AS x, toTypeName(x)

```


```
┌─x─────┬─toTypeName(array(1, 2))─┐
│ [1,2] │ Array(UInt8)            │
└───────┴─────────────────────────┘

```


```
SELECT [1, 2] AS x, toTypeName(x)

```


```
┌─x─────┬─toTypeName([1, 2])─┐
│ [1,2] │ Array(UInt8)       │
└───────┴────────────────────┘

```


## Работа с типами данных​

При создании массива «на лету» ClickHouse автоматически определяет тип аргумента как самый узкий тип данных, который может хранить все перечисленные аргументы. Если в массиве есть значенияNullableили литералыNULL, тип элемента массива также становитсяNullable.

Если ClickHouse не может определить тип данных, генерируется исключение. Например, это происходит при попытке создать массив, содержащий одновременно строки и числа (SELECT array(1, 'a')).

Примеры автоматического определения типа данных:


```
SELECT array(1, 2, NULL) AS x, toTypeName(x)

```


```
┌─x──────────┬─toTypeName(array(1, 2, NULL))─┐
│ [1,2,NULL] │ Array(Nullable(UInt8))        │
└────────────┴───────────────────────────────┘

```

Если вы попытаетесь создать массив несовместимых типов данных, ClickHouse выбросит исключение:


```
SELECT array(1, 'a')

```


```
Received exception from server (version 1.1.54388):
Code: 386. DB::Exception: Received from localhost:9000, 127.0.0.1. DB::Exception: There is no supertype for types UInt8, String because some of them are String/FixedString and some of them are not.

```


## Размер массива​

Можно определить размер массива, используя подстолбецsize0, не считывая весь столбец целиком. Для многомерных массивов вы можете использоватьsizeN-1, гдеN— требуемая размерность.

Пример

Запрос:


```
CREATE TABLE t_arr (`arr` Array(Array(Array(UInt32)))) ENGINE = MergeTree ORDER BY tuple();

INSERT INTO t_arr VALUES ([[[12, 13, 0, 1],[12]]]);

SELECT arr.size0, arr.size1, arr.size2 FROM t_arr;

```

Результат:


```
┌─arr.size0─┬─arr.size1─┬─arr.size2─┐
│         1 │ [2]       │ [[4,1]]   │
└───────────┴───────────┴───────────┘

```


## Чтение вложенных подстолбцов из Array​

Если вложенный типTвнутриArrayимеет подстолбцы (например, если этоименованный кортеж), вы можете читать его подстолбцы из типаArray(T)с теми же именами подстолбцов. Тип подстолбца будетArrayот типа исходного подстолбца.

Пример


```
CREATE TABLE t_arr (arr Array(Tuple(field1 UInt32, field2 String))) ENGINE = MergeTree ORDER BY tuple();
INSERT INTO t_arr VALUES ([(1, 'Hello'), (2, 'World')]), ([(3, 'This'), (4, 'is'), (5, 'subcolumn')]);
SELECT arr.field1, toTypeName(arr.field1), arr.field2, toTypeName(arr.field2) from t_arr;

```


```
┌─arr.field1─┬─toTypeName(arr.field1)─┬─arr.field2────────────────┬─toTypeName(arr.field2)─┐
│ [1,2]      │ Array(UInt32)          │ ['Hello','World']         │ Array(String)          │
│ [3,4,5]    │ Array(UInt32)          │ ['This','is','subcolumn'] │ Array(String)          │
└────────────┴────────────────────────┴───────────────────────────┴────────────────────────┘

```
