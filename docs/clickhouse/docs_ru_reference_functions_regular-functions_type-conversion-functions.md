# Функции преобразования типов - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/functions/regular-functions/type-conversion-functions


## Распространённые проблемы при преобразовании данных


```
SELECT
    toTypeName(toLowCardinality('') AS val) AS source_type,
    toTypeName(toString(val)) AS to_type_result_type,
    toTypeName(CAST(val, 'String')) AS cast_result_type

┌─source_type────────────┬─to_type_result_type────┬─cast_result_type─┐
│ LowCardinality(String) │ LowCardinality(String) │ String           │
└────────────────────────┴────────────────────────┴──────────────────┘

SELECT
    toTypeName(toNullable('') AS val) AS source_type,
    toTypeName(toString(val)) AS to_type_result_type,
    toTypeName(CAST(val, 'String')) AS cast_result_type

┌─source_type──────┬─to_type_result_type─┬─cast_result_type─┐
│ Nullable(String) │ Nullable(String)    │ String           │
└──────────────────┴─────────────────────┴──────────────────┘

SELECT
    toTypeName(toNullable('') AS val) AS source_type,
    toTypeName(toString(val)) AS to_type_result_type,
    toTypeName(CAST(val, 'String')) AS cast_result_type
SETTINGS cast_keep_nullable = 1

┌─source_type──────┬─to_type_result_type─┬─cast_result_type─┐
│ Nullable(String) │ Nullable(String)    │ Nullable(String) │
└──────────────────┴─────────────────────┴──────────────────┘

```


## Примечания к функциям `toString`

- При преобразовании в строку или из строки значение форматируется или разбирается по тем же правилам, что и для формата TabSeparated (и почти всех остальных текстовых форматов). Если строку не удаётся разобрать, генерируется исключение, и запрос отменяется.
- При преобразовании дат в числа или наоборот дата соответствует количеству дней с начала эпохи Unix.
- При преобразовании значений даты и времени в числа или наоборот дата и время соответствуют количеству секунд с начала эпохи Unix.
- Функция `toString` для аргумента `DateTime` может принимать второй аргумент типа String, содержащий имя часового пояса, например: `Europe/Amsterdam`. В этом случае время форматируется в соответствии с указанным часовым поясом.

## Примечания к функциям `toDate`/`toDateTime`


```
YYYY-MM-DD
YYYY-MM-DD hh:mm:ss

```


```
SELECT
    now() AS ts,
    time_zone,
    toString(ts, time_zone) AS str_tz_datetime
FROM system.time_zones
WHERE time_zone LIKE 'Europe%'
LIMIT 10

```


```
┌──────────────────ts─┬─time_zone─────────┬─str_tz_datetime─────┐
│ 2023-09-08 19:14:59 │ Europe/Amsterdam  │ 2023-09-08 21:14:59 │
│ 2023-09-08 19:14:59 │ Europe/Andorra    │ 2023-09-08 21:14:59 │
│ 2023-09-08 19:14:59 │ Europe/Astrakhan  │ 2023-09-08 23:14:59 │
│ 2023-09-08 19:14:59 │ Europe/Athens     │ 2023-09-08 22:14:59 │
│ 2023-09-08 19:14:59 │ Europe/Belfast    │ 2023-09-08 20:14:59 │
│ 2023-09-08 19:14:59 │ Europe/Belgrade   │ 2023-09-08 21:14:59 │
│ 2023-09-08 19:14:59 │ Europe/Berlin     │ 2023-09-08 21:14:59 │
│ 2023-09-08 19:14:59 │ Europe/Bratislava │ 2023-09-08 21:14:59 │
│ 2023-09-08 19:14:59 │ Europe/Brussels   │ 2023-09-08 21:14:59 │
│ 2023-09-08 19:14:59 │ Europe/Bucharest  │ 2023-09-08 22:14:59 │
└─────────────────────┴───────────────────┴─────────────────────┘

```


## CAST


```
CAST(x, T)
or CAST(x AS T)
or x::T

```

