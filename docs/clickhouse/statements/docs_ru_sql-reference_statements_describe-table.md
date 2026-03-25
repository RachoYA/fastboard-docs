# DESCRIBE TABLE | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/sql-reference/statements/describe-table

Возвращает информацию о столбцах таблицы.

Синтаксис


```
DESC|DESCRIBE TABLE [db.]table [INTO OUTFILE filename] [FORMAT format]

```

ОператорDESCRIBEвозвращает строку для каждого столбца таблицы со следующими значениями типаString:

- name— имя столбца.
- type— тип столбца.
- default_type— клауза, используемая ввыражении по умолчаниюстолбца:DEFAULT,MATERIALIZEDилиALIAS. Если выражение по умолчанию отсутствует, возвращается пустая строка.
- default_expression— выражение, указанное после клаузыDEFAULT.
- comment—комментарий столбца.
- codec_expression—кодек, применяемый к столбцу.
- ttl_expression— выражениеTTL.
- is_subcolumn— флаг, равный1для внутренних подстолбцов. Включается в результат только в том случае, если описание подстолбцов включено настройкойdescribe_include_subcolumns.
Все столбцы в структурах данныхNestedописываются отдельно. Имя каждого столбца предваряется именем родительского столбца и точкой.

Чтобы показать внутренние подстолбцы других типов данных, используйте настройкуdescribe_include_subcolumns.

Пример

Запрос:


```
CREATE TABLE describe_example (
    id UInt64, text String DEFAULT 'unknown' CODEC(ZSTD),
    user Tuple (name String, age UInt8)
) ENGINE = MergeTree() ORDER BY id;

DESCRIBE TABLE describe_example;
DESCRIBE TABLE describe_example SETTINGS describe_include_subcolumns=1;

```

Результат:


```
┌─name─┬─type──────────────────────────┬─default_type─┬─default_expression─┬─comment─┬─codec_expression─┬─ttl_expression─┐
│ id   │ UInt64                        │              │                    │         │                  │                │
│ text │ String                        │ DEFAULT      │ 'unknown'          │         │ ZSTD(1)          │                │
│ user │ Tuple(name String, age UInt8) │              │                    │         │                  │                │
└──────┴───────────────────────────────┴──────────────┴────────────────────┴─────────┴──────────────────┴────────────────┘

```

Второй запрос дополнительно показывает подстолбцы:


```
┌─name──────┬─type──────────────────────────┬─default_type─┬─default_expression─┬─comment─┬─codec_expression─┬─ttl_expression─┬─is_subcolumn─┐
│ id        │ UInt64                        │              │                    │         │                  │                │            0 │
│ text      │ String                        │ DEFAULT      │ 'unknown'          │         │ ZSTD(1)          │                │            0 │
│ user      │ Tuple(name String, age UInt8) │              │                    │         │                  │                │            0 │
│ user.name │ String                        │              │                    │         │                  │                │            1 │
│ user.age  │ UInt8                         │              │                    │         │                  │                │            1 │
└───────────┴───────────────────────────────┴──────────────┴────────────────────┴─────────┴──────────────────┴────────────────┴──────────────┘

```

Оператор DESCRIBE можно также использовать с подзапросами и скалярными выражениями:


```
DESCRIBE SELECT 1 FORMAT TSV;

```

или


```
DESCRIBE (SELECT 1) FORMAT TSV;

```

Результат:


```
1       UInt8

```

При таком использовании возвращаются метаданные о результирующих столбцах указанного запроса или подзапроса. Это полезно для понимания структуры сложных запросов до их выполнения.

См. также

- Параметрdescribe_include_subcolumns.