# Оператор EXPLAIN - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/statements/explain


```
EXPLAIN [AST | SYNTAX | QUERY TREE | PLAN | PIPELINE | ANALYZE | ESTIMATE | TABLE OVERRIDE | WHATIF] [setting = value, ...]
    [
      SELECT ... |
      tableFunction(...) [COLUMNS (...)] [ORDER BY ...] [PARTITION BY ...] [PRIMARY KEY] [SAMPLE BY ...] [TTL ...]
    ]
    [FORMAT ...]

```


```
EXPLAIN SELECT sum(number) FROM numbers(10) UNION ALL SELECT sum(number) FROM numbers(10) ORDER BY sum(number) ASC FORMAT TSV;

```


```
Output: sum(number)

Union
├──Aggregating
│  │  Keys:
│  │  Aggregates: sum(number)
│  │  Skip merging: 0
│  └──ReadFromSystemNumbers
│        Output: number
└──Sorting (Sorting for ORDER BY)
   │  Sort description: sum(number) ASC
   └──Aggregating
      │  Keys:
      │  Aggregates: sum(number)
      │  Skip merging: 0
      └──ReadFromSystemNumbers
            Output: number

```


## Типы EXPLAIN

- `AST` — Абстрактное синтаксическое дерево.
- `SYNTAX` — Текст запроса после оптимизаций на уровне AST.
- `QUERY TREE` — Дерево запроса после оптимизаций на уровне дерева запроса.
- `PLAN` — План выполнения запроса.
- `PIPELINE` — Конвейер выполнения запроса.
- `ANALYZE` — Выполняет запрос и дополняет план выполнения измеренными метриками времени выполнения.
- `ESTIMATE` — Оценочное количество строк, меток и частей, которые будут прочитаны из таблиц при обработке запроса.
- `TABLE OVERRIDE` — Провалидированный результат переопределения таблицы в схеме табличной функции.

### EXPLAIN AST

- `graph` – Выводит AST в виде графа, описанного на языке описания графов [DOT](https://en.wikipedia.org/wiki/DOT_(graph_description_language)). По умолчанию: 0.

```
EXPLAIN AST SELECT 1;

```


```
SelectWithUnionQuery (children 1)
 ExpressionList (children 1)
  SelectQuery (children 1)
   ExpressionList (children 1)
    Literal UInt64_1

```


```
EXPLAIN AST ALTER TABLE t1 DELETE WHERE date = today();

```


```
  explain
  AlterQuery  t1 (children 1)
   ExpressionList (children 1)
    AlterCommand 27 (children 1)
     Function equals (children 1)
      ExpressionList (children 2)
       Identifier date
       Function today (children 1)
        ExpressionList

```


### EXPLAIN SYNTAX

- `oneline` – Выводить запрос в одну строку. По умолчанию: `0`.
- `run_query_tree_passes` – Выполнять проходы по дереву запроса перед выводом дерева запроса. По умолчанию: `0`.
- `query_tree_passes` – Если задано `run_query_tree_passes`, указывает, сколько проходов выполнить. Если `query_tree_passes` не указано, выполняются все проходы.

```
EXPLAIN SYNTAX SELECT * FROM system.numbers AS a, system.numbers AS b, system.numbers AS c WHERE a.number = b.number AND b.number = c.number;

```


```
SELECT *
FROM system.numbers AS a, system.numbers AS b, system.numbers AS c
WHERE (a.number = b.number) AND (b.number = c.number)

```


```
EXPLAIN SYNTAX run_query_tree_passes = 1 SELECT * FROM system.numbers AS a, system.numbers AS b, system.numbers AS c WHERE a.number = b.number AND b.number = c.number;

```


```
SELECT
    __table1.number AS `a.number`,
    __table2.number AS `b.number`,
    __table3.number AS `c.number`
FROM system.numbers AS __table1
ALL INNER JOIN system.numbers AS __table2 ON __table1.number = __table2.number
ALL INNER JOIN system.numbers AS __table3 ON __table2.number = __table3.number

```


### EXPLAIN QUERY TREE

- `run_passes` — Выполнить все проходы по дереву запроса перед его выводом. По умолчанию: `1`.
- `dump_passes` — Вывести информацию об использованных проходах по дереву запроса перед выводом дерева запроса. По умолчанию: `0`.
- `passes` — Указывает, сколько проходов по дереву запроса выполнить. Если задано значение `-1`, выполняются все проходы по дереву запроса. По умолчанию: `-1`.
- `dump_tree` — Показать дерево запроса. По умолчанию: `1`.
- `dump_ast` — Показать AST запроса, сгенерированное из дерева запроса. По умолчанию: `0`.

```
EXPLAIN QUERY TREE SELECT id, value FROM test_table;

```


```
QUERY id: 0
  PROJECTION COLUMNS
    id UInt64
    value String
  PROJECTION
    LIST id: 1, nodes: 2
      COLUMN id: 2, column_name: id, result_type: UInt64, source_id: 3
      COLUMN id: 4, column_name: value, result_type: String, source_id: 3
  JOIN TREE
    TABLE id: 3, table_name: default.test_table

```


### EXPLAIN PLAN

- `optimize` — Управляет тем, применять ли оптимизации плана запроса перед его отображением. Значение по умолчанию: 1.
- `header` — Выводит заголовок для шага. Значение по умолчанию: 0.
- `description` — Выводит описание шага. Значение по умолчанию: 1.
- `indexes` — Показывает используемые индексы, количество отфильтрованных частей и количество отфильтрованных гранул для каждого применённого индекса. Значение по умолчанию: 0. Поддерживается для таблиц [MergeTree](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/mergetree). Начиная с ClickHouse >= v25.9, этот оператор показывает осмысленный результат только при использовании с `SETTINGS use_query_condition_cache = 0, use_skip_indexes_on_data_read = 0`.
- `projections` — Показывает все проанализированные проекции и их влияние на фильтрацию на уровне частей на основе условий по первичному ключу проекции. Для каждой проекции в этом разделе приводится статистика, включая количество частей, строк, меток и диапазонов, оценённых с использованием первичного ключа проекции. Также показывается, сколько частей данных было пропущено благодаря этой фильтрации без чтения из самой проекции. Была ли проекция действительно использована для чтения или только проанализирована для фильтрации, можно определить по полю `description`. Значение по умолчанию: 0. Поддерживается для таблиц [MergeTree](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/mergetree).
- `actions` — Выводит подробную информацию о действиях шага. Значение по умолчанию: 1.
- `sorting` — Выводит описание сортировки для каждого шага плана, который формирует отсортированный вывод. Значение по умолчанию: 0.
- `keep_logical_steps` — Сохраняет логические шаги плана для JOIN вместо преобразования их в физические реализации JOIN. Значение по умолчанию: 0.
- `json` — Выводит шаги плана запроса как строку в формате [JSON](https://clickhouse.com/docs/ru/reference/formats/JSON/JSON). Значение по умолчанию: 0. Чтобы избежать лишнего экранирования, рекомендуется использовать формат [TabSeparatedRaw (TSVRaw)](https://clickhouse.com/docs/ru/reference/formats/TabSeparated/TabSeparatedRaw).
- `input_headers` — Выводит входные заголовки для шага. Значение по умолчанию: 0. В основном полезно только разработчикам для отладки проблем, связанных с несоответствием входных и выходных заголовков.
- `column_structure` — Также выводит структуру столбцов в заголовках помимо их имени и типа. Значение по умолчанию: 0. В основном полезно только разработчикам для отладки проблем, связанных с несоответствием входных и выходных заголовков.
- `distributed` — Показывает планы запроса, выполняемые на удалённых узлах для distributed таблиц или параллельных реплик. Не поддерживается вместе с `json`. Значение по умолчанию: 0.
- `compact` — Если включено, скрывает из плана шаги выражений и подробную информацию о действиях (входы, функции, псевдонимы и позиции вывода). Действует только при `actions = 1`. Значение по умолчанию: 1.
- `pretty` — Выводит дерево плана с использованием символов построения линий (├──, └──, │) вместо отступов для наглядного отображения иерархии. Также форматирует свойства шага JOIN в одну строку. Значение по умолчанию: 1.

```
EXPLAIN SELECT sum(number) FROM numbers(10) GROUP BY number % 4  LIMIT 1;

```


```
Output: sum(number)

Limit (preliminary LIMIT)
│  Limit 1
│  Offset 0
└──Aggregating
   │  Keys: number MOD 4
   │  Aggregates: sum(number)
   │  Skip merging: 0
   └──ReadFromSystemNumbers
         Output: number

```


```
EXPLAIN json = 1, description = 0 SELECT 1 UNION ALL SELECT 2 FORMAT TSVRaw;

```


```
[
  {
    "Plan": {
      "Node Type": "Union",
      "Node Id": "Union_10",
      "Plans": [
        {
          "Node Type": "Expression",
          "Node Id": "Expression_13",
          "Plans": [
            {
              "Node Type": "ReadFromStorage",
              "Node Id": "ReadFromStorage_0"
            }
          ]
        },
        {
          "Node Type": "Expression",
          "Node Id": "Expression_16",
          "Plans": [
            {
              "Node Type": "ReadFromStorage",
              "Node Id": "ReadFromStorage_4"
            }
          ]
        }
      ]
    }
  }
]

```


```
{
  "Node Type": "ReadFromStorage",
  "Description": "SystemOne"
}

```


```
EXPLAIN json = 1, description = 0, header = 1 SELECT 1, 2 + dummy;

```


```
[
  {
    "Plan": {
      "Node Type": "Expression",
      "Node Id": "Expression_5",
      "Header": [
        {
          "Name": "1",
          "Type": "UInt8"
        },
        {
          "Name": "plus(2, dummy)",
          "Type": "UInt16"
        }
      ],
      "Plans": [
        {
          "Node Type": "ReadFromStorage",
          "Node Id": "ReadFromStorage_0",
          "Header": [
            {
              "Name": "dummy",
              "Type": "UInt8"
            }
          ]
        }
      ]
    }
  }
]

```

- `Name` — имя индекса (в настоящее время используется только для индексов `Skip`).
- `Keys` — массив столбцов, используемых индексом.
- `Condition` — используемое условие.
- `Description` — описание индекса (в настоящее время используется только для индексов `Skip`).
- `Parts` — количество частей после/до применения индекса.
- `Granules` — количество гранул после/до применения индекса.
- `Ranges` — количество диапазонов гранул после применения индекса.

```
"Node Type": "ReadFromMergeTree",
"Indexes": [
  {
    "Type": "Partition Min-Max",
    "Keys": ["y"],
    "Condition": "(y in [1, +inf))",
    "Parts": 4/5,
    "Granules": 11/12
  },
  {
    "Type": "Partition",
    "Keys": ["y", "bitAnd(z, 3)"],
    "Condition": "and((bitAnd(z, 3) not in [1, 1]), and((y in [1, +inf)), (bitAnd(z, 3) not in [1, 1])))",
    "Parts": 3/4,
    "Granules": 10/11
  },
  {
    "Type": "PrimaryKey",
    "Keys": ["x", "y"],
    "Condition": "and((x in [11, +inf)), (y in [1, +inf)))",
    "Parts": 2/3,
    "Granules": 6/10,
    "Search Algorithm": "generic exclusion search"
  },
  {
    "Type": "Skip",
    "Name": "t_minmax",
    "Description": "minmax GRANULARITY 2",
    "Parts": 1/2,
    "Granules": 2/6
  },
  {
    "Type": "Skip",
    "Name": "t_set",
    "Description": "set GRANULARITY 2",
    "": 1/1,
    "Granules": 1/2
  }
]

```

- `Name` — Имя проекции.
- `Condition` — Используемое условие по первичному ключу проекции.
- `Description` — Описание того, как используется проекция (например, для фильтрации на уровне частей).
- `Selected Parts` — Количество частей, выбранных проекцией.
- `Selected Marks` — Количество выбранных меток.
- `Selected Ranges` — Количество выбранных диапазонов.
- `Selected Rows` — Количество выбранных строк.
- `Filtered Parts` — Количество частей, пропущенных из-за фильтрации на уровне частей.

```
"Node Type": "ReadFromMergeTree",
"Projections": [
  {
    "Name": "region_proj",
    "Description": "Projection has been analyzed and is used for part-level filtering",
    "Condition": "(region in ['us_west', 'us_west'])",
    "Search Algorithm": "binary search",
    "Selected Parts": 3,
    "Selected Marks": 3,
    "Selected Ranges": 3,
    "Selected Rows": 3,
    "Filtered Parts": 2
  },
  {
    "Name": "user_id_proj",
    "Description": "Projection has been analyzed and is used for part-level filtering",
    "Condition": "(user_id in [107, 107])",
    "Search Algorithm": "binary search",
    "Selected Parts": 1,
    "Selected Marks": 1,
    "Selected Ranges": 1,
    "Selected Rows": 1,
    "Filtered Parts": 2
  }
]

```


```
EXPLAIN json = 1, actions = 1, description = 0 SELECT 1 FORMAT TSVRaw;

```


```
[
  {
    "Plan": {
      "Node Type": "Expression",
      "Node Id": "Expression_5",
      "Expression": {
        "Inputs": [
          {
            "Name": "dummy",
            "Type": "UInt8"
          }
        ],
        "Actions": [
          {
            "Node Type": "INPUT",
            "Result Type": "UInt8",
            "Result Name": "dummy",
            "Arguments": [0],
            "Removed Arguments": [0],
            "Result": 0
          },
          {
            "Node Type": "COLUMN",
            "Result Type": "UInt8",
            "Result Name": "1",
            "Column": "Const(UInt8)",
            "Arguments": [],
            "Removed Arguments": [],
            "Result": 1
          }
        ],
        "Outputs": [
          {
            "Name": "1",
            "Type": "UInt8"
          }
        ],
        "Positions": [1]
      },
      "Plans": [
        {
          "Node Type": "ReadFromStorage",
          "Node Id": "ReadFromStorage_0"
        }
      ]
    }
  }
]

```


```
EXPLAIN actions = 1, compact = 0 SELECT sum(number) FROM numbers(10) GROUP BY number % 4;

```


```
Output: sum(number)

Expression ((Project names + Projection))
│  Actions: INPUT : 0 -> sum(__table1.number) UInt64 : 0
│           INPUT :: 1 -> modulo(__table1.number, 4_UInt8) UInt8 : 1
│           ALIAS sum(__table1.number) :: 0 -> sum(number) UInt64 : 2
│  Positions: 2
└──Aggregating
   │  Keys: number MOD 4
   │  Aggregates: sum(number)
   │  Skip merging: 0
   └──Expression ((Before GROUP BY + Change column names to column identifiers))
      │  Actions: INPUT : 0 -> number UInt64 : 0
      │           COLUMN Const(UInt8) -> 4_UInt8 UInt8 : 1
      │           ALIAS number :: 0 -> __table1.number UInt64 : 2
      │           FUNCTION modulo(__table1.number : 2, 4_UInt8 :: 1) -> modulo(__table1.number, 4_UInt8) UInt8 : 0
      │  Positions: 0 2
      └──ReadFromSystemNumbers
            Output: number

```


```
EXPLAIN distributed=1 SELECT * FROM remote('127.0.0.{1,2}', numbers(2)) WHERE number = 1;

```


```
Union
  Expression ((Project names + (Projection + (Change column names to column identifiers + (Project names + Projection)))))
    Filter ((WHERE + Change column names to column identifiers))
      ReadFromSystemNumbers
  Expression ((Project names + (Projection + Change column names to column identifiers)))
    ReadFromRemote (Read from remote replica)
      Expression ((Project names + Projection))
        Filter ((WHERE + Change column names to column identifiers))
          ReadFromSystemNumbers

```


```
SET enable_parallel_replicas = 2, max_parallel_replicas = 2, cluster_for_parallel_replicas = 'default';

EXPLAIN distributed=1 SELECT sum(number) FROM test_table GROUP BY number % 4;

```


```
Expression ((Project names + Projection))
  MergingAggregated
    Union
      Aggregating
        Expression ((Before GROUP BY + Change column names to column identifiers))
          ReadFromMergeTree (default.test_table)
      ReadFromRemoteParallelReplicas
        BlocksMarshalling
          Aggregating
            Expression ((Before GROUP BY + Change column names to column identifiers))
              ReadFromMergeTree (default.test_table)

```

- **Выходные столбцы запроса** выводятся в верхней части плана.
- **Выражения** в фильтрах, ключах агрегации, описаниях сортировки и оконных функциях отображаются в человекочитаемой SQL-подобной нотации (например, `a + 1 > 5` вместо `greater(plus(a, 1), 5)`). Для наглядности внутренние префиксы идентификаторов столбцов (например, `__table1.`) удаляются.
- **Исходные шаги** (например, `ReadFromMergeTree`) отображают свои выходные столбцы.
- **Шаги фильтрации** отображают условие фильтрации в SQL-нотации. Если присутствуют runtime-фильтры JOIN, они показываются отдельно.
- **Шаги агрегации** отображают ключи и агрегатные функции с их аргументами (например, `sum(c)`, `count()`).
- **Множества `IN`**, заданные кортежными литералами, показывают свои значения (усечённые для больших множеств), множества на основе подзапросов помечаются как `subquery1`, `subquery2` и т. д., а множества из таблиц с движком `Set` показывают имя таблицы.
- **Шаги JOIN** отображают отношение JOIN в математической нотации, оценочное количество строк в результате, а также то, какие выходные столбцы поступают с левой, а какие — с правой стороны. Для представления различных типов JOIN используются следующие символы:

| Символ | Тип JOIN |
| --- | --- |
| `⋈` | Inner JOIN |
| `⟕` | Left JOIN |
| `⟖` | Right JOIN |
| `⟗` | Full JOIN |
| `⋉` | Left Semi JOIN |
| `⋊` | Right Semi JOIN |
| `⋉` with strikethrough | Left Anti JOIN |
| `⋊` with strikethrough | Right Anti JOIN |
| `×` | Cross JOIN |


```
CREATE TABLE t1 (id UInt64, value String) ENGINE = MergeTree ORDER BY id;
CREATE TABLE t2 (id UInt64, value String) ENGINE = MergeTree ORDER BY id;
INSERT INTO t1 SELECT number, toString(number) FROM numbers(100);
INSERT INTO t2 SELECT number, toString(number) FROM numbers(100);

EXPLAIN actions = 1, compact = 1, pretty = 1
SELECT * FROM t1 INNER JOIN t2 ON t1.id = t2.id FORMAT Raw;

```


```
Output: id, value, id, value

Join (JOIN FillRightFirst)
│  t1[100] ⋈ t2[100]
│  Type: inner | Strictness: all | Algorithm: SpillingHashJoin(HashJoin)
│  Result rows: 100
│  Join conditions: id = id
│  Output:
│    Left:  id, value
│    Right: id, value
├──ReadFromMergeTree (default.t1)
│     Read type: Default
│     Parts: 1 | Granules: 1
│     Output: id, value
│     Runtime filters: RF1(id, id from default.t2)
└──BuildRuntimeFilter (Build runtime join filter on id)
   │  Filter id: RF1
   │  Source table: default.t2
   └──ReadFromMergeTree (default.t2)
         Read type: Default
         Parts: 1 | Granules: 1
         Output: id, value

```


### EXPLAIN PIPELINE

- `header` — Выводит заголовок для каждого выходного порта. По умолчанию: 0.
- `graph` — Выводит граф, описанный на языке описания графов [DOT](https://en.wikipedia.org/wiki/DOT_(graph_description_language)). По умолчанию: 0.
- `compact` — Выводит граф в компактном режиме, если включена настройка `graph`. По умолчанию: 1.
- `compact_repeated_processor_chains` — Объединяет соседние повторяющиеся цепочки процессоров в текстовом выводе, показывая одну копию цепочки с числом повторений. Это может упростить чтение параллельных конвейеров, когда одна и та же цепочка встречается много раз, например при JOIN. На вывод графа это не влияет. По умолчанию: 0.

```
Resize 16 → 1
  FillingRightJoinSide          │
    SimpleSquashingTransform    │ × 16
      Resize 1 → 16

```


```
EXPLAIN PIPELINE SELECT sum(number) FROM numbers_mt(100000) GROUP BY number % 4;

```


```
(Union)
(Expression)
ExpressionTransform
  (Expression)
  ExpressionTransform
    (Aggregating)
    Resize 2 → 1
      AggregatingTransform × 2
        (Expression)
        ExpressionTransform × 2
          (SettingQuotaAndLimits)
            (ReadFromStorage)
            NumbersRange × 2 0 → 1

```


### EXPLAIN ANALYZE

- `header` — см. раздел [EXPLAIN PLAN](#explain-plan).
- `description` — см. раздел [EXPLAIN PLAN](#explain-plan).
- `projections` — см. раздел [EXPLAIN PLAN](#explain-plan).
- `sorting` — см. раздел [EXPLAIN PLAN](#explain-plan).
- `input_headers` — см. раздел [EXPLAIN PLAN](#explain-plan).
- `column_structure` — см. раздел [EXPLAIN PLAN](#explain-plan).
- `actions` — см. раздел [EXPLAIN PLAN](#explain-plan). По умолчанию: 1.
- `indexes` — см. раздел [EXPLAIN PLAN](#explain-plan). По умолчанию: 1.
- `compact` — см. раздел [EXPLAIN PLAN](#explain-plan). По умолчанию: 1.
- `pretty` — см. раздел [EXPLAIN PLAN](#explain-plan). По умолчанию: 1.
- `processors` — для `EXPLAIN ANALYZE` выводит дополнительную строку для каждого этапа с распределением времени выполнения по каждому процессору: `min`, `median`, `max` и `sum`. Это полезно для выявления перекоса нагрузки между параллельными процессорами. По умолчанию: 0.
- **Квоты и ограничения.** Он учитывается в тех же [quotas](https://clickhouse.com/docs/ru/concepts/features/configuration/server-config/quotas) и подпадает под те же [limits](https://clickhouse.com/docs/ru/concepts/features/configuration/settings/query-complexity) (например, `query_selects`, `read_rows`), что и при прямом выполнении запроса. Источники, освобождённые от квот на этапе планирования (такие как `system.one`), не учитываются.
- **Неуспешные транзакции.** Внутри [transaction](https://clickhouse.com/docs/ru/concepts/features/operations/insert/transactions), которая уже завершилась ошибкой (`ROLLED_BACK`), он отклоняется с `INVALID_TRANSACTION`, так же как и обычный `SELECT` — сначала выполните `ROLLBACK`.
- **Потоковые чтения.** При потоковом чтении (`FROM ... STREAM`) он отклоняется с `NOT_IMPLEMENTED`, потому что такое чтение никогда не завершается.
- **Распределённые запросы.** Он не поддерживается для запросов, выполняемых в режиме [distributed](https://clickhouse.com/docs/ru/reference/engines/table-engines/special/distributed).

```
EXPLAIN ANALYZE SELECT number % 10 AS k, count() FROM numbers_mt(1000000) GROUP BY k;

```


```
Query summary:
  Time:        10.72 ms (planning 6.45 ms · execution 4.26 ms)
  Read:        1.00 million rows, 8.00 MB (234.49 million rows/s., 1.88 GB/s.)
  Peak memory: 28.98 KiB

Output: number MOD 10, count()

Expression ((Project names + Projection))
│  I/O: rows 10 → 10 · 90 B → 90 B
│    time 21.82 us (0.5%) · parallelism 0.98/1
└──Aggregating
   │  Keys: number MOD 10
   │  Aggregates: count()
   │  Skip merging: 0
   │  I/O: rows 1.00 million → 10 (0.00%) · 1.00 MB → 90 B
   │    Stage (partial aggregation): time 868.45 us (20.4%) · parallelism 3.80/15
   │    Stage (final aggregation): time 445.27 us (10.4%) · parallelism 1.11/16
   └──Expression ((Before GROUP BY + Change column names to column identifiers))
      │  I/O: rows 1.00 million → 1.00 million · 8.00 MB → 1.00 MB
      │    time 677.07 us (15.9%) · parallelism 4.31/15
      └──ReadFromSystemNumbers
            Output: number
            I/O: rows 0 → 1.00 million · 0 B → 8.00 MB
              time 993.94 us (23.3%) · parallelism 7.52/15

```


```
   Query summary:
     Time:        <total> (planning <planning> · execution <execution>)
     Read:        <rows> rows, <bytes> (<rows/s>, <bytes/s>)
     Peak memory: <peak>

```

- `Time` — общее время, разделённое на этапы планирования (то есть создание плана + оптимизация плана + построение конвейера) и выполнения (запуск конвейера).
- `Read` — строки и несжатые байты, прочитанные из таблиц, с указанием пропускной способности — те же числа, которые нижний колонтитул обычного запроса показывает как “Processed”.
- `Peak memory` — пиковое потребление памяти запросом.

```
I/O: rows <in> → <out> (<selectivity>%) · <bytes_in> → <bytes_out>
  [Stage (<stage>): ]time <t> (<share>%) · parallelism <avg>/<max>

```

- `rows <in> → <out>` — строки, вошедшие в шаг и вышедшие из него; (`<selectivity>`%) показывает, насколько шаг отфильтровал (`out/in`) или расширил данные; не показывается, если число входных строк равно числу выходных строк или если число входных строк равно `0`.
- `<bytes_in> → <bytes_out>` — несжатые байты в памяти, проходящие через шаг (не указывается, если оба значения равны нулю).
- `time <t> (<share>%)` — фактическое время, в течение которого стадия была активна, и её доля от времени выполнения запроса (то есть без времени сборки). Обратите внимание: сумма долей может превышать 100%, потому что стадии и шаги выполняются параллельно.
- `parallelism <avg>/<max>` — среднее число потоков CPU, одновременно работающих в пределах этой стадии, из максимально возможного числа. Значение, близкое к максимуму, означает, что стадия хорошо распараллелена; близкое к 1 — что она выполнялась в основном последовательно.
- `Stage (<stage>)` — имя стадии. Для шага с одной стадией строка времени выводится сразу, без метки `Stage (...)`. Для шагов с несколькими стадиями выводится по одной помеченной строке на каждую стадию; например, для `Aggregating` показываются `Stage (partial aggregation)` и `Stage (final aggregation)`, а для hash JOIN — `Stage (build)` и `Stage (probe)`.
- общего числа задач внутри шага плана;
- максимального числа потоков обработки запроса, заданного в `max_threads`.

```
Time per processor (<n>): min <t> · median <t> · max <t> · sum <t>

```


### EXPLAIN ESTIMATE


```
CREATE TABLE ttt (i Int64) ENGINE = MergeTree() ORDER BY i SETTINGS index_granularity = 16, write_final_mark = 0;
INSERT INTO ttt SELECT number FROM numbers(128);
OPTIMIZE TABLE ttt;

```


```
EXPLAIN ESTIMATE SELECT * FROM ttt;

```


```
┌─database─┬─table─┬─parts─┬─rows─┬─marks─┐
│ default  │ ttt   │     1 │  128 │     8 │
└──────────┴───────┴───────┴──────┴───────┘

```


### EXPLAIN WHATIF


```
EXPLAIN WHATIF [empirical = 0] SELECT ...

```

- `empirical` — `1` (по умолчанию) запускает индекс в памяти на гранулах, отобранных после базовой фильтрации, чтобы измерить коэффициент пропуска (верхнюю границу). `0` пропускает этот этап. В любом случае, если empirical не даёт результата (отключён или индекс нельзя вычислить в памяти), оценщик переключается на [статистику столбцов](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/mergetree#column-statistics), а затем — на сводку только по применимости, если недоступно ни то, ни другое.

```
Baseline (after PK + partition + existing indexes):
  table:       db.t
  parts:       1
  marks:       100
  est_bytes:   1.50 MiB             (only when the query reads rows)

With idx_b (minmax, hypothetical):
  status:       applicable
  marks:        1
  est_bytes:    15.00 KiB           (only when baseline bytes are known)
  skip_ratio:   99.0%

Estimation:
  source:           empirical | statistical | applicability_only
  empirical_status: ok | unsupported | disabled
  sampled_parts:    50 / 100        (only when source = empirical)
  sampled_marks:    50 / 100        (only when source = empirical)
  elapsed_us:       631             (only when source = empirical)

```

- `source` — как была получена оценка.
- `empirical`: индекс строится в памяти по гранулам, оставшимся после базового pruning, и подсчитывается, сколько гранул индекс мог бы пропустить. Это верхняя граница — см. ограничения в [`CREATE HYPOTHETICAL INDEX`](https://clickhouse.com/docs/ru/reference/statements/hypothetical-index#limitations).
- `statistical`: вычисляется на основе статистики столбцов. Используется, когда empirical отключён (`empirical = 0`) или empirical не смог дать результат, а для соответствующих столбцов задана статистика.
- `applicability_only`: индекс применим к предикату, но ни эмпирическая, ни статистическая оценка не дали результата (например, `empirical = 0` и статистика столбцов не задана). Возвращает `skip_ratio: 0.0%` как консервативную границу.
- `sampled_parts` / `sampled_marks` — `<baseline-pruned> / <total in the table>`. Показывает, какая доля таблицы осталась после pruning по PK, партициям и существующим индексам, то есть какие данные поступают на вход гипотетическому индексу.
- `est_bytes` — оценка количества прочитанных байтов, полученная на основе среднего размера строки в таблице, поэтому она приблизительна и зависит от хранилища и сжатия. Строка baseline появляется только тогда, когда запрос читает строки; строка для каждого кандидата — только когда известна базовая оценка объёма в байтах.

```
CREATE TABLE t (a UInt64, b UInt64) ENGINE = MergeTree ORDER BY a
SETTINGS index_granularity = 100;

INSERT INTO t SELECT number, number FROM numbers(10000);

CREATE HYPOTHETICAL INDEX idx_b ON t (b) TYPE minmax GRANULARITY 1;

EXPLAIN WHATIF SELECT * FROM t WHERE b = 42;

```


```
Baseline (after PK + partition + existing indexes):
  table:       default.t
  parts:       1
  marks:       100
  est_bytes:   85.52 KiB

With idx_b (minmax, hypothetical):
  status:       applicable
  marks:        1
  est_bytes:    875.00 B
  skip_ratio:   99.0%

Estimation:
  source:           empirical
  empirical_status: ok
  sampled_parts:    1 / 1
  sampled_marks:    100 / 100

```


```
ALTER TABLE t ADD STATISTICS b TYPE TDigest;
ALTER TABLE t MATERIALIZE STATISTICS b SETTINGS mutations_sync = 1;

```


```
EXPLAIN WHATIF empirical = 0 SELECT * FROM t WHERE b < 10;

```


```
With idx_b (minmax, hypothetical):
  status:       applicable
  marks:        1
  est_bytes:    1.66 KiB
  skip_ratio:   99.9%

Estimation:
  source:           statistical
  empirical_status: disabled

```


### EXPLAIN TABLE OVERRIDE


```
CREATE TABLE db.tbl (
    id INT PRIMARY KEY,
    created DATETIME DEFAULT now()
)

```


```
EXPLAIN TABLE OVERRIDE mysql('127.0.0.1:3306', 'db', 'tbl', 'root', 'clickhouse')
PARTITION BY toYYYYMM(assumeNotNull(created))

```


```
┌─explain─────────────────────────────────────────────────┐
│ PARTITION BY uses columns: `created` Nullable(DateTime) │
└─────────────────────────────────────────────────────────┘

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
