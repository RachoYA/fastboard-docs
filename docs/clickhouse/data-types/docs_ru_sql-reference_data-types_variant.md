# Variant(T1, T2, ...) | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/sql-reference/data-types/variant

Этот тип представляет собой объединение других типов данных. ТипVariant(T1, T2, ..., TN)означает, что каждая строка этого типа
имеет значение либо типаT1, либоT2, ... либоTN, либо не имеет значения (NULL).

Порядок вложенных типов не имеет значения: Variant(T1, T2) = Variant(T2, T1).
Вложенными типами могут быть произвольные типы, за исключением типов Nullable(...), LowCardinality(Nullable(...)) и Variant(...).

Не рекомендуется использовать похожие типы в качестве вариантов (например, разные числовые типы, такие какVariant(UInt32, Int64), или разные типы дат, такие какVariant(Date, DateTime)),
поскольку работа со значениями таких типов может приводить к неоднозначности. По умолчанию создание такого типаVariantприведёт к исключению, но это поведение можно изменить с помощью настройкиallow_suspicious_variant_types.


## Создание типа Variant​

Использование типаVariantв определении столбца таблицы:


```
CREATE TABLE test (v Variant(UInt64, String, Array(UInt64))) ENGINE = Memory;
INSERT INTO test VALUES (NULL), (42), ('Hello, World!'), ([1, 2, 3]);
SELECT v FROM test;

```


```
┌─v─────────────┐
│ ᴺᵁᴸᴸ          │
│ 42            │
│ Hello, World! │
│ [1,2,3]       │
└───────────────┘

```

Использование CAST для обычных столбцов:


```
SELECT toTypeName(variant) AS type_name, 'Hello, World!'::Variant(UInt64, String, Array(UInt64)) as variant;

```


```
┌─type_name──────────────────────────────┬─variant───────┐
│ Variant(Array(UInt64), String, UInt64) │ Hello, World! │
└────────────────────────────────────────┴───────────────┘

```

Использование функцийif/multiIf, когда аргументы не имеют общего типа (для этого должна быть включена настройкаuse_variant_as_common_type):


```
SET use_variant_as_common_type = 1;
SELECT if(number % 2, number, range(number)) as variant FROM numbers(5);

```


```
┌─variant───┐
│ []        │
│ 1         │
│ [0,1]     │
│ 3         │
│ [0,1,2,3] │
└───────────┘

```


```
SET use_variant_as_common_type = 1;
SELECT multiIf((number % 4) = 0, 42, (number % 4) = 1, [1, 2, 3], (number % 4) = 2, 'Hello, World!', NULL) AS variant FROM numbers(4);

```


```
┌─variant───────┐
│ 42            │
│ [1,2,3]       │
│ Hello, World! │
│ ᴺᵁᴸᴸ          │
└───────────────┘

```

Использование функцийarray/map, если элементы массива или значения Map не имеют общего типа (для этого должен быть включён настройкаuse_variant_as_common_type):


```
SET use_variant_as_common_type = 1;
SELECT array(range(number), number, 'str_' || toString(number)) as array_of_variants FROM numbers(3);

```


```
┌─array_of_variants─┐
│ [[],0,'str_0']    │
│ [[0],1,'str_1']   │
│ [[0,1],2,'str_2'] │
└───────────────────┘

```


```
SET use_variant_as_common_type = 1;
SELECT map('a', range(number), 'b', number, 'c', 'str_' || toString(number)) as map_of_variants FROM numbers(3);

```


```
┌─map_of_variants───────────────┐
│ {'a':[],'b':0,'c':'str_0'}    │
│ {'a':[0],'b':1,'c':'str_1'}   │
│ {'a':[0,1],'b':2,'c':'str_2'} │
└───────────────────────────────┘

```


## Чтение вложенных типов Variant как подколонок​

Тип Variant поддерживает чтение отдельного вложенного типа из столбца Variant, используя имя типа как подколонку.
Таким образом, если у вас есть столбецvariant Variant(T1, T2, T3), вы можете прочитать подколонку типаT2, используя синтаксисvariant.T2,
эта подколонка будет иметь типNullable(T2), еслиT2может быть обёрнут вNullable, иT2в противном случае. Эта подколонка будет
того же размера, что и исходный столбецVariant, и будет содержать значенияNULL(или пустые значения, еслиT2не может быть обёрнут вNullable)
во всех строках, в которых значение в исходном столбцеVariantне имеет типаT2.

