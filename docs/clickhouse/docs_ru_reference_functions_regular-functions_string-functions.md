# Функции для работы со строками - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-functions


## CRC32


```
CRC32(s)

```

- `s` — строка `String`, для которой вычисляется CRC32. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT CRC32('ClickHouse')

```


```
┌─CRC32('ClickHouse')─┐
│          1538217360 │
└─────────────────────┘

```


## CRC32IEEE


```
CRC32IEEE(s)

```

- `s` — строка, для которой вычисляется CRC32. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT CRC32IEEE('ClickHouse');

```


```
┌─CRC32IEEE('ClickHouse')─┐
│              3089448422 │
└─────────────────────────┘

```


## CRC64


```
CRC64(s)

```

- `s` — строка, для которой вычисляется CRC64. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT CRC64('ClickHouse');

```


```
┌──CRC64('ClickHouse')─┐
│ 12126588151325169346 │
└──────────────────────┘

```


## appendTrailingCharIfAbsent


```
appendTrailingCharIfAbsent(s, c)

```

- `s` — Входная строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `c` — Символ, который нужно добавить, если он отсутствует. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT appendTrailingCharIfAbsent('https://example.com', '/');

```


```
┌─appendTraili⋯.com', '/')─┐
│ https://example.com/     │
└──────────────────────────┘

```


## ascii


```
ascii(s)

```

- `s` — Входная строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT ascii('234')

```


```
┌─ascii('234')─┐
│           50 │
└──────────────┘

```


## base32Decode


```
base32Decode(encoded)

```

- `encoded` — столбец типа String или константа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT base32Decode('IVXGG33EMVSA====');

```


```
┌─base32Decode('IVXGG33EMVSA====')─┐
│ Encoded                          │
└──────────────────────────────────┘

```


## base32Encode


```
base32Encode(plaintext)

```

- `plaintext` — Открытый текст, который нужно закодировать. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT base32Encode('Encoded')

```


```
┌─base32Encode('Encoded')─┐
│ IVXGG33EMVSA====        │
└─────────────────────────┘

```


## base58Decode


```
base58Decode(encoded[, expected_size])

```

- `encoded` — Столбец или константа типа String для декодирования. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `expected_size` — Необязательно. Ожидаемый размер результата декодирования в байтах. Если указано 32 или 64, используется оптимизированный декодер; для остальных значений используется универсальный декодер. [`UInt8, UInt16, UInt32, or UInt64`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT base58Decode('JxF12TrwUP45BMd');

```


```
┌─base58Decode⋯rwUP45BMd')─┐
│ Hello World              │
└──────────────────────────┘

```


## base58Encode


```
base58Encode(plaintext)

```

- `plaintext` — Открытый текст, который нужно закодировать. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT base58Encode('ClickHouse');

```


```
┌─base58Encode('ClickHouse')─┐
│ 4nhk8K7GHXf6zx             │
└────────────────────────────┘

```


## base64Decode


```
base64Decode(encoded)

```

- `encoded` — столбец типа String или константа для декодирования. Если строка некорректно закодирована в Base64, генерируется исключение. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT base64Decode('Y2xpY2tob3VzZQ==')

```


```
┌─base64Decode('Y2xpY2tob3VzZQ==')─┐
│ clickhouse                       │
└──────────────────────────────────┘

```


## base64Encode


```
base64Encode(plaintext)

```

- `plaintext` — столбец или константа с открытым текстом для декодирования. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT base64Encode('clickhouse')

```


```
┌─base64Encode('clickhouse')─┐
│ Y2xpY2tob3VzZQ==           │
└────────────────────────────┘

```


## base64URLDecode


```
base64URLDecode(encoded)

```

- `encoded` — столбец типа String или константа для кодирования. Если строка закодирована в Base64 некорректно, будет сгенерировано исключение. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT base64URLDecode('aHR0cHM6Ly9jbGlja2hvdXNlLmNvbQ')

```


```
┌─base64URLDecode('aHR0cHM6Ly9jbGlja2hvdXNlLmNvbQ')─┐
│ https://clickhouse.com                            │
└───────────────────────────────────────────────────┘

```


## base64URLEncode


```
base64URLEncode(plaintext)

```

- `plaintext` — столбец или константа с открытым текстом для кодирования. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT base64URLEncode('https://clickhouse.com')

```


```
┌─base64URLEncode('https://clickhouse.com')─┐
│ aHR0cHM6Ly9jbGlja2hvdXNlLmNvbQ            │
└───────────────────────────────────────────┘

```


## basename


```
basename(expr)

```

- `expr` — Строковое выражение. Обратные косые черты должны быть экранированы. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT 'some/long/path/to/file' AS a, basename(a)

```


```
┌─a──────────────────────┬─basename('some/long/path/to/file')─┐
│ some/long/path/to/file │ file                               │
└────────────────────────┴────────────────────────────────────┘

```


```
SELECT 'some\\long\\path\\to\\file' AS a, basename(a)

```


```
┌─a──────────────────────┬─basename('some\\long\\path\\to\\file')─┐
│ some\long\path\to\file │ file                                   │
└────────────────────────┴────────────────────────────────────────┘

```


```
SELECT 'some-file-name' AS a, basename(a)

```


```
┌─a──────────────┬─basename('some-file-name')─┐
│ some-file-name │ some-file-name             │
└────────────────┴────────────────────────────┘

```


## byteHammingDistance


```
byteHammingDistance(s1, s2)

```

- `s1` — Первая строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `s2` — Вторая строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT byteHammingDistance('karolin', 'kathrin')

```


```
┌─byteHammingDistance('karolin', 'kathrin')─┐
│                                         3 │
└───────────────────────────────────────────┘

```


## caseFoldUTF8


```
caseFoldUTF8(str)

```

- `str` — входная строка в кодировке UTF-8. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT caseFoldUTF8('Straße')

```


```
┌─caseFoldUTF8('Straße')─┐
│ strasse                │
└────────────────────────┘

```


