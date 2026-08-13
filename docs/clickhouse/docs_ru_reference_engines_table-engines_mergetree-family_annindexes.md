# Точный и приближённый векторный поиск - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/annindexes

- Точный векторный поиск вычисляет расстояние между заданной точкой и всеми точками векторного пространства. Это обеспечивает максимально возможную точность, то есть возвращённые точки гарантированно являются истинными ближайшими соседями. Поскольку векторное пространство просматривается полностью, точный векторный поиск может быть слишком медленным для практического применения.
- Приближённый векторный поиск — это группа методов (например, специальные структуры данных, такие как графы и случайные леса), которые позволяют получать результаты гораздо быстрее, чем точный векторный поиск. Точность результата обычно является “достаточно хорошей” для практического использования. Многие приближённые методы предоставляют параметры для настройки компромисса между точностью результата и временем поиска.

```
WITH [...] AS reference_vector
SELECT [...]
FROM table
WHERE [...] -- предложение WHERE необязательно
ORDER BY <DistanceFunction>(vectors, reference_vector)
LIMIT <N>

```


## Точный векторный поиск


### Пример


```
CREATE TABLE tab(id Int32, vec Array(Float32)) ENGINE = MergeTree ORDER BY id;

INSERT INTO tab VALUES (0, [1.0, 0.0]), (1, [1.1, 0.0]), (2, [1.2, 0.0]), (3, [1.3, 0.0]), (4, [1.4, 0.0]), (5, [1.5, 0.0]), (6, [0.0, 2.0]), (7, [0.0, 2.1]), (8, [0.0, 2.2]), (9, [0.0, 2.3]), (10, [0.0, 2.4]), (11, [0.0, 2.5]);

WITH [0., 2.] AS reference_vec
SELECT id, vec
FROM tab
ORDER BY L2Distance(vec, reference_vec) ASC
LIMIT 3;

```


```
   ┌─id─┬─vec─────┐
1. │  6 │ [0,2]   │
2. │  7 │ [0,2.1] │
3. │  8 │ [0,2.2] │
   └────┴─────────┘

```


## Приближённый векторный поиск


### Индексы векторного сходства


#### Создание индекса векторного сходства


```
CREATE TABLE table
(
  [...],
  vectors Array(Float*),
  INDEX <index_name> vectors TYPE vector_similarity(<type>, <distance_function>, <dimensions>) [GRANULARITY <N>]
)
ENGINE = MergeTree
ORDER BY [...]

```


```
ALTER TABLE table ADD INDEX <index_name> vectors TYPE vector_similarity(<type>, <distance_function>, <dimensions>) [GRANULARITY <N>];

```


```
ALTER TABLE table MATERIALIZE INDEX <index_name> SETTINGS mutations_sync = 2;

```