Подколонки Variant также могут читаться с помощью функцииvariantElement(variant_column, type_name).

Примеры:


```
CREATE TABLE test (v Variant(UInt64, String, Array(UInt64))) ENGINE = Memory;
INSERT INTO test VALUES (NULL), (42), ('Hello, World!'), ([1, 2, 3]);
SELECT v, v.String, v.UInt64, v.`Array(UInt64)` FROM test;

```


```
┌─v─────────────┬─v.String──────┬─v.UInt64─┬─v.Array(UInt64)─┐
│ ᴺᵁᴸᴸ          │ ᴺᵁᴸᴸ          │     ᴺᵁᴸᴸ │ []              │
│ 42            │ ᴺᵁᴸᴸ          │       42 │ []              │
│ Hello, World! │ Hello, World! │     ᴺᵁᴸᴸ │ []              │
│ [1,2,3]       │ ᴺᵁᴸᴸ          │     ᴺᵁᴸᴸ │ [1,2,3]         │
└───────────────┴───────────────┴──────────┴─────────────────┘

```


```
SELECT toTypeName(v.String), toTypeName(v.UInt64), toTypeName(v.`Array(UInt64)`) FROM test LIMIT 1;

```


```
┌─toTypeName(v.String)─┬─toTypeName(v.UInt64)─┬─toTypeName(v.Array(UInt64))─┐
│ Nullable(String)     │ Nullable(UInt64)     │ Array(UInt64)               │
└──────────────────────┴──────────────────────┴─────────────────────────────┘

```


```
SELECT v, variantElement(v, 'String'), variantElement(v, 'UInt64'), variantElement(v, 'Array(UInt64)') FROM test;

```


```
┌─v─────────────┬─variantElement(v, 'String')─┬─variantElement(v, 'UInt64')─┬─variantElement(v, 'Array(UInt64)')─┐
│ ᴺᵁᴸᴸ          │ ᴺᵁᴸᴸ                        │                        ᴺᵁᴸᴸ │ []                                 │
│ 42            │ ᴺᵁᴸᴸ                        │                          42 │ []                                 │
│ Hello, World! │ Hello, World!               │                        ᴺᵁᴸᴸ │ []                                 │
│ [1,2,3]       │ ᴺᵁᴸᴸ                        │                        ᴺᵁᴸᴸ │ [1,2,3]                            │
└───────────────┴─────────────────────────────┴─────────────────────────────┴────────────────────────────────────┘

```

Чтобы узнать, какой вариант хранится в каждой строке, можно использовать функциюvariantType(variant_column). Она возвращает значение типаEnumс именем типа варианта для каждой строки (или'None', если строка имеет значениеNULL).

Пример:


```
CREATE TABLE test (v Variant(UInt64, String, Array(UInt64))) ENGINE = Memory;
INSERT INTO test VALUES (NULL), (42), ('Hello, World!'), ([1, 2, 3]);
SELECT variantType(v) FROM test;

```


```
┌─variantType(v)─┐
│ None           │
│ UInt64         │
│ String         │
│ Array(UInt64)  │
└────────────────┘

```


```
SELECT toTypeName(variantType(v)) FROM test LIMIT 1;

```


```
┌─toTypeName(variantType(v))──────────────────────────────────────────┐
│ Enum8('None' = -1, 'Array(UInt64)' = 0, 'String' = 1, 'UInt64' = 2) │
└─────────────────────────────────────────────────────────────────────┘

```


## Преобразование между столбцом Variant и другими столбцами​

Существует четыре возможных преобразования, которые можно выполнить для столбца типаVariant.


### Преобразование столбца String в столбец Variant​

Преобразование изStringвVariantвыполняется путём парсинга значения типаVariantиз строкового значения:


```
SELECT '42'::Variant(String, UInt64) AS variant, variantType(variant) AS variant_type

```