## compareSubstrings


```
compareSubstrings(s1, s2, s1_offset, s2_offset, num_bytes)

```

- `s1` — Первая строка для сравнения. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `s2` — Вторая строка для сравнения. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `s1_offset` — Позиция в `s1` (с нумерацией с нуля), с которой начинается сравнение. [`UInt*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `s2_offset` — Позиция в `s2` (с нумерацией с нуля), с которой начинается сравнение. [`UInt*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `num_bytes` — Максимальное количество байтов для сравнения в обеих строках. Если `s1_offset` (или `s2_offset`) + `num_bytes` превышает длину входной строки, значение `num_bytes` будет соответственно уменьшено. [`UInt*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `-1`, если `s1`[`s1_offset` : `s1_offset` + `num_bytes`] < `s2`[`s2_offset` : `s2_offset` + `num_bytes`].
- `0`, если `s1`[`s1_offset` : `s1_offset` + `num_bytes`] = `s2`[`s2_offset` : `s2_offset` + `num_bytes`].
- `1`, если `s1`[`s1_offset` : `s1_offset` + `num_bytes`] > `s2`[`s2_offset` : `s2_offset` + `num_bytes`]. [`Int8`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT compareSubstrings('Saxony', 'Anglo-Saxon', 0, 6, 5) AS result

```


```
┌─result─┐
│      0 │
└────────┘

```


## concat


```
concat([s1, s2, ...])

```

- `s1, s2, ...` — Любое количество значений произвольного типа. [`Any`](https://clickhouse.com/docs/ru/reference/data-types/index)

```
SELECT concat('Hello, ', 'World!')

```


```
┌─concat('Hello, ', 'World!')─┐
│ Hello, World!               │
└─────────────────────────────┘

```


```
SELECT concat(42, 144)

```


```
┌─concat(42, 144)─┐
│ 42144           │
└─────────────────┘

```


## concatAssumeInjective


```
concatAssumeInjective([s1, s2, ...])

```

- `s1, s2, ...` — Любое количество значений произвольного типа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring)

```
SELECT concat(key1, key2), sum(value) FROM key_val GROUP BY concatAssumeInjective(key1, key2)

```


```
┌─concat(key1, key2)─┬─sum(value)─┐
│ Hello, World!      │          3 │
│ Hello, World!      │          2 │
│ Hello, World       │          3 │
└────────────────────┴────────────┘

```


## concatWithSeparator


```
concatWithSeparator(sep[, exp1, exp2, ...])

```

- `sep` — Разделитель, который будет использоваться. [`const String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`const FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring)
- `exp1, exp2, ...` — Выражения для объединения. Аргументы, не имеющие тип `String` или `FixedString`, преобразуются в строки с использованием сериализации по умолчанию. Поскольку это снижает производительность, использовать аргументы не типа `String`/`FixedString` не рекомендуется. [`Any`](https://clickhouse.com/docs/ru/reference/data-types/index)

```
SELECT concatWithSeparator('a', '1', '2', '3', '4')

```


```
┌─concatWithSeparator('a', '1', '2', '3', '4')─┐
│ 1a2a3a4                                      │
└──────────────────────────────────────────────┘

```


## concatWithSeparatorAssumeInjective


```
concatWithSeparatorAssumeInjective(sep[, exp1, exp2, ... ])

```

- `sep` — Используемый разделитель. [`const String`](https://clickhouse.com/docs/ru/reference/data-types/string) or [`const FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring)
- `exp1, exp2, ...` — Выражения для объединения. Аргументы типа, отличного от `String` или `FixedString`, преобразуются в строки с использованием сериализации по умолчанию. Поскольку это снижает производительность, использовать аргументы не типа `String`/`FixedString` не рекомендуется. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) or [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring)

```
CREATE TABLE user_data (
user_id UInt32,
first_name String,
last_name String,
score UInt32
)
ENGINE = MergeTree
ORDER BY tuple();

INSERT INTO user_data VALUES
(1, 'John', 'Doe', 100),
(2, 'Jane', 'Smith', 150),
(3, 'John', 'Wilson', 120),
(4, 'Jane', 'Smith', 90);

SELECT
    concatWithSeparatorAssumeInjective('-', first_name, last_name) as full_name,
    sum(score) as total_score
FROM user_data
GROUP BY concatWithSeparatorAssumeInjective('-', first_name, last_name);

```


```
┌─full_name───┬─total_score─┐
│ Jane-Smith  │         240 │
│ John-Doe    │         100 │
│ John-Wilson │         120 │
└─────────────┴─────────────┘

```


## conv


```
conv(number, from_base, to_base)

```

- `number` — Число, которое нужно преобразовать. Может быть строкой или числовым типом. - `from_base` — Исходное основание системы счисления (2-36). Должно быть целым числом. - `to_base` — Целевое основание системы счисления (2-36). Должно быть целым числом.

```
SELECT conv('10', 10, 2)

```


```
1010

```


```
SELECT conv('FF', 16, 10)

```


```
255

```


```
SELECT conv('-1', 10, 16)

```


```
FFFFFFFFFFFFFFFF

```


```
SELECT conv('1010', 2, 8)

```


```
12

```


## convertCharset


```
convertCharset(s, from, to)

```

- `s` — Входная строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `from` — Исходная кодировка символов. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `to` — Целевая кодировка символов. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT convertCharset('Café', 'UTF-8', 'ISO-8859-1');

```


```
┌─convertChars⋯SO-8859-1')─┐
│ Caf�                     │
└──────────────────────────┘

```


## damerauLevenshteinDistance


```
damerauLevenshteinDistance(s1, s2)

```

- `s1` — Первая входная строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `s2` — Вторая входная строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT damerauLevenshteinDistance('clickhouse', 'mouse')

```


```
┌─damerauLevenshteinDistance('clickhouse', 'mouse')─┐
│                                                 6 │
└───────────────────────────────────────────────────┘

```


## decodeHTMLComponent


```
decodeHTMLComponent(s)

```

- `s` — строка, содержащая HTML-сущности для декодирования. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT decodeHTMLComponent('&lt;div&gt;Hello &amp; &quot;World&quot;&lt;/div&gt;')

```


```
┌─decodeHTMLComponent('&lt;div&gt;Hello &amp; &quot;World&quot;&lt;/div&gt;')─┐
│ <div>Hello & "World"</div>                                                  │
└─────────────────────────────────────────────────────────────────────────────┘

```


## decodeXMLComponent


```
decodeXMLComponent(s)

```

- `s` — Строка, содержащая XML-сущности, которые нужно декодировать. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT decodeXMLComponent('&lt;tag&gt;Hello &amp; World&lt;/tag&gt;')

```


```
┌─decodeXMLCom⋯;/tag&gt;')─┐
│ <tag>Hello & World</tag> │
└──────────────────────────┘

```


## editDistance


```
editDistance(s1, s2)

```

- `s1` — Первая входная строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `s2` — Вторая входная строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT editDistance('clickhouse', 'mouse')

```


```
┌─editDistance('clickhouse', 'mouse')─┐
│                                   6 │
└─────────────────────────────────────┘

```


## editDistanceUTF8


```
editDistanceUTF8(s1, s2)

```

- `s1` — Первая входная строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `s2` — Вторая входная строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT editDistanceUTF8('我是谁', '我是我') AS distance

```


```
┌─distance─┐
│        1 │
└──────────┘

```


## encodeXMLComponent


```
encodeXMLComponent(s)

```

- `s` — строка для экранирования. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    '<tag>Hello & "World"</tag>' AS original,
    encodeXMLComponent('<tag>Hello & "World"</tag>') AS xml_encoded;

```


```
┌─original───────────────────┬─xml_encoded──────────────────────────────────────────┐
│ <tag>Hello & "World"</tag> │ &lt;tag&gt;Hello &amp; &quot;World&quot;&lt;/tag&gt; │
└────────────────────────────┴──────────────────────────────────────────────────────┘

```


## endsWith


```
endsWith(s, suffix)

```

- `s` — Проверяемая строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `suffix` — Проверяемый суффикс. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT endsWith('ClickHouse', 'House');

```


```
┌─endsWith('Cl⋯', 'House')─┐
│                        1 │
└──────────────────────────┘

```


## endsWithCaseInsensitive


```
endsWithCaseInsensitive(s, suffix)

```

- `s` — Строка для проверки. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `suffix` — Регистронезависимый суффикс для проверки. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT endsWithCaseInsensitive('ClickHouse', 'HOUSE');

```


```
┌─endsWithCaseInsensitive('Cl⋯', 'HOUSE')─┐
│                                       1 │
└─────────────────────────────────────────┘

```


## endsWithCaseInsensitiveUTF8


```
endsWithCaseInsensitiveUTF8(s, suffix)

```

- `s` — проверяемая строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `suffix` — регистронезависимый суффикс для проверки. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT endsWithCaseInsensitiveUTF8('данных', 'ых');

```


```
┌─endsWithCaseInsensitiveUTF8('данных', 'ых')─┐
│                                           1 │
└─────────────────────────────────────────────┘

```


## endsWithUTF8


```
endsWithUTF8(s, suffix)

```

- `s` — Проверяемая строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `suffix` — Проверяемый суффикс. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT endsWithUTF8('данных', 'ых');

```


```
┌─endsWithUTF8('данных', 'ых')─┐
│                            1 │
└──────────────────────────────┘

```


## extractTextFromHTML

- Удаление всех HTML/XML-тегов
- Удаление комментариев (`{/* */}`)
- Удаление элементов script и style вместе с их содержимым
- Обработку секций CDATA (копируются дословно)
- Корректную обработку и нормализацию пробельных символов

```
extractTextFromHTML(html)

```

- `html` — `String`, содержащая HTML-контент, из которого нужно извлечь текст. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT extractTextFromHTML('
<html>
    <head><title>Page Title</title></head>
    <body>
        <p>Hello <b>World</b>!</p>
        <script>alert("test");</script>
        <!-- comment -->
    </body>
</html>
');

```


```
┌─extractTextFromHTML('<html><head>...')─┐
│ Page Title Hello World!                │
└────────────────────────────────────────┘

```


## firstLine


```
firstLine(s)

```

- `s` — Входная строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT firstLine('foo\\nbar\\nbaz')

```


```
┌─firstLine('foo\nbar\nbaz')─┐
│ foo                        │
└────────────────────────────┘

```


## idnaDecode


```
idnaDecode(s)

```

- `s` — входная строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT idnaDecode('xn--strae-oqa.xn--mnchen-3ya.de')

```


```
┌─idnaDecode('xn--strae-oqa.xn--mnchen-3ya.de')─┐
│ straße.münchen.de                             │
└───────────────────────────────────────────────┘

```


## idnaEncode


```
idnaEncode(s)

```

- `s` — Входная строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT idnaEncode('straße.münchen.de')

```


```
┌─idnaEncode('straße.münchen.de')─────┐
│ xn--strae-oqa.xn--mnchen-3ya.de     │
└─────────────────────────────────────┘

```


## initcap


```
initcap(s)

```

- `s` — Входная строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT initcap('building for fast')

```


```
┌─initcap('building for fast')─┐
│ Building For Fast            │
└──────────────────────────────┘

```


```
SELECT initcap('John''s cat won''t eat.');

```


```
┌─initcap('Joh⋯n\'t eat.')─┐
│ John'S Cat Won'T Eat.    │
└──────────────────────────┘

```


## initcapUTF8


```
initcapUTF8(s)

```

- `s` — Входная строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT initcapUTF8('не тормозит')

```


```
┌─initcapUTF8('не тормозит')─┐
│ Не Тормозит                │
└────────────────────────────┘

```


## isValidASCII


```
isValidASCII(str)

```

- Отсутствуют.

```
SELECT isValidASCII('hello') AS is_ascii, isValidASCII('你好') AS is_not_ascii

```


## isValidUTF8


```
isValidUTF8(s)

```

- `s` — Строка, которую нужно проверить на корректность UTF-8. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT isValidUTF8('\\xc3\\xb1') AS valid, isValidUTF8('\\xc3\\x28') AS invalid

```


```
┌─valid─┬─invalid─┐
│     1 │       0 │
└───────┴─────────┘

```


## jaroSimilarity


```
jaroSimilarity(s1, s2)

```

- `s1` — Первая входная строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `s2` — Вторая входная строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT jaroSimilarity('clickhouse', 'click')

```


```
┌─jaroSimilarity('clickhouse', 'click')─┐
│                    0.8333333333333333 │
└───────────────────────────────────────┘

```


## jaroWinklerSimilarity


```
jaroWinklerSimilarity(s1, s2)

```

- `s1` — Первая входная строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `s2` — Вторая входная строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT jaroWinklerSimilarity('clickhouse', 'click')

```


```
┌─jaroWinklerSimilarity('clickhouse', 'click')─┐
│                           0.8999999999999999 │
└──────────────────────────────────────────────┘

```


## left


```
left(s, offset)

```

- `s` — Строка, из которой извлекается подстрока. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring)
- `offset` — Смещение в байтах. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- Для положительного `offset` — подстроку строки `s` длиной `offset` байт, начиная слева.
- Для отрицательного `offset` — подстроку строки `s` длиной `length(s) - |offset|` байт, начиная слева.
- Пустую строку, если `length` равно `0`. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT left('Hello World', 5)

```


```
Hello

```


```
SELECT left('Hello World', -6)

```


```
Hello

```


## leftPad


```
leftPad(string, length[, pad_string])

```

- `string` — Входная строка, которую нужно дополнить. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `length` — Длина результирующей строки. Если значение меньше длины входной строки, входная строка усекается до `length` символов. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `pad_string` — Необязательно. Строка, используемая для дополнения входной строки. Если не указана, входная строка дополняется пробелами. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT leftPad('abc', 7, '*'), leftPad('def', 7)

```


```
┌─leftPad('abc', 7, '*')─┬─leftPad('def', 7)─┐
│ ****abc                │     def           │
└────────────────────────┴───────────────────┘

```


## leftPadUTF8


```
leftPadUTF8(string, length[, pad_string])

```

- `string` — Входная строка, которую нужно дополнить. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `length` — Длина результирующей строки. Если это значение меньше длины входной строки, она укорачивается до `length` символов. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `pad_string` — Необязательно. Строка, которой дополняется входная строка. Если не указана, входная строка дополняется пробелами. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT leftPadUTF8('абвг', 7, '*'), leftPadUTF8('дежз', 7)

```


```
┌─leftPadUTF8('абвг', 7, '*')─┬─leftPadUTF8('дежз', 7)─┐
│ ***абвг                     │    дежз                │
└─────────────────────────────┴────────────────────────┘

```


## leftUTF8


```
leftUTF8(s, offset)

```

- `s` — Строка в кодировке UTF-8, из которой вычисляется подстрока. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring)
- `offset` — Количество байтов смещения. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- Для положительного `offset` — подстроку `s` длиной `offset` байт, начиная с левой стороны строки.\n”
- Для отрицательного `offset` — подстроку `s` длиной `length(s) - |offset|` байт, начиная с левой стороны строки.\n”
- Пустую строку, если `length` равен 0. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT leftUTF8('Привет', 4)

```


```
Прив

```


```
SELECT leftUTF8('Привет', -4)

```


```
Пр

```


## lengthUTF8


```
lengthUTF8(s)

```

- `s` — строка, содержащая корректный текст в кодировке UTF-8. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT lengthUTF8('Здравствуй, мир!')

```


```
┌─lengthUTF8('Здравствуй, мир!')─┐
│                             16 │
└────────────────────────────────┘

```


## lower


```
lower(s)

```

- `s` — Строка, которую нужно преобразовать в нижний регистр. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT lower('CLICKHOUSE')

```


```
┌─lower('CLICKHOUSE')─┐
│ clickhouse          │
└─────────────────────┘

```


## lowerUTF8


```
lowerUTF8(input)

```

- `input` — Строка, которую нужно преобразовать в нижний регистр. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT lowerUTF8('München') as Lowerutf8;

```


```
münchen

```


## naturalSortKey


```
naturalSortKey(s)

```

- `s` — строка, преобразуемая в ключ естественной сортировки. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT s FROM t ORDER BY naturalSortKey(s)

```


```
┌─s───┐
│ a1  │
│ a02 │
└─────┘

```


## normalizeUTF8NFC


```
normalizeUTF8NFC(str)

```

- `str` — входная строка в кодировке UTF-8. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
'é' AS original, -- e + комбинирующий акут (U+0065 + U+0301)
length(original),
normalizeUTF8NFC('é') AS nfc_normalized, -- é (U+00E9)
length(nfc_normalized);

```


```
┌─original─┬─length(original)─┬─nfc_normalized─┬─length(nfc_normalized)─┐
│ é        │                2 │ é              │                      2 │
└──────────┴──────────────────┴────────────────┴────────────────────────┘

```


## normalizeUTF8NFD


```
normalizeUTF8NFD(str)

```

- `str` — входная строка в кодировке UTF-8. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    'é' AS original, -- é (U+00E9)
    length(original),
    normalizeUTF8NFD('é') AS nfd_normalized, -- e + комбинирующий акут (U+0065 + U+0301)
    length(nfd_normalized);

```


```
┌─original─┬─length(original)─┬─nfd_normalized─┬─length(nfd_normalized)─┐
│ é        │                2 │ é              │                      3 │
└──────────┴──────────────────┴────────────────┴────────────────────────┘

```


## normalizeUTF8NFKC


```
normalizeUTF8NFKC(str)

```

- `str` — входная строка в кодировке UTF-8. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    '① ② ③' AS original,                           -- Circled number characters
    normalizeUTF8NFKC('① ② ③') AS nfkc_normalized  -- Converts to 1 2 3

```


```
┌─original─┬─nfkc_normalized─┐
│ ① ② ③    │ 1 2 3           │
└──────────┴─────────────────┘

```


## normalizeUTF8NFKCCasefold


```
normalizeUTF8NFKCCasefold(str)

```

- `str` — входная строка в кодировке UTF-8. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    'Ä ① Hello' AS original,
    normalizeUTF8NFKCCasefold('Ä ① Hello') AS nfkc_cf_normalized;

```


```
┌─original───┬─nfkc_cf_normalized─┐
│ Ä ① Hello │ ä 1 hello           │
└────────────┴────────────────────┘

```


## normalizeUTF8NFKD


```
normalizeUTF8NFKD(str)

```

- `str` — входная строка в кодировке UTF-8. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT
    'H₂O²' AS original,                           -- H + subscript 2 + O + superscript 2
    normalizeUTF8NFKD('H₂O²') AS nfkd_normalized  -- Converts to H 2 O 2

```


```
┌─original─┬─nfkd_normalized─┐
│ H₂O²     │ H2O2            │
└──────────┴─────────────────┘

```


## punycodeDecode


```
punycodeDecode(s)

```

- `s` — строка, закодированная в Punycode. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT punycodeDecode('Mnchen-3ya')

```


```
┌─punycodeDecode('Mnchen-3ya')─┐
│ München                      │
└──────────────────────────────┘

```


## punycodeEncode


```
punycodeEncode(s)

```

- `s` — Входное значение. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT punycodeEncode('München')

```


```
┌─punycodeEncode('München')─┐
│ Mnchen-3ya                │
└───────────────────────────┘

```


## regexpExtract


```
regexpExtract(haystack, pattern[, index])

```

- `haystack` — String, строка, в которой ищется совпадение с шаблоном регулярного выражения. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `pattern` — String, шаблон регулярного выражения. `pattern` может содержать несколько групп регулярного выражения, а `index` указывает, какую именно группу нужно извлечь. Индекс `0` означает совпадение со всем регулярным выражением. [`const String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `index` — Необязательный. Неотрицательное целое число, указывающее, какую группу регулярного выражения нужно извлечь. По умолчанию используется `1`, если `pattern` содержит хотя бы одну захватывающую группу, и `0` (всё совпадение), если `pattern` не содержит захватывающих групп. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT
    regexpExtract('100-200', '(\\d+)-(\\d+)', 1),
    regexpExtract('100-200', '(\\d+)-(\\d+)', 2),
    regexpExtract('100-200', '(\\d+)-(\\d+)', 0),
    regexpExtract('100-200', '(\\d+)-(\\d+)'),
    regexpExtract('100-200', '\\d+');

```


```
┌─regexpExtract('100-200', '(\\d+)-(\\d+)', 1)─┬─regexpExtract('100-200', '(\\d+)-(\\d+)', 2)─┬─regexpExtract('100-200', '(\\d+)-(\\d+)', 0)─┬─regexpExtract('100-200', '(\\d+)-(\\d+)')─┬─regexpExtract('100-200', '\\d+')─┐
│ 100                                          │ 200                                          │ 100-200                                      │ 100                                       │ 100                              │
└──────────────────────────────────────────────┴──────────────────────────────────────────────┴──────────────────────────────────────────────┴───────────────────────────────────────────┴──────────────────────────────────┘

```


## regexpPosition


```
regexpPosition(haystack, pattern[, position[, occurrence[, return_option[, flags[, subexpression]]]]])

```

- `haystack` — Строка, в которой выполняется поиск. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `pattern` — Шаблон регулярного выражения. [`const String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `position` — Необязательно. Позиция в байтах, начиная с 1, с которой начинается поиск. По умолчанию: 1. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `occurrence` — Необязательно. Какое по счёту совпадение вернуть. По умолчанию: 1. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `return_option` — Необязательно. `0` возвращает позицию начала совпадения, `1` — позицию сразу после совпадения. По умолчанию: 0. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `flags` — Необязательно. Флаги регулярного выражения. Поддерживаются: `i` (регистронезависимый), `c` (с учётом регистра), `m`/`n` (многострочные якоря), `s` (точка соответствует символу новой строки). По умолчанию: пустая строка. [`const String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `subexpression` — Необязательно. Индекс группы захвата, позицию которой нужно вернуть. `0` означает всё совпадение. По умолчанию: 0. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT
    regexpPosition('hello world', 'world'),
    regexpPosition('aXbXcXd', 'X', 1, 2),
    regexpPosition('aXbXcXd', 'X', 1, 2, 1),
    regexpPosition('Hello WORLD', 'world', 1, 1, 0, 'i'),
    regexpPosition('foo123bar456', '([a-z]+)([0-9]+)', 1, 2, 0, '', 2);

```


```
┌─...─┬─...─┬─...─┬─...─┬─...─┐
│   7 │   4 │   5 │   7 │  10 │
└─────┴─────┴─────┴─────┴─────┘

```


## removeDiacriticsUTF8


```
removeDiacriticsUTF8(str)

```

- `str` — входная строка в кодировке UTF-8. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT removeDiacriticsUTF8('café résumé naïve')

```


```
┌─removeDiacriticsUTF8('café résumé naïve')─┐
│ cafe resume naive                         │
└───────────────────────────────────────────┘

```


## repeat


```
repeat(s, n)

```

- `s` — строка, которую нужно повторить. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `n` — количество повторений строки. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT repeat('abc', 10)

```


```
┌─repeat('abc', 10)──────────────┐
│ abcabcabcabcabcabcabcabcabcabc │
└────────────────────────────────┘

```


## reverseUTF8


```
reverseUTF8(s)

```

- `s` — String, содержащая корректный текст в кодировке UTF-8. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT reverseUTF8('ClickHouse')

```


```
esuoHkcilC

```


## right


```
right(s, offset)

```

- `s` — Строка, из которой извлекается подстрока. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring)
- `offset` — Количество байт смещения. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- Для положительного `offset` — подстроку `s` длиной `offset` байт, отсчитываемую от конца строки.
- Для отрицательного `offset` — подстроку `s` длиной `length(s) - |offset|` байт, отсчитываемую от конца строки.
- Пустую строку, если `length` равно `0`. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT right('Hello', 3)

```


```
llo

```


```
SELECT right('Hello', -3)

```


```
lo

```


## rightPad


```
rightPad(string, length[, pad_string])

```

- `string` — Исходная строка, которую нужно дополнить. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `length` — Длина результирующей строки. Если значение меньше длины входной строки, входная строка укорачивается до `length` символов. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `pad_string` — Необязательно. Строка, которой дополняется исходная строка. Если не указана, исходная строка дополняется пробелами. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT rightPad('abc', 7, '*'), rightPad('abc', 7)

```


```
┌─rightPad('abc', 7, '*')─┬─rightPad('abc', 7)─┐
│ abc****                 │ abc                │
└─────────────────────────┴────────────────────┘

```


## rightPadUTF8


```
rightPadUTF8(string, length[, pad_string])

```

- `string` — Входная строка, которую нужно дополнить. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `length` — Длина результирующей строки. Если значение меньше длины входной строки, входная строка укорачивается до `length` символов. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `pad_string` — Необязательно. Строка, которой дополняется входная строка. Если не указана, входная строка дополняется пробелами. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT rightPadUTF8('абвг', 7, '*'), rightPadUTF8('абвг', 7)

```


```
┌─rightPadUTF8('абвг', 7, '*')─┬─rightPadUTF8('абвг', 7)─┐
│ абвг***                      │ абвг                    │
└──────────────────────────────┴─────────────────────────┘

```


## rightUTF8


```
rightUTF8(s, offset)

```

- `s` — Строка в кодировке UTF-8, из которой извлекается подстрока. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring)
- `offset` — Смещение в байтах. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- Для положительного `offset` — подстроку `s` длиной `offset` байт, отсчитываемую от конца строки.
- Для отрицательного `offset` — подстроку `s` длиной `length(s) - |offset|` байт, отсчитываемую от конца строки.
- Пустую строку, если `length` равно `0`. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT rightUTF8('Привет', 4)

```


```
ивет

```


```
SELECT rightUTF8('Привет', -4)

```


```
ет

```


## soundex


```
soundex(s)

```

- `s` — Входная строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT soundex('aksel')

```


```
┌─soundex('aksel')─┐
│ A240             │
└──────────────────┘

```


## space


```
space(n)

```

- `n` — Количество повторений пробела. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT space(3) AS res, length(res);

```


```
┌─res─┬─length(res)─┐
│     │           3 │
└─────┴─────────────┘

```


## sparseGrams


```
sparseGrams(s[, min_ngram_length[, max_ngram_length[, min_cutoff_length]]])

```

- `s` — Входная строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `min_ngram_length` — Необязательно. Минимальная длина извлекаемой n-граммы. Значение по умолчанию и минимально допустимое значение — 3. [`UInt*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `max_ngram_length` — Необязательно. Максимальная длина извлекаемой n-граммы. Значение по умолчанию — 100. Должно быть не меньше `min_ngram_length`. [`UInt*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `min_cutoff_length` — Необязательно. Если указано, возвращаются только n-граммы длиной не меньше `min_cutoff_length`. Значение по умолчанию совпадает с `min_ngram_length`. Должно быть не меньше `min_ngram_length` и не больше `max_ngram_length`. [`UInt*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT sparseGrams('alice', 3)

```


```
┌─sparseGrams('alice', 3)────────────┐
│ ['ali','lic','lice','ice']         │
└────────────────────────────────────┘

```


## sparseGramsHashes


```
sparseGramsHashes(s[, min_ngram_length, max_ngram_length])

```

- `s` — Входная строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `min_ngram_length` — Необязательно. Минимальная длина извлекаемой n-граммы. Значение по умолчанию и минимально допустимое значение — 3. [`UInt*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `max_ngram_length` — Необязательно. Максимальная длина извлекаемой n-граммы. Значение по умолчанию — 100. Должно быть не меньше `min_ngram_length`. [`UInt*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `min_cutoff_length` — Необязательно. Если указано, возвращаются только n-граммы длиной не меньше `min_cutoff_length`. Значение по умолчанию совпадает с `min_ngram_length`. Должно быть не меньше `min_ngram_length` и не больше `max_ngram_length`. [`UInt*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT sparseGramsHashes('alice', 3)

```


```
┌─sparseGramsHashes('alice', 3)──────────────────────┐
│ [1481062250,2450405249,4012725991,1918774096]      │
└────────────────────────────────────────────────────┘

```


## sparseGramsHashesUTF8


```
sparseGramsHashesUTF8(s[, min_ngram_length, max_ngram_length])

```

- `s` — Входная строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `min_ngram_length` — Необязательно. Минимальная длина извлекаемой n-граммы. Значение по умолчанию и минимально допустимое значение — 3. [`UInt*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `max_ngram_length` — Необязательно. Максимальная длина извлекаемой n-граммы. Значение по умолчанию — 100. Должно быть не меньше `min_ngram_length`. [`UInt*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `min_cutoff_length` — Необязательно. Если указано, возвращаются только n-граммы длиной не меньше `min_cutoff_length`. Значение по умолчанию совпадает с `min_ngram_length`. Должно быть не меньше `min_ngram_length` и не больше `max_ngram_length`. [`UInt*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT sparseGramsHashesUTF8('алиса', 3)

```


```
┌─sparseGramsHashesUTF8('алиса', 3)─┐
│ [4178533925,3855635300,561830861] │
└───────────────────────────────────┘

```


## sparseGramsUTF8


```
sparseGramsUTF8(s[, min_ngram_length[, max_ngram_length[, min_cutoff_length]]])

```

- `s` — Входная строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `min_ngram_length` — Необязательно. Минимальная длина извлекаемой n-граммы. Значение по умолчанию и минимально допустимое значение — 3. [`UInt*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `max_ngram_length` — Необязательно. Максимальная длина извлекаемой n-граммы. Значение по умолчанию — 100. Должно быть не меньше `min_ngram_length`. [`UInt*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `min_cutoff_length` — Необязательно. Если параметр указан, возвращаются только n-граммы длиной не менее `min_cutoff_length`. Значение по умолчанию совпадает со значением `min_ngram_length`. Должно быть не меньше `min_ngram_length` и не больше `max_ngram_length`. [`UInt*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT sparseGramsUTF8('алиса', 3)

```


```
┌─sparseGramsUTF8('алиса', 3)─┐
│ ['али','лис','иса']         │
└─────────────────────────────┘

```


## startsWith


```
startsWith(s, prefix)

```

- `s` — Строка для проверки. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `prefix` — Префикс, наличие которого нужно проверить. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT startsWith('ClickHouse', 'Click');

```


```
┌─startsWith('⋯', 'Click')─┐
│                        1 │
└──────────────────────────┘

```


## startsWithCaseInsensitive


```
startsWithCaseInsensitive(s, prefix)

```

- `s` — Строка, которую нужно проверить. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `prefix` — Регистронезависимый префикс, наличие которого нужно проверить. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT startsWithCaseInsensitive('ClickHouse', 'CLICK');

```


```
┌─startsWithCaseInsensitive('⋯', 'CLICK')─┐
│                                       1 │
└─────────────────────────────────────────┘

```


## startsWithCaseInsensitiveUTF8


```
startsWithCaseInsensitiveUTF8(s, prefix)

```

- `s` — Строка, которую нужно проверить. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `prefix` — Регистронезависимый префикс, наличие которого нужно проверить. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT startsWithCaseInsensitiveUTF8('приставка', 'при')

```


```
┌─startsWithUT⋯ка', 'при')─┐
│                        1 │
└──────────────────────────┘

```


## startsWithUTF8


```
startsWithUTF8(s, prefix)

```

- `s` — Строка, которую нужно проверить. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `prefix` — Префикс, наличие которого нужно проверить. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT startsWithUTF8('приставка', 'при')

```


```
┌─startsWithUT⋯ка', 'при')─┐
│                        1 │
└──────────────────────────┘

```


## stringBytesEntropy


```
stringBytesEntropy(s)

```

- `s` — строка для анализа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT stringBytesEntropy('Hello, world!')

```


```
┌─stringBytesEntropy('Hello, world!')─┐
│                         3.07049960  │
└─────────────────────────────────────┘

```


## stringBytesUniq


```
stringBytesUniq(s)

```

- `s` — анализируемая строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT stringBytesUniq('Hello')

```


```
┌─stringBytesUniq('Hello')─┐
│                        4 │
└──────────────────────────┘

```


## stringJaccardIndex


```
stringJaccardIndex(s1, s2)

```

- `s1` — Первая входная строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `s2` — Вторая входная строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT stringJaccardIndex('clickhouse', 'mouse')

```


```
┌─stringJaccardIndex('clickhouse', 'mouse')─┐
│                                       0.4 │
└───────────────────────────────────────────┘

```


## stringJaccardIndexUTF8


```
stringJaccardIndexUTF8(s1, s2)

```

- `s1` — Первая входная строка в кодировке UTF-8. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `s2` — Вторая входная строка в кодировке UTF-8. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT stringJaccardIndexUTF8('我爱你', '我也爱你') AS jaccard_index

```


```
┌─jaccard_index─┐
│          0.75 │
└───────────────┘

```


## substring

- Если `offset` равен `0`, возвращается пустая строка.
- Если `offset` отрицательный, подстрока начинается на `offset` символов от конца строки, а не от её начала.

```
substring(s, offset[, length])

```

- `s` — Строка, из которой извлекается подстрока. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring) или [`Enum`](https://clickhouse.com/docs/ru/reference/data-types/enum)
- `offset` — Начальная позиция подстроки в `s`. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `length` — Необязательный параметр. Максимальная длина подстроки. [`(U)Int*`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT 'database' AS db, substr(db, 5), substr(db, 5, 1)

```


```
┌─db───────┬─substring('database', 5)─┬─substring('database', 5, 1)─┐
│ database │ base                     │ b                           │
└──────────┴──────────────────────────┴─────────────────────────────┘

```


## substringIndex


```
substringIndex(s, delim, count)

```

- `s` — Строка, из которой нужно извлечь подстроку. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `delim` — Символ-разделитель. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `count` — Количество вхождений разделителя, которое нужно учесть перед извлечением подстроки. Если `count` положительный, возвращается всё слева от последнего разделителя (считая слева). Если `count` отрицательный, возвращается всё справа от последнего разделителя (считая справа). [`UInt`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Int`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT substringIndex('www.clickhouse.com', '.', 2)

```


```
┌─substringIndex('www.clickhouse.com', '.', 2)─┐
│ www.clickhouse                               │
└──────────────────────────────────────────────┘

```


## substringIndexUTF8


```
substringIndexUTF8(s, delim, count)

```

- `s` — Строка, из которой извлекается подстрока. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `delim` — Символ-разделитель. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `count` — Количество вхождений разделителя, которое нужно отсчитать перед извлечением подстроки. Если `count` положительный, возвращается всё слева от последнего разделителя (при отсчёте слева). Если `count` отрицательный, возвращается всё справа от последнего разделителя (при отсчёте справа). [`UInt`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`Int`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT substringIndexUTF8('www.straßen-in-europa.de', '.', 2)

```


```
www.straßen-in-europa

```


## substringUTF8

- Если `offset` равен `0`, возвращается пустая строка.
- Если `offset` отрицательный, подстрока начинается с кодовой точки, расположенной на `offset` позиций от конца строки, а не от начала.

```
substringUTF8(s, offset[, length])

```

- `s` — Строка, из которой извлекается подстрока. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string) или [`FixedString`](https://clickhouse.com/docs/ru/reference/data-types/fixedstring) или [`Enum`](https://clickhouse.com/docs/ru/reference/data-types/enum)
- `offset` — Начальная позиция подстроки в `s`. [`Int`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`UInt`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)
- `length` — Максимальная длина подстроки. Необязательный параметр. [`Int`](https://clickhouse.com/docs/ru/reference/data-types/int-uint) или [`UInt`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT 'Täglich grüßt das Murmeltier.' AS str, substringUTF8(str, 9), substringUTF8(str, 9, 5)

```


```
Täglich grüßt das Murmeltier.    grüßt das Murmeltier.    grüßt

```


## toValidUTF8


```
toValidUTF8(s)

```

- `s` — Любая последовательность байтов, представленная объектом типа данных String. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT toValidUTF8('\\x61\\xF0\\x80\\x80\\x80b')

```


```
c
┌─toValidUTF8('a����b')─┐
│ a�b                   │
└───────────────────────┘

```


## trimBoth


```
trimBoth(s[, trim_characters])

```

- `s` — Обрезаемая строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `trim_characters` — Необязательно. Символы, которые нужно удалить. Если не указано, удаляются стандартные пробельные символы. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT trimBoth('$$ClickHouse$$', '$')

```


```
┌─trimBoth('$$⋯se$$', '$')─┐
│ ClickHouse               │
└──────────────────────────┘

```


## trimLeft


```
trimLeft(input[, trim_characters])

```

- `input` — Строка, из которой удаляются символы. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `trim_characters` — Необязательно. Символы, которые нужно удалить. Если не указано, удаляются распространённые пробельные символы. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT trimLeft('ClickHouse', 'Click');

```


```
┌─trimLeft('Cl⋯', 'Click')─┐
│ House                    │
└──────────────────────────┘

```


## trimRight


```
trimRight(s[, trim_characters])

```

- `s` — Строка, из которой нужно удалить символы. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `trim_characters` — Необязательные символы для удаления. Если не указаны, удаляются обычные пробельные символы. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT trimRight('ClickHouse','House');

```


```
┌─trimRight('C⋯', 'House')─┐
│ Click                    │
└──────────────────────────┘

```


## tryBase32Decode


```
tryBase32Decode(encoded)

```

- `encoded` — столбец String или константа, которую нужно декодировать. Если строка не является корректной строкой в кодировке Base32, то в случае ошибки возвращается пустая строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT tryBase32Decode('IVXGG33EMVSA====');

```


```
┌─tryBase32Decode('IVXGG33EMVSA====')─┐
│ Encoded                             │
└─────────────────────────────────────┘

```


## tryBase58Decode


```
tryBase58Decode(encoded[, expected_size])

```

- `encoded` — Столбец типа String или константа. Если строка некорректно закодирована в Base58, в случае ошибки возвращается пустая строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)
- `expected_size` — Необязательно. Ожидаемый размер декодированного значения в байтах. Если указано 32 или 64, используется оптимизированный декодер; для других значений используется универсальный декодер. [`UInt8, UInt16, UInt32, or UInt64`](https://clickhouse.com/docs/ru/reference/data-types/int-uint)

```
SELECT tryBase58Decode('3dc8KtHrwM') AS res, tryBase58Decode('invalid') AS res_invalid;

```


```
┌─res─────┬─res_invalid─┐
│ Encoded │             │
└─────────┴─────────────┘

```


## tryBase64Decode


```
tryBase64Decode(encoded)

```

- `encoded` — столбец `String` или константа для декодирования. Если строка не является корректной строкой в кодировке Base64, в случае ошибки возвращается пустая строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT tryBase64Decode('Y2xpY2tob3VzZQ==')

```


```
┌─tryBase64Decode('Y2xpY2tob3VzZQ==')─┐
│ clickhouse                          │
└─────────────────────────────────────┘

```


## tryBase64URLDecode


```
tryBase64URLDecode(encoded)

```

- `encoded` — столбец типа String или константа для декодирования. Если строка не является допустимой строкой в кодировке Base64, то в случае ошибки возвращается пустая строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT tryBase64URLDecode('aHR0cHM6Ly9jbGlja2hvdXNlLmNvbQ')

```


```
┌─tryBase64URLDecode('aHR0cHM6Ly9jbGlja2hvdXNlLmNvbQ')─┐
│ https://clickhouse.com                               │
└──────────────────────────────────────────────────────┘

```


## tryIdnaEncode


```
tryIdnaEncode(s)

```

- `s` — Входная строка. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT tryIdnaEncode('straße.münchen.de')

```


```
┌─tryIdnaEncode('straße.münchen.de')──┐
│ xn--strae-oqa.xn--mnchen-3ya.de     │
└─────────────────────────────────────┘

```


## tryPunycodeDecode


```
tryPunycodeDecode(s)

```

- `s` — строка, закодированная в Punycode. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT tryPunycodeDecode('Mnchen-3ya')

```


```
┌─tryPunycodeDecode('Mnchen-3ya')─┐
│ München                         │
└─────────────────────────────────┘

```


## upper


```
upper(s)

```

- `s` — Строка, которую нужно преобразовать в верхний регистр. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT upper('clickhouse')

```


```
┌─upper('clickhouse')─┐
│ CLICKHOUSE          │
└─────────────────────┘

```


## upperUTF8


```
upperUTF8(s)

```

- `s` — строкового типа. [`String`](https://clickhouse.com/docs/ru/reference/data-types/string)

```
SELECT upperUTF8('München') AS Upperutf8

```


```
┌─Upperutf8─┐
│ MÜNCHEN   │
└───────────┘

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
