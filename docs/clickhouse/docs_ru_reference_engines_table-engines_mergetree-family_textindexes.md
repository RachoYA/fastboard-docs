# Полнотекстовый поиск с текстовыми индексами - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/textindexes


```
1: The cat likes mice.
2: Mice are afraid of dogs.
3: I have two dogs and a cat.

```


```
1: The, cat, likes, mice
2: Mice, are, afraid, of, dogs
3: I, have, two, dogs, and, a, cat

```


```
1: the, cat, likes, mice
2: mice, are, afraid, of, dogs
3: i, have, two, dogs, and, a, cat

```


```
1: cat, likes, mice
2: mice, afraid, dogs
3: have, two, dogs, cat

```


```
afraid : [2]
cat    : [1, 3]
dogs   : [2, 3]
have   : [3]
likes  : [1]
mice   : [1]
two    : [3]

```


## Создание текстового индекса


```
CREATE TABLE table
(
    key UInt64,
    str String,
    INDEX text_idx str TYPE text(
                                -- Mandatory parameters:
                                tokenizer = splitByNonAlpha
                                            | splitByString[(S)]
                                            | asciiCJK
                                            | ngrams[(N)]
                                            | sparseGrams[(min_length[, max_length[, min_cutoff_length]])]
                                            | array
                                -- Optional parameters:
                                [, preprocessor = expression(str)]
                                [, postprocessor = expression(str)]
                                [, support_phrase_search = 0 | 1 ] -- experimental
                                -- Optional advanced parameters:
                                [, dictionary_block_size = D]
                                [, dictionary_block_frontcoding_compression = B]
                                [, posting_list_block_size = C]
                                [, posting_list_codec = 'none' | 'bitpacking' ]
                            )
)
ENGINE = MergeTree
ORDER BY key

```