```
┌─variant─┬─variant_type─┐
│ 42      │ UInt64       │
└─────────┴──────────────┘

```


```
SELECT '[1, 2, 3]'::Variant(String, Array(UInt64)) as variant, variantType(variant) as variant_type

```


```
┌─variant─┬─variant_type──┐
│ [1,2,3] │ Array(UInt64) │
└─────────┴───────────────┘

```


```
SELECT CAST(map('key1', '42', 'key2', 'true', 'key3', '2020-01-01'), 'Map(String, Variant(UInt64, Bool, Date))') AS map_of_variants, mapApply((k, v) -> (k, variantType(v)), map_of_variants) AS map_of_variant_types```

```


```
┌─map_of_variants─────────────────────────────┬─map_of_variant_types──────────────────────────┐
│ {'key1':42,'key2':true,'key3':'2020-01-01'} │ {'key1':'UInt64','key2':'Bool','key3':'Date'} │
└─────────────────────────────────────────────┴───────────────────────────────────────────────┘

```

Чтобы отключить парсинг при преобразовании изStringвVariant, можно выключить настройкуcast_string_to_dynamic_use_inference:


```
SET cast_string_to_variant_use_inference = 0;
SELECT '[1, 2, 3]'::Variant(String, Array(UInt64)) as variant, variantType(variant) as variant_type

```


```
┌─variant───┬─variant_type─┐
│ [1, 2, 3] │ String       │
└───────────┴──────────────┘

```


### Converting an ordinary column to a Variant column​

It is possible to convert an ordinary column with typeTto aVariantcolumn containing this type:


```
SELECT toTypeName(variant) AS type_name, [1,2,3]::Array(UInt64)::Variant(UInt64, String, Array(UInt64)) as variant, variantType(variant) as variant_name

```


```
┌─type_name──────────────────────────────┬─variant─┬─variant_name──┐
│ Variant(Array(UInt64), String, UInt64) │ [1,2,3] │ Array(UInt64) │
└────────────────────────────────────────┴─────────┴───────────────┘

```

Примечание: преобразование из типаStringвсегда выполняется посредством парсинга; если вам нужно преобразовать столбецStringв вариантStringтипаVariantбез парсинга, можно сделать следующее:


```
SELECT '[1, 2, 3]'::Variant(String)::Variant(String, Array(UInt64), UInt64) as variant, variantType(variant) as variant_type

```


```
┌─variant───┬─variant_type─┐
│ [1, 2, 3] │ String       │
└───────────┴──────────────┘

```


### Converting a Variant column to an ordinary column​

It is possible to convert aVariantcolumn to an ordinary column. In this case all nested variants will be converted to a destination type:


```
CREATE TABLE test (v Variant(UInt64, String)) ENGINE = Memory;
INSERT INTO test VALUES (NULL), (42), ('42.42');
SELECT v::Nullable(Float64) FROM test;

```


```
┌─CAST(v, 'Nullable(Float64)')─┐
│                         ᴺᵁᴸᴸ │
│                           42 │
│                        42.42 │
└──────────────────────────────┘

```


### Преобразование одного Variant в другой Variant​

It is possible to convert aVariantcolumn to anotherVariantcolumn, but only if the destinationVariantcolumn contains all nested types from the originalVariant:


```
CREATE TABLE test (v Variant(UInt64, String)) ENGINE = Memory;
INSERT INTO test VALUES (NULL), (42), ('String');
SELECT v::Variant(UInt64, String, Array(UInt64)) FROM test;

```


```
┌─CAST(v, 'Variant(UInt64, String, Array(UInt64))')─┐
│ ᴺᵁᴸᴸ                                              │
│ 42                                                │
│ String                                            │
└───────────────────────────────────────────────────┘

```


## Reading Variant type from the data​

All text formats (TSV, CSV, CustomSeparated, Values, JSONEachRow, etc) supports readingVarianttype. During data parsing ClickHouse tries to insert value into most appropriate variant type.

Example:


```
SELECT
    v,
    variantElement(v, 'String') AS str,
    variantElement(v, 'UInt64') AS num,
    variantElement(v, 'Float64') AS float,
    variantElement(v, 'DateTime') AS date,
    variantElement(v, 'Array(UInt64)') AS arr