- `x` — Значение любого типа. [`Any`](https://clickhouse.com/docs/ru/reference/data-types/index)
- `T` — Целевой тип данных. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT CAST(42, 'String')

```


```
┌─CAST(42, 'String')─┐
│ 42                 │
└────────────────────┘

```


```
SELECT CAST('2025-01-01' AS Date)

```


```
┌─CAST('2025-01-01', 'Date')─┐
│                 2025-01-01 │
└────────────────────────────┘

```


```
SELECT '123'::UInt32

```


```
┌─CAST('123', 'UInt32')─┐
│                   123 │
└───────────────────────┘

```


## DATE


```
DATE(expr)

```

- `expr` — Значение, которое необходимо преобразовать. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`UInt32`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Date`](https://clickhouse.com/docs/ru/reference/data-types/date) или [`DateTime`](https://clickhouse.com/docs/ru/reference/data-types/datetime)

```
SELECT DATE('2023-01-01')

```


```
2023-01-01

```


## accurateCast


```
accurateCast(x, T)

```

- `x` — Значение для преобразования. [`Any`](https://clickhouse.com/docs/ru/reference/data-types/index)
- `T` — Имя целевого типа данных. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT accurateCast(42, 'UInt16')

```


```
┌─accurateCast(42, 'UInt16')─┐
│                         42 │
└────────────────────────────┘

```


```
SELECT accurateCast('123.45', 'Float64')

```


```
┌─accurateCast('123.45', 'Float64')─┐
│                            123.45 │
└───────────────────────────────────┘

```


## accurateCastOrDefault


```
accurateCastOrDefault(x, T[, default_value])

```

- `x` — Значение для преобразования. [`Any`](https://clickhouse.com/docs/ru/reference/data-types/index)
- `T` — Имя целевого типа данных. [`const String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `default_value` — Необязательный параметр. Значение по умолчанию, которое возвращается, если преобразование не удалось. [`Any`](https://clickhouse.com/docs/ru/reference/data-types/index)

```
SELECT accurateCastOrDefault(42, 'String')

```


```
┌─accurateCastOrDefault(42, 'String')─┐
│ 42                                  │
└─────────────────────────────────────┘

```


```
SELECT accurateCastOrDefault('abc', 'UInt32', 999::UInt32)

```


```
┌─accurateCastOrDefault('abc', 'UInt32', 999)─┐
│                                         999 │
└─────────────────────────────────────────────┘

```


```
SELECT accurateCastOrDefault('abc', 'UInt32')

```


```
┌─accurateCastOrDefault('abc', 'UInt32')─┐
│                                      0 │
└────────────────────────────────────────┘

```


## accurateCastOrNull


```
accurateCastOrNull(x, T)

```

- `x` — Значение, которое нужно преобразовать. [`Any`](https://clickhouse.com/docs/ru/reference/data-types/index)
- `T` — Имя целевого типа данных. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT accurateCastOrNull(42, 'String')

```


```
┌─accurateCastOrNull(42, 'String')─┐
│ 42                               │
└──────────────────────────────────┘

```


```
SELECT accurateCastOrNull('abc', 'UInt32')

```


```
┌─accurateCastOrNull('abc', 'UInt32')─┐
│                                ᴺᵁᴸᴸ │
└─────────────────────────────────────┘

```


## formatRow


```
formatRow(format, x, y, ...)

```

- `format` — Текстовый формат. Например, CSV, TSV. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `x, y, ...` — Выражения. [`Any`](https://clickhouse.com/docs/ru/reference/data-types/index)

```
SELECT formatRow('CSV', number, 'good')
FROM numbers(3)

```


```
┌─formatRow('CSV', number, 'good')─┐
│ 0,"good"                        ↴│
│ 1,"good"                        ↴│
│ 2,"good"                        ↴│
└──────────────────────────────────┘

```


```
SELECT formatRow('CustomSeparated', number, 'good')
FROM numbers(3)
SETTINGS format_custom_result_before_delimiter='<prefix>\n', format_custom_result_after_delimiter='<suffix>'

```


```
┌─formatRow('CustomSeparated', number, 'good')─┐
│ <prefix>                                    ↴│
│↳0	good                                     ↴│
│↳<suffix>                                     │
│ <prefix>                                    ↴│
│↳1	good                                     ↴│
│↳<suffix>                                     │
│ <prefix>                                    ↴│
│↳2	good                                     ↴│
│↳<suffix>                                     │
└──────────────────────────────────────────────┘

```


## formatRowNoNewline


```
formatRowNoNewline(format, x, y, ...)

```

- `format` — Текстовый формат, например CSV или TSV. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `x, y, ...` — Выражения. [`Any`](https://clickhouse.com/docs/ru/reference/data-types/index)

```
SELECT formatRowNoNewline('CSV', number, 'good')
FROM numbers(3)

```


```
┌─formatRowNoNewline('CSV', number, 'good')─┐
│ 0,"good"                                  │
│ 1,"good"                                  │
│ 2,"good"                                  │
└───────────────────────────────────────────┘

```


## fromUnixTimestamp64Micro


```
fromUnixTimestamp64Micro(value[, timezone])

```

- `value` — Unix-временная метка в микросекундах. [`Int64`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `timezone` — Необязательно. Часовой пояс возвращаемого значения. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT fromUnixTimestamp64Micro(1640995200123456)

```


```
┌─fromUnixTimestamp64Micro(1640995200123456)─┐
│                 2022-01-01 00:00:00.123456 │
└────────────────────────────────────────────┘

```


## fromUnixTimestamp64Milli


```
fromUnixTimestamp64Milli(value[, timezone])

```

- `value` — Unix-временная метка в миллисекундах. [`Int64`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `timezone` — Необязательный параметр. Часовой пояс возвращаемого значения. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT fromUnixTimestamp64Milli(1640995200123)

```


```
┌─fromUnixTimestamp64Milli(1640995200123)─┐
│                 2022-01-01 00:00:00.123 │
└─────────────────────────────────────────┘

```


## fromUnixTimestamp64Nano


```
fromUnixTimestamp64Nano(value[, timezone])

```

- `value` — Unix-временная метка в наносекундах. [`Int64`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `timezone` — Необязательно. Часовой пояс возвращаемого значения. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT fromUnixTimestamp64Nano(1640995200123456789)

```


```
┌─fromUnixTimestamp64Nano(1640995200123456789)─┐
│                2022-01-01 00:00:00.123456789 │
└──────────────────────────────────────────────┘

```


## fromUnixTimestamp64Second


```
fromUnixTimestamp64Second(value[, timezone])

```

- `value` — Unix-временная метка в секундах. [`Int64`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `timezone` — Необязательный. Часовой пояс для возвращаемого значения. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT fromUnixTimestamp64Second(1640995200)

```


```
┌─fromUnixTimestamp64Second(1640995200)─┐
│                   2022-01-01 00:00:00 │
└───────────────────────────────────────┘

```


## parseDateTime


```
parseDateTime(time_string, format[, timezone])

```

- `time_string` — Строка, которую нужно разобрать в DateTime. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `format` — Строка формата, определяющая, как разбирать time_string. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `timezone` — Необязательно. Часовой пояс. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT parseDateTime('2025-01-04+23:00:00', '%Y-%m-%d+%H:%i:%s')

```


```
┌─parseDateTime('2025-01-04+23:00:00', '%Y-%m-%d+%H:%i:%s')─┐
│                                       2025-01-04 23:00:00 │
└───────────────────────────────────────────────────────────┘

```


## parseDateTime32BestEffort


```
parseDateTime32BestEffort(time_string[, time_zone])

```

- `time_string` — Строка `String`, содержащая дату и время для преобразования. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `time_zone` — Необязательный. Часовой пояс, в соответствии с которым разбирается `time_string`. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT parseDateTime32BestEffort('23/10/2025 12:12:57')
AS parseDateTime32BestEffort

```


```
┌─parseDateTime32BestEffort─┐
│       2025-10-23 12:12:57 │
└───────────────────────────┘

```


```
SELECT parseDateTime32BestEffort('Sat, 18 Aug 2025 07:22:16 GMT', 'Asia/Istanbul')
AS parseDateTime32BestEffort

```


```
┌─parseDateTime32BestEffort─┐
│       2025-08-18 10:22:16 │
└───────────────────────────┘

```


```
SELECT parseDateTime32BestEffort('1284101485')
AS parseDateTime32BestEffort

```


```
┌─parseDateTime32BestEffort─┐
│       2015-07-07 12:04:41 │
└───────────────────────────┘

```


## parseDateTime32BestEffortOrNull


```
parseDateTime32BestEffortOrNull(time_string[, time_zone])

```

- `time_string` — Строка `String`, содержащая дату и время для преобразования. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `time_zone` — Необязательно. Часовой пояс, в соответствии с которым разбирается `time_string`. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    parseDateTime32BestEffortOrNull('23/10/2025 12:12:57') AS valid,
    parseDateTime32BestEffortOrNull('invalid date') AS invalid

```


```
┌─valid───────────────┬─invalid─┐
│ 2025-10-23 12:12:57 │    ᴺᵁᴸᴸ │
└─────────────────────┴─────────┘

```


## parseDateTime32BestEffortOrZero


```
parseDateTime32BestEffortOrZero(time_string[, time_zone])

```

- `time_string` — Строка с датой и временем для преобразования. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `time_zone` — Необязательно. Часовой пояс, в соответствии с которым разбирается `time_string`. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    parseDateTime32BestEffortOrZero('23/10/2025 12:12:57') AS valid,
    parseDateTime32BestEffortOrZero('invalid date') AS invalid

```


```
┌─valid───────────────┬─invalid─────────────┐
│ 2025-10-23 12:12:57 │ 1970-01-01 00:00:00 │
└─────────────────────┴─────────────────────┘

```


## parseDateTime64


```
parseDateTime64(time_string, format[, timezone])

```

- `time_string` — Строка, которую нужно разобрать как DateTime64. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `format` — Строка формата, задающая способ разбора time_string. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `timezone` — Необязательно. Часовой пояс. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT parseDateTime64('2025-01-04 23:00:00.123', '%Y-%m-%d %H:%i:%s.%f')

```


```
┌─parseDateTime64('2025-01-04 23:00:00.123', '%Y-%m-%d %H:%i:%s.%f')─┐
│                                         2025-01-04 23:00:00.123000 │
└────────────────────────────────────────────────────────────────────┘

```


## parseDateTime64BestEffort


```
parseDateTime64BestEffort(time_string[, precision[, time_zone]])

```

- `time_string` — Строка, содержащая дату или дату и время для преобразования. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `precision` — Необязательно. Требуемая точность. `3` для миллисекунд, `6` для микросекунд. По умолчанию: `3`. [`UInt8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `time_zone` — Необязательно. Часовой пояс. Функция разбирает `time_string` с учетом часового пояса. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT parseDateTime64BestEffort('2025-01-01') AS a, toTypeName(a) AS t
UNION ALL
SELECT parseDateTime64BestEffort('2025-01-01 01:01:00.12346') AS a, toTypeName(a) AS t
UNION ALL
SELECT parseDateTime64BestEffort('2025-01-01 01:01:00.12346',6) AS a, toTypeName(a) AS t
UNION ALL
SELECT parseDateTime64BestEffort('2025-01-01 01:01:00.12346',3,'Asia/Istanbul') AS a, toTypeName(a) AS t
FORMAT PrettyCompactMonoBlock

```


```
┌──────────────────────────a─┬─t──────────────────────────────┐
│ 2025-01-01 01:01:00.123000 │ DateTime64(3)                  │
│ 2025-01-01 00:00:00.000000 │ DateTime64(3)                  │
│ 2025-01-01 01:01:00.123460 │ DateTime64(6)                  │
│ 2025-12-31 22:01:00.123000 │ DateTime64(3, 'Asia/Istanbul') │
└────────────────────────────┴────────────────────────────────┘

```


## parseDateTime64BestEffortOrNull


```
parseDateTime64BestEffortOrNull(time_string[, precision[, time_zone]])

```

- `time_string` — Строка, содержащая дату или дату и время для преобразования. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `precision` — Необязательно. Требуемая точность. `3` для миллисекунд, `6` для микросекунд. По умолчанию: `3`. [`UInt8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `time_zone` — Необязательно. Часовой пояс. Функция разбирает `time_string` в соответствии с часовым поясом. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT parseDateTime64BestEffortOrNull('2025-01-01 01:01:00.123') AS valid,
       parseDateTime64BestEffortOrNull('invalid') AS invalid

```


```
┌─valid───────────────────┬─invalid─┐
│ 2025-01-01 01:01:00.123 │    ᴺᵁᴸᴸ │
└─────────────────────────┴─────────┘

```


## parseDateTime64BestEffortOrZero


```
parseDateTime64BestEffortOrZero(time_string[, precision[, time_zone]])

```

- `time_string` — Строка, содержащая дату или дату и время для преобразования. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `precision` — Необязательно. Требуемая точность. `3` для миллисекунд, `6` для микросекунд. По умолчанию: `3`. [`UInt8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `time_zone` — Необязательно. Часовой пояс. Функция разбирает `time_string` с учетом этого часового пояса. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT parseDateTime64BestEffortOrZero('2025-01-01 01:01:00.123') AS valid,
       parseDateTime64BestEffortOrZero('invalid') AS invalid

```


```
┌─valid───────────────────┬─invalid─────────────────┐
│ 2025-01-01 01:01:00.123 │ 1970-01-01 00:00:00.000 │
└─────────────────────────┴─────────────────────────┘

```


## parseDateTime64BestEffortUS


```
parseDateTime64BestEffortUS(time_string [, precision [, time_zone]])

```

- `time_string` — Строка `String`, содержащая дату или дату и время для преобразования. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `precision` — Необязательно. Требуемая точность. `3` для миллисекунд, `6` для микросекунд. По умолчанию: `3`. [`UInt8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `time_zone` — Необязательно. Часовой пояс. Функция разбирает `time_string` в соответствии с указанным часовым поясом. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT parseDateTime64BestEffortUS('02/10/2025 12:30:45.123') AS us_format,
       parseDateTime64BestEffortUS('15/08/2025 10:15:30.456') AS fallback_to_standard

```


```
┌─us_format───────────────┬─fallback_to_standard────┐
│ 2025-02-10 12:30:45.123 │ 2025-08-15 10:15:30.456 │
└─────────────────────────┴─────────────────────────┘

```


## parseDateTime64BestEffortUSOrNull


```
parseDateTime64BestEffortUSOrNull(time_string[, precision[, time_zone]])

```

- `time_string` — Строка, содержащая дату или дата и время для преобразования. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `precision` — Необязательный параметр. Требуемая точность. `3` для миллисекунд, `6` для микросекунд. По умолчанию: `3`. [`UInt8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `time_zone` — Необязательный параметр. Часовой пояс. Функция разбирает `time_string` в соответствии с этим часовым поясом. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT parseDateTime64BestEffortUSOrNull('02/10/2025 12:30:45.123') AS valid_us,
       parseDateTime64BestEffortUSOrNull('invalid') AS invalid

```


```
┌─valid_us────────────────┬─invalid─┐
│ 2025-02-10 12:30:45.123 │    ᴺᵁᴸᴸ │
└─────────────────────────┴─────────┘

```


## parseDateTime64BestEffortUSOrZero


```
parseDateTime64BestEffortUSOrZero(time_string [, precision [, time_zone]])

```

- `time_string` — Строка, содержащая дату или дату и время для преобразования. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `precision` — Необязательно. Требуемая точность: `3` для миллисекунд, `6` для микросекунд. По умолчанию: `3`. [`UInt8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `time_zone` — Необязательно. Часовой пояс. Функция разбирает `time_string` в соответствии с этим часовым поясом. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT parseDateTime64BestEffortUSOrZero('02/10/2025 12:30:45.123') AS valid_us,
       parseDateTime64BestEffortUSOrZero('invalid') AS invalid

```


```
┌─valid_us────────────────┬─invalid─────────────────┐
│ 2025-02-10 12:30:45.123 │ 1970-01-01 00:00:00.000 │
└─────────────────────────┴─────────────────────────┘

```


## parseDateTime64InJodaSyntax


```
parseDateTime64InJodaSyntax(time_string, format[, timezone])

```

- `time_string` — Строка `String`, которую нужно разобрать в DateTime64. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `format` — Строка формата в синтаксисе Joda, задающая способ разбора time_string. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `timezone` — Необязательно. Часовой пояс. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT parseDateTime64InJodaSyntax('2025-01-04 23:00:00.123', 'yyyy-MM-dd HH:mm:ss.SSS')

```


```
┌─parseDateTime64InJodaSyntax('2025-01-04 23:00:00.123', 'yyyy-MM-dd HH:mm:ss.SSS')─┐
│                                                           2025-01-04 23:00:00.123 │
└───────────────────────────────────────────────────────────────────────────────────┘

```


## parseDateTime64InJodaSyntaxOrNull


```
parseDateTime64InJodaSyntaxOrNull(time_string, format[, timezone])

```

- `time_string` — строка, которую нужно разобрать как DateTime64. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `format` — строка формата в синтаксисе Joda, задающая способ разбора time_string. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `timezone` — необязательный параметр. Часовой пояс. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT parseDateTime64InJodaSyntaxOrNull('2025-01-04 23:00:00.123', 'yyyy-MM-dd HH:mm:ss.SSS')

```


```
┌─parseDateTime64InJodaSyntaxOrNull('2025-01-04 23:00:00.123', 'yyyy-MM-dd HH:mm:ss.SSS')─┐
│                                                                 2025-01-04 23:00:00.123 │
└─────────────────────────────────────────────────────────────────────────────────────────┘

```


## parseDateTime64InJodaSyntaxOrZero


```
parseDateTime64InJodaSyntaxOrZero(time_string, format[, timezone])

```

- `time_string` — Строка `String`, которую нужно преобразовать в DateTime64. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `format` — Строка формата в синтаксисе Joda, задающая способ разбора time_string. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `timezone` — Необязательный параметр. Часовой пояс. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT parseDateTime64InJodaSyntaxOrZero('2025-01-04 23:00:00.123', 'yyyy-MM-dd HH:mm:ss.SSS')

```


```
┌─parseDateTime64InJodaSyntaxOrZero('2025-01-04 23:00:00.123', 'yyyy-MM-dd HH:mm:ss.SSS')─┐
│                                                                 2025-01-04 23:00:00.123 │
└─────────────────────────────────────────────────────────────────────────────────────────┘

```


## parseDateTime64OrNull


```
parseDateTime64OrNull(time_string, format[, timezone])

```

- `time_string` — Строка, которую нужно разобрать как DateTime64. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `format` — Строка формата, задающая способ разбора time_string. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `timezone` — Необязательный параметр. Часовой пояс. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT parseDateTime64OrNull('2025-01-04 23:00:00.123', '%Y-%m-%d %H:%i:%s.%f')

```


```
┌─parseDateTime64OrNull('2025-01-04 23:00:00.123', '%Y-%m-%d %H:%i:%s.%f')─┐
│                                               2025-01-04 23:00:00.123000 │
└──────────────────────────────────────────────────────────────────────────┘

```


## parseDateTime64OrZero


```
parseDateTime64OrZero(time_string, format[, timezone])

```

- `time_string` — Строка, которую нужно разобрать в DateTime64. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `format` — Строка формата, задающая, как разобрать time_string. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `timezone` — Необязательный параметр. Часовой пояс. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT parseDateTime64OrZero('2025-01-04 23:00:00.123', '%Y-%m-%d %H:%i:%s.%f')

```


```
┌─parseDateTime64OrZero('2025-01-04 23:00:00.123', '%Y-%m-%d %H:%i:%s.%f')─┐
│                                               2025-01-04 23:00:00.123000 │
└──────────────────────────────────────────────────────────────────────────┘

```


## parseDateTimeBestEffort

- Строка, содержащая 9–10-значную Unix-временную метку.
- Строка с датой и компонентом времени: `YYYYMMDDhhmmss`, `DD/MM/YYYY hh:mm:ss`, `DD-MM-YY hh:mm`, `YYYY-MM-DD hh:mm:ss` и т. д.
- Строка с датой, но без компонента времени: `YYYY`, `YYYYMM`, `YYYY*MM`, `DD/MM/YYYY`, `DD-MM-YY` и т. д.
- Строка с днем и временем: `DD`, `DD hh`, `DD hh:mm`. В этом случае `MM` заменяется на `01`.
- Строка, содержащая дату и время вместе с информацией о смещении часового пояса: `YYYY-MM-DD hh:mm:ss ±h:mm` и т. д.
- Временная метка syslog: `Mmm dd hh:mm:ss`. Например, `Jun 9 14:20:32`.

```
parseDateTimeBestEffort(time_string[, time_zone])

```

- `time_string` — Строка с датой и временем для преобразования. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `time_zone` — Необязательный параметр. Часовой пояс, в соответствии с которым разбирается `time_string`. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT parseDateTimeBestEffort('23/10/2025 12:12:57') AS parseDateTimeBestEffort

```


```
┌─parseDateTimeBestEffort─┐
│     2025-10-23 12:12:57 │
└─────────────────────────┘

```


```
SELECT parseDateTimeBestEffort('Sat, 18 Aug 2025 07:22:16 GMT', 'Asia/Istanbul') AS parseDateTimeBestEffort

```


```
┌─parseDateTimeBestEffort─┐
│     2025-08-18 10:22:16 │
└─────────────────────────┘

```


```
SELECT parseDateTimeBestEffort('1735689600') AS parseDateTimeBestEffort

```


```
┌─parseDateTimeBestEffort─┐
│     2025-01-01 00:00:00 │
└─────────────────────────┘

```


## parseDateTimeBestEffortOrNull

- Строка, содержащая 9..10-значную Unix-временную метку.
- Строка с датой и компонентом времени: `YYYYMMDDhhmmss`, `DD/MM/YYYY hh:mm:ss`, `DD-MM-YY hh:mm`, `YYYY-MM-DD hh:mm:ss` и т. д.
- Строка с датой, но без компонента времени: `YYYY`, `YYYYMM`, `YYYY*MM`, `DD/MM/YYYY`, `DD-MM-YY` и т. д.
- Строка с днем и временем: `DD`, `DD hh`, `DD hh:mm`. В этом случае `MM` заменяется на `01`.
- Строка, включающая дату и время вместе с информацией о смещении часового пояса: `YYYY-MM-DD hh:mm:ss ±h:mm` и т. д.
- Syslog-временная метка: `Mmm dd hh:mm:ss`. Например, `Jun 9 14:20:32`.

```
parseDateTimeBestEffortOrNull(time_string[, time_zone])

```

- `time_string` — Строка, содержащая дату и время для преобразования. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `time_zone` — Необязательно. Часовой пояс, в соответствии с которым разбирается `time_string`. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT parseDateTimeBestEffortOrNull('23/10/2025 12:12:57') AS valid,
       parseDateTimeBestEffortOrNull('invalid') AS invalid

```


```
┌─valid───────────────┬─invalid─┐
│ 2025-10-23 12:12:57 │    ᴺᵁᴸᴸ │
└─────────────────────┴─────────┘

```


## parseDateTimeBestEffortOrZero

- Строка, содержащая 9..10-значную Unix-временную метку.
- Строка с датой и временем: `YYYYMMDDhhmmss`, `DD/MM/YYYY hh:mm:ss`, `DD-MM-YY hh:mm`, `YYYY-MM-DD hh:mm:ss` и т. д.
- Строка с датой, но без времени: `YYYY`, `YYYYMM`, `YYYY*MM`, `DD/MM/YYYY`, `DD-MM-YY` и т. д.
- Строка с днём и временем: `DD`, `DD hh`, `DD hh:mm`. В этом случае вместо `MM` подставляется `01`.
- Строка, включающая дату и время вместе с информацией о смещении часового пояса: `YYYY-MM-DD hh:mm:ss ±h:mm` и т. д.
- Временная метка syslog: `Mmm dd hh:mm:ss`. Например, `Jun 9 14:20:32`.

```
parseDateTimeBestEffortOrZero(time_string[, time_zone])

```

- `time_string` — Строка `String`, содержащая дату и время для преобразования. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `time_zone` — Необязательно. Часовой пояс, в соответствии с которым разбирается `time_string`. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT parseDateTimeBestEffortOrZero('23/10/2025 12:12:57') AS valid,
       parseDateTimeBestEffortOrZero('invalid') AS invalid

```


```
┌─valid───────────────┬─invalid─────────────┐
│ 2025-10-23 12:12:57 │ 1970-01-01 00:00:00 │
└─────────────────────┴─────────────────────┘

```


## parseDateTimeBestEffortUS


```
parseDateTimeBestEffortUS(time_string[, time_zone])

```

- `time_string` — `String` с датой и временем для преобразования. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `time_zone` — Необязательно. Часовой пояс, в соответствии с которым разбирается `time_string`. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT parseDateTimeBestEffortUS('02/10/2025') AS us_format,
       parseDateTimeBestEffortUS('15/08/2025') AS fallback_to_standard

```


```
┌─us_format───────────┬─fallback_to_standard─┐
│ 2025-02-10 00:00:00 │  2025-08-15 00:00:00 │
└─────────────────────┴──────────────────────┘

```


## parseDateTimeBestEffortUSOrNull


```
parseDateTimeBestEffortUSOrNull(time_string[, time_zone])

```

- `time_string` — Строка, содержащая дату и время для преобразования. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `time_zone` — Необязательный. Часовой пояс, в соответствии с которым разбирается `time_string`. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT parseDateTimeBestEffortUSOrNull('02/10/2025') AS valid_us,
       parseDateTimeBestEffortUSOrNull('invalid') AS invalid

```


```
┌─valid_us────────────┬─invalid─┐
│ 2025-02-10 00:00:00 │    ᴺᵁᴸᴸ │
└─────────────────────┴─────────┘

```


## parseDateTimeBestEffortUSOrZero


```
parseDateTimeBestEffortUSOrZero(time_string[, time_zone])

```

- `time_string` — Строка, содержащая дату и время для преобразования. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `time_zone` — Необязательно. Часовой пояс, в соответствии с которым разбирается `time_string`. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT parseDateTimeBestEffortUSOrZero('02/10/2025') AS valid_us,
       parseDateTimeBestEffortUSOrZero('invalid') AS invalid

```


```
┌─valid_us────────────┬─invalid─────────────┐
│ 2025-02-10 00:00:00 │ 1970-01-01 00:00:00 │
└─────────────────────┴─────────────────────┘

```


## parseDateTimeInJodaSyntax


```
parseDateTimeInJodaSyntax(time_string, format[, timezone])

```

- `time_string` — Строка для разбора в DateTime. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `format` — Строка формата в синтаксисе Joda, задающая способ разбора time_string. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `timezone` — Необязательно. Часовой пояс. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT parseDateTimeInJodaSyntax('2025-01-04 23:00:00', 'yyyy-MM-dd HH:mm:ss')

```


```
┌─parseDateTimeInJodaSyntax('2025-01-04 23:00:00', 'yyyy-MM-dd HH:mm:ss')─┐
│                                                     2025-01-04 23:00:00 │
└─────────────────────────────────────────────────────────────────────────┘

```


## parseDateTimeInJodaSyntaxOrNull


```
parseDateTimeInJodaSyntaxOrNull(time_string, format[, timezone])

```

- `time_string` — Строка, которую нужно разобрать как DateTime. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `format` — Строка формата в синтаксисе Joda, задающая способ разбора time_string. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `timezone` — Необязательно. Часовой пояс. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT parseDateTimeInJodaSyntaxOrNull('2025-01-04 23:00:00', 'yyyy-MM-dd HH:mm:ss')

```


```
┌─parseDateTimeInJodaSyntaxOrNull('2025-01-04 23:00:00', 'yyyy-MM-dd HH:mm:ss')─┐
│                                                           2025-01-04 23:00:00 │
└───────────────────────────────────────────────────────────────────────────────┘

```


## parseDateTimeInJodaSyntaxOrZero


```
parseDateTimeInJodaSyntaxOrZero(time_string, format[, timezone])

```

- `time_string` — строка, которую нужно разобрать как DateTime. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `format` — строка формата в синтаксисе Joda, задающая, как разбирать time_string. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `timezone` — Необязательно. Часовой пояс. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT parseDateTimeInJodaSyntaxOrZero('2025-01-04 23:00:00', 'yyyy-MM-dd HH:mm:ss')

```


```
┌─parseDateTimeInJodaSyntaxOrZero('2025-01-04 23:00:00', 'yyyy-MM-dd HH:mm:ss')─┐
│                                                           2025-01-04 23:00:00 │
└───────────────────────────────────────────────────────────────────────────────┘

```


## parseDateTimeOrNull


```
parseDateTimeOrNull(time_string, format[, timezone])

```

- `time_string` — Строка, преобразуемая в DateTime. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `format` — Строка формата, задающая способ разбора time_string. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `timezone` — Необязательный параметр. Часовой пояс. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT parseDateTimeOrNull('2025-01-04+23:00:00', '%Y-%m-%d+%H:%i:%s')

```


```
┌─parseDateTimeOrNull('2025-01-04+23:00:00', '%Y-%m-%d+%H:%i:%s')─┐
│                                            2025-01-04 23:00:00  │
└─────────────────────────────────────────────────────────────────┘

```


## parseDateTimeOrZero


```
parseDateTimeOrZero(time_string, format[, timezone])

```

- `time_string` — Строка для разбора в DateTime. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `format` — Строка формата, задающая способ разбора time_string. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `timezone` — Необязательно. Часовой пояс. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT parseDateTimeOrZero('2025-01-04+23:00:00', '%Y-%m-%d+%H:%i:%s')

```


```
┌─parseDateTimeOrZero('2025-01-04+23:00:00', '%Y-%m-%d+%H:%i:%s')─┐
│                                             2025-01-04 23:00:00 │
└─────────────────────────────────────────────────────────────────┘

```


## reinterpret


```
reinterpret(x, type)

```

- `x` — Значение для переинтерпретации. При переинтерпретации в `String` исходный `Array` должен состоять из непрерывно расположенных элементов фиксированного размера. [`Any`](https://clickhouse.com/docs/ru/reference/data-types/index)
- `type` — Целевой тип. Если это массив, тип его элементов должен иметь фиксированную длину. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT reinterpret(toInt8(-1), 'UInt8') AS int_to_uint,
    reinterpret(toInt8(1), 'Float32') AS int_to_float,
    reinterpret('1', 'UInt32') AS string_to_int

```


```
┌─int_to_uint─┬─int_to_float─┬─string_to_int─┐
│         255 │        1e-45 │            49 │
└─────────────┴──────────────┴───────────────┘

```


```
SELECT reinterpret(x'3108b4403108d4403108b4403108d440', 'Array(Float32)') AS string_to_array_of_Float32

```


```
┌─string_to_array_of_Float32─┐
│ [5.626,6.626,5.626,6.626]  │
└────────────────────────────┘

```


```
SELECT hex(reinterpret([toUInt8(1), toUInt8(2), toUInt8(255)]::Array(UInt8), 'String')) AS array_of_UInt8_to_string

```


```
┌─array_of_UInt8_to_string─┐
│ 0102FF                   │
└──────────────────────────┘

```


## reinterpretAsDate


```
reinterpretAsDate(x)

```

- `x` — Количество дней с начала эпохи Unix. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float), или [`Date`](https://clickhouse.com/docs/ru/reference/data-types/date), или [`DateTime`](https://clickhouse.com/docs/ru/reference/data-types/datetime), или [`UUID`](https://clickhouse.com/docs/ru/reference/data-types/uuid), или [`String`](https://clickhouse.com/docs/ru/reference/data-types/string), или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring)

```
SELECT reinterpretAsDate(65), reinterpretAsDate('A')

```


```
┌─reinterpretAsDate(65)─┬─reinterpretAsDate('A')─┐
│            1970-03-07 │             1970-03-07 │
└───────────────────────┴────────────────────────┘

```


## reinterpretAsDateTime


```
reinterpretAsDateTime(x)

```

- `x` — Число секунд с начала эпохи Unix. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`Date`](https://clickhouse.com/docs/ru/reference/data-types/date) или [`DateTime`](https://clickhouse.com/docs/ru/reference/data-types/datetime) или [`UUID`](https://clickhouse.com/docs/ru/reference/data-types/uuid) или [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring)

```
SELECT reinterpretAsDateTime(65), reinterpretAsDateTime('A')

```


```
┌─reinterpretAsDateTime(65)─┬─reinterpretAsDateTime('A')─┐
│       1970-01-01 01:01:05 │        1970-01-01 01:01:05 │
└───────────────────────────┴────────────────────────────┘

```


## reinterpretAsFixedString


```
reinterpretAsFixedString(x)

```

- `x` — значение, которое нужно переинтерпретировать в строку. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`Date`](https://clickhouse.com/docs/ru/reference/data-types/date) или [`DateTime`](https://clickhouse.com/docs/ru/reference/data-types/datetime)

```
SELECT
    reinterpretAsFixedString(toDateTime('1970-01-01 01:01:05')),
    reinterpretAsFixedString(toDate('1970-03-07'))

```


```
┌─reinterpretAsFixedString(toDateTime('1970-01-01 01:01:05'))─┬─reinterpretAsFixedString(toDate('1970-03-07'))─┐
│ A                                                           │ A                                              │
└─────────────────────────────────────────────────────────────┴────────────────────────────────────────────────┘

```


## reinterpretAsFloat32


```
reinterpretAsFloat32(x)

```

- `x` — Значение, переинтерпретируемое как Float32. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`Date`](https://clickhouse.com/docs/ru/reference/data-types/date) или [`DateTime`](https://clickhouse.com/docs/ru/reference/data-types/datetime) или [`UUID`](https://clickhouse.com/docs/ru/reference/data-types/uuid) или [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring)

```
SELECT reinterpretAsUInt32(toFloat32(0.2)) AS x, reinterpretAsFloat32(x)

```


```
┌──────────x─┬─reinterpretAsFloat32(x)─┐
│ 1045220557 │                     0.2 │
└────────────┴─────────────────────────┘

```


## reinterpretAsFloat64


```
reinterpretAsFloat64(x)

```

- `x` — Значение, переинтерпретируемое как Float64. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`Date`](https://clickhouse.com/docs/ru/reference/data-types/date) или [`DateTime`](https://clickhouse.com/docs/ru/reference/data-types/datetime) или [`UUID`](https://clickhouse.com/docs/ru/reference/data-types/uuid) или [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring)

```
SELECT reinterpretAsUInt64(toFloat64(0.2)) AS x, reinterpretAsFloat64(x)

```


```
┌───────────────────x─┬─reinterpretAsFloat64(x)─┐
│ 4596373779694328218 │                     0.2 │
└─────────────────────┴─────────────────────────┘

```


## reinterpretAsInt128


```
reinterpretAsInt128(x)

```

- `x` — Значение, переинтерпретируемое как Int128. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`Date`](https://clickhouse.com/docs/ru/reference/data-types/date) или [`DateTime`](https://clickhouse.com/docs/ru/reference/data-types/datetime) или [`UUID`](https://clickhouse.com/docs/ru/reference/data-types/uuid) или [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring)

```
SELECT
    toInt64(257) AS x,
    toTypeName(x),
    reinterpretAsInt128(x) AS res,
    toTypeName(res)

```


```
┌───x─┬─toTypeName(x)─┬─res─┬─toTypeName(res)─┐
│ 257 │ Int64         │ 257 │ Int128          │
└─────┴───────────────┴─────┴─────────────────┘

```


## reinterpretAsInt16


```
reinterpretAsInt16(x)

```

- `x` — Значение, переинтерпретируемое как Int16. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`Date`](https://clickhouse.com/docs/ru/reference/data-types/date) или [`DateTime`](https://clickhouse.com/docs/ru/reference/data-types/datetime) или [`UUID`](https://clickhouse.com/docs/ru/reference/data-types/uuid) или [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring)

```
SELECT
    toInt8(257) AS x,
    toTypeName(x),
    reinterpretAsInt16(x) AS res,
    toTypeName(res)

```


```
┌─x─┬─toTypeName(x)─┬─res─┬─toTypeName(res)─┐
│ 1 │ Int8          │   1 │ Int16           │
└───┴───────────────┴─────┴─────────────────┘

```


## reinterpretAsInt256


```
reinterpretAsInt256(x)

```

- `x` — Значение для переинтерпретации в Int256. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`Date`](https://clickhouse.com/docs/ru/reference/data-types/date) или [`DateTime`](https://clickhouse.com/docs/ru/reference/data-types/datetime) или [`UUID`](https://clickhouse.com/docs/ru/reference/data-types/uuid) или [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring)

```
SELECT
    toInt128(257) AS x,
    toTypeName(x),
    reinterpretAsInt256(x) AS res,
    toTypeName(res)

```


```
┌───x─┬─toTypeName(x)─┬─res─┬─toTypeName(res)─┐
│ 257 │ Int128        │ 257 │ Int256          │
└─────┴───────────────┴─────┴─────────────────┘

```


## reinterpretAsInt32


```
reinterpretAsInt32(x)

```

- `x` — Значение, которое нужно реинтерпретировать как Int32. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`Date`](https://clickhouse.com/docs/ru/reference/data-types/date) или [`DateTime`](https://clickhouse.com/docs/ru/reference/data-types/datetime) или [`UUID`](https://clickhouse.com/docs/ru/reference/data-types/uuid) или [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring)

```
SELECT
    toInt16(257) AS x,
    toTypeName(x),
    reinterpretAsInt32(x) AS res,
    toTypeName(res)

```


```
┌───x─┬─toTypeName(x)─┬─res─┬─toTypeName(res)─┐
│ 257 │ Int16         │ 257 │ Int32           │
└─────┴───────────────┴─────┴─────────────────┘

```


## reinterpretAsInt64


```
reinterpretAsInt64(x)

```

- `x` — значение, которое нужно переинтерпретировать как Int64. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`Date`](https://clickhouse.com/docs/ru/reference/data-types/date) или [`DateTime`](https://clickhouse.com/docs/ru/reference/data-types/datetime) или [`UUID`](https://clickhouse.com/docs/ru/reference/data-types/uuid) или [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring)

```
SELECT
    toInt32(257) AS x,
    toTypeName(x),
    reinterpretAsInt64(x) AS res,
    toTypeName(res)

```


```
┌───x─┬─toTypeName(x)─┬─res─┬─toTypeName(res)─┐
│ 257 │ Int32         │ 257 │ Int64           │
└─────┴───────────────┴─────┴─────────────────┘

```


## reinterpretAsInt8


```
reinterpretAsInt8(x)

```

- `x` — значение для переинтерпретации как Int8. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) or [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) or [`Date`](https://clickhouse.com/docs/ru/reference/data-types/date) or [`DateTime`](https://clickhouse.com/docs/ru/reference/data-types/datetime) or [`UUID`](https://clickhouse.com/docs/ru/reference/data-types/uuid) or [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) or [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring)

```
SELECT
    toUInt8(257) AS x,
    toTypeName(x),
    reinterpretAsInt8(x) AS res,
    toTypeName(res)

```


```
┌─x─┬─toTypeName(x)─┬─res─┬─toTypeName(res)─┐
│ 1 │ UInt8         │   1 │ Int8            │
└───┴───────────────┴─────┴─────────────────┘

```


## reinterpretAsString


```
reinterpretAsString(x)

```

- `x` — Значение, которое нужно переинтерпретировать в строку. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`Date`](https://clickhouse.com/docs/ru/reference/data-types/date) или [`DateTime`](https://clickhouse.com/docs/ru/reference/data-types/datetime) или [`Array`](https://clickhouse.com/docs/ru/reference/data-types/array)

```
SELECT
    reinterpretAsString(toDateTime('1970-01-01 01:01:05')),
    reinterpretAsString(toDate('1970-03-07'))

```


```
┌─reinterpretAsString(toDateTime('1970-01-01 01:01:05'))─┬─reinterpretAsString(toDate('1970-03-07'))─┐
│ A                                                      │ A                                         │
└────────────────────────────────────────────────────────┴───────────────────────────────────────────┘

```


```
SELECT hex(reinterpretAsString([toUInt8(1), toUInt8(2), toUInt8(255)]::Array(UInt8))) AS array_of_UInt8_to_string

```


```
┌─array_of_UInt8_to_string─┐
│ 0102FF                   │
└──────────────────────────┘

```


## reinterpretAsUInt128


```
reinterpretAsUInt128(x)

```

- `x` — Значение, которое нужно переинтерпретировать как UInt128. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`Date`](https://clickhouse.com/docs/ru/reference/data-types/date) или [`DateTime`](https://clickhouse.com/docs/ru/reference/data-types/datetime) или [`UUID`](https://clickhouse.com/docs/ru/reference/data-types/uuid) или [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring)

```
SELECT
    toUInt64(257) AS x,
    toTypeName(x),
    reinterpretAsUInt128(x) AS res,
    toTypeName(res)

```


```
┌───x─┬─toTypeName(x)─┬─res─┬─toTypeName(res)─┐
│ 257 │ UInt64        │ 257 │ UInt128         │
└─────┴───────────────┴─────┴─────────────────┘

```


## reinterpretAsUInt16


```
reinterpretAsUInt16(x)

```

- `x` — Значение, которое нужно переинтерпретировать как UInt16. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`Date`](https://clickhouse.com/docs/ru/reference/data-types/date) или [`DateTime`](https://clickhouse.com/docs/ru/reference/data-types/datetime) или [`UUID`](https://clickhouse.com/docs/ru/reference/data-types/uuid) или [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring)

```
SELECT
    toUInt8(257) AS x,
    toTypeName(x),
    reinterpretAsUInt16(x) AS res,
    toTypeName(res)

```


```
┌─x─┬─toTypeName(x)─┬─res─┬─toTypeName(res)─┐
│ 1 │ UInt8         │   1 │ UInt16          │
└───┴───────────────┴─────┴─────────────────┘

```


## reinterpretAsUInt256


```
reinterpretAsUInt256(x)

```

- `x` — значение, которое нужно переинтерпретировать как UInt256. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`Date`](https://clickhouse.com/docs/ru/reference/data-types/date) или [`DateTime`](https://clickhouse.com/docs/ru/reference/data-types/datetime) или [`UUID`](https://clickhouse.com/docs/ru/reference/data-types/uuid) или [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring)

```
SELECT
    toUInt128(257) AS x,
    toTypeName(x),
    reinterpretAsUInt256(x) AS res,
    toTypeName(res)

```


```
┌───x─┬─toTypeName(x)─┬─res─┬─toTypeName(res)─┐
│ 257 │ UInt128       │ 257 │ UInt256         │
└─────┴───────────────┴─────┴─────────────────┘

```


## reinterpretAsUInt32


```
reinterpretAsUInt32(x)

```

- `x` — Значение, которое нужно реинтерпретировать как UInt32. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`Date`](https://clickhouse.com/docs/ru/reference/data-types/date) или [`DateTime`](https://clickhouse.com/docs/ru/reference/data-types/datetime) или [`UUID`](https://clickhouse.com/docs/ru/reference/data-types/uuid) или [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring)

```
SELECT
    toUInt16(257) AS x,
    toTypeName(x),
    reinterpretAsUInt32(x) AS res,
    toTypeName(res)

```


```
┌───x─┬─toTypeName(x)─┬─res─┬─toTypeName(res)─┐
│ 257 │ UInt16        │ 257 │ UInt32          │
└─────┴───────────────┴─────┴─────────────────┘

```


## reinterpretAsUInt64


```
reinterpretAsUInt64(x)

```

- `x` — Значение, которое нужно переинтерпретировать как UInt64. [`Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`UInt*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`Date`](https://clickhouse.com/docs/ru/reference/data-types/date) или [`DateTime`](https://clickhouse.com/docs/ru/reference/data-types/datetime) или [`UUID`](https://clickhouse.com/docs/ru/reference/data-types/uuid) или [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring)

```
SELECT
    toUInt32(257) AS x,
    toTypeName(x),
    reinterpretAsUInt64(x) AS res,
    toTypeName(res)

```


```
┌───x─┬─toTypeName(x)─┬─res─┬─toTypeName(res)─┐
│ 257 │ UInt32        │ 257 │ UInt64          │
└─────┴───────────────┴─────┴─────────────────┘

```


## reinterpretAsUInt8


```
reinterpretAsUInt8(x)

```

- `x` — Значение, которое нужно переинтерпретировать как UInt8. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`Date`](https://clickhouse.com/docs/ru/reference/data-types/date) или [`DateTime`](https://clickhouse.com/docs/ru/reference/data-types/datetime) или [`UUID`](https://clickhouse.com/docs/ru/reference/data-types/uuid) или [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring)

```
SELECT
    toInt8(-1) AS val,
    toTypeName(val),
    reinterpretAsUInt8(val) AS res,
    toTypeName(res);

```


```
┌─val─┬─toTypeName(val)─┬─res─┬─toTypeName(res)─┐
│  -1 │ Int8            │ 255 │ UInt8           │
└─────┴─────────────────┴─────┴─────────────────┘

```


## reinterpretAsUUID


```
reinterpretAsUUID(fixed_string)

```

- `fixed_string` — Байтовая строка в формате big-endian. [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring)

```
SELECT reinterpretAsUUID(reverse(unhex('000102030405060708090a0b0c0d0e0f')))

```


```
┌─reinterpretAsUUID(reverse(unhex('000102030405060708090a0b0c0d0e0f')))─┐
│                                  08090a0b-0c0d-0e0f-0001-020304050607 │
└───────────────────────────────────────────────────────────────────────┘

```


## toBFloat16

- [`toBFloat16OrZero`](#toBFloat16OrZero).
- [`toBFloat16OrNull`](#toBFloat16OrNull).

```
toBFloat16(expr)

```

- `expr` — выражение, возвращающее число или строковое представление числа. [`Выражение`](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/expression)

```
SELECT
toBFloat16(toFloat32(42.7)),
toBFloat16(toFloat32('42.7')),
toBFloat16('42.7')
FORMAT Vertical;

```


```
toBFloat16(toFloat32(42.7)): 42.5
toBFloat16(t⋯32('42.7')):    42.5
toBFloat16('42.7'):          42.5

```


## toBFloat16OrNull

- Строковые представления числовых значений.
- Строковые представления двоичных и шестнадцатеричных значений.
- Числовые значения.
- [`toBFloat16`](#toBFloat16).
- [`toBFloat16OrZero`](#toBFloat16OrZero).

```
toBFloat16OrNull(x)

```

- `x` — Строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT toBFloat16OrNull('0x5E'), -- unsupported arguments
       toBFloat16OrNull('12.3'), -- typical use
       toBFloat16OrNull('12.3456789') -- silent loss of precision

```


```
\N
12.25
12.3125

```


## toBFloat16OrZero

- Строковые представления числовых значений.
- Строковые представления двоичных и шестнадцатеричных значений.
- Числовые значения.
- [`toBFloat16`](#toBFloat16).
- [`toBFloat16OrNull`](#toBFloat16OrNull).

```
toBFloat16OrZero(x)

```

- `x` — Строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT toBFloat16OrZero('0x5E'), -- unsupported arguments
       toBFloat16OrZero('12.3'), -- typical use
       toBFloat16OrZero('12.3456789') -- silent loss of precision

```


```
0
12.25
12.3125

```


## toBool


```
toBool(expr)

```

- `expr` — выражение, возвращающее число или строку. Для строк принимает значения ‘true’ или ‘false’ (регистронезависимо). [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`Expression`](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/expression)

```
SELECT
    toBool(toUInt8(1)),
    toBool(toInt8(-1)),
    toBool(toFloat32(1.01)),
    toBool('true'),
    toBool('false'),
    toBool('FALSE')
FORMAT Vertical

```


```
toBool(toUInt8(1)):      true
toBool(toInt8(-1)):      true
toBool(toFloat32(1.01)): true
toBool('true'):          true
toBool('false'):         false
toBool('FALSE'):         false

```


## toDate


```
toDate(x)

```

- `x` — Входное значение для преобразования. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring) или [`DateTime`](https://clickhouse.com/docs/ru/reference/data-types/datetime) или [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float)

```
SELECT toDate('2025-04-15')

```


```
2025-04-15

```


```
SELECT toDate(toDateTime('2025-04-15 10:30:00'))

```


```
2025-04-15

```


```
SELECT toDate(20297)

```


```
2025-07-28

```


## toDate32


```
toDate32(expr)

```

- `expr` — значение для преобразования. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string), [`UInt32`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Date`](https://clickhouse.com/docs/ru/reference/data-types/date)

```
SELECT toDate32('2025-01-01') AS value, toTypeName(value)
FORMAT Vertical

```


```
Строка 1:
──────
value:           2025-01-01
toTypeName(value): Date32

```


```
SELECT toDate32('1899-01-01') AS value, toTypeName(value)
FORMAT Vertical

```


```
Строка 1:
──────
value:           1900-01-01
toTypeName(value): Date32

```


## toDate32OrDefault


```
toDate32OrDefault(expr[, default])

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float)
- `default` — Необязательно. Значение по умолчанию, возвращаемое, если преобразование не удалось. [`Date32`](https://clickhouse.com/docs/ru/reference/data-types/date32)

```
SELECT toDate32OrDefault('1930-01-01', toDate32('2020-01-01'))

```


```
1930-01-01

```


```
SELECT toDate32OrDefault('xx1930-01-01', toDate32('2020-01-01'))

```


```
2020-01-01

```


## toDate32OrNull


```
toDate32OrNull(x)

```

- `x` — строковое представление даты. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT toDate32OrNull('2025-01-01'), toDate32OrNull('invalid')

```


```
┌─toDate32OrNull('2025-01-01')─┬─toDate32OrNull('invalid')─┐
│                   2025-01-01 │                      ᴺᵁᴸᴸ │
└──────────────────────────────┴───────────────────────────┘

```


## toDate32OrZero

- [`toDate32`](#toDate32)
- [`toDate32OrNull`](#toDate32OrNull)
- [`toDate32OrDefault`](#toDate32OrDefault)

```
toDate32OrZero(x)

```

- `x` — строковое представление даты. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT toDate32OrZero('2025-01-01'), toDate32OrZero('')

```


```
┌─toDate32OrZero('2025-01-01')─┬─toDate32OrZero('')─┐
│                   2025-01-01 │         1900-01-01 │
└──────────────────────────────┴────────────────────┘

```


## toDateOrDefault


```
toDateOrDefault(expr[, default])

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float)
- `default` — Необязательно. Значение по умолчанию, которое возвращается, если разбор завершился неуспешно. [`Date`](https://clickhouse.com/docs/ru/reference/data-types/date)

```
SELECT toDateOrDefault('2022-12-30')

```


```
2022-12-30

```


```
SELECT toDateOrDefault('', CAST('2023-01-01', 'Date'))

```


```
2023-01-01

```


## toDateOrNull


```
toDateOrNull(x)

```

- `x` — Строковое представление даты, либо целое число дней, либо Unix-временная метка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`(U)Int8/16/32/64`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT toDateOrNull('2025-12-30'), toDateOrNull('invalid')

```


```
┌─toDateOrNull('2025-12-30')─┬─toDateOrNull('invalid')─┐
│                 2025-12-30 │                    ᴺᵁᴸᴸ │
└────────────────────────────┴─────────────────────────┘

```


## toDateOrZero

- [`toDate`](#toDate)
- [`toDateOrNull`](#toDateOrNull)
- [`toDateOrDefault`](#toDateOrDefault)

```
toDateOrZero(x)

```

- `x` — строковое представление даты. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT toDateOrZero('2025-12-30'), toDateOrZero('')

```


```
┌─toDateOrZero('2025-12-30')─┬─toDateOrZero('')─┐
│                 2025-12-30 │       1970-01-01 │
└────────────────────────────┴──────────────────┘

```


## toDateTime


```
toDateTime(expr[, time_zone])

```

- `expr` — Значение. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`Int`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Date`](https://clickhouse.com/docs/ru/reference/data-types/date) или [`DateTime`](https://clickhouse.com/docs/ru/reference/data-types/datetime)
- `time_zone` — Часовой пояс. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT toDateTime('2025-01-01 00:00:00'), toDateTime(1735689600, 'UTC')
FORMAT Vertical

```


```
Row 1:
──────
toDateTime('2025-01-01 00:00:00'): 2025-01-01 00:00:00
toDateTime(1735689600, 'UTC'):     2025-01-01 00:00:00

```


## toDateTime32


```
toDateTime32(x[, timezone])

```

- `x` — Входное значение, которое нужно преобразовать. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring) или [`UInt*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`Date`](https://clickhouse.com/docs/ru/reference/data-types/date) или [`DateTime`](https://clickhouse.com/docs/ru/reference/data-types/datetime) или [`DateTime64`](https://clickhouse.com/docs/ru/reference/data-types/datetime64)
- `timezone` — Необязательно. Часовой пояс для возвращаемого значения `DateTime`. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT toDateTime64('2025-01-01 00:00:00.000', 3) AS value, toTypeName(value);

```


```
┌───────────────────value─┬─toTypeName(value)─┐
│ 2025-01-01 00:00:00.000 │ DateTime64(3)     │
└─────────────────────────┴───────────────────┘

```


```
SELECT toDateTime64(1735689600.000, 3) AS value, toTypeName(value);
-- without the decimal point the value is still treated as Unix Timestamp in seconds
SELECT toDateTime64(1546300800000, 3) AS value, toTypeName(value);

```


```
┌───────────────────value─┬─toTypeName(value)─┐
│ 2025-01-01 00:00:00.000 │ DateTime64(3)     │
└─────────────────────────┴───────────────────┘
┌───────────────────value─┬─toTypeName(value)─┐
│ 2299-12-31 23:59:59.000 │ DateTime64(3)     │
└─────────────────────────┴───────────────────┘

```


```
SELECT toDateTime64('2025-01-01 00:00:00', 3, 'Asia/Istanbul') AS value, toTypeName(value);

```


```
┌───────────────────value─┬─toTypeName(toDateTime64('2025-01-01 00:00:00', 3, 'Asia/Istanbul'))─┐
│ 2025-01-01 00:00:00.000 │ DateTime64(3, 'Asia/Istanbul')                                      │
└─────────────────────────┴─────────────────────────────────────────────────────────────────────┘

```


## toDateTime64


```
toDateTime64(expr, scale[, timezone])

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`Выражение`](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/expression)
- `scale` — Размер тика (precision): 10^(-scale) секунд. [`UInt8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `timezone` — Необязательно. Часовой пояс для указанного объекта `DateTime64`. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT toDateTime64('2025-01-01 00:00:00.000', 3) AS value, toTypeName(value);

```


```
┌───────────────────value─┬─toTypeName(toDateTime64('2025-01-01 00:00:00.000', 3))─┐
│ 2025-01-01 00:00:00.000 │ DateTime64(3)                                          │
└─────────────────────────┴────────────────────────────────────────────────────────┘

```


```
SELECT toDateTime64(1546300800.000, 3) AS value, toTypeName(value);
-- Без десятичной точки значение по-прежнему интерпретируется как Unix-временная метка в секундах
SELECT toDateTime64(1546300800000, 3) AS value, toTypeName(value);

```


```
┌───────────────────value─┬─toTypeName(toDateTime64(1546300800000, 3))─┐
│ 2282-12-31 00:00:00.000 │ DateTime64(3)                              │
└─────────────────────────┴────────────────────────────────────────────┘

```


```
SELECT toDateTime64('2025-01-01 00:00:00', 3, 'Asia/Istanbul') AS value, toTypeName(value);

```


```
┌───────────────────value─┬─toTypeName(toDateTime64('2025-01-01 00:00:00', 3, 'Asia/Istanbul'))─┐
│ 2025-01-01 00:00:00.000 │ DateTime64(3, 'Asia/Istanbul')                                      │
└─────────────────────────┴─────────────────────────────────────────────────────────────────────┘

```


## toDateTime64OrDefault


```
toDateTime64OrDefault(expr, scale[, timezone, default])

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float)
- `scale` — Размер тика (precision): 10^-precision секунд. [`UInt8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `timezone` — Необязательно. Часовой пояс. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `default` — Необязательно. Значение по умолчанию, которое возвращается, если разбор завершился неудачно. [`DateTime64`](https://clickhouse.com/docs/ru/reference/data-types/datetime64)

```
SELECT toDateTime64OrDefault('1976-10-18 00:00:00.30', 3)

```


```
1976-10-18 00:00:00.300

```


```
SELECT toDateTime64OrDefault('1976-10-18 00:00:00 30', 3, 'UTC', toDateTime64('2001-01-01 00:00:00.00',3))

```


```
2000-12-31 23:00:00.000

```


## toDateTime64OrNull


```
toDateTime64OrNull(x[, precision[, timezone]])

```

- `x` — строковое представление даты и времени с субсекундной точностью или целочисленная Unix-временная метка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`(U)Int8/16/32/64`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `precision` — необязательно. Субсекундная точность возвращаемого значения. [`UInt8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `timezone` — необязательно. Часовой пояс возвращаемого значения. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT toDateTime64OrNull('2025-12-30 13:44:17.123'), toDateTime64OrNull('invalid')

```


```
┌─toDateTime64OrNull('2025-12-30 13:44:17.123')─┬─toDateTime64OrNull('invalid')─┐
│                       2025-12-30 13:44:17.123 │                          ᴺᵁᴸᴸ │
└───────────────────────────────────────────────┴───────────────────────────────┘

```


## toDateTime64OrZero

- [toDateTime64](#toDateTime64).
- [toDateTime64OrNull](#toDateTime64OrNull).
- [toDateTime64OrDefault](#toDateTime64OrDefault).

```
toDateTime64OrZero(x)

```

- `x` — Строковое представление даты и времени с субсекундной точностью. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT toDateTime64OrZero('2025-12-30 13:44:17.123'), toDateTime64OrZero('invalid')

```


```
┌─toDateTime64OrZero('2025-12-30 13:44:17.123')─┬─toDateTime64OrZero('invalid')─┐
│                       2025-12-30 13:44:17.123 │       1970-01-01 00:00:00.000 │
└───────────────────────────────────────────────┴───────────────────────────────┘

```


## toDateTimeOrDefault


```
toDateTimeOrDefault(expr[, timezone, default])

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint), или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float)
- `timezone` — Необязательно. Часовой пояс. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `default` — Необязательно. Значение по умолчанию, которое возвращается, если разбор завершился неуспешно. [`DateTime`](https://clickhouse.com/docs/ru/reference/data-types/datetime)

```
SELECT toDateTimeOrDefault('2022-12-30 13:44:17')

```


```
2022-12-30 13:44:17

```


```
SELECT toDateTimeOrDefault('', 'UTC', CAST('2023-01-01', 'DateTime(\'UTC\')'))

```


```
2023-01-01 00:00:00

```


## toDateTimeOrNull


```
toDateTimeOrNull(x[, timezone])

```

- `x` — Строковое представление даты и времени или целочисленная Unix-временная метка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`(U)Int8/16/32/64`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `timezone` — Необязательно. Часовой пояс возвращаемого значения. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT toDateTimeOrNull('2025-12-30 13:44:17'), toDateTimeOrNull('invalid')

```


```
┌─toDateTimeOrNull('2025-12-30 13:44:17')─┬─toDateTimeOrNull('invalid')─┐
│                     2025-12-30 13:44:17 │                        ᴺᵁᴸᴸ │
└─────────────────────────────────────────┴─────────────────────────────┘

```


```
SELECT toDateTimeOrNull(1583851242, 'Asia/Shanghai'), toDateTimeOrNull(4294967296)

```


```
┌─toDateTimeOrNull(1583851242, 'Asia/Shanghai')─┬─toDateTimeOrNull(4294967296)─┐
│                           2020-03-10 22:40:42 │                         ᴺᵁᴸᴸ │
└───────────────────────────────────────────────┴──────────────────────────────┘

```


## toDateTimeOrZero


```
toDateTimeOrZero(x)

```

- `x` — Строковое представление даты и времени. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT toDateTimeOrZero('2025-12-30 13:44:17'), toDateTimeOrZero('invalid')

```


```
┌─toDateTimeOrZero('2025-12-30 13:44:17')─┬─toDateTimeOrZero('invalid')─┐
│                     2025-12-30 13:44:17 │         1970-01-01 00:00:00 │
└─────────────────────────────────────────┴─────────────────────────────┘

```


## toDecimal128

- Значения или строковые представления типа (U)Int*.
- Значения или строковые представления типа Float*.
- Значения Float* `NaN` и `Inf` или их строковые представления (регистронезависимо).
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toDecimal128('0xc0fe', 1);`.

```
toDecimal128(expr, S)

```

- `expr` — выражение, возвращающее число или строковое представление числа. [`Expression`](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/expression)
- `S` — параметр scale в диапазоне от 0 до 38, задающий, сколько цифр может быть в дробной части числа. [`UInt8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT
    toDecimal128(99, 1) AS a, toTypeName(a) AS type_a,
    toDecimal128(99.67, 2) AS b, toTypeName(b) AS type_b,
    toDecimal128('99.67', 3) AS c, toTypeName(c) AS type_c
FORMAT Vertical

```


```
Row 1:
──────
a:      99
type_a: Decimal(38, 1)
b:      99.67
type_b: Decimal(38, 2)
c:      99.67
type_c: Decimal(38, 3)

```


## toDecimal128OrDefault


```
toDecimal128OrDefault(expr, S[, default])

```

- `expr` — Строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `S` — Параметр scale в диапазоне от 0 до 38, который указывает, сколько цифр может содержать дробная часть числа. [`UInt8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `default` — Необязательно. Значение по умолчанию, возвращаемое, если преобразование в тип Decimal128(S) завершается неуспешно. [`Decimal128(S)`](https://clickhouse.com/docs/ru/reference/data-types/decimal)

```
SELECT toDecimal128OrDefault(toString(1/42), 18)

```


```
0.023809523809523808

```


```
SELECT toDecimal128OrDefault('Inf', 0, CAST('-1', 'Decimal128(0)'))

```


```
-1

```


## toDecimal128OrNull

- Значения или строковые представления типа (U)Int*.
- Значения или строковые представления типа Float*.
- Значения или строковые представления значений Float* `NaN` и `Inf` (регистронезависимо).
- Строковые представления двоичных и шестнадцатеричных значений.
- Значения, выходящие за пределы `Decimal128`: `(-1*10^(38 - S), 1*10^(38 - S))`.
- [`toDecimal128`](#toDecimal128).
- [`toDecimal128OrZero`](#toDecimal128OrZero).
- [`toDecimal128OrDefault`](#toDecimal128OrDefault).

```
toDecimal128OrNull(expr, S)

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`Expression`](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/expression)
- `S` — Параметр scale в диапазоне от 0 до 38, задающий, сколько цифр может содержать дробная часть числа. [`UInt8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT toDecimal128OrNull('42.7', 2), toDecimal128OrNull('invalid', 2)

```


```
┌─toDecimal128OrNull('42.7', 2)─┬─toDecimal128OrNull('invalid', 2)─┐
│                         42.70 │                             ᴺᵁᴸᴸ │
└───────────────────────────────┴──────────────────────────────────┘

```


## toDecimal128OrZero

- Значения или строковые представления типа (U)Int*.
- Значения или строковые представления типа Float*.
- Значения Float* `NaN` и `Inf` или их строковые представления (регистронезависимо).
- Строковые представления двоичных и шестнадцатеричных значений.

```
toDecimal128OrZero(expr, S)

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`Expression`](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/expression)
- `S` — параметр scale в диапазоне от 0 до 38, который задаёт, сколько цифр может быть в дробной части числа. [`UInt8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT toDecimal128OrZero('42.7', 2), toDecimal128OrZero('invalid', 2)

```


```
┌─toDecimal128OrZero('42.7', 2)─┬─toDecimal128OrZero('invalid', 2)─┐
│                         42.70 │                             0.00 │
└───────────────────────────────┴──────────────────────────────────┘

```


## toDecimal256

- Значения или строковые представления типа (U)Int*.
- Значения или строковые представления типа Float*.
- Значения или строковые представления значений Float* `NaN` и `Inf` (регистронезависимо).
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toDecimal256('0xc0fe', 1);`.

```
toDecimal256(expr, S)

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`Expression`](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/expression)
- `S` — параметр scale от 0 до 76, задающий, сколько знаков может быть в дробной части числа. [`UInt8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT
    toDecimal256(99, 1) AS a, toTypeName(a) AS type_a,
    toDecimal256(99.67, 2) AS b, toTypeName(b) AS type_b,
    toDecimal256('99.67', 3) AS c, toTypeName(c) AS type_c
FORMAT Vertical

```


```
Row 1:
──────
a:      99
type_a: Decimal(76, 1)
b:      99.67
type_b: Decimal(76, 2)
c:      99.67
type_c: Decimal(76, 3)

```


## toDecimal256OrDefault


```
toDecimal256OrDefault(expr, S[, default])

```

- `expr` — Строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `S` — Параметр scale в диапазоне от 0 до 76, задающий, сколько цифр может быть в дробной части числа. [`UInt8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `default` — Необязательно. Значение по умолчанию, которое возвращается, если разбор в тип Decimal256(S) завершается неуспешно. [`Decimal256(S)`](https://clickhouse.com/docs/ru/reference/data-types/decimal)

```
SELECT toDecimal256OrDefault(toString(1/42), 76)

```


```
0.023809523809523808

```


```
SELECT toDecimal256OrDefault('Inf', 0, CAST('-1', 'Decimal256(0)'))

```


```
-1

```


## toDecimal256OrNull

- Значения или строковые представления типа (U)Int*.
- Значения или строковые представления типа Float*.
- Значения Float* `NaN` и `Inf`, а также их строковые представления (регистронезависимо).
- Строковые представления двоичных и шестнадцатеричных значений.
- Значения, выходящие за пределы `Decimal256`: `(-1 * 10^(76 - S), 1 * 10^(76 - S))`.
- [`toDecimal256`](#toDecimal256).
- [`toDecimal256OrZero`](#toDecimal256OrZero).
- [`toDecimal256OrDefault`](#toDecimal256OrDefault).

```
toDecimal256OrNull(expr, S)

```

- `expr` — выражение, возвращающее число или строковое представление числа. [`Выражение`](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/expression)
- `S` — параметр scale в диапазоне от 0 до 76, задающий, сколько цифр может быть в дробной части числа. [`UInt8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT toDecimal256OrNull('42.7', 2), toDecimal256OrNull('invalid', 2)

```


```
┌─toDecimal256OrNull('42.7', 2)─┬─toDecimal256OrNull('invalid', 2)─┐
│                         42.70 │                             ᴺᵁᴸᴸ │
└───────────────────────────────┴──────────────────────────────────┘

```


## toDecimal256OrZero

- Значения или строковые представления типа (U)Int*.
- Значения или строковые представления типа Float*.
- Значения или строковые представления значений Float* `NaN` и `Inf` (регистронезависимо).
- Строковые представления двоичных и шестнадцатеричных значений.
- [`toDecimal256`](#toDecimal256).
- [`toDecimal256OrNull`](#toDecimal256OrNull).
- [`toDecimal256OrDefault`](#toDecimal256OrDefault).

```
toDecimal256OrZero(expr, S)

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`Expression`](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/expression)
- `S` — Параметр scale в диапазоне от 0 до 76, задающий количество цифр в дробной части числа. [`UInt8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT toDecimal256OrZero('42.7', 2), toDecimal256OrZero('invalid', 2)

```


```
┌─toDecimal256OrZero('42.7', 2)─┬─toDecimal256OrZero('invalid', 2)─┐
│                         42.70 │                             0.00 │
└───────────────────────────────┴──────────────────────────────────┘

```


## toDecimal32

- Значения или строковые представления типа (U)Int*.
- Значения или строковые представления типа Float*.
- Значения или строковые представления значений Float* `NaN` и `Inf` (регистронезависимо).
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toDecimal32('0xc0fe', 1);`.

```
toDecimal32(expr, S)

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`Expression`](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/expression)
- `S` — Параметр scale в диапазоне от 0 до 9, указывающий, сколько цифр может быть в дробной части числа. [`UInt8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT
    toDecimal32(2, 1) AS a, toTypeName(a) AS type_a,
    toDecimal32(4.2, 2) AS b, toTypeName(b) AS type_b,
    toDecimal32('4.2', 3) AS c, toTypeName(c) AS type_c
FORMAT Vertical

```


```
Row 1:
──────
a:      2
type_a: Decimal(9, 1)
b:      4.2
type_b: Decimal(9, 2)
c:      4.2
type_c: Decimal(9, 3)

```


## toDecimal32OrDefault


```
toDecimal32OrDefault(expr, S[, default])

```

- `expr` — Строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `S` — Параметр масштаба от 0 до 9, задающий, сколько цифр может быть в дробной части числа. [`UInt8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `default` — Необязательно. Значение по умолчанию, которое возвращается, если не удалось выполнить разбор в тип Decimal32(S). [`Decimal32(S)`](https://clickhouse.com/docs/ru/reference/data-types/decimal)

```
SELECT toDecimal32OrDefault(toString(0.0001), 5)

```


```
0.0001

```


```
SELECT toDecimal32OrDefault('Inf', 0, CAST('-1', 'Decimal32(0)'))

```


```
-1

```


## toDecimal32OrNull

- Значения или строковые представления типа (U)Int*.
- Значения или строковые представления типа Float*.
- Значения или строковые представления значений Float* `NaN` и `Inf` (регистронезависимо).
- Строковые представления двоичных и шестнадцатеричных значений.
- Значения, выходящие за границы `Decimal32`:`(-1*10^(9 - S), 1*10^(9 - S))`.
- [`toDecimal32`](#toDecimal32).
- [`toDecimal32OrZero`](#toDecimal32OrZero).
- [`toDecimal32OrDefault`](#toDecimal32OrDefault).

```
toDecimal32OrNull(expr, S)

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`Выражение`](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/expression)
- `S` — параметр масштаба в диапазоне от 0 до 9, задающий, сколько цифр может быть в дробной части числа. [`UInt8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT toDecimal32OrNull('42.7', 2), toDecimal32OrNull('invalid', 2)

```


```
┌─toDecimal32OrNull('42.7', 2)─┬─toDecimal32OrNull('invalid', 2)─┐
│                        42.70 │                            ᴺᵁᴸᴸ │
└──────────────────────────────┴─────────────────────────────────┘

```


## toDecimal32OrZero

- Значения или строковые представления типа (U)Int*.
- Значения или строковые представления типа Float*.
- Значения или строковые представления значений Float* `NaN` и `Inf` (регистронезависимые).
- Строковые представления двоичных и шестнадцатеричных значений.

```
toDecimal32OrZero(expr, S)

```

- `expr` — Выражение, возвращающее число или его строковое представление. [`Выражение`](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/expression)
- `S` — параметр масштаба со значением от 0 до 9, задающий, сколько цифр может быть в дробной части числа. [`UInt8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT toDecimal32OrZero('42.7', 2), toDecimal32OrZero('invalid', 2)

```


```
┌─toDecimal32OrZero('42.7', 2)─┬─toDecimal32OrZero('invalid', 2)─┐
│                        42.70 │                            0.00 │
└──────────────────────────────┴─────────────────────────────────┘

```


## toDecimal64

- Значения или строковые представления типа (U)Int*.
- Значения или строковые представления типа Float*.
- Значения или строковые представления значений Float* `NaN` и `Inf` (регистронезависимо).
- Строковые представления бинарных и шестнадцатеричных значений, например `SELECT toDecimal64('0xc0fe', 1);`.

```
toDecimal64(expr, S)

```

- `expr` — Выражение, возвращающее число или его строковое представление. [`Выражение`](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/expression)
- `S` — параметр масштаба от 0 до 18, указывающий, сколько цифр может быть в дробной части числа. [`UInt8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT
    toDecimal64(2, 1) AS a, toTypeName(a) AS type_a,
    toDecimal64(4.2, 2) AS b, toTypeName(b) AS type_b,
    toDecimal64('4.2', 3) AS c, toTypeName(c) AS type_c
FORMAT Vertical

```


```
Row 1:
──────
a:      2.0
type_a: Decimal(18, 1)
b:      4.20
type_b: Decimal(18, 2)
c:      4.200
type_c: Decimal(18, 3)

```


## toDecimal64OrDefault


```
toDecimal64OrDefault(expr, S[, default])

```

- `expr` — Строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `S` — Параметр масштаба в диапазоне от 0 до 18, задающий, сколько цифр может содержать дробная часть числа. [`UInt8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `default` — Необязательно. Значение по умолчанию, которое возвращается, если преобразование в тип Decimal64(S) не удалось. [`Decimal64(S)`](https://clickhouse.com/docs/ru/reference/data-types/decimal)

```
SELECT toDecimal64OrDefault(toString(0.0001), 18)

```


```
0.0001

```


```
SELECT toDecimal64OrDefault('Inf', 0, CAST('-1', 'Decimal64(0)'))

```


```
-1

```


## toDecimal64OrNull

- Значения или строковые представления типа (U)Int*.
- Значения или строковые представления типа Float*.
- Значения Float* `NaN` и `Inf`, а также их строковые представления (регистронезависимые).
- Строковые представления двоичных и шестнадцатеричных значений.
- Значения, выходящие за пределы `Decimal64`: `(-1*10^(18 - S), 1*10^(18 - S))`.
- [`toDecimal64`](#toDecimal64).
- [`toDecimal64OrZero`](#toDecimal64OrZero).
- [`toDecimal64OrDefault`](#toDecimal64OrDefault).

```
toDecimal64OrNull(expr, S)

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`Выражение`](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/expression)
- `S` — параметр масштаба в диапазоне от 0 до 18, задающий, сколько цифр может содержать дробная часть числа. [`UInt8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT toDecimal64OrNull('42.7', 2), toDecimal64OrNull('invalid', 2)

```


```
┌─toDecimal64OrNull('42.7', 2)─┬─toDecimal64OrNull('invalid', 2)─┐
│                        42.70 │                            ᴺᵁᴸᴸ │
└──────────────────────────────┴─────────────────────────────────┘

```


## toDecimal64OrZero

- Значения или строковые представления типа (U)Int*.
- Значения или строковые представления типа Float*.
- Значения или строковые представления значений Float* `NaN` и `Inf` (регистронезависимо).
- Строковые представления двоичных и шестнадцатеричных значений.
- [`toDecimal64`](#toDecimal64).
- [`toDecimal64OrNull`](#toDecimal64OrNull).
- [`toDecimal64OrDefault`](#toDecimal64OrDefault).

```
toDecimal64OrZero(expr, S)

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`Выражение`](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/expression)
- `S` — параметр масштаба в диапазоне от 0 до 18, определяющий, сколько цифр может быть в дробной части числа. [`UInt8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT toDecimal64OrZero('42.7', 2), toDecimal64OrZero('invalid', 2)

```


```
┌─toDecimal64OrZero('42.7', 2)─┬─toDecimal64OrZero('invalid', 2)─┐
│                        42.70 │                            0.00 │
└──────────────────────────────┴─────────────────────────────────┘

```


## toDecimalString


```
toDecimalString(number, scale)

```

- `number` — Числовое значение, которое нужно преобразовать в строку. Может иметь любой числовой тип (Int, UInt, Float, Decimal). [`Int8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) or [`Int16`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) or [`Int32`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) or [`Int64`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) or [`UInt8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) or [`UInt16`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) or [`UInt32`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) or [`UInt64`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) or [`Float32`](https://clickhouse.com/docs/ru/reference/data-types/float) or [`Float64`](https://clickhouse.com/docs/ru/reference/data-types/float) or [`Decimal`](https://clickhouse.com/docs/ru/reference/data-types/decimal)
- `scale` — Количество цифр для отображения в дробной части. При необходимости результат будет округлён. [`UInt8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT toDecimalString(2.1456, 2)

```


```
┌─toDecimalString(2.1456, 2)─┐
│ 2.15                       │
└────────────────────────────┘

```


```
SELECT toDecimalString(5, 3)

```


```
┌─toDecimalString(5, 3)─┐
│ 5.000                 │
└───────────────────────┘

```


```
SELECT toDecimalString(CAST(123.456 AS Decimal(10,3)), 2) AS decimal_val,
       toDecimalString(CAST(42.7 AS Float32), 4) AS float_val

```


```
┌─decimal_val─┬─float_val─┐
│ 123.46      │ 42.7000   │
└─────────────┴───────────┘

```


## toFixedString


```
toFixedString(s, N)

```

- `s` — Строка, которую нужно преобразовать. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `N` — Длина результирующей FixedString. [`const UInt*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT toFixedString('foo', 8) AS s;

```


```
┌─s─────────────┐
│ foo\0\0\0\0\0 │
└───────────────┘

```


## toFloat32

- Значения типа (U)Int*.
- Строковые представления (U)Int8/16/32/128/256.
- Значения типа Float*, включая `NaN` и `Inf`.
- Строковые представления Float*, включая `NaN` и `Inf` (регистронезависимые).
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toFloat32('0xc0fe');`.
- [`toFloat32OrZero`](#toFloat32OrZero).
- [`toFloat32OrNull`](#toFloat32OrNull).
- [`toFloat32OrDefault`](#toFloat32OrDefault).

```
toFloat32(expr)

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`Выражение`](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/expression)

```
SELECT
    toFloat32(42.7),
    toFloat32('42.7'),
    toFloat32('NaN')
FORMAT Vertical

```


```
Строка 1:
──────
toFloat32(42.7):   42.7
toFloat32('42.7'): 42.7
toFloat32('NaN'):  nan

```


## toFloat32OrDefault


```
toFloat32OrDefault(expr[, default])

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float)
- `default` — Необязательно. Значение по умолчанию, которое возвращается, если не удалось выполнить разбор. [`Float32`](https://clickhouse.com/docs/ru/reference/data-types/float)

```
SELECT toFloat32OrDefault('8', CAST('0', 'Float32'))

```


```
8

```


```
SELECT toFloat32OrDefault('abc', CAST('0', 'Float32'))

```


```
0

```


## toFloat32OrNull

- Значения типа (U)Int*.
- Строковые представления (U)Int8/16/32/128/256.
- Значения типа Float*, включая `NaN` и `Inf`.
- Строковые представления Float*, включая `NaN` и `Inf` (регистронезависимо).
- Строковые представления двоичных и шестнадцатеричных значений, например: `SELECT toFloat32OrNull('0xc0fe');`.
- Недопустимые строковые форматы.
- [`toFloat32`](#toFloat32).
- [`toFloat32OrZero`](#toFloat32OrZero).
- [`toFloat32OrDefault`](#toFloat32OrDefault).

```
toFloat32OrNull(x)

```

- `x` — Строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    toFloat32OrNull('42.7'),
    toFloat32OrNull('NaN'),
    toFloat32OrNull('abc')
FORMAT Vertical

```


```
Строка 1:
──────
toFloat32OrNull('42.7'): 42.7
toFloat32OrNull('NaN'):  nan
toFloat32OrNull('abc'):  \N

```


## toFloat32OrZero

- [`toFloat32`](#toFloat32).
- [`toFloat32OrNull`](#toFloat32OrNull).
- [`toFloat32OrDefault`](#toFloat32OrDefault).

```
toFloat32OrZero(x)

```

- `x` — Строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    toFloat32OrZero('42.7'),
    toFloat32OrZero('abc')
FORMAT Vertical

```


```
Строка 1:
──────
toFloat32OrZero('42.7'): 42.7
toFloat32OrZero('abc'):  0

```


## toFloat64

- Значения типа (U)Int*.
- Строковые представления значений типа (U)Int8/16/32/128/256.
- Значения типа Float*, включая `NaN` и `Inf`.
- Строковые представления значений типа Float*, включая `NaN` и `Inf` (регистронезависимо).
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toFloat64('0xc0fe');`.
- [`toFloat64OrZero`](#toFloat64OrZero).
- [`toFloat64OrNull`](#toFloat64OrNull).
- [`toFloat64OrDefault`](#toFloat64OrDefault).

```
toFloat64(expr)

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`Expression`](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/expression)

```
SELECT
    toFloat64(42.7),
    toFloat64('42.7'),
    toFloat64('NaN')
FORMAT Vertical

```


```
Строка 1:
──────
toFloat64(42.7):   42.7
toFloat64('42.7'): 42.7
toFloat64('NaN'):  nan

```


## toFloat64OrDefault


```
toFloat64OrDefault(expr[, default])

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float)
- `default` — Необязательно. Значение по умолчанию, возвращаемое при неуспешном парсинге. [`Float64`](https://clickhouse.com/docs/ru/reference/data-types/float)

```
SELECT toFloat64OrDefault('8', CAST('0', 'Float64'))

```


```
8

```


```
SELECT toFloat64OrDefault('abc', CAST('0', 'Float64'))

```


```
0

```


## toFloat64OrNull

- Значения типа (U)Int*.
- Строковые представления (U)Int8/16/32/128/256.
- Значения типа Float*, включая `NaN` и `Inf`.
- Строковые представления значений типа Float*, включая `NaN` и `Inf` (регистронезависимо).
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toFloat64OrNull('0xc0fe');`.
- Недопустимые строковые форматы.
- [`toFloat64`](#toFloat64).
- [`toFloat64OrZero`](#toFloat64OrZero).
- [`toFloat64OrDefault`](#toFloat64OrDefault).

```
toFloat64OrNull(x)

```

- `x` — строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    toFloat64OrNull('42.7'),
    toFloat64OrNull('NaN'),
    toFloat64OrNull('abc')
FORMAT Vertical

```


```
строка 1:
──────
toFloat64OrNull('42.7'): 42.7
toFloat64OrNull('NaN'):  nan
toFloat64OrNull('abc'):  \N

```


## toFloat64OrZero

- [`toFloat64`](#toFloat64).
- [`toFloat64OrNull`](#toFloat64OrNull).
- [`toFloat64OrDefault`](#toFloat64OrDefault).

```
toFloat64OrZero(x)

```

- `x` — Строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    toFloat64OrZero('42.7'),
    toFloat64OrZero('abc')
FORMAT Vertical

```


```
Строка 1:
──────
toFloat64OrZero('42.7'): 42.7
toFloat64OrZero('abc'):  0

```


## toInt128

- Значения или строковые представления типа (U)Int*.
- Значения типа Float*.
- Строковые представления значений Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toInt128('0xc0fe');`.
- [`toInt128OrZero`](#toInt128OrZero).
- [`toInt128OrNull`](#toInt128OrNull).
- [`toInt128OrDefault`](#toInt128OrDefault).

```
toInt128(expr)

```

- `expr` — Выражение, возвращающее число или его строковое представление. [`Expression`](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/expression)

```
SELECT
    toInt128(-128),
    toInt128(-128.8),
    toInt128('-128')
FORMAT Vertical

```


```
Row 1:
──────
toInt128(-128):   -128
toInt128(-128.8): -128
toInt128('-128'): -128

```


## toInt128OrDefault


```
toInt128OrDefault(expr[, default])

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint), или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float)
- `default` — Необязательно. Значение по умолчанию, которое возвращается, если разбор не удался. [`Int128`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT toInt128OrDefault('-128', CAST('-1', 'Int128'))

```


```
-128

```


```
SELECT toInt128OrDefault('abc', CAST('-1', 'Int128'))

```


```
-1

```


## toInt128OrNull

- Строковые представления (U)Int*.
- Строковые представления значений Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных чисел, например `SELECT toInt128OrNull('0xc0fe');`.
- [`toInt128`](#toInt128).
- [`toInt128OrZero`](#toInt128OrZero).
- [`toInt128OrDefault`](#toInt128OrDefault).

```
toInt128OrNull(x)

```

- `x` — Строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    toInt128OrNull('-128'),
    toInt128OrNull('abc')
FORMAT Vertical

```


```
Row 1:
──────
toInt128OrNull('-128'): -128
toInt128OrNull('abc'):  \N

```


## toInt128OrZero

- [`toInt128`](#toInt128).
- [`toInt128OrNull`](#toInt128OrNull).
- [`toInt128OrDefault`](#toInt128OrDefault).

```
toInt128OrZero(x)

```

- `x` — Входное значение для преобразования. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`Decimal`](https://clickhouse.com/docs/ru/reference/data-types/decimal) или [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Date`](https://clickhouse.com/docs/ru/reference/data-types/date) или [`DateTime`](https://clickhouse.com/docs/ru/reference/data-types/datetime)

```
SELECT toInt128OrZero('123')

```


```
123

```


```
SELECT toInt128OrZero('abc')

```


```
0

```


## toInt16

- Значения или строковые представления типа (U)Int*.
- Значения типа Float*.
- Строковые представления значений типа Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например: `SELECT toInt16('0xc0fe');`.
- [`toInt16OrZero`](#toInt16OrZero).
- [`toInt16OrNull`](#toInt16OrNull).
- [`toInt16OrDefault`](#toInt16OrDefault).

```
toInt16(expr)

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`Expression`](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/expression)

```
SELECT
    toInt16(-16),
    toInt16(-16.16),
    toInt16('-16')
FORMAT Vertical

```


```
Row 1:
──────
toInt16(-16):    -16
toInt16(-16.16): -16
toInt16('-16'):  -16

```


## toInt16OrDefault


```
toInt16OrDefault(expr[, default])

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float)
- `default` — Необязательно. Значение по умолчанию, которое возвращается, если преобразование не удалось. [`Int16`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT toInt16OrDefault('-16', CAST('-1', 'Int16'))

```


```
-16

```


```
SELECT toInt16OrDefault('abc', CAST('-1', 'Int16'))

```


```
-1

```


## toInt16OrNull

- Строковые представления (U)Int*.
- Строковые представления значений Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toInt16OrNull('0xc0fe');`.
- [`toInt16`](#toInt16).
- [`toInt16OrZero`](#toInt16OrZero).
- [`toInt16OrDefault`](#toInt16OrDefault).

```
toInt16OrNull(x)

```

- `x` — строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    toInt16OrNull('-16'),
    toInt16OrNull('abc')
FORMAT Vertical

```


```
Row 1:
──────
toInt16OrNull('-16'): -16
toInt16OrNull('abc'): \N

```


## toInt16OrZero

- Строковые представления значений (U)Int*.
- Строковые представления значений Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toInt16OrZero('0xc0fe');`.
- [`toInt16`](#toInt16).
- [`toInt16OrNull`](#toInt16OrNull).
- [`toInt16OrDefault`](#toInt16OrDefault).

```
toInt16OrZero(x)

```

- `x` — Строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    toInt16OrZero('16'),
    toInt16OrZero('abc')
FORMAT Vertical

```


```
Row 1:
──────
toInt16OrZero('16'): 16
toInt16OrZero('abc'): 0

```


## toInt256

- Значения или строковые представления типа (U)Int*.
- Значения типа Float*.
- Строковые представления значений Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toInt256('0xc0fe');`.
- [`toInt256OrZero`](#toInt256OrZero).
- [`toInt256OrNull`](#toInt256OrNull).
- [`toInt256OrDefault`](#toInt256OrDefault).

```
toInt256(expr)

```

- `expr` — выражение, возвращающее число или его строковое представление. [`Expression`](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/expression)

```
SELECT
    toInt256(-256),
    toInt256(-256.256),
    toInt256('-256')
FORMAT Vertical

```


```
Row 1:
──────
toInt256(-256):     -256
toInt256(-256.256): -256
toInt256('-256'):   -256

```


## toInt256OrDefault


```
toInt256OrDefault(expr[, default])

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string), [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float)
- `default` — Необязательно. Значение по умолчанию, которое возвращается, если парсинг не удался. [`Int256`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT toInt256OrDefault('-256', CAST('-1', 'Int256'))

```


```
-256

```


```
SELECT toInt256OrDefault('abc', CAST('-1', 'Int256'))

```


```
-1

```


## toInt256OrNull

- Строковые представления (U)Int*.
- Строковые представления значений Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toInt256OrNull('0xc0fe');`.
- [`toInt256`](#toInt256).
- [`toInt256OrZero`](#toInt256OrZero).
- [`toInt256OrDefault`](#toInt256OrDefault).

```
toInt256OrNull(x)

```

- `x` — строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    toInt256OrNull('-256'),
    toInt256OrNull('abc')
FORMAT Vertical

```


```
Row 1:
──────
toInt256OrNull('-256'): -256
toInt256OrNull('abc'):  \N

```


## toInt256OrZero

- [`toInt256`](#toInt256).
- [`toInt256OrNull`](#toInt256OrNull).
- [`toInt256OrDefault`](#toInt256OrDefault).

```
toInt256OrZero(x)

```

- `x` — Входное значение, которое нужно преобразовать. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`Decimal`](https://clickhouse.com/docs/ru/reference/data-types/decimal) или [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Date`](https://clickhouse.com/docs/ru/reference/data-types/date) или [`DateTime`](https://clickhouse.com/docs/ru/reference/data-types/datetime)

```
SELECT toInt256OrZero('123')

```


```
123

```


```
SELECT toInt256OrZero('abc')

```


```
0

```


## toInt32

- Значения или строковые представления типа (U)Int*.
- Значения типа Float*.
- Строковые представления значений типа Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toInt32('0xc0fe');`.
- [`toInt32OrZero`](#toInt32OrZero).
- [`toInt32OrNull`](#toInt32OrNull).
- [`toInt32OrDefault`](#toInt32OrDefault).

```
toInt32(expr)

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`Expression`](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/expression)

```
SELECT
    toInt32(-32),
    toInt32(-32.32),
    toInt32('-32')
FORMAT Vertical

```


```
Row 1:
──────
toInt32(-32):    -32
toInt32(-32.32): -32
toInt32('-32'):  -32

```


## toInt32OrDefault


```
toInt32OrDefault(expr[, default])

```

- `expr` — Выражение, возвращающее число или его строковое представление. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float)
- `default` — Необязательно. Значение по умолчанию, которое возвращается, если парсинг завершился неудачно. [`Int32`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT toInt32OrDefault('-32', CAST('-1', 'Int32'))

```


```
-32

```


```
SELECT toInt32OrDefault('abc', CAST('-1', 'Int32'))

```


```
-1

```


## toInt32OrNull

- Строковые представления (U)Int*.
- Строковые представления значений Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toInt32OrNull('0xc0fe');`.
- [`toInt32`](#toInt32).
- [`toInt32OrZero`](#toInt32OrZero).
- [`toInt32OrDefault`](#toInt32OrDefault).

```
toInt32OrNull(x)

```

- `x` — Строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    toInt32OrNull('-32'),
    toInt32OrNull('abc')
FORMAT Vertical

```


```
Row 1:
──────
toInt32OrNull('-32'): -32
toInt32OrNull('abc'): \N

```


## toInt32OrZero

- Строковые представления (U)Int*.
- Строковые представления значений Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toInt32OrZero('0xc0fe');`.
- [`toInt32`](#toInt32).
- [`toInt32OrNull`](#toInt32OrNull).
- [`toInt32OrDefault`](#toInt32OrDefault).

```
toInt32OrZero(x)

```

- `x` — Строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    toInt32OrZero('32'),
    toInt32OrZero('abc')
FORMAT Vertical

```


```
Row 1:
──────
toInt32OrZero('32'): 32
toInt32OrZero('abc'): 0

```


## toInt64

- Значения или строковые представления типа (U)Int*.
- Значения типа Float*.
- Строковые представления значений Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toInt64('0xc0fe');`.
- [`toInt64OrZero`](#toInt64OrZero).
- [`toInt64OrNull`](#toInt64OrNull).
- [`toInt64OrDefault`](#toInt64OrDefault).

```
toInt64(expr)

```

- `expr` — Выражение, возвращающее число или строковое представление числа. Поддерживаются: значения или строковые представления значений типа (U)Int*, значения типа Float*. Не поддерживаются: строковые представления значений Float*, включая NaN и Inf, а также строковые представления двоичных и шестнадцатеричных значений. [`Expression`](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/expression)

```
SELECT
    toInt64(-64),
    toInt64(-64.64),
    toInt64('-64')
FORMAT Vertical

```


```
Row 1:
──────
toInt64(-64):    -64
toInt64(-64.64): -64
toInt64('-64'):  -64

```


## toInt64OrDefault


```
toInt64OrDefault(expr[, default])

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float)
- `default` — Необязательный параметр. Значение по умолчанию, которое возвращается, если не удалось выполнить парсинг. [`Int64`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT toInt64OrDefault('-64', CAST('-1', 'Int64'))

```


```
-64

```


```
SELECT toInt64OrDefault('abc', CAST('-1', 'Int64'))

```


```
-1

```


## toInt64OrNull

- Строковые представления значений (U)Int*.
- Строковые представления значений Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toInt64OrNull('0xc0fe');`.
- [`toInt64`](#toInt64).
- [`toInt64OrZero`](#toInt64OrZero).
- [`toInt64OrDefault`](#toInt64OrDefault).

```
toInt64OrNull(x)

```

- `x` — Строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    toInt64OrNull('-64'),
    toInt64OrNull('abc')
FORMAT Vertical

```


```
Row 1:
──────
toInt64OrNull('-64'): -64
toInt64OrNull('abc'): \N

```


## toInt64OrZero

- [`toInt64`](#toInt64).
- [`toInt64OrNull`](#toInt64OrNull).
- [`toInt64OrDefault`](#toInt64OrDefault).

```
toInt64OrZero(x)

```

- `x` — Входное значение для преобразования. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`Decimal`](https://clickhouse.com/docs/ru/reference/data-types/decimal) или [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Date`](https://clickhouse.com/docs/ru/reference/data-types/date) или [`DateTime`](https://clickhouse.com/docs/ru/reference/data-types/datetime)

```
SELECT toInt64OrZero('123')

```


```
123

```


```
SELECT toInt64OrZero('abc')

```


```
0

```


## toInt8

- Значения или строковые представления значений типа (U)Int*.
- Значения типа Float*.
- Строковые представления значений Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toInt8('0xc0fe');`.
- [`toInt8OrZero`](#toInt8OrZero).
- [`toInt8OrNull`](#toInt8OrNull).
- [`toInt8OrDefault`](#toInt8OrDefault).

```
toInt8(expr)

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`Выражение`](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/expression)

```
SELECT
    toInt8(-8),
    toInt8(-8.8),
    toInt8('-8')
FORMAT Vertical

```


```
Row 1:
──────
toInt8(-8):   -8
toInt8(-8.8): -8
toInt8('-8'): -8

```


## toInt8OrDefault


```
toInt8OrDefault(expr[, default])

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float)
- `default` — Необязательно. Значение по умолчанию, которое возвращается, если разбор завершился неудачно. [`Int8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT toInt8OrDefault('-8', CAST('-1', 'Int8'))

```


```
-8

```


```
SELECT toInt8OrDefault('abc', CAST('-1', 'Int8'))

```


```
-1

```


## toInt8OrNull

- Строковые представления (U)Int*.
- Строковые представления значений Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toInt8OrNull('0xc0fe');`.
- [`toInt8`](#toInt8).
- [`toInt8OrZero`](#toInt8OrZero).
- [`toInt8OrDefault`](#toInt8OrDefault).

```
toInt8OrNull(x)

```

- `x` — Строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    toInt8OrNull('-8'),
    toInt8OrNull('abc')
FORMAT Vertical

```


```
Row 1:
──────
toInt8OrNull('-8'):  -8
toInt8OrNull('abc'): \N

```


## toInt8OrZero

- Строковые представления (U)Int*.
- Строковые представления значений Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toInt8OrZero('0xc0fe');`.
- [`toInt8`](#toInt8).
- [`toInt8OrNull`](#toInt8OrNull).
- [`toInt8OrDefault`](#toInt8OrDefault).

```
toInt8OrZero(x)

```

- `x` — Строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    toInt8OrZero('8'),
    toInt8OrZero('abc')
FORMAT Vertical

```


```
Row 1:
──────
toInt8OrZero('8'): 8
toInt8OrZero('abc'): 0

```


## toInterval


```
toInterval(value, unit)

```

- `value` — Числовое значение, задающее количество единиц. Может быть любого числового типа: [`Int8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) or [`Int16`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) or [`Int32`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) or [`Int64`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) or [`UInt8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) or [`UInt16`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) or [`UInt32`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) or [`UInt64`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) or [`Float32`](https://clickhouse.com/docs/ru/reference/data-types/float) or [`Float64`](https://clickhouse.com/docs/ru/reference/data-types/float)
- `unit` — Единица времени. Должна быть строковой константой. Допустимые значения: ‘nanosecond’, ‘microsecond’, ‘millisecond’, ‘second’, ‘minute’, ‘hour’, ‘day’, ‘week’, ‘month’, ‘quarter’, ‘year’. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    toInterval(5, 'second') AS seconds,
    toInterval(3, 'day') AS days,
    toInterval(2, 'month') AS months

```


```
┌─seconds─┬─days─┬─months─┐
│ 5       │ 3    │ 2      │
└─────────┴──────┴────────┘

```


```
SELECT
    now() AS current_time,
    now() + toInterval(1, 'hour') AS one_hour_later,
    now() - toInterval(7, 'day') AS week_ago

```


```
┌─────────current_time─┬──one_hour_later─────┬────────────week_ago─┐
│ 2025-01-04 10:30:00  │ 2025-01-04 11:30:00 │ 2024-12-28 10:30:00 │
└──────────────────────┴─────────────────────┴─────────────────────┘

```


```
SELECT toDate('2025-01-01') + toInterval(number, 'day') AS dates
FROM numbers(5)

```


```
┌──────dates─┐
│ 2025-01-01 │
│ 2025-01-02 │
│ 2025-01-03 │
│ 2025-01-04 │
│ 2025-01-05 │
└────────────┘

```


## toIntervalDay


```
toIntervalDay(n)

```

- `n` — Количество дней. Целые числа, их строковые представления, а также числа с плавающей точкой. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
WITH
    toDate('2025-06-15') AS date,
    toIntervalDay(5) AS interval_to_days
SELECT date + interval_to_days AS result

```


```
┌─────result─┐
│ 2025-06-20 │
└────────────┘

```


## toIntervalHour


```
toIntervalHour(n)

```

- `n` — Количество часов. Целые числа, их строковые представления, а также числа с плавающей точкой. [`Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`UInt*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
WITH
    toDate('2025-06-15') AS date,
    toIntervalHour(12) AS interval_to_hours
SELECT date + interval_to_hours AS result

```


```
┌──────────────result─┐
│ 2025-06-15 12:00:00 │
└─────────────────────┘

```


## toIntervalMicrosecond


```
toIntervalMicrosecond(n)

```

- `n` — количество микросекунд. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
WITH
    toDateTime('2025-06-15') AS date,
    toIntervalMicrosecond(30) AS interval_to_microseconds
SELECT date + interval_to_microseconds AS result

```


```
┌─────────────────────result─┐
│ 2025-06-15 00:00:00.000030 │
└────────────────────────────┘

```


## toIntervalMillisecond


```
toIntervalMillisecond(n)

```

- `n` — число миллисекунд. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
WITH
    toDateTime('2025-06-15') AS date,
    toIntervalMillisecond(30) AS interval_to_milliseconds
SELECT date + interval_to_milliseconds AS result

```


```
┌──────────────────result─┐
│ 2025-06-15 00:00:00.030 │
└─────────────────────────┘

```


## toIntervalMinute


```
toIntervalMinute(n)

```

- `n` — Количество минут. Целые числа или их строковые представления, а также числа с плавающей точкой. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
WITH
    toDate('2025-06-15') AS date,
    toIntervalMinute(12) AS interval_to_minutes
SELECT date + interval_to_minutes AS result

```


```
┌──────────────result─┐
│ 2025-06-15 00:12:00 │
└─────────────────────┘

```


## toIntervalMonth


```
toIntervalMonth(n)

```

- `n` — количество месяцев. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
WITH
    toDate('2025-06-15') AS date,
    toIntervalMonth(1) AS interval_to_month
SELECT date + interval_to_month AS result

```


```
┌─────result─┐
│ 2025-07-15 │
└────────────┘

```


## toIntervalNanosecond


```
toIntervalNanosecond(n)

```

- `n` — Количество наносекунд. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
WITH
    toDateTime('2025-06-15') AS date,
    toIntervalNanosecond(30) AS interval_to_nanoseconds
SELECT date + interval_to_nanoseconds AS result

```


```
┌────────────────────────result─┐
│ 2025-06-15 00:00:00.000000030 │
└───────────────────────────────┘

```


## toIntervalQuarter


```
toIntervalQuarter(n)

```

- `n` — количество кварталов. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
WITH
    toDate('2025-06-15') AS date,
    toIntervalQuarter(1) AS interval_to_quarter
SELECT date + interval_to_quarter AS result

```


```
┌─────result─┐
│ 2025-09-15 │
└────────────┘

```


## toIntervalSecond


```
toIntervalSecond(n)

```

- `n` — Количество секунд. Целые числа, их строковые представления, а также числа с плавающей точкой. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
WITH
    toDate('2025-06-15') AS date,
    toIntervalSecond(30) AS interval_to_seconds
SELECT date + interval_to_seconds AS result

```


```
┌──────────────result─┐
│ 2025-06-15 00:00:30 │
└─────────────────────┘

```


## toIntervalWeek


```
toIntervalWeek(n)

```

- `n` — Количество недель. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
WITH
    toDate('2025-06-15') AS date,
    toIntervalWeek(1) AS interval_to_week
SELECT date + interval_to_week AS result

```


```
┌─────result─┐
│ 2025-06-22 │
└────────────┘

```


## toIntervalYear


```
toIntervalYear(n)

```

- `n` — Количество лет. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float) или [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
WITH
    toDate('2024-06-15') AS date,
    toIntervalYear(1) AS interval_to_year
SELECT date + interval_to_year AS result

```


```
┌─────result─┐
│ 2025-06-15 │
└────────────┘

```


## toLowCardinality


```
toLowCardinality(expr)

```

- `expr` — выражение, результат которого имеет один из поддерживаемых типов данных: [`String`](https://clickhouse.com/docs/ru/reference/data-types/string), [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring), [`Date`](https://clickhouse.com/docs/ru/reference/data-types/date), [`DateTime`](https://clickhouse.com/docs/ru/reference/data-types/datetime), [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float)

```
SELECT toLowCardinality('1')

```


```
┌─toLowCardinality('1')─┐
│ 1                     │
└───────────────────────┘

```


## toString


```
toString(value[, timezone])

```

- `value` — Значение для преобразования в строку. [`Any`](https://clickhouse.com/docs/ru/reference/data-types/index)
- `timezone` — Необязательно. Имя часового пояса для преобразования значения DateTime. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    now() AS ts,
    time_zone,
    toString(ts, time_zone) AS str_tz_datetime
FROM system.time_zones
WHERE time_zone LIKE 'Europe%'
LIMIT 10

```


```
┌──────────────────ts─┬─time_zone─────────┬─str_tz_datetime─────┐
│ 2023-09-08 19:14:59 │ Europe/Amsterdam  │ 2023-09-08 21:14:59 │
│ 2023-09-08 19:14:59 │ Europe/Andorra    │ 2023-09-08 21:14:59 │
│ 2023-09-08 19:14:59 │ Europe/Astrakhan  │ 2023-09-08 23:14:59 │
│ 2023-09-08 19:14:59 │ Europe/Athens     │ 2023-09-08 22:14:59 │
│ 2023-09-08 19:14:59 │ Europe/Belfast    │ 2023-09-08 20:14:59 │
└─────────────────────┴───────────────────┴─────────────────────┘

```


## toStringCutToZero


```
toStringCutToZero(s)

```

- `s` — обрабатываемое значение типа `String` или `FixedString`. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring)

```
SELECT
    toStringCutToZero('hello'),
    toStringCutToZero('hello\0world')

```


```
┌─toStringCutToZero('hello')─┬─toStringCutToZero('hello\0world')─┐
│ hello                      │ hello                             │
└────────────────────────────┴───────────────────────────────────┘

```


## toTime


```
toTime(x)

```

- `x` — Входное значение для преобразования. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) or [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring) or [`DateTime`](https://clickhouse.com/docs/ru/reference/data-types/datetime) or [`DateTime64`](https://clickhouse.com/docs/ru/reference/data-types/datetime64) or [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) or [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float)

```
SET enable_time_time64_type = 1;
SET use_legacy_to_time = 0;
SELECT toTime(toDateTime64('2025-04-15 14:30:25.123', 3))

```


```
14:30:25

```


```
SET enable_time_time64_type = 1;
SET use_legacy_to_time = 0;
SELECT toTime(toDateTime('2025-04-15 14:30:25'))

```


```
14:30:25

```


```
SET enable_time_time64_type = 1;
SET use_legacy_to_time = 0;
SELECT toTime(toDateTime(52225, 'UTC'))

```


```
14:30:25

```


## toTime64


```
toTime64(x, scale)

```

- `x` — Входное значение для преобразования. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring) или [`DateTime64`](https://clickhouse.com/docs/ru/reference/data-types/datetime64) или [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float)
- `scale` — Точность (количество знаков после запятой, `0`–`9`) результирующего `Time64`. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SET enable_time_time64_type = 1;
SELECT toTime64('14:30:25.123456', 6)

```


```
14:30:25.123456

```


```
SET enable_time_time64_type = 1;
SELECT toTime64(toDateTime64('2025-04-15 14:30:25.123456', 6), 6)

```


```
14:30:25.123456

```


```
SET enable_time_time64_type = 1;
SELECT toTime64(52225.123456, 6)

```


```
14:30:25.123456

```


## toTime64OrNull

- [`toTime64`](#toTime64)
- [`toTime64OrZero`](#toTime64OrZero)

```
toTime64OrNull(x)

```

- `x` — строковое представление времени с субсекундной точностью. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT toTime64OrNull('12:30:45.123'), toTime64OrNull('invalid')

```


```
┌─toTime64OrNull('12:30:45.123')─┬─toTime64OrNull('invalid')─┐
│                   12:30:45.123 │                      ᴺᵁᴸᴸ │
└────────────────────────────────┴───────────────────────────┘

```


## toTime64OrZero


```
toTime64OrZero(x)

```

- `x` — строковое представление времени с субсекундной точностью. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT toTime64OrZero('12:30:45.123'), toTime64OrZero('invalid')

```


```
┌─toTime64OrZero('12:30:45.123')─┬─toTime64OrZero('invalid')─┐
│                   12:30:45.123 │              00:00:00.000 │
└────────────────────────────────┴───────────────────────────┘

```


## toTimeOrNull

- [`toTime`](#toTime)
- [`toTimeOrZero`](#toTimeOrZero)

```
toTimeOrNull(x)

```

- `x` — строковое представление времени. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT toTimeOrNull('12:30:45'), toTimeOrNull('invalid')

```


```
┌─toTimeOrNull('12:30:45')─┬─toTimeOrNull('invalid')─┐
│                 12:30:45 │                    ᴺᵁᴸᴸ │
└──────────────────────────┴─────────────────────────┘

```


## toTimeOrZero


```
toTimeOrZero(x)

```

- `x` — Строковое представление времени. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT toTimeOrZero('12:30:45'), toTimeOrZero('invalid')

```


```
┌─toTimeOrZero('12:30:45')─┬─toTimeOrZero('invalid')─┐
│                 12:30:45 │                00:00:00 │
└──────────────────────────┴─────────────────────────┘

```


## toUInt128

- Значения или строковые представления типа (U)Int*.
- Значения типа Float*.
- Строковые представления значений Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toUInt128('0xc0fe');`.
- [`toUInt128OrZero`](#toUInt128OrZero).
- [`toUInt128OrNull`](#toUInt128OrNull).
- [`toUInt128OrDefault`](#toUInt128OrDefault).

```
toUInt128(expr)

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`Выражение`](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/expression)

```
SELECT
    toUInt128(128),
    toUInt128(128.8),
    toUInt128('128')
FORMAT Vertical

```


```
Row 1:
──────
toUInt128(128):   128
toUInt128(128.8): 128
toUInt128('128'): 128

```


## toUInt128OrDefault


```
toUInt128OrDefault(expr[, default])

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float)
- `default` — Необязательно. Значение по умолчанию, которое будет возвращено, если разбор не выполнен. [`UInt128`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT toUInt128OrDefault('128', CAST('0', 'UInt128'))

```


```
128

```


```
SELECT toUInt128OrDefault('abc', CAST('0', 'UInt128'))

```


```
0

```


## toUInt128OrNull

- Строковые представления (U)Int*.
- Строковые представления значений Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toUInt128OrNull('0xc0fe');`.
- [`toUInt128`](#toUInt128).
- [`toUInt128OrZero`](#toUInt128OrZero).
- [`toUInt128OrDefault`](#toUInt128OrDefault).

```
toUInt128OrNull(x)

```

- `x` — строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    toUInt128OrNull('128'),
    toUInt128OrNull('abc')
FORMAT Vertical

```


```
Row 1:
──────
toUInt128OrNull('128'): 128
toUInt128OrNull('abc'): \N

```


## toUInt128OrZero

- Строковые представления (U)Int*.
- Строковые представления значений Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toUInt128OrZero('0xc0fe');`.
- [`toUInt128`](#toUInt128).
- [`toUInt128OrNull`](#toUInt128OrNull).
- [`toUInt128OrDefault`](#toUInt128OrDefault).

```
toUInt128OrZero(x)

```

- `x` — Строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    toUInt128OrZero('128'),
    toUInt128OrZero('abc')
FORMAT Vertical

```


```
Row 1:
──────
toUInt128OrZero('128'): 128
toUInt128OrZero('abc'): 0

```


## toUInt16

- Значения или строковые представления типа (U)Int*.
- Значения типа Float*.
- Строковые представления значений Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toUInt16('0xc0fe');`.
- [`toUInt16OrZero`](#toUInt16OrZero).
- [`toUInt16OrNull`](#toUInt16OrNull).
- [`toUInt16OrDefault`](#toUInt16OrDefault).

```
toUInt16(expr)

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`Выражение`](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/expression)

```
SELECT
    toUInt16(16),
    toUInt16(16.16),
    toUInt16('16')
FORMAT Vertical

```


```
Row 1:
──────
toUInt16(16):    16
toUInt16(16.16): 16
toUInt16('16'):  16

```


## toUInt16OrDefault


```
toUInt16OrDefault(expr[, default])

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float)
- `default` — Необязательный параметр. Значение по умолчанию, которое возвращается, если парсинг завершился неудачно. [`UInt16`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT toUInt16OrDefault('16', CAST('0', 'UInt16'))

```


```
16

```


```
SELECT toUInt16OrDefault('abc', CAST('0', 'UInt16'))

```


```
0

```


## toUInt16OrNull

- Строковые представления (U)Int8/16/32/128/256.
- Строковые представления значений Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toUInt16OrNull('0xc0fe');`.
- [`toUInt16`](#toUInt16).
- [`toUInt16OrZero`](#toUInt16OrZero).
- [`toUInt16OrDefault`](#toUInt16OrDefault).

```
toUInt16OrNull(x)

```

- `x` — Строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    toUInt16OrNull('16'),
    toUInt16OrNull('abc')
FORMAT Vertical

```


```
Row 1:
──────
toUInt16OrNull('16'):  16
toUInt16OrNull('abc'): \N

```


## toUInt16OrZero

- Строковые представления (U)Int8/16/32/128/256.
- Строковые представления значений Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toUInt16OrZero('0xc0fe');`.
- [`toUInt16`](#toUInt16).
- [`toUInt16OrNull`](#toUInt16OrNull).
- [`toUInt16OrDefault`](#toUInt16OrDefault).

```
toUInt16OrZero(x)

```

- `x` — Строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    toUInt16OrZero('16'),
    toUInt16OrZero('abc')
FORMAT Vertical

```


```
Row 1:
──────
toUInt16OrZero('16'):  16
toUInt16OrZero('abc'): 0

```


## toUInt256

- Значения или строковые представления типа (U)Int*.
- Значения типа Float*.
- Строковые представления значений Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toUInt256('0xc0fe');`.
- [`toUInt256OrZero`](#toUInt256OrZero).
- [`toUInt256OrNull`](#toUInt256OrNull).
- [`toUInt256OrDefault`](#toUInt256OrDefault).

```
toUInt256(expr)

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`Выражение`](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/expression)

```
SELECT
    toUInt256(256),
    toUInt256(256.256),
    toUInt256('256')
FORMAT Vertical

```


```
Row 1:
──────
toUInt256(256):     256
toUInt256(256.256): 256
toUInt256('256'):   256

```


## toUInt256OrDefault


```
toUInt256OrDefault(expr[, default])

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string), [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float)
- `default` — Необязательно. Значение по умолчанию, которое возвращается, если не удалось выполнить разбор. [`UInt256`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT toUInt256OrDefault('-256', CAST('0', 'UInt256'))

```


```
0

```


```
SELECT toUInt256OrDefault('abc', CAST('0', 'UInt256'))

```


```
0

```


## toUInt256OrNull

- Строковые представления значений (U)Int*.
- Строковые представления значений Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toUInt256OrNull('0xc0fe');`.
- [`toUInt256`](#toUInt256).
- [`toUInt256OrZero`](#toUInt256OrZero).
- [`toUInt256OrDefault`](#toUInt256OrDefault).

```
toUInt256OrNull(x)

```

- `x` — строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    toUInt256OrNull('256'),
    toUInt256OrNull('abc')
FORMAT Vertical

```


```
Row 1:
──────
toUInt256OrNull('256'): 256
toUInt256OrNull('abc'): \N

```


## toUInt256OrZero

- Строковые представления (U)Int*.
- Строковые представления значений Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toUInt256OrZero('0xc0fe');`.
- [`toUInt256`](#toUInt256).
- [`toUInt256OrNull`](#toUInt256OrNull).
- [`toUInt256OrDefault`](#toUInt256OrDefault).

```
toUInt256OrZero(x)

```

- `x` — Строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    toUInt256OrZero('256'),
    toUInt256OrZero('abc')
FORMAT Vertical

```


```
Row 1:
──────
toUInt256OrZero('256'): 256
toUInt256OrZero('abc'): 0

```


## toUInt32

- Значения или строковые представления типа (U)Int*.
- Значения типа Float*.
- Строковые представления значений Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toUInt32('0xc0fe');`.
- [`toUInt32OrZero`](#toUInt32OrZero).
- [`toUInt32OrNull`](#toUInt32OrNull).
- [`toUInt32OrDefault`](#toUInt32OrDefault).

```
toUInt32(expr)

```

- `expr` — выражение, возвращающее число или строковое представление числа. [`Выражение`](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/expression)

```
SELECT
    toUInt32(32),
    toUInt32(32.32),
    toUInt32('32')
FORMAT Vertical

```


```
Row 1:
──────
toUInt32(32):    32
toUInt32(32.32): 32
toUInt32('32'):  32

```


## toUInt32OrDefault


```
toUInt32OrDefault(expr[, default])

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint), или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float)
- `default` — Необязательно. Значение по умолчанию, которое возвращается, если parsing завершается неуспешно. [`UInt32`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT toUInt32OrDefault('32', CAST('0', 'UInt32'))

```


```
32

```


```
SELECT toUInt32OrDefault('abc', CAST('0', 'UInt32'))

```


```
0

```


## toUInt32OrNull

- Строковые представления (U)Int8/16/32/128/256.
- Строковые представления значений Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toUInt32OrNull('0xc0fe');`.
- [`toUInt32`](#toUInt32).
- [`toUInt32OrZero`](#toUInt32OrZero).
- [`toUInt32OrDefault`](#toUInt32OrDefault).

```
toUInt32OrNull(x)

```

- `x` — Строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    toUInt32OrNull('32'),
    toUInt32OrNull('abc')
FORMAT Vertical

```


```
Row 1:
──────
toUInt32OrNull('32'):  32
toUInt32OrNull('abc'): \N

```


## toUInt32OrZero

- Строковые представления (U)Int8/16/32/128/256.
- Строковые представления значений Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toUInt32OrZero('0xc0fe');`.
- [`toUInt32`](#toUInt32).
- [`toUInt32OrNull`](#toUInt32OrNull).
- [`toUInt32OrDefault`](#toUInt32OrDefault).

```
toUInt32OrZero(x)

```

- `x` — строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    toUInt32OrZero('32'),
    toUInt32OrZero('abc')
FORMAT Vertical

```


```
Row 1:
──────
toUInt32OrZero('32'):  32
toUInt32OrZero('abc'): 0

```


## toUInt64

- Значения или строковые представления типа (U)Int*.
- Значения типа Float*.
- Строковые представления значений Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toUInt64('0xc0fe');`.
- [`toUInt64OrZero`](#toUInt64OrZero).
- [`toUInt64OrNull`](#toUInt64OrNull).
- [`toUInt64OrDefault`](#toUInt64OrDefault).

```
toUInt64(expr)

```

- `expr` — Выражение, возвращающее число или его строковое представление. [`Выражение`](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/expression)

```
SELECT
    toUInt64(64),
    toUInt64(64.64),
    toUInt64('64')
FORMAT Vertical

```


```
Row 1:
──────
toUInt64(64):    64
toUInt64(64.64): 64
toUInt64('64'):  64

```


## toUInt64OrDefault


```
toUInt64OrDefault(expr[, default])

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float)
- `default` — Необязательно. Значение по умолчанию, которое возвращается, если преобразование не удалось. [`UInt64`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT toUInt64OrDefault('64', CAST('0', 'UInt64'))

```


```
64

```


```
SELECT toUInt64OrDefault('abc', CAST('0', 'UInt64'))

```


```
0

```


## toUInt64OrNull

- Строковые представления (U)Int*.
- Строковые представления значений Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toUInt64OrNull('0xc0fe');`.
- [`toUInt64`](#toUInt64).
- [`toUInt64OrZero`](#toUInt64OrZero).
- [`toUInt64OrDefault`](#toUInt64OrDefault).

```
toUInt64OrNull(x)

```

- `x` — строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    toUInt64OrNull('64'),
    toUInt64OrNull('abc')
FORMAT Vertical

```


```
Row 1:
──────
toUInt64OrNull('64'):  64
toUInt64OrNull('abc'): \N

```


## toUInt64OrZero

- Строковые представления (U)Int*.
- Строковые представления значений Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например: `SELECT toUInt64OrZero('0xc0fe');`.
- [`toUInt64`](#toUInt64).
- [`toUInt64OrNull`](#toUInt64OrNull).
- [`toUInt64OrDefault`](#toUInt64OrDefault).

```
toUInt64OrZero(x)

```

- `x` — Строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    toUInt64OrZero('64'),
    toUInt64OrZero('abc')
FORMAT Vertical

```


```
Row 1:
──────
toUInt64OrZero('64'):  64
toUInt64OrZero('abc'): 0

```


## toUInt8

- Значения или строковые представления типа (U)Int*.
- Значения типа Float*.
- Строковые представления значений типа Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toUInt8('0xc0fe');`.
- [`toUInt8OrZero`](#toUInt8OrZero).
- [`toUInt8OrNull`](#toUInt8OrNull).
- [`toUInt8OrDefault`](#toUInt8OrDefault).

```
toUInt8(expr)

```

- `expr` — выражение, возвращающее число или строковое представление числа. [`Выражение`](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/expression)

```
SELECT
    toUInt8(8),
    toUInt8(8.8),
    toUInt8('8')
FORMAT Vertical

```


```
Row 1:
──────
toUInt8(8):   8
toUInt8(8.8): 8
toUInt8('8'): 8

```


## toUInt8OrDefault


```
toUInt8OrDefault(expr[, default])

```

- `expr` — Выражение, возвращающее число или строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint), или [`Float*`](https://clickhouse.com/docs/ru/reference/data-types/float)
- `default` — Необязательно. Значение по умолчанию, которое возвращается, если разбор не удался. [`UInt8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT toUInt8OrDefault('8', CAST('0', 'UInt8'))

```


```
8

```


```
SELECT toUInt8OrDefault('abc', CAST('0', 'UInt8'))

```


```
0

```


## toUInt8OrNull

- Строковые представления (U)Int8/16/32/128/256.
- Строковые представления обычных значений типа Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toUInt8OrNull('0xc0fe');`.
- [`toUInt8`](#toUInt8).
- [`toUInt8OrZero`](#toUInt8OrZero).
- [`toUInt8OrDefault`](#toUInt8OrDefault).

```
toUInt8OrNull(x)

```

- `x` — строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    toUInt8OrNull('42'),
    toUInt8OrNull('abc')
FORMAT Vertical

```


```
Row 1:
──────
toUInt8OrNull('42'):  42
toUInt8OrNull('abc'): \N

```


## toUInt8OrZero

- Строковые представления (U)Int8/16/32/128/256.
- Строковые представления обычных значений Float*, включая `NaN` и `Inf`.
- Строковые представления двоичных и шестнадцатеричных значений, например `SELECT toUInt8OrZero('0xc0fe');`.
- [`toUInt8`](#toUInt8).
- [`toUInt8OrNull`](#toUInt8OrNull).
- [`toUInt8OrDefault`](#toUInt8OrDefault).

```
toUInt8OrZero(x)

```

- `x` — строковое представление числа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    toUInt8OrZero('-8'),
    toUInt8OrZero('abc')
FORMAT Vertical

```


```
Row 1:
──────
toUInt8OrZero('-8'):  0
toUInt8OrZero('abc'): 0

```


## toUUID


```
toUUID(string)

```

- `string` — UUID в строковом формате. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring)

```
SELECT toUUID('61f0c404-5cb3-11e7-907b-a6006ad3dba0') AS uuid

```


```
┌─────────────────────────────────uuid─┐
│ 61f0c404-5cb3-11e7-907b-a6006ad3dba0 │
└──────────────────────────────────────┘

```


## toUUIDOrZero

- Строковые представления UUID в стандартном формате (8-4-4-4-12 шестнадцатеричных цифр).
- Строковые представления UUID без дефисов (32 шестнадцатеричные цифры).
- Недопустимые строковые форматы.
- Типы, отличные от строковых.

```
toUUIDOrZero(x)

```

- `x` — строковое представление UUID. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    toUUIDOrZero('550e8400-e29b-41d4-a716-446655440000') AS valid_uuid,
    toUUIDOrZero('invalid-uuid') AS invalid_uuid

```


```
┌─valid_uuid───────────────────────────┬─invalid_uuid─────────────────────────┐
│ 550e8400-e29b-41d4-a716-446655440000 │ 00000000-0000-0000-0000-000000000000 │
└──────────────────────────────────────┴──────────────────────────────────────┘

```


## toUnixTimestamp64Micro


```
toUnixTimestamp64Micro(value)

```

- `value` — значение типа DateTime64 с любой точностью. [`DateTime64`](https://clickhouse.com/docs/ru/reference/data-types/datetime64)

```
WITH toDateTime64('2025-02-13 23:31:31.011123', 6, 'UTC') AS dt64
SELECT toUnixTimestamp64Micro(dt64);

```


```
┌─toUnixTimestamp64Micro(dt64)─┐
│             1739489491011123 │
└──────────────────────────────┘

```


## toUnixTimestamp64Milli


```
toUnixTimestamp64Milli(value)

```

- `value` — значение типа DateTime64 с любой точностью. [`DateTime64`](https://clickhouse.com/docs/ru/reference/data-types/datetime64)

```
WITH toDateTime64('2025-02-13 23:31:31.011', 3, 'UTC') AS dt64
SELECT toUnixTimestamp64Milli(dt64);

```


```
┌─toUnixTimestamp64Milli(dt64)─┐
│                1739489491011 │
└──────────────────────────────┘

```


## toUnixTimestamp64Nano


```
toUnixTimestamp64Nano(value)

```

- `value` — значение типа DateTime64 с любой точностью. [`DateTime64`](https://clickhouse.com/docs/ru/reference/data-types/datetime64)

```
WITH toDateTime64('2025-02-13 23:31:31.011123456', 9, 'UTC') AS dt64
SELECT toUnixTimestamp64Nano(dt64);

```


```
┌─toUnixTimestamp64Nano(dt64)────┐
│            1739489491011123456 │
└────────────────────────────────┘

```


## toUnixTimestamp64Second


```
toUnixTimestamp64Second(value)

```

- `value` — значение типа DateTime64 с любой точностью. [`DateTime64`](https://clickhouse.com/docs/ru/reference/data-types/datetime64)

```
WITH toDateTime64('2025-02-13 23:31:31.011', 3, 'UTC') AS dt64
SELECT toUnixTimestamp64Second(dt64);

```


```
┌─toUnixTimestamp64Second(dt64)─┐
│                    1739489491 │
└───────────────────────────────┘

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
