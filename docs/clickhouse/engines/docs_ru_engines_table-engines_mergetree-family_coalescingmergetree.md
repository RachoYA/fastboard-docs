# Движок таблицы CoalescingMergeTree | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/engines/table-engines/mergetree-family/coalescingmergetree

Этот движок таблицы доступен начиная с версии 25.6 как в OSS, так и в Cloud.

Этот движок наследуется отMergeTree. Ключевое отличие заключается в том, как сливаются части данных: для таблицCoalescingMergeTreeClickHouse заменяет все строки с одинаковым первичным ключом (или, точнее, с одинаковымключом сортировки) одной строкой, содержащей последние значения, отличные от NULL, для каждого столбца.

Это позволяет выполнять upsert-операции на уровне отдельных столбцов, то есть вы можете обновлять только отдельные столбцы, а не целые строки.

CoalescingMergeTreeпредназначен для использования с типами Nullable в неклю́чевых столбцах. Если столбцы не являются Nullable, поведение такое же, как уReplacingMergeTree.


## Создание таблицы​


```
CREATE TABLE [IF NOT EXISTS] [db.]table_name [ON CLUSTER cluster]
(
    name1 [type1] [DEFAULT|MATERIALIZED|ALIAS expr1],
    name2 [type2] [DEFAULT|MATERIALIZED|ALIAS expr2],
    ...
) ENGINE = CoalescingMergeTree([columns])
[PARTITION BY expr]
[ORDER BY expr]
[SAMPLE BY expr]
[SETTINGS name=value, ...]

```

Описание параметров запроса см. в разделеописание запроса.


### Параметры движка CoalescingMergeTree​


#### Столбцы​

columns— необязательный параметр. Кортеж имен столбцов, значения в которых будут объединены. Указанные столбцы не должны входить в ключ партиционирования или сортировки. Еслиcolumnsне указан, ClickHouse объединяет значения во всех столбцах, которые не входят в ключ сортировки.


### Части запроса​

При создании таблицыCoalescingMergeTreeтребуются те жечасти запроса, что и при создании таблицыMergeTree.

Не используйте этот метод в новых проектах и, по возможности, переведите старые проекты на метод, описанный выше.


```
CREATE TABLE [IF NOT EXISTS] [db.]table_name [ON CLUSTER cluster]
(
  name1 [type1] [DEFAULT|MATERIALIZED|ALIAS expr1],
  name2 [type2] [DEFAULT|MATERIALIZED|ALIAS expr2],
  ...
) ENGINE [=] CoalescingMergeTree(date-column [, sampling_expression], (primary, key), index_granularity, [columns])

```

Все параметры, за исключениемcolumns, имеют то же значение, что и вMergeTree.columns— кортеж имен столбцов, значения которых будут суммироваться. Необязательный параметр. Описание см. в тексте выше.

- columns— кортеж имен столбцов, значения которых будут суммироваться. Необязательный параметр. Описание см. в тексте выше.

## Пример использования​

Рассмотрим следующую таблицу:


```
CREATE TABLE test_table
(
    key UInt64,
    value_int Nullable(UInt32),
    value_string Nullable(String),
    value_date Nullable(Date)
)
ENGINE = CoalescingMergeTree()
ORDER BY key

```

Добавьте в неё данные:


```
INSERT INTO test_table VALUES(1, NULL, NULL, '2025-01-01'), (2, 10, 'test', NULL);
INSERT INTO test_table VALUES(1, 42, 'win', '2025-02-01');
INSERT INTO test_table(key, value_date) VALUES(2, '2025-02-01');

```

Результат будет выглядеть так:


```
SELECT * FROM test_table ORDER BY key;

```


```
┌─key─┬─value_int─┬─value_string─┬─value_date─┐
│   1 │        42 │ win          │ 2025-02-01 │
│   1 │      ᴺᵁᴸᴸ │ ᴺᵁᴸᴸ         │ 2025-01-01 │
│   2 │      ᴺᵁᴸᴸ │ ᴺᵁᴸᴸ         │ 2025-02-01 │
│   2 │        10 │ test         │       ᴺᵁᴸᴸ │
└─────┴───────────┴──────────────┴────────────┘

```

Рекомендуемый запрос для получения корректного окончательного результата:


```
SELECT * FROM test_table FINAL ORDER BY key;

```


```
┌─key─┬─value_int─┬─value_string─┬─value_date─┐
│   1 │        42 │ win          │ 2025-02-01 │
│   2 │        10 │ test         │ 2025-02-01 │
└─────┴───────────┴──────────────┴────────────┘

```

Использование модификатораFINALуказывает ClickHouse применять логику слияния на этапе выполнения запроса, гарантируя получение корректного, объединённого «последнего» значения для каждого столбца. Это самый безопасный и точный метод при выполнении запросов к таблице CoalescingMergeTree.

Подход с использованиемGROUP BYможет возвращать некорректные результаты, если части данных в таблице ещё не были полностью слиты.SELECT key, last_value(value_int), last_value(value_string), last_value(value_date)  FROM test_table GROUP BY key; -- Not recommended.


```
SELECT key, last_value(value_int), last_value(value_string), last_value(value_date)  FROM test_table GROUP BY key; -- Not recommended.

```