FROM format(JSONEachRow, 'v Variant(String, UInt64, Float64, DateTime, Array(UInt64))', $$
{"v" : "Hello, World!"},
{"v" : 42},
{"v" : 42.42},
{"v" : "2020-01-01 00:00:00"},
{"v" : [1, 2, 3]}
$$)

```


```
┌─v───────────────────┬─str───────────┬──num─┬─float─┬────────────────date─┬─arr─────┐
│ Hello, World!       │ Hello, World! │ ᴺᵁᴸᴸ │  ᴺᵁᴸᴸ │                ᴺᵁᴸᴸ │ []      │
│ 42                  │ ᴺᵁᴸᴸ          │   42 │  ᴺᵁᴸᴸ │                ᴺᵁᴸᴸ │ []      │
│ 42.42               │ ᴺᵁᴸᴸ          │ ᴺᵁᴸᴸ │ 42.42 │                ᴺᵁᴸᴸ │ []      │
│ 2020-01-01 00:00:00 │ ᴺᵁᴸᴸ          │ ᴺᵁᴸᴸ │  ᴺᵁᴸᴸ │ 2020-01-01 00:00:00 │ []      │
│ [1,2,3]             │ ᴺᵁᴸᴸ          │ ᴺᵁᴸᴸ │  ᴺᵁᴸᴸ │                ᴺᵁᴸᴸ │ [1,2,3] │
└─────────────────────┴───────────────┴──────┴───────┴─────────────────────┴─────────┘

```


## Comparing values of Variant type​

Values of aVarianttype can be compared only with values with the sameVarianttype.

По умолчанию операторы сравнения используютреализацию сравнения Variant по умолчанию,
применяя сравнение к каждому варианту типа по отдельности. Это можно отключить, установив настройкуuse_variant_default_implementation_for_comparisons = 0,
чтобы использовать нативные правила сравнения Variant, описанные ниже.Обратите внимание, чтоORDER BYвсегда использует нативное сравнение.

Нативные правила сравнения Variant:

The result of operator<for valuesv1with underlying typeT1andv2with underlying typeT2of a typeVariant(..., T1, ... T2, ...)is defined as follows:

- IfT1 = T2 = T, the result will bev1.T < v2.T(underlying values will be compared).
- IfT1 != T2, the result will beT1 < T2(type names will be compared).
Examples:


```
SET allow_suspicious_types_in_order_by = 1;
CREATE TABLE test (v1 Variant(String, UInt64, Array(UInt32)), v2 Variant(String, UInt64, Array(UInt32))) ENGINE=Memory;
INSERT INTO test VALUES (42, 42), (42, 43), (42, 'abc'), (42, [1, 2, 3]), (42, []), (42, NULL);

```


```
SELECT v2, variantType(v2) AS v2_type FROM test ORDER BY v2;

```


```
┌─v2──────┬─v2_type───────┐
│ []      │ Array(UInt32) │
│ [1,2,3] │ Array(UInt32) │
│ abc     │ String        │
│ 42      │ UInt64        │
│ 43      │ UInt64        │
│ ᴺᵁᴸᴸ    │ None          │
└─────────┴───────────────┘

```


```
SELECT v1, variantType(v1) AS v1_type, v2, variantType(v2) AS v2_type, v1 = v2, v1 < v2, v1 > v2 FROM test;

```


```
┌─v1─┬─v1_type─┬─v2──────┬─v2_type───────┬─equals(v1, v2)─┬─less(v1, v2)─┬─greater(v1, v2)─┐
│ 42 │ UInt64  │ 42      │ UInt64        │              1 │            0 │               0 │
│ 42 │ UInt64  │ 43      │ UInt64        │              0 │            1 │               0 │
│ 42 │ UInt64  │ abc     │ String        │              0 │            0 │               1 │
│ 42 │ UInt64  │ [1,2,3] │ Array(UInt32) │              0 │            0 │               1 │
│ 42 │ UInt64  │ []      │ Array(UInt32) │              0 │            0 │               1 │
│ 42 │ UInt64  │ ᴺᵁᴸᴸ    │ None          │              0 │            1 │               0 │
└────┴─────────┴─────────┴───────────────┴────────────────┴──────────────┴─────────────────┘