- [String](https://clickhouse.com/docs/ru/reference/data-types/string) и [FixedString](https://clickhouse.com/docs/ru/reference/data-types/fixedstring),
- [Array(String)](https://clickhouse.com/docs/ru/reference/data-types/array) и [Array(FixedString)](https://clickhouse.com/docs/ru/reference/data-types/array),
- [Map](https://clickhouse.com/docs/ru/reference/data-types/map) (через функции [mapKeys](https://clickhouse.com/docs/ru/reference/functions/regular-functions/tuple-map-functions#mapKeys) и [mapValues](https://clickhouse.com/docs/ru/reference/functions/regular-functions/tuple-map-functions#mapValues)),
- [JSON](https://clickhouse.com/docs/ru/reference/data-types/newjson) (через функции [JSONAllPaths](https://clickhouse.com/docs/ru/reference/functions/regular-functions/json-functions#JSONAllPaths) и [`JSONAllValues`](https://clickhouse.com/docs/ru/reference/functions/regular-functions/json-functions#JSONAllValues)).

```
ALTER TABLE table
    ADD INDEX text_idx str TYPE text(
                                -- Mandatory parameters:
                                tokenizer = splitByNonAlpha
                                            | splitByString[(S)]
                                            | asciiCJK
                                            | ngrams[(N)]
                                            | sparseGrams[(min_length[, max_length[, min_cutoff_length]])]
                                            | array
                                -- Optional parameters:
                                [, preprocessor = expression(str)]
                                [, postprocessor = expression(str)]
                                [, support_phrase_search = 0 | 1 ] -- experimental
                                -- Optional advanced parameters:
                                [, dictionary_block_size = D]
                                [, dictionary_block_frontcoding_compression = B]
                                [, posting_list_block_size = C]
                                [, posting_list_codec = 'none' | 'bitpacking' ]
                            )


```


```
ALTER TABLE table MATERIALIZE INDEX text_idx SETTINGS mutations_sync = 2;

```


```
ALTER TABLE table DROP INDEX text_idx;

```

- `splitByNonAlpha` разбивает строки по неалфавитно-цифровым ASCII-символам (см. функцию [splitByNonAlpha](https://clickhouse.com/docs/ru/reference/functions/regular-functions/splitting-merging-functions#splitByNonAlpha)).
- `splitByString(S)` разбивает строки по заданным пользователем строкам-разделителям `S` (см. функцию [splitByString](https://clickhouse.com/docs/ru/reference/functions/regular-functions/splitting-merging-functions#splitByString)). Разделители можно задать с помощью необязательного параметра, например, `tokenizer = splitByString([', ', '; ', '\n', '\\'])`. Обратите внимание, что каждая строка может состоять из нескольких символов (`', '` в примере). Список разделителей по умолчанию, если он не указан явно (например, `tokenizer = splitByString`), — это один пробел `[' ']`.
- `asciiCJK` разбивает строки на токены, используя правила границ слов Unicode (аналогично [Unicode Text Segmentation (UAX #29)](https://unicode.org/reports/tr29/)). ASCII-буквенно-цифровые символы и символы подчёркивания образуют токены с соединительными символами (ASCII `:` для букв, `.` и `'` для символов одного типа). Не-ASCII-символы Unicode, включая символы [CJK](https://en.wikipedia.org/wiki/CJK_characters), становятся односимвольными токенами.
- `ngrams(N)` разбивает строки на `N`-граммы одинаковой длины (см. функцию [ngrams](https://clickhouse.com/docs/ru/reference/functions/regular-functions/splitting-merging-functions#ngrams)). Длину n-граммы можно задать с помощью необязательного целочисленного параметра от 1 до 8, например, `tokenizer = ngrams(3)`. Размер n-граммы по умолчанию, если он не указан явно (например, `tokenizer = ngrams`), равен 3.
- `sparseGrams(min_length, max_length, min_cutoff_length)` разбивает строки на n-граммы переменной длины, содержащие не менее `min_length` и не более `max_length` (включительно) символов (см. функцию [sparseGrams](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-functions#sparseGrams)). Если не указано явно, значения `min_length` и `max_length` по умолчанию равны 3 и 100. Если передан параметр `min_cutoff_length`, возвращаются только n-граммы длиной не меньше `min_cutoff_length`. По сравнению с `ngrams(N)`, токенизатор `sparseGrams` создаёт N-граммы переменной длины, что позволяет более гибко представлять исходный текст. Например, `tokenizer = sparseGrams(3, 5, 4)` внутренне генерирует из входной строки 3-, 4- и 5-граммы, но возвращаются только 4- и 5-граммы.
- `array` не выполняет токенизацию, то есть каждое значение строки является токеном (см. функцию [array](https://clickhouse.com/docs/ru/reference/functions/regular-functions/array-functions#array)).

```
SELECT tokens('abc def', 'ngrams', 3);

```


```
['abc','bc ','c d',' de','def']

```

- Приведение к нижнему/верхнему регистру или свёртка регистра для регистронезависимого сопоставления, например [lower](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-functions#lower), [lowerUTF8](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-functions#lowerUTF8), [caseFoldUTF8](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-functions#caseFoldUTF8).
- Нормализация UTF-8, например [normalizeUTF8NFC](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-functions#normalizeUTF8NFC), [normalizeUTF8NFD](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-functions#normalizeUTF8NFD), [normalizeUTF8NFKC](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-functions#normalizeUTF8NFKC), [normalizeUTF8NFKD](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-functions#normalizeUTF8NFKD), [normalizeUTF8NFKCCasefold](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-functions#normalizeUTF8NFKCCasefold), [toValidUTF8](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-functions#toValidUTF8).
- Удаление или преобразование нежелательных символов или подстрок, например диакритических знаков, с помощью [extractTextFromHTML](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-functions#extractTextFromHTML), [substring](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-functions#substring), [idnaEncode](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-functions#idnaEncode), [translate](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-replace-functions#translate), [removeDiacriticsUTF8](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-functions#removeDiacriticsUTF8).
- `INDEX idx col TYPE text(tokenizer = 'splitByNonAlpha', preprocessor = lower(col))`
- `INDEX idx col TYPE text(tokenizer = 'splitByNonAlpha', preprocessor = substringIndex(col, '\n', 1))`
- `INDEX idx col TYPE text(tokenizer = 'splitByNonAlpha', preprocessor = lower(extractTextFromHTML(col)))`
- `INDEX idx col TYPE text(tokenizer = 'splitByNonAlpha', preprocessor = removeDiacriticsUTF8(caseFoldUTF8(col)))`
- `INDEX idx lower(col) TYPE text(tokenizer = 'splitByNonAlpha', preprocessor = upper(lower(col)))`
- `INDEX idx lower(col) TYPE text(tokenizer = 'splitByNonAlpha', preprocessor = concat(lower(col), lower(col)))`
- Не допускается: `INDEX idx lower(col) TYPE text(tokenizer = 'splitByNonAlpha', preprocessor = concat(col, col))`

```
CREATE TABLE table
(
    str String,
    INDEX idx str TYPE text(tokenizer = 'splitByNonAlpha', preprocessor = lower(str))
)
ENGINE = MergeTree
ORDER BY tuple();

SELECT count() FROM table WHERE hasToken(str, 'Foo');

```


```
CREATE TABLE table
(
    str String,
    INDEX idx lower(str) TYPE text(tokenizer = 'splitByNonAlpha')
)
ENGINE = MergeTree
ORDER BY tuple();

SELECT count() FROM table WHERE hasToken(str, lower('Foo'));

```


```
CREATE TABLE table
(
    arr Array(String),
    INDEX idx arr TYPE text(tokenizer = 'splitByNonAlpha', preprocessor = lower(arr))

    -- This is not legal:
    INDEX idx_illegal arr TYPE text(tokenizer = 'splitByNonAlpha', preprocessor = arraySort(arr))
)
ENGINE = MergeTree
ORDER BY tuple();

SELECT count() FROM tab WHERE hasAllTokens(arr, 'foo');

```


```
CREATE TABLE table
(
    map Map(String, String),
    INDEX idx mapKeys(map)  TYPE text(tokenizer = 'splitByNonAlpha', preprocessor = lower(mapKeys(map)))
)
ENGINE = MergeTree
ORDER BY tuple();

SELECT count() FROM tab WHERE hasAllTokens(mapKeys(map), 'foo');

```

- **Фильтрация стоп-слов (чрезвычайно частых токенов)**. Очень распространенные токены, такие как “the”, “a” и “is”, почти не влияют на релевантность поиска и раздувают индекс. Вы можете использовать постпроцессор, чтобы отбрасывать их, преобразуя в пустые токены — пустые токены игнорируются, то есть не добавляются в индекс. Пример: `if(str IN ('the', 'a', 'an', 'of', 'in', 'is', 'it'), '', str)`
- **Удаление временных меток**. Строки Log часто начинаются со структурированной временной метки, например `2024-01-15T10:23:45`, или содержат ее. Индексация токенов временных меток раздувает индекс строками, не имеющими значения для релевантности поиска. Есть два взаимодополняющих способа игнорировать временные метки:
- **Подход с постпроцессором**: используйте токенизатор `splitByString` (разбиение по пробельным символам), чтобы вся временная метка стала одним токеном, а затем используйте `parseDateTimeOrNull`, чтобы распознать и отбросить ее. Пример: `if(isNull(parseDateTimeOrNull(str, '%Y-%m-%dT%H:%i:%S')), str, '')` Для временных меток со смещением часового пояса или дробными секундами используйте `parseDateTimeBestEffortOrNull(str)` без явной строки формата.
- **Подход с препроцессором**: удалите временную метку из полной строки лога *до* токенизации с помощью regular expression. Пример: `replaceRegexpAll(str, '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2} ', '')` Это работает с любым токенизатором и эффективнее, поскольку символы временной метки вообще не токенизируются. Оба подхода можно комбинировать: препроцессор удаляет временную метку, а постпроцессор нормализует или фильтрует оставшиеся токены (например, приводит к нижнему регистру и отбрасывает слова уровня серьезности, такие как `ERROR` или `INFO`).
- **Стемминг**. Сопоставление каждого токена с его основой улучшает полноту поиска, позволяя находить морфологические варианты с общим корнем. Например, при английском стемминге “running”, “runs” и “run” приводятся к основе “run”, поэтому запрос по любому из этих вариантов найдет их все. ClickHouse предоставляет встроенную функцию [stem](https://clickhouse.com/docs/ru/reference/functions/regular-functions/nlp-functions#stem) для нескольких языков. Пример: `stem(str, 'en')`
- **Нормализация регистра**. Приведение токенов к нижнему или верхнему регистру для включения сопоставления, например [lower](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-functions#lower), [lowerUTF8](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-functions#lowerUTF8). Для приведения к нижнему или верхнему регистру мы рекомендуем использовать препроцессор вместо постпроцессора.”
- Для `hasToken`, `hasAllTokens`, `hasAnyTokens` и `hasPhrase` (с любым поддерживаемым токенизатором): постпроцессор применяется и к токенам в haystack, и к поисковому needle, обеспечивая полностью нормализованное сопоставление (например, регистронезависимый поиск). Для `hasPhrase` токены после постобработки располагаются без промежутков, поэтому токен, который постпроцессор отбрасывает, не оставляет позиционного разрыва, и фраза всё равно сопоставляется через него — например, при постпроцессоре стоп-слов, отбрасывающем `the`, `hasPhrase(col, 'see cat')` соответствует документу `see the cat`.
- Для всех остальных функций (`=`, `IN`, `has`, `hasAny`, `hasAll`, `mapContains*`): для поиска с использованием индексной подсказки постобработке подвергается только needle; предикат на уровне строки по-прежнему сравнивается с исходными значениями столбца.
- Удаление стоп-слов с помощью выражения постпроцессора:

```
CREATE TABLE table
(
    str String,
    INDEX idx(str) TYPE text(
        tokenizer = 'splitByNonAlpha',
        postprocessor = if(str IN ('the', 'a', 'an', 'of', 'in', 'is', 'it'), '', str)
    )
)
ENGINE = MergeTree
ORDER BY tuple();

```

- Удалите временные метки с помощью выражения постпроцессора:

```
-- Log lines: '2024-01-15T10:23:45 ERROR connection failed'
-- The splitByString tokenizer (default: whitespace) keeps the full timestamp as one token.
-- parseDateTimeOrNull detects and drops it; non-timestamp words are kept.
CREATE TABLE logs
(
    id   UInt64,
    line String,
    INDEX idx(line) TYPE text(
        tokenizer    = 'splitByString',
        postprocessor = if(isNull(parseDateTimeOrNull(line, '%Y-%m-%dT%H:%i:%S')), line, '')
    )
)
ENGINE = MergeTree ORDER BY id;

-- Only message-level words are indexed; timestamp tokens are not stored.
SELECT count() FROM logs WHERE hasAllTokens(line, ['ERROR']);       -- fast index lookup
SELECT count() FROM logs WHERE hasAllTokens(line, ['2024-01-15T10:23:45']);  -- returns 0: token was never indexed

```

- Удалите временные метки с помощью выражения препроцессора:

```
-- The preprocessor strips the ISO timestamp prefix before tokenization.
-- Any tokenizer can be used; timestamp characters are never seen by the tokenizer.
CREATE TABLE logs
(
    id   UInt64,
    line String,
    INDEX idx(line) TYPE text(
        tokenizer   = 'splitByNonAlpha',
        preprocessor = replaceRegexpAll(line, '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2} ', '')
    )
)
ENGINE = MergeTree ORDER BY id;

```

- Удалите временные метки с помощью общего выражения для препроцессора и постпроцессора:

```
-- Preprocessor strips the timestamp, then lowercases the remainder.
-- Postprocessor drops the severity word (error, info, warn, debug) after tokenization.
-- Result: only substantive message words are stored in the index.
CREATE TABLE logs
(
    id   UInt64,
    line String,
    INDEX idx(line) TYPE text(
        tokenizer    = 'splitByNonAlpha',
        preprocessor = lower(replaceRegexpAll(line, '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2} ', '')),
        postprocessor = if(line IN ('error', 'info', 'warn', 'warning', 'debug', 'critical'), '', line)
    )
)
ENGINE = MergeTree ORDER BY id;

-- Example log line: '2024-01-15T10:23:45 ERROR connection failed'
-- After preprocessor:  'error connection failed'
-- After tokenization:  ['error', 'connection', 'failed']
-- After postprocessor: ['connection', 'failed']   ← 'error' dropped as severity word
SELECT count() FROM logs WHERE hasAllTokens(line, ['connection']);

```

- Примените стемминг к токенам с помощью выражения постпроцессора:

```
CREATE TABLE table
(
    str String,
    INDEX idx(str) TYPE text(
        tokenizer = 'splitByNonAlpha',
        postprocessor = stem(str, 'en')
    )
)
ENGINE = MergeTree
ORDER BY tuple();

-- The query token 'running' is stemmed to 'run' before the lookup,
-- matching rows that contain 'run', 'runs', 'ran', 'running', etc.
SELECT count() FROM table WHERE hasAllTokens(str, ['running']);

```


| Функция | Поддерживает препроцессор | Совместимые токенизаторы | Поддерживает постпроцессор |
| --- | --- | --- | --- |
| `=` | да | все | да |
| `IN` | да | все | да |
| [hasToken](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-search-functions#hasToken) | да | все (в первую очередь для `splitByNonAlpha`) | да |
| [hasAnyTokens(col, str)](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-search-functions#hasAnyTokens) | да | все | да |
| [hasAllTokens(col, str)](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-search-functions#hasAllTokens) | да | все | да |
| [hasAnyTokens(col, arr)](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-search-functions#hasAnyTokens) | нет (элементы массива используются как токены без изменений) | все | да |
| [hasAllTokens(col, arr)](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-search-functions#hasAllTokens) | нет (элементы массива используются как токены без изменений) | все | да |
| [hasPhrase](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-search-functions#hasPhrase) | да | `splitByNonAlpha`, `splitByString`, `ngrams`, `asciiCJK` | да |
| [startsWith](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-functions#startsWith) | да | `splitByNonAlpha`, `ngrams`, `sparseGrams`, `asciiCJK` | да |
| [endsWith](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-functions#endsWith) | да | `splitByNonAlpha`, `ngrams`, `sparseGrams`, `asciiCJK` | да |
| [like](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-search-functions#like) | да¹ | `splitByNonAlpha`, `ngrams`, `sparseGrams`, `asciiCJK`¹ | да¹ |
| [match](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-search-functions#match) | да¹ | `splitByNonAlpha`, `ngrams`, `sparseGrams`, `asciiCJK`¹ | да¹ |
| [ilike](https://clickhouse.com/docs/ru/reference/functions/regular-functions/string-search-functions#like) | да² (`lower`/`upper` only) | `splitByNonAlpha`, `array`² | нет² |
| [mapContainsKey](https://clickhouse.com/docs/ru/reference/functions/regular-functions/tuple-map-functions#mapContainsKey) | да | все | да |
| [mapContainsValue](https://clickhouse.com/docs/ru/reference/functions/regular-functions/tuple-map-functions#mapContainsValue) | да | все | да |
| [mapContainsKeyLike](https://clickhouse.com/docs/ru/reference/functions/regular-functions/tuple-map-functions#mapContainsKeyLike) | да | `splitByNonAlpha`, `ngrams`, `sparseGrams`, `asciiCJK` | да |
| [mapContainsValueLike](https://clickhouse.com/docs/ru/reference/functions/regular-functions/tuple-map-functions#mapContainsValueLike) | да | `splitByNonAlpha`, `ngrams`, `sparseGrams`, `asciiCJK` | да |
| [has](https://clickhouse.com/docs/ru/reference/functions/regular-functions/array-functions#has) | да | `array` | да |
| [hasAny](https://clickhouse.com/docs/ru/reference/functions/regular-functions/array-functions#hasAny) | да | `array` | да |
| [hasAll](https://clickhouse.com/docs/ru/reference/functions/regular-functions/array-functions#hasAll) | да | `array` | да |


```
CREATE TABLE table(
    k UInt64,
    s String,
    INDEX idx s TYPE text(tokenizer = ngrams(2)))
ENGINE = MergeTree()
ORDER BY k;

SHOW CREATE TABLE table;

```


```
┌─statement──────────────────────────────────────────────────────────────┐
│ CREATE TABLE default.table                                            ↴│
│↳(                                                                     ↴│
│↳    `k` UInt64,                                                       ↴│
│↳    `s` String,                                                       ↴│
│↳    INDEX idx s TYPE text(tokenizer = ngrams(2)) GRANULARITY 100000000↴│ <-- here
│↳)                                                                     ↴│
│↳ENGINE = MergeTree                                                    ↴│
│↳ORDER BY k                                                            ↴│
│↳SETTINGS index_granularity = 8192                                      │
└────────────────────────────────────────────────────────────────────────┘

```


## Использование текстового индекса


### Поддерживаемые функции


```
SELECT [...]
FROM [...]
WHERE string_search_function(column_with_text_index)

```


#### `=`


```
SELECT * from table WHERE str = 'Hello';

```


#### `IN`


```
SELECT * from table WHERE str IN ('Hello', 'World');

```


#### `LIKE` и `match`


```
SELECT count() FROM table WHERE comment LIKE 'support%';

```


```
SELECT count() FROM table WHERE comment LIKE ' support %'; -- или `% support %`

```


#### `multiSearchAny` and `multiMatchAny`


```
SELECT count() FROM table WHERE multiSearchAny(comment, ['clickhouse', 'support']);

```


```
SELECT count() FROM table WHERE multiSearchAny(comment, [' clickhouse ', ' support ']);

```


#### `startsWith` и `endsWith`


```
SELECT count() FROM table WHERE startsWith(comment, 'clickhouse support');

```


```
startsWith(comment, 'clickhouse supports ')`

```


```
SELECT count() FROM table WHERE endsWith(comment, ' olap engine');

```


#### `hasToken`


```
SELECT count() FROM table WHERE hasToken(comment, 'clickhouse');

```


#### `hasAnyTokens` and `hasAllTokens`


```
-- Токены поиска переданы как строковый аргумент
SELECT count() FROM table WHERE hasAnyTokens(comment, 'clickhouse olap');
SELECT count() FROM table WHERE hasAllTokens(comment, 'clickhouse olap');

-- Токены поиска переданы как Array(String)
SELECT count() FROM table WHERE hasAnyTokens(comment, ['clickhouse', 'olap']);
SELECT count() FROM table WHERE hasAllTokens(comment, ['clickhouse', 'olap']);

```


#### `hasPhrase`


```
-- Matches: 'clickhouse' and 'olap' must appear consecutively in that order
SELECT count() FROM table WHERE hasPhrase(comment, 'clickhouse olap');

-- Does NOT match a row containing 'olap clickhouse' (wrong order)
-- Does NOT match a row containing 'clickhouse fast olap' (non-consecutive)

```


#### `has`


```
SELECT count() FROM table WHERE has(array, 'clickhouse');

```


#### `hasAny` и `hasAll`


```
SELECT count() FROM table WHERE hasAny(tags, ['clickhouse', 'olap']);
SELECT count() FROM table WHERE hasAll(tags, ['clickhouse', 'olap']);

```


#### `mapContains`


```
SELECT count() FROM table WHERE mapContainsKey(map, 'clickhouse');
-- OR
SELECT count() FROM table WHERE mapContains(map, 'clickhouse');

```


#### `mapContainsValue`


```
SELECT count() FROM table WHERE mapContainsValue(map, 'clickhouse');

```


#### `mapContainsKeyLike` и `mapContainsValueLike`


```
SELECT count() FROM table WHERE mapContainsKeyLike(map, '% clickhouse %');
SELECT count() FROM table WHERE mapContainsValueLike(map, '% clickhouse %');

```


#### `operator[]`


```
SELECT count() FROM table WHERE map['engine'] = 'clickhouse';

```


### Индексация столбцов Array(String)


```
CREATE TABLE posts
(
    post_id UInt64,
    title String,
    content String,
    keywords Array(String)
)
ENGINE = MergeTree
ORDER BY (post_id);

```


```
SELECT count() FROM posts WHERE has(keywords, 'clickhouse'); -- медленное полное сканирование таблицы — проверяет каждое ключевое слово в каждом посте

```


```
ALTER TABLE posts ADD INDEX keywords_idx(keywords) TYPE text(tokenizer = splitByNonAlpha);
ALTER TABLE posts MATERIALIZE INDEX keywords_idx; -- Не забудьте перестроить индекс для существующих данных

```


### Индексация столбцов типа Map


```
CREATE TABLE logs
(
    id UInt64,
    timestamp DateTime,
    message String,
    attributes Map(String, String)
)
ENGINE = MergeTree
ORDER BY (timestamp);

```


```
-- Находит все журналы с данными об ограничении частоты запросов:
SELECT * FROM logs WHERE has(mapKeys(attributes), 'rate_limit'); -- медленное полное сканирование таблицы

-- Находит все журналы с определённого IP-адреса:
SELECT * FROM logs WHERE has(mapValues(attributes), '192.168.1.1'); -- медленное полное сканирование таблицы

```


```
ALTER TABLE logs ADD INDEX attributes_keys_idx mapKeys(attributes) TYPE text(tokenizer = array);
ALTER TABLE posts MATERIALIZE INDEX attributes_keys_idx;

```


```
ALTER TABLE logs ADD INDEX attributes_vals_idx mapValues(attributes) TYPE text(tokenizer = array);
ALTER TABLE posts MATERIALIZE INDEX attributes_vals_idx;

```


```
-- Найти все запросы с ограничением частоты:
SELECT * FROM logs WHERE mapContainsKey(attributes, 'rate_limit'); -- fast

-- Найти все записи журнала с определённого IP-адреса:
SELECT * FROM logs WHERE has(mapValues(attributes), '192.168.1.1'); -- fast

-- Найти все записи журнала, в которых любой атрибут содержит ошибку:
SELECT * FROM logs WHERE mapContainsValueLike(attributes, '% error %'); -- fast

```


### Индексация JSON-столбцов

- **Индексы для конкретных подстолбцов** — создайте текстовый индекс для известного JSON-пути, как и для обычного столбца. При этом индексируются *значения* по этому пути.
- **Индексы на основе путей с [JSONAllPaths](https://clickhouse.com/docs/ru/reference/functions/regular-functions/json-functions#JSONAllPaths)** — индексируют *все пути*, присутствующие в каждой грануле, чтобы пропускать гранулы, в которых не может быть запрашиваемого пути. Как и в случае со столбцами `Map`.
- **Индексы на основе значений с [JSONAllValues](https://clickhouse.com/docs/ru/reference/functions/regular-functions/json-functions#JSONAllValues)** — индексируют *все значения* по всем JSON-путям, чтобы ускорить полнотекстовый поиск по любому подстолбцу JSON с помощью одного индекса.

#### Индексы для определённых подстолбцов

- **Типизированный путь**, объявленный в подсказке типа JSON, — прямой доступ по имени: `json.a`.
- **Динамический путь** с явным приведением типа — используйте синтаксис приведения `::`: `json.b::String`.

```
CREATE TABLE sensor_data
(
    data JSON(sensor_id String),
    INDEX idx_sensor data.sensor_id TYPE text(tokenizer = splitByNonAlpha),
    INDEX idx_location data.location::String TYPE text(tokenizer = splitByNonAlpha)
)
ENGINE = MergeTree
ORDER BY tuple()
SETTINGS index_granularity = 1;

INSERT INTO sensor_data SELECT toJSONString(map('sensor_id', 'id_' || number , 'location', 'room_' || toString(number))) FROM numbers(4);
INSERT INTO sensor_data SELECT toJSONString(map('sensor_id', 'id_' || number, 'location', 'room_' || toString(number))) FROM numbers(4, 4);

```


```
EXPLAIN indexes = 1 SELECT * FROM sensor_data WHERE data.sensor_id = 'id_5';

```


```
...
    Indexes:
      Skip
        Name: idx_sensor
        Description: text
        Condition: (mode: All; tokens: ["5", "id"])
        Parts: 1/2
        Granules: 1/8

```


```
EXPLAIN indexes = 1 SELECT * FROM sensor_data WHERE data.location::String = 'room_5';

```


```
...
    Indexes:
      Skip
        Name: idx_location
        Description: text
        Condition: (mode: All; tokens: ["5", "room"])
        Parts: 1/2
        Granules: 1/8

```


#### Индексы по путям с JSONAllPaths


```
CREATE TABLE events
(
    data JSON,
    INDEX idx JSONAllPaths(data) TYPE text(tokenizer = array)
)
ENGINE = MergeTree
ORDER BY tuple();

INSERT INTO events VALUES ('{"user": {"name": "Alice"}, "action": "login"}');
INSERT INTO events VALUES ('{"metric": {"cpu": 0.95}, "host": "srv1"}');

```


```
EXPLAIN indexes = 1 SELECT * FROM events WHERE data.user.name = 'Alice';

```


```
...
    Indexes:
      Skip
        Name: idx
        Description: text
        Condition: (mode: All; tokens: ["user.name"])
        Parts: 1/2
        Granules: 1/2

```


```
EXPLAIN indexes = 1 SELECT * FROM events WHERE data.nonexistent = 1;

```


```
...
    Indexes:
      Skip
        Name: idx
        Description: text
        Condition: (mode: All; tokens: ["nonexistent"])
        Parts: 0/2
        Granules: 0/2

```


```
EXPLAIN indexes = 1 SELECT * FROM events WHERE data.user.name IS NOT NULL;

```


```
...
    Indexes:
      Skip
        Name: idx
        Description: text
        Condition: (mode: All; tokens: ["user.name"])
        Parts: 1/2
        Granules: 1/2

```


#### Индексы по значениям с JSONAllValues


```
CREATE TABLE events
(
    id UInt64,
    data JSON,
    INDEX json_idx JSONAllValues(data) TYPE text(tokenizer = splitByNonAlpha)
)
ENGINE = MergeTree
ORDER BY id;

```


```
SELECT * FROM events WHERE data.user_name = 'alice';
SELECT * FROM events WHERE data.message LIKE '% error %';
SELECT * FROM events WHERE startsWith(data.status, 'fail');
SELECT * FROM events WHERE hasToken(data.title, 'clickhouse');

```


```
SELECT * FROM events WHERE hasAllTokens(data.message::String, 'connection timeout');
SELECT * FROM events WHERE data.status_code::UInt64 = 404;
SELECT * FROM events WHERE has(data.tags::Array(String), 'bug')

```


```
SELECT * FROM events WHERE data.level IN ('error', 'critical');

```


### Фразовый поиск


```
SELECT *
FROM tab
WHERE hasAllTokens(col, 'weather in Tokyo')

```


```
SELECT *
FROM tab
WHERE hasPhrase(col, 'weather in Tokyo')

```


#### Пример


```
CREATE TABLE tab (
    id UInt32,
    text String,
    INDEX idx text TYPE text(tokenizer = splitByNonAlpha)
)
ENGINE = MergeTree
ORDER BY id;

INSERT INTO tab VALUES
    (1, 'weather in New York'),
    (2, 'New weather in York'),
    (3, 'weather in New Orleans');

```


```
SELECT id, text FROM tab WHERE hasPhrase(text, 'weather in New York');

```


```
   ┌─id─┬─text────────────────┐
1. │  1 │ weather in New York │
   └────┴─────────────────────┘

```


## Настройка производительности


### Прямое чтение


```
SELECT column_a, column_b, ...
FROM [...]
WHERE string_search_function(column_with_text_index)

```

- Настройка [query_plan_direct_read_from_text_index](https://clickhouse.com/docs/ru/reference/settings/session-settings#query_plan_direct_read_from_text_index) (по умолчанию true), которая определяет, включено ли прямое чтение в целом.
- Настройка [use_skip_indexes_on_data_read](https://clickhouse.com/docs/ru/reference/settings/session-settings#use_skip_indexes_on_data_read) была обязательным предварительным условием для прямого чтения в версиях ClickHouse < 26.4.

```
EXPLAIN PLAN actions = 1
SELECT count()
FROM table
WHERE hasToken(col, 'some_token')
SETTINGS query_plan_direct_read_from_text_index = 0, -- отключить прямое чтение

```


```
[...]
Filter ((WHERE + Change column names to column identifiers))
Filter column: hasToken(__table1.col, 'some_token'_String) (removed)
Actions: INPUT : 0 -> col String : 0
         COLUMN Const(String) -> 'some_token'_String String : 1
         FUNCTION hasToken(col :: 0, 'some_token'_String :: 1) -> hasToken(__table1.col, 'some_token'_String) UInt8 : 2
[...]

```


```
EXPLAIN PLAN actions = 1
SELECT count()
FROM table
WHERE hasToken(col, 'some_token')
SETTINGS query_plan_direct_read_from_text_index = 1, -- включить прямое чтение

```


```
[...]
Expression (Before GROUP BY)
Positions:
  Filter
  Filter column: __text_index_idx_hasToken_94cc2a813036b453d84b6fb344a63ad3 (removed)
  Actions: INPUT :: 0 -> __text_index_idx_hasToken_94cc2a813036b453d84b6fb344a63ad3 UInt8 : 0
[...]

```


```
EXPLAIN actions = 1
SELECT count()
FROM table
WHERE (col LIKE '%some-token%') AND (d >= today())
SETTINGS query_plan_text_index_add_hint = 0
FORMAT TSV

```


```
[...]
Prewhere filter column: and(like(__table1.col, \'%some-token%\'_String), greaterOrEquals(__table1.d, _CAST(20440_Date, \'Date\'_String))) (removed)
[...]

```


```
EXPLAIN actions = 1
SELECT count()
FROM table
WHERE col LIKE '%some-token%'
SETTINGS query_plan_text_index_add_hint = 1

```


```
[...]
Prewhere filter column: and(__text_index_idx_col_like_d306f7c9c95238594618ac23eb7a3f74, like(__table1.col, \'%some-token%\'_String), greaterOrEquals(__table1.d, _CAST(20440_Date, \'Date\'_String))) (removed)
[...]

```


### Запросы LIKE/ILIKE

- [use_text_index_like_evaluation_by_dictionary_scan](https://clickhouse.com/docs/ru/reference/settings/session-settings#use_text_index_like_evaluation_by_dictionary_scan)
- [text_index_like_min_pattern_length](https://clickhouse.com/docs/ru/reference/settings/session-settings#text_index_like_min_pattern_length)
- [text_index_like_max_postings_to_read](https://clickhouse.com/docs/ru/reference/settings/session-settings#text_index_like_max_postings_to_read)

### Кэширование


#### Настройки кэша токенов


| Параметр | Описание |
| --- | --- |
| [text_index_tokens_cache_policy](https://clickhouse.com/docs/ru/reference/settings/server-settings/settings#text_index_tokens_cache_policy) | Имя политики кэша токенов текстового индекса. |
| [text_index_tokens_cache_size](https://clickhouse.com/docs/ru/reference/settings/server-settings/settings#text_index_tokens_cache_size) | Максимальный размер кэша в байтах. |
| [text_index_tokens_cache_max_entries](https://clickhouse.com/docs/ru/reference/settings/server-settings/settings#text_index_tokens_cache_max_entries) | Максимальное количество десериализованных токенов в кэше. |
| [text_index_tokens_cache_size_ratio](https://clickhouse.com/docs/ru/reference/settings/server-settings/settings#text_index_tokens_cache_size_ratio) | Размер защищённой очереди в кэше токенов текстового индекса относительно общего размера кэша. |


#### Настройки кэша заголовков


| Setting | Description |
| --- | --- |
| [text_index_header_cache_policy](https://clickhouse.com/docs/ru/reference/settings/server-settings/settings#text_index_header_cache_policy) | Имя политики кэша заголовков текстового индекса. |
| [text_index_header_cache_size](https://clickhouse.com/docs/ru/reference/settings/server-settings/settings#text_index_header_cache_size) | Максимальный размер кэша в байтах. |
| [text_index_header_cache_max_entries](https://clickhouse.com/docs/ru/reference/settings/server-settings/settings#text_index_header_cache_max_entries) | Максимальное количество десериализованных заголовков в кэше. |
| [text_index_header_cache_size_ratio](https://clickhouse.com/docs/ru/reference/settings/server-settings/settings#text_index_header_cache_size_ratio) | Размер защищённой очереди в кэше заголовков текстового индекса относительно общего размера кэша. |


#### Настройки кэша списков вхождений


| Настройка | Описание |
| --- | --- |
| [text_index_postings_cache_policy](https://clickhouse.com/docs/ru/reference/settings/server-settings/settings#text_index_postings_cache_policy) | Имя политики кэша списков вхождений текстового индекса. |
| [text_index_postings_cache_size](https://clickhouse.com/docs/ru/reference/settings/server-settings/settings#text_index_postings_cache_size) | Максимальный размер кэша в байтах. |
| [text_index_postings_cache_max_entries](https://clickhouse.com/docs/ru/reference/settings/server-settings/settings#text_index_postings_cache_max_entries) | Максимальное количество десериализованных списков вхождений в кэше. |
| [text_index_postings_cache_size_ratio](https://clickhouse.com/docs/ru/reference/settings/server-settings/settings#text_index_postings_cache_size_ratio) | Размер защищённой очереди в кэше списков вхождений текстового индекса относительно общего размера кэша. |


## Ограничения

- Материализация текстовых индексов с большим количеством токенов (например, 10 миллиардов токенов) может потреблять значительный объём памяти. Материализация текстового индекса может происходить напрямую (`ALTER TABLE <table> MATERIALIZE INDEX <index>`) или косвенно во время слияния частей.
- Невозможно материализовать текстовые индексы для частей, содержащих более 4.294.967.296 (= 2^32 = около 4,2 миллиарда) строк. Без материализованного текстового индекса запросы переходят к медленному полному перебору внутри части. Для оценки наихудшего случая предположим, что часть содержит один столбец типа String и настройка MergeTree `max_bytes_to_merge_at_max_space_in_pool` (по умолчанию: 150 GB) не изменялась. В этом случае такая ситуация возникает, если в столбце в среднем содержится менее 29,5 символа на строку. На практике таблицы также содержат другие столбцы, и этот порог в несколько раз ниже (в зависимости от количества, типа и размера других столбцов).

## Текстовые индексы и индексы на основе фильтра Блума

- Основаны на вероятностных структурах данных, которые могут давать ложноположительные срабатывания.
- Способны отвечать только на вопросы о принадлежности множеству, то есть столбец может содержать токен X или точно не содержать X.
- Хранят информацию на уровне гранул, что позволяет пропускать крупные диапазоны при выполнении запроса.
- Их сложно правильно настроить (пример см. [здесь](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/mergetree#n-gram-bloom-filter)).
- Они довольно компактны (от нескольких килобайт до нескольких мегабайт на часть).
- Строят детерминированный инвертированный индекс по токенам. Сам индекс не может давать ложноположительных срабатываний.
- Специально оптимизированы для полнотекстового поиска.
- Хранят информацию на уровне строк, что обеспечивает эффективный поиск по терминам.
- Они довольно велики (от десятков до сотен мегабайт на часть).
- Они не поддерживают расширенную токенизацию и предобработку.
- Они не поддерживают поиск по нескольким токенам.
- Они не обеспечивают характеристик производительности, ожидаемых от инвертированного индекса.
- Они обеспечивают токенизацию и предобработку
- Они эффективно поддерживают `hasAllTokens`, `LIKE`, `match` и аналогичные функции текстового поиска.
- Они значительно лучше масштабируются на больших текстовых корпусах.

## Подробности реализации

- словаря, который сопоставляет каждому токену список вхождений, и
- набора списков вхождений, каждый из которых представляет собой множество номеров строк.

## Пример: датасет Hacker News


```
CREATE TABLE hackernews (
    id UInt64,
    deleted UInt8,
    type String,
    author String,
    timestamp DateTime,
    comment String,
    dead UInt8,
    parent UInt64,
    poll UInt64,
    children Array(UInt32),
    url String,
    score UInt32,
    title String,
    parts Array(UInt32),
    descendants UInt32
)
ENGINE = MergeTree
ORDER BY (type, author);

```


```
INSERT INTO hackernews
    SELECT * FROM s3Cluster(
        'default',
        'https://datasets-documentation.s3.eu-west-3.amazonaws.com/hackernews/hacknernews.parquet',
        'Parquet',
        '
    id UInt64,
    deleted UInt8,
    type String,
    by String,
    time DateTime,
    text String,
    dead UInt8,
    parent UInt64,
    poll UInt64,
    kids Array(UInt32),
    url String,
    score UInt32,
    title String,
    parts Array(UInt32),
    descendants UInt32');

```


```
-- Add the index
ALTER TABLE hackernews ADD INDEX comment_idx comment TYPE text(tokenizer = splitByNonAlpha);

-- Materialize the index for existing data
ALTER TABLE hackernews MATERIALIZE INDEX comment_idx SETTINGS mutations_sync = 2;

```


### 1. Использование `hasToken`


```
SELECT count()
FROM hackernews
WHERE hasToken(comment, 'ClickHouse')
SETTINGS query_plan_direct_read_from_text_index = 0;

┌─count()─┐
│     516 │
└─────────┘

1 row in set. Elapsed: 0.362 sec. Processed 24.90 million rows, 9.51 GB

```


```
SELECT count()
FROM hackernews
WHERE hasToken(comment, 'ClickHouse')
SETTINGS query_plan_direct_read_from_text_index = 1;

┌─count()─┐
│     516 │
└─────────┘

1 row in set. Elapsed: 0.008 sec. Processed 3.15 million rows, 3.15 MB

```


### 2. Использование `hasAnyTokens`


```
SELECT count()
FROM hackernews
WHERE hasAnyTokens(comment, 'love ClickHouse')
SETTINGS query_plan_direct_read_from_text_index = 0;

┌─count()─┐
│  408426 │
└─────────┘

1 row in set. Elapsed: 1.329 sec. Processed 28.74 million rows, 9.72 GB

```


```
SELECT count()
FROM hackernews
WHERE hasAnyTokens(comment, 'love ClickHouse')
SETTINGS query_plan_direct_read_from_text_index = 1;

┌─count()─┐
│  408426 │
└─────────┘

1 row in set. Elapsed: 0.015 sec. Processed 27.99 million rows, 27.99 MB

```


### 3. Использование `hasAllTokens`


```
SELECT count()
FROM hackernews
WHERE hasAllTokens(comment, 'love ClickHouse')
SETTINGS query_plan_direct_read_from_text_index = 0;

┌─count()─┐
│      11 │
└─────────┘

1 row in set. Elapsed: 0.184 sec. Processed 147.46 thousand rows, 57.03 MB

```


```
SELECT count()
FROM hackernews
WHERE hasAllTokens(comment, 'love ClickHouse')
SETTINGS query_plan_direct_read_from_text_index = 1;

┌─count()─┐
│      11 │
└─────────┘

1 row in set. Elapsed: 0.007 sec. Processed 147.46 thousand rows, 147.46 KB

```


### 4. Составной поиск: OR, AND, NOT, …


```
SELECT count()
FROM hackernews
WHERE hasToken(comment, 'ClickHouse') OR hasToken(comment, 'clickhouse')
SETTINGS query_plan_direct_read_from_text_index = 0;

┌─count()─┐
│     769 │
└─────────┘

1 row in set. Elapsed: 0.450 sec. Processed 25.87 million rows, 9.58 GB

```


```
SELECT count()
FROM hackernews
WHERE hasToken(comment, 'ClickHouse') OR hasToken(comment, 'clickhouse')
SETTINGS query_plan_direct_read_from_text_index = 1;

┌─count()─┐
│     769 │
└─────────┘

1 row in set. Elapsed: 0.013 sec. Processed 25.87 million rows, 51.73 MB

```


## Связанные материалы

- Блог: [Объявляем о выходе полнотекстового поиска ClickHouse в General Availability](https://clickhouse.com/blog/full-text-search-ga-release)
- Блог: [Создание высокопроизводительного полнотекстового поиска для Объектного хранилища](https://clickhouse.com/blog/clickhouse-full-text-search-object-storage)
- Видео: [Введение в полнотекстовый поиск в ClickHouse](https://www.youtube.com/watch?v=9zPmf1a_heU)
- Видео: [Что внутри: полнотекстовый поиск в ClickHouse при его масштабе и скорости](https://www.youtube.com/watch?v=8JbqE_ubfkU)
- Презентация: [Полнотекстовый поиск в ClickHouse изнутри: быстрый, нативный и столбцовый](https://github.com/ClickHouse/clickhouse-presentations/blob/master/2025-tumuchdata-munich/ClickHouse_%20full-text%20search%20-%2011.11.2025%20Munich%20Database%20Meetup.pdf)
- Презентация: [Инвертированные индексы баз данных: зачем, что и как, FOSDEM 2026](https://presentations.clickhouse.com/2026-fosdem-inverted-index/Inverted_indexes_the_what_the_why_the_how.pdf)
- Блог: [Представляем инвертированные индексы в ClickHouse](https://clickhouse.com/blog/clickhouse-search-with-inverted-indices)
- Блог: [Полнотекстовый поиск в ClickHouse изнутри: быстрый, нативный и столбцовый](https://clickhouse.com/blog/clickhouse-full-text-search)
- Видео: [Полнотекстовые индексы: проектирование и эксперименты](https://www.youtube.com/watch?v=O_MnyUkrIq8)
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
