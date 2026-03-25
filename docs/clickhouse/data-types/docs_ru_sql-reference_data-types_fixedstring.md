# FixedString(N) | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/sql-reference/data-types/fixedstring

Строка фиксированной длины изNбайт (не в символах и не в кодовых точках).

Чтобы объявить столбец типаFixedString, используйте следующий синтаксис:


```
<column_name> FixedString(N)

```

ГдеN— натуральное число.

ТипFixedStringэффективен, когда данные имеют длину ровноNбайт. Во всех остальных случаях он, скорее всего, снизит эффективность.

Примеры значений, которые могут эффективно храниться в столбцах типаFixedString:

- Бинарное представление IP-адресов (FixedString(16)для IPv6).
- Коды языков (ru_RU, en_US ... ).
- Коды валют (USD, RUB ... ).
- Бинарное представление хешей (FixedString(16)для MD5,FixedString(32)для SHA256).
Для хранения значений UUID используйте тип данныхUUID.

При вставке данных ClickHouse:

- Дополняет строку нулевыми байтами, если строка содержит меньше, чемNбайт.
- Выбрасывает исключениеToo large value for FixedString(N), если строка содержит больше, чемNбайт.
Рассмотрим следующую таблицу с единственным столбцом типаFixedString(2):


```


INSERT INTO FixedStringTable VALUES ('a'), ('ab'), ('');

```


```
SELECT
    name,
    toTypeName(name),
    length(name),
    empty(name)
FROM FixedStringTable;

```


```
┌─name─┬─toTypeName(name)─┬─length(name)─┬─empty(name)─┐
│ a    │ FixedString(2)   │            2 │           0 │
│ ab   │ FixedString(2)   │            2 │           0 │
│      │ FixedString(2)   │            2 │           1 │
└──────┴──────────────────┴──────────────┴─────────────┘

```

Обратите внимание, что длина значенияFixedString(N)является фиксированной. ФункцияlengthвозвращаетN, даже если значениеFixedString(N)заполнено только нулевыми байтами, однако функцияemptyв этом случае возвращает1.

Выборка данных с предложениемWHEREвозвращает разные результаты в зависимости от того, как сформулировано условие:

- Если используется оператор равенства=или==или функцияequals, ClickHouseнеучитывает символ\0, т.е. запросыSELECT * FROM FixedStringTable WHERE name = 'a';иSELECT * FROM FixedStringTable WHERE name = 'a\0';возвращают один и тот же результат.
- Если используется предложениеLIKE, ClickHouseучитываетсимвол\0, поэтому может потребоваться явно указать символ\0в условии фильтрации.

```
SELECT name
FROM FixedStringTable
WHERE name = 'a'
FORMAT JSONStringsEachRow

{"name":"a\u0000"}


SELECT name
FROM FixedStringTable
WHERE name = 'a\0'
FORMAT JSONStringsEachRow

{"name":"a\u0000"}


SELECT name
FROM FixedStringTable
WHERE name = 'a'
FORMAT JSONStringsEachRow

Query id: c32cec28-bb9e-4650-86ce-d74a1694d79e

{"name":"a\u0000"}


SELECT name
FROM FixedStringTable
WHERE name LIKE 'a'
FORMAT JSONStringsEachRow

0 rows in set.


SELECT name
FROM FixedStringTable
WHERE name LIKE 'a\0'
FORMAT JSONStringsEachRow

{"name":"a\u0000"}

```