- `L2Distance` — [евклидово расстояние](https://en.wikipedia.org/wiki/Euclidean_distance), то есть длину отрезка между двумя точками в евклидовом пространстве,
- `cosineDistance` — [косинусное расстояние](https://en.wikipedia.org/wiki/Cosine_similarity#Cosine_distance), то есть угол между двумя ненулевыми векторами, или
- `dotProduct` — [скалярное произведение](https://en.wikipedia.org/wiki/Dot_product) (внутреннее произведение), то есть сумму попарных произведений элементов двух векторов. Для нормализованных данных эквивалентно `cosineDistance`.

```
CREATE TABLE table
(
  [...],
  vectors Array(Float*),
  INDEX index_name vectors TYPE vector_similarity('hnsw', <distance_function>, <dimensions>[, <quantization>, <hnsw_max_connections_per_layer>, <hnsw_candidate_list_size_for_construction>]) [GRANULARITY N]
)
ENGINE = MergeTree
ORDER BY [...]

```

- `<quantization>` управляет квантованием векторов в графе близости. Возможные значения: `f64`, `f32`, `f16`, `bf16`, `i8` или `b1`. Значение по умолчанию — `bf16`. Обратите внимание, что этот параметр не влияет на представление векторов в исходном столбце.
- `<hnsw_max_connections_per_layer>` управляет числом соседей для каждого узла графа, также известным как гиперпараметр HNSW `M`. Значение по умолчанию — `32`. Значение `0` означает использование значения по умолчанию.
- `<hnsw_candidate_list_size_for_construction>` управляет размером динамического списка кандидатов при построении графа HNSW, также известным как гиперпараметр HNSW `ef_construction`. Значение по умолчанию — `128`. Значение `0` означает использование значения по умолчанию.
- Индексы векторного сходства можно создавать только для столбцов типа [Array(Float32)](https://clickhouse.com/docs/ru/reference/data-types/array), [Array(Float64)](https://clickhouse.com/docs/ru/reference/data-types/array) или [Array(BFloat16)](https://clickhouse.com/docs/ru/reference/data-types/array). Массивы nullable- и low-cardinality-значений с плавающей точкой, такие как `Array(Nullable(Float32))` и `Array(LowCardinality(Float32))`, не допускаются.
- Индексы векторного сходства должны создаваться для одиночных столбцов.
- Индексы векторного сходства можно создавать для вычисляемых выражений (например, `INDEX index_name arraySort(vectors) TYPE vector_similarity([...])`), но такие индексы впоследствии нельзя использовать для приближённого поиска соседей.
- Индексы векторного сходства требуют, чтобы все массивы в исходном столбце содержали по `<dimension>` элементов — это проверяется при создании индекса. Чтобы как можно раньше выявлять нарушения этого требования, пользователи могут добавить [ограничение](https://clickhouse.com/docs/ru/reference/statements/create/table#constraints) для векторного столбца, например `CONSTRAINT same_length CHECK length(vectors) = 256`.
- Аналогично, значения массива в исходном столбце не должны быть пустыми (`[]`) или иметь значение по умолчанию (тоже `[]`).

```
Storage consumption = Number of vectors * Dimension * Size of column data type

```


```
Storage consumption = 1 million * 1536 * 4 (for Float32) = 6.1 GB

```


```
Память для векторов в индексе (mv) = Количество векторов * Размерность * Размер квантованного типа данных
Память для графа в памяти (mg) = Количество векторов * hnsw_max_connections_per_layer * Bytes_per_node_id (= 4) * Layer_node_repetition_factor (= 2)

Потребление памяти: mv + mg

```


```
Память для векторов в индексе (mv) = 1 миллион * 1536 * 2 (для BFloat16) = 3072 МБ
Память для графа в оперативной памяти (mg) = 1 миллион * 64 * 2 * 4 = 512 МБ

Потребление памяти = 3072 + 512 = 3584 МБ

```


#### Использование индекса векторного сходства


```
WITH [...] AS reference_vector
SELECT [...]
FROM table
WHERE [...] -- предложение WHERE не является обязательным
ORDER BY <DistanceFunction>(vectors, reference_vector)
LIMIT <N>

```


```
EXPLAIN indexes = 1
WITH [0.462, 0.084, ..., -0.110] AS reference_vec
SELECT id, vec
FROM tab
ORDER BY L2Distance(vec, reference_vec) ASC
LIMIT 10;

```


```
┌─explain─────────────────────────────────────────────────────────────────────────────────────────┐
 1. │ Expression (Project names)                                                                      │
 2. │   Limit (preliminary LIMIT (without OFFSET))                                                    │
 3. │     Sorting (Sorting for ORDER BY)                                                              │
 4. │       Expression ((Before ORDER BY + (Projection + Change column names to column identifiers))) │
 5. │         ReadFromMergeTree (default.tab)                                                         │
 6. │         Indexes:                                                                                │
 7. │           PrimaryKey                                                                            │
 8. │             Condition: true                                                                     │
 9. │             Parts: 1/1                                                                          │
10. │             Granules: 575/575                                                                   │
11. │           Skip                                                                                  │
12. │             Name: idx                                                                           │
13. │             Description: vector_similarity GRANULARITY 100000000                                │
14. │             Parts: 1/1                                                                          │
15. │             Granules: 10/575                                                                    │
    └─────────────────────────────────────────────────────────────────────────────────────────────────┘

```

- Постфильтрация означает, что сначала используется индекс векторного сходства, а затем ClickHouse применяет дополнительные фильтры, указанные в предложении `WHERE`.
- Префильтрация означает, что порядок применения фильтра становится обратным.
- У постфильтрации есть общая проблема: она может вернуть меньше строк, чем указано в секции `LIMIT <N>`. Это происходит, когда одна или несколько строк результата, возвращённых индексом векторного сходства, не проходят дополнительные фильтры.
- Префильтрация в общем случае остаётся нерешённой задачей. Некоторые специализированные векторные базы данных поддерживают алгоритмы префильтрации, но большинство реляционных баз данных (включая ClickHouse) переходят к точному поиску ближайших соседей, то есть к полному перебору без индекса.

```
WITH [0., 2.] AS reference_vec
SELECT id, vec
FROM tab
WHERE year = 2025
ORDER BY L2Distance(vec, reference_vec) ASC
LIMIT 3;

```

- условие фильтрации отбрасывает хотя бы одну строку в пределах части, ClickHouse переключится на префильтрацию для “оставшихся” диапазонов внутри этой части,
- условие фильтрации не отбрасывает ни одной строки в пределах части, ClickHouse выполнит постфильтрацию для этой части.

```
SELECT bookid, author, title
FROM books
WHERE price < 2.00
ORDER BY cosineDistance(book_vector, getEmbedding('Books on ancient Asian empires'))
LIMIT 10

```


```
SELECT bookid, author, title
FROM books
WHERE price < 2.00
ORDER BY cosineDistance(book_vector, getEmbedding('Books on ancient Asian empires'))
LIMIT 10
SETTING vector_search_index_fetch_multiplier = 3.0;

```


```
EXPLAIN header = 1
WITH [0., 2.] AS reference_vec
SELECT id
FROM tab
ORDER BY L2Distance(vec, reference_vec) ASC
LIMIT 3
SETTINGS vector_search_with_rescoring = 0

```


```
Query id: a2a9d0c8-a525-45c1-96ca-c5a11fa66f47

    ┌─explain─────────────────────────────────────────────────────────────────────────────────────────────────┐
 1. │ Expression (Project names)                                                                              │
 2. │ Header: id Int32                                                                                        │
 3. │   Limit (preliminary LIMIT (without OFFSET))                                                            │
 4. │   Header: L2Distance(__table1.vec, _CAST([0., 2.]_Array(Float64), 'Array(Float64)'_String)) Float64     │
 5. │           __table1.id Int32                                                                             │
 6. │     Sorting (Sorting for ORDER BY)                                                                      │
 7. │     Header: L2Distance(__table1.vec, _CAST([0., 2.]_Array(Float64), 'Array(Float64)'_String)) Float64   │
 8. │             __table1.id Int32                                                                           │
 9. │       Expression ((Before ORDER BY + (Projection + Change column names to column identifiers)))         │
10. │       Header: L2Distance(__table1.vec, _CAST([0., 2.]_Array(Float64), 'Array(Float64)'_String)) Float64 │
11. │               __table1.id Int32                                                                         │
12. │         ReadFromMergeTree (default.tab)                                                                 │
13. │         Header: id Int32                                                                                │
14. │                 _distance Float32                                                                       │
    └─────────────────────────────────────────────────────────────────────────────────────────────────────────┘

```


#### Настройка производительности


```
CREATE TABLE tab(id Int32, vec Array(Float32) CODEC(NONE), INDEX idx vec TYPE vector_similarity('hnsw', 'L2Distance', 2)) ENGINE = MergeTree ORDER BY id;

```


```
2026-02-03 07:39:10.351635 [1386] f0ac5c85-1b1c-4f35-8848-87a1d1aa00ba : VectorSimilarityIndex Start loading vector similarity index

<...>

2026-02-03 07:40:25.217603 [1386] f0ac5c85-1b1c-4f35-8848-87a1d1aa00ba : VectorSimilarityIndex Loaded vector similarity index: max_level = 2, connectivity = 64, size = 1808111, capacity = 1808111, memory_usage = 8.00 GiB, bytes_per_vector = 4096, scalar_words = 1024, nodes = 1808111, edges = 51356964, max_edges = 233395072

```


```
SELECT metric, value
FROM system.metrics
WHERE metric = 'VectorSimilarityIndexCacheBytes'

```


```
SYSTEM FLUSH LOGS query_log;

SELECT ProfileEvents['VectorSimilarityIndexCacheHits'], ProfileEvents['VectorSimilarityIndexCacheMisses']
FROM system.query_log
WHERE type = 'QueryFinish' AND query_id = '<...>'
ORDER BY event_time_microseconds;

```


| Квантование | Название | Хранилище на размерность |
| --- | --- | --- |
| f32 | Одинарная точность | 4 байта |
| f16 | Половинная точность | 2 байта |
| bf16 (default) | Половинная точность (brain float) | 2 байта |
| i8 | Четвертная точность | 1 байт |
| b1 | Двоичное | 1 бит |


```
search_v = openai_client.embeddings.create(input = "[Good Books]", model='text-embedding-3-large', dimensions=1536).data[0].embedding

params = {'search_v': search_v}
result = chclient.query(
   "SELECT id FROM items
    ORDER BY cosineDistance(vector, %(search_v)s)
    LIMIT 10",
    parameters = params)

```


```
search_v = openai_client.embeddings.create(input = "[Good Books]", model='text-embedding-3-large', dimensions=1536).data[0].embedding

params = {'$search_v_binary$': np.array(search_v, dtype=np.float32).tobytes()}
result = chclient.query(
   "SELECT id FROM items
    ORDER BY cosineDistance(vector, reinterpret($search_v_binary$, 'Array(Float32)'))
    LIMIT 10"
    parameters = params)

```


#### Администрирование и мониторинг


```
SELECT database, table, name, formatReadableSize(data_compressed_bytes)
FROM system.data_skipping_indices
WHERE type = 'vector_similarity';

```


```
┌─database─┬─table─┬─name─┬─formatReadab⋯ssed_bytes)─┐
│ default  │ tab   │ idx  │ 348.00 MB                │
└──────────┴───────┴──────┴──────────────────────────┘

```


#### Отличия от обычных индексов пропуска данных


#### Пример


```
CREATE TABLE tab(id Int32, vec Array(Float32), INDEX idx vec TYPE vector_similarity('hnsw', 'L2Distance', 2)) ENGINE = MergeTree ORDER BY id;

INSERT INTO tab VALUES (0, [1.0, 0.0]), (1, [1.1, 0.0]), (2, [1.2, 0.0]), (3, [1.3, 0.0]), (4, [1.4, 0.0]), (5, [1.5, 0.0]), (6, [0.0, 2.0]), (7, [0.0, 2.1]), (8, [0.0, 2.2]), (9, [0.0, 2.3]), (10, [0.0, 2.4]), (11, [0.0, 2.5]);

WITH [0., 2.] AS reference_vec
SELECT id, vec
FROM tab
ORDER BY L2Distance(vec, reference_vec) ASC
LIMIT 3;

```


```
   ┌─id─┬─vec─────┐
1. │  6 │ [0,2]   │
2. │  7 │ [0,2.1] │
3. │  8 │ [0,2.2] │
   └────┴─────────┘

```

- [LAION-400M](https://clickhouse.com/docs/ru/get-started/sample-datasets/laion)
- [LAION-5B](https://clickhouse.com/docs/ru/get-started/sample-datasets/laion5b)
- [dbpedia](https://clickhouse.com/docs/ru/get-started/sample-datasets/dbpedia)
- [hackernews](https://clickhouse.com/docs/ru/get-started/sample-datasets/hacker-news-vector-search)

### Векторный поиск с квантизованными кодеками


#### Введение

- **Масштаб.** Время, необходимое для построения графа, и объём памяти для его хранения — помимо самих векторов — становятся основными затратами.
- **Фильтрация.** При селективном предложении `WHERE` обход графа становится неэффективным, поскольку либо не удаётся добраться до небольшого множества строк, удовлетворяющих предикату, либо приходится проверять непропорционально большое число кандидатов, чтобы их найти.

#### Объявление кодека


```
SET allow_experimental_codecs = 1;

CREATE TABLE vectors
(
    id UInt32,
    vec Array(Float32) CODEC(Quantized('rabitq', 1536))
)
ENGINE = MergeTree ORDER BY id;

```


#### Методы квантования

- `Quantized('rabitq', dimensions)` — один знаковый бит на координату плюс несмещённый коэффициент коррекции косинуса (`dimensions/8 + 4` байта). Небольшой, быстрый для `popcount`, хороший вариант по умолчанию. Только `cosineDistance`.
- `Quantized('turboquant', dimensions)` — два бита на координату (1-битный код MSE и 1-битный код остатка) для кандидатов с более высокой точностью (`dimensions/4 + 4` байта). Только `cosineDistance`.
- `Quantized('int8', dimensions)` — один код `Int8` на координату плюс норма вектора (`dimensions + 4` байта); самый крупный, но и наиболее точно передающий значения плоский код. Поддерживает `L2Distance` и `cosineDistance`.
- `Quantized('prefix', dimensions, leading_dimensions, 'int8'|'bf16')` — Matryoshka: сохраняет только первые `leading_dimensions` координат в формате `Int8` (с масштабом для каждого вектора) или `BFloat16`. Очень компактные коды для эмбеддингов, обученных с использованием Matryoshka Representation Learning. Поддерживает `L2Distance` и `cosineDistance`.
- `Quantized('product', dimensions, nbits, m)` — Product Quantization: кодовая книга для каждой части, обученная методом k-means; каждый вектор преобразуется в `m` кодов по `nbits` бит (поэтому `dimensions` должно быть кратно `m`). Самый компактный вариант и максимальная полнота на байт, но требует этапа обучения во время вставки. Поддерживает `L2Distance` и `cosineDistance`.

#### Прозрачный поиск


```
WITH [/* reference vector of `dimensions` floats */] AS reference_vec
SELECT id
FROM vectors
ORDER BY cosineDistance(vec, reference_vec) ASC
LIMIT 10
SETTINGS vector_search_use_quantized_codes = 1;

```


#### Настройки

- `allow_experimental_codecs` — должен быть включен, чтобы можно было объявить кодек `Quantized` (по умолчанию: `0`).
- `vector_search_use_quantized_codes` — включает двухстадийное преобразование с отбором shortlist и пересчётом оценок (по умолчанию: `0`). Если параметр выключен, поисковые запросы выполняют точное сканирование векторов с полной точностью.
- `vector_search_index_fetch_multiplier` — сколько кандидатов включать в shortlist относительно `LIMIT` запроса: при сканировании сохраняются лучшие `LIMIT × multiplier` кодов перед пересчётом оценок. Чем больше значение, тем выше полнота, но тем больше объём пересчёта оценок. Значение по умолчанию — `1` (без избыточной выборки), поэтому для хорошей полноты его обычно нужно увеличить, например до `10` или выше.

#### Рассчитано на масштабирование

- **Векторизовано.** Ядра сканирования написаны под SIMD, с выбором во время выполнения самых широких инструкций, которые поддерживает CPU: аппаратный `popcount` для методов sign-code (`rabitq`, `turboquant`) и широкие инструкции fused-multiply-add для остальных.
- **Параллельно по ядрам и частям.** Линейное сканирование легко распараллеливается, и ClickHouse именно так его и обрабатывает: расстояния вычисляются сразу во всех доступных потоках и по всем частям таблицы, и только финальное слияние top-`k` выполняется последовательно.
- **Распределённо.** В сегментированном кластере работа распределяется по машинам — каждый сегмент параллельно сканирует свою часть данных, а координатор объединяет shortlist’ы.
- **Столбцовый формат и удобная фильтрация.** Квантованные коды занимают отдельный столбец, сжимаются и читаются по тому же пути I/O, что и любой другой столбец, поэтому выборочное `WHERE` просто оставляет меньше кодов для сканирования.
- **Без отдельного этапа построения.** Коды создаются по мере записи векторов и объединяются конкатенацией — индекс не нужно строить, настраивать или перестраивать, поэтому таблица готова к поиску сразу после поступления данных.

### Квантованный бит (QBit)

- Хранения исходных данных с полной точностью.
- Возможности задавать точность квантования во время выполнения запроса.

```
column_name QBit(element_type, dimension[, stride])

```

- `element_type` – тип каждого элемента вектора. Поддерживаемые типы: `Int8`, `BFloat16`, `Float32` и `Float64`
- `dimension` – количество элементов в каждом векторе
- `stride` – необязательно. Делитель `dimension`, который разбивает размерности на `dimension / stride` смежных групп, хранящихся в отдельных потоках, так что при поиске только по первым размерностям считывается меньше потоков (полезно для эмбеддинг-векторов Matryoshka). По умолчанию используется `dimension`; в этом случае тип побайтно идентичен `QBit` без `stride`. Подробности см. на [странице типа данных `QBit`](https://clickhouse.com/docs/ru/reference/data-types/qbit).

#### Создание таблицы `QBit` и добавление в неё данных


```
CREATE TABLE fruit_animal (
    word String,
    vec QBit(Float64, 5)
) ENGINE = MergeTree
ORDER BY word;

INSERT INTO fruit_animal VALUES
    ('apple', [-0.99105519, 1.28887844, -0.43526649, -0.98520696, 0.66154391]),
    ('banana', [-0.69372815, 0.25587061, -0.88226235, -2.54593015, 0.05300475]),
    ('orange', [0.93338752, 2.06571317, -0.54612565, -1.51625717, 0.69775337]),
    ('dog', [0.72138876, 1.55757105, 2.10953259, -0.33961248, -0.62217325]),
    ('cat', [-0.56611276, 0.52267331, 1.27839863, -0.59809804, -1.26721048]),
    ('horse', [-0.61435682, 0.48542571, 1.21091247, -0.62530446, -1.33082533]);

```


#### Векторный поиск с `QBit`


```
SELECT
    word,
    L2DistanceTransposed(vec, [-0.88693672, 1.31532824, -0.51182908, -0.99652702, 0.59907770], 64) AS distance
FROM fruit_animal
ORDER BY distance;

```


```
   ┌─word───┬────────────distance─┐
1. │ apple  │ 0.14639757188169716 │
2. │ banana │   1.998961369007679 │
3. │ orange │   2.039041552613732 │
4. │ cat    │   2.752802631487914 │
5. │ horse  │  2.7555776805484813 │
6. │ dog    │   3.382295083120104 │
   └────────┴─────────────────────┘

```


```
SELECT
    word,
    L2DistanceTransposed(vec, [-0.88693672, 1.31532824, -0.51182908, -0.99652702, 0.59907770], 12) AS distance
FROM fruit_animal
ORDER BY distance;

```


```
   ┌─word───┬───────────distance─┐
1. │ apple  │  0.757668703053566 │
2. │ orange │ 1.5499475034938677 │
3. │ banana │ 1.6168396735102937 │
4. │ cat    │  2.429752230904804 │
5. │ horse  │  2.524650475528617 │
6. │ dog    │   3.17766975527459 │
   └────────┴────────────────────┘

```


#### Особенности производительности

- **Более высокая точность** (ближе к исходной разрядности данных): более точные результаты, но запросы выполняются медленнее
- **Более низкая точность**: более быстрые запросы с приближенными результатами, меньшее использование памяти

### Справочные материалы

- [Векторный поиск с ClickHouse — Часть 1](https://clickhouse.com/blog/vector-search-clickhouse-p1)
- [Векторный поиск с ClickHouse — Часть 2](https://clickhouse.com/blog/vector-search-clickhouse-p2)
- [Мы создали движок векторного поиска, который позволяет выбирать точность на этапе выполнения запроса](https://clickhouse.com/blog/qbit-vector-search)
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