```

Если вам нужно найти строку с определённым значениемVariant, вы можете сделать одно из следующего:

- Привести значение к соответствующему типуVariant:

```
SELECT * FROM test WHERE v2 == [1,2,3]::Array(UInt32)::Variant(String, UInt64, Array(UInt32));

```


```
┌─v1─┬─v2──────┐
│ 42 │ [1,2,3] │
└────┴─────────┘

```

- Сравнить подстолбецVariantс требуемым типом:

```
SELECT * FROM test WHERE v2.`Array(UInt32)` == [1,2,3] -- or using variantElement(v2, 'Array(UInt32)')

```


```
┌─v1─┬─v2──────┐
│ 42 │ [1,2,3] │
└────┴─────────┘

```

Иногда может быть полезно дополнительно проверить тип варианта, так как подстолбцы со сложными типами, такими какArray/Map/Tuple, не могут находиться внутриNullableи будут иметь значения по умолчанию вместоNULLв строках с другими типами:


```
SELECT v2, v2.`Array(UInt32)`, variantType(v2) FROM test WHERE v2.`Array(UInt32)` == [];

```


```
┌─v2───┬─v2.Array(UInt32)─┬─variantType(v2)─┐
│ 42   │ []               │ UInt64          │
│ 43   │ []               │ UInt64          │
│ abc  │ []               │ String          │
│ []   │ []               │ Array(UInt32)   │
│ ᴺᵁᴸᴸ │ []               │ None            │
└──────┴──────────────────┴─────────────────┘

```


```
SELECT v2, v2.`Array(UInt32)`, variantType(v2) FROM test WHERE variantType(v2) == 'Array(UInt32)' AND v2.`Array(UInt32)` == [];

```


```
┌─v2─┬─v2.Array(UInt32)─┬─variantType(v2)─┐
│ [] │ []               │ Array(UInt32)   │
└────┴──────────────────┴─────────────────┘

```

Note:values of variants with different numeric types are considered as different variants and not compared between each other, their type names are compared instead.

Example:


```
SET allow_suspicious_variant_types = 1;
CREATE TABLE test (v Variant(UInt32, Int64)) ENGINE=Memory;
INSERT INTO test VALUES (1::UInt32), (1::Int64), (100::UInt32), (100::Int64);
SELECT v, variantType(v) FROM test ORDER by v;

```


```
┌─v───┬─variantType(v)─┐
│ 1   │ Int64          │
│ 100 │ Int64          │
│ 1   │ UInt32         │
│ 100 │ UInt32         │
└─────┴────────────────┘

```

Noteby defaultVarianttype is not allowed inGROUP BY/ORDER BYkeys, if you want to use it consider its special comparison rule and enableallow_suspicious_types_in_group_by/allow_suspicious_types_in_order_bysettings.


## JSONExtract functions with Variant​

AllJSONExtract*functions supportVarianttype:


```
SELECT JSONExtract('{"a" : [1, 2, 3]}', 'a', 'Variant(UInt32, String, Array(UInt32))') AS variant, variantType(variant) AS variant_type;

```


```
┌─variant─┬─variant_type──┐
│ [1,2,3] │ Array(UInt32) │
└─────────┴───────────────┘

```


```
SELECT JSONExtract('{"obj" : {"a" : 42, "b" : "Hello", "c" : [1,2,3]}}', 'obj', 'Map(String, Variant(UInt32, String, Array(UInt32)))') AS map_of_variants, mapApply((k, v) -> (k, variantType(v)), map_of_variants) AS map_of_variant_types

```


```
┌─map_of_variants──────────────────┬─map_of_variant_types────────────────────────────┐
│ {'a':42,'b':'Hello','c':[1,2,3]} │ {'a':'UInt32','b':'String','c':'Array(UInt32)'} │
└──────────────────────────────────┴─────────────────────────────────────────────────┘

```


```
SELECT JSONExtractKeysAndValues('{"a" : 42, "b" : "Hello", "c" : [1,2,3]}', 'Variant(UInt32, String, Array(UInt32))') AS variants, arrayMap(x -> (x.1, variantType(x.2)), variants) AS variant_types

```


```
┌─variants───────────────────────────────┬─variant_types─────────────────────────────────────────┐
│ [('a',42),('b','Hello'),('c',[1,2,3])] │ [('a','UInt32'),('b','String'),('c','Array(UInt32)')] │
└────────────────────────────────────────┴───────────────────────────────────────────────────────┘

```


## Функции с аргументами типа Variant​

Большинство функций в ClickHouse автоматически поддерживают аргументы типаVariantблагодаряреализации по умолчанию для Variant.
Начиная с версии26.1, когда функция, которая явно не обрабатывает типы Variant, получает столбец типа Variant, ClickHouse:

- Извлекает из столбца Variant каждый вариант типа
- Выполняет функцию отдельно для каждого варианта типа
- Объединяет результаты соответствующим образом в зависимости от типов результата
Это позволяет использовать обычные функции со столбцами типа Variant без специальной обработки.

Пример:


```
CREATE TABLE test (v Variant(UInt32, String)) ENGINE = Memory;
INSERT INTO test VALUES (42), ('hello'), (NULL);
SELECT *, toTypeName(v) FROM test WHERE v = 42;

```


```
   ┌─v──┬─toTypeName(v)───────────┐
1. │ 42 │ Variant(String, UInt32) │
   └────┴─────────────────────────┘

```

Оператор сравнения автоматически применяется к каждому типу внутри Variant отдельно, что позволяет выполнять фильтрацию по столбцам типа Variant.

Поведение результирующего типа:

Результирующий тип зависит от того, что функция возвращает для каждого варианта:

- Разные результирующие типы:Variant(T1, T2, ...)CREATE TABLE test2 (v Variant(UInt64, Float64)) ENGINE = Memory;
INSERT INTO test2 VALUES (42::UInt64), (42.42);
SELECT v + 1 AS result, toTypeName(result) FROM test2;┌─result─┬─toTypeName(plus(v, 1))──┐
│     43 │ Variant(Float64, UInt64) │
│  43.42 │ Variant(Float64, UInt64) │
└────────┴─────────────────────────┘
Разные результирующие типы:Variant(T1, T2, ...)


```
CREATE TABLE test2 (v Variant(UInt64, Float64)) ENGINE = Memory;
INSERT INTO test2 VALUES (42::UInt64), (42.42);
SELECT v + 1 AS result, toTypeName(result) FROM test2;

```


```
┌─result─┬─toTypeName(plus(v, 1))──┐
│     43 │ Variant(Float64, UInt64) │
│  43.42 │ Variant(Float64, UInt64) │
└────────┴─────────────────────────┘

```

- Несовместимость типов:NULLдля несовместимых вариантовCREATE TABLE test3 (v Variant(Array(UInt32), UInt32)) ENGINE = Memory;
INSERT INTO test3 VALUES ([1,2,3]), (42);
SELECT v + 10 AS result, toTypeName(result) FROM test3;┌─result─┬─toTypeName(plus(v, 10))─┐
│   ᴺᵁᴸᴸ │ Nullable(UInt64)        │
│     52 │ Nullable(UInt64)        │
└────────┴─────────────────────────┘
Несовместимость типов:NULLдля несовместимых вариантов


```
CREATE TABLE test3 (v Variant(Array(UInt32), UInt32)) ENGINE = Memory;
INSERT INTO test3 VALUES ([1,2,3]), (42);
SELECT v + 10 AS result, toTypeName(result) FROM test3;

```


```
┌─result─┬─toTypeName(plus(v, 10))─┐
│   ᴺᵁᴸᴸ │ Nullable(UInt64)        │
│     52 │ Nullable(UInt64)        │
└────────┴─────────────────────────┘

```

Обработка ошибок:Когда функция не может обработать тип варианта, перехватываются только ошибки, связанные с типами (ILLEGAL_TYPE_OF_ARGUMENT,
TYPE_MISMATCH, CANNOT_CONVERT_TYPE, NO_COMMON_TYPE), и для таких строк результатом становится NULL. Другие ошибки, такие как
деление на ноль или нехватка памяти, пробрасываются обычным образом, чтобы не скрывать реальные проблемы.
