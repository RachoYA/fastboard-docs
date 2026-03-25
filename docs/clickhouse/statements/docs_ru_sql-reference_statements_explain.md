# Команда EXPLAIN | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/sql-reference/statements/explain

Показывает план выполнения команды.

Синтаксис:


```
EXPLAIN [AST | SYNTAX | QUERY TREE | PLAN | PIPELINE | ESTIMATE | TABLE OVERRIDE] [setting = value, ...]
    [
      SELECT ... |
      tableFunction(...) [COLUMNS (...)] [ORDER BY ...] [PARTITION BY ...] [PRIMARY KEY] [SAMPLE BY ...] [TTL ...]
    ]
    [FORMAT ...]

```

Пример:


```
EXPLAIN SELECT sum(number) FROM numbers(10) UNION ALL SELECT sum(number) FROM numbers(10) ORDER BY sum(number) ASC FORMAT TSV;

```


```
Union
  Expression (Projection)
    Expression (Before ORDER BY and SELECT)
      Aggregating
        Expression (Before GROUP BY)
          SettingQuotaAndLimits (Set limits and quota after reading from storage)
            ReadFromStorage (SystemNumbers)
  Expression (Projection)
    MergingSorted (Merge sorted streams for ORDER BY)
      MergeSorting (Merge sorted blocks for ORDER BY)
        PartialSorting (Sort each block for ORDER BY)
          Expression (Before ORDER BY and SELECT)
            Aggregating
              Expression (Before GROUP BY)
                SettingQuotaAndLimits (Set limits and quota after reading from storage)
                  ReadFromStorage (SystemNumbers)

```


## Типы EXPLAIN​

- AST— абстрактное синтаксическое дерево.
- SYNTAX— текст запроса после оптимизаций на уровне AST.
- QUERY TREE— дерево запроса после оптимизаций на уровне Query Tree.
- PLAN— план выполнения запроса.
- PIPELINE— конвейер выполнения запроса.

### EXPLAIN AST​

Выводит AST запроса. Поддерживаются все типы запросов, а не толькоSELECT.

Настройки:

- graph– выводит AST в виде графа, описанного на языке описания графовDOT. По умолчанию — 0.
Примеры:


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


### EXPLAIN SYNTAX​

Показывает абстрактное синтаксическое дерево (AST) запроса после синтаксического анализа.

Для этого выполняется парсинг запроса, построение AST запроса и дерева запроса, при необходимости — запуск анализатора запроса и проходов оптимизации, а затем преобразование дерева запроса обратно в AST запроса.

Настройки:

- oneline– Выводить запрос в одну строку. По умолчанию:0.
- run_query_tree_passes– Выполнять проходы по дереву запроса перед выводом дерева запроса. По умолчанию:0.
- query_tree_passes– Если заданrun_query_tree_passes, определяет, сколько проходов выполнять. Без указанияquery_tree_passesвыполняются все проходы.
Примеры:


```
EXPLAIN SYNTAX SELECT * FROM system.numbers AS a, system.numbers AS b, system.numbers AS c WHERE a.number = b.number AND b.number = c.number;

```

Вывод:


```
SELECT *
FROM system.numbers AS a, system.numbers AS b, system.numbers AS c
WHERE (a.number = b.number) AND (b.number = c.number)

```

При использованииrun_query_tree_passes:


```
EXPLAIN SYNTAX run_query_tree_passes = 1 SELECT * FROM system.numbers AS a, system.numbers AS b, system.numbers AS c WHERE a.number = b.number AND b.number = c.number;

```

Результат:


```
SELECT
    __table1.number AS `a.number`,
    __table2.number AS `b.number`,
    __table3.number AS `c.number`
FROM system.numbers AS __table1
ALL INNER JOIN system.numbers AS __table2 ON __table1.number = __table2.number
ALL INNER JOIN system.numbers AS __table3 ON __table2.number = __table3.number

```


### EXPLAIN QUERY TREE​

Настройки:

- run_passes— Выполнять все проходы по дереву запроса перед выводом дерева запроса. По умолчанию:1.
- dump_passes— Выводить информацию об использованных проходах перед выводом дерева запроса. По умолчанию:0.
- passes— Определяет, сколько проходов выполнить. При значении-1выполняются все проходы. По умолчанию:-1.
- dump_tree— Отображать дерево запроса. По умолчанию:1.
- dump_ast— Отображать AST запроса, сгенерированное из дерева запроса. По умолчанию:0.
Пример:


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


### EXPLAIN PLAN​

Выводит шаги плана запроса.

Настройки:

- optimize— Управляет тем, применяются ли оптимизации плана запроса перед его выводом. По умолчанию: 1.
- header— Печатает заголовок вывода для шага. По умолчанию: 0.
- description— Печатает описание шага. По умолчанию: 1.
- indexes— Показывает используемые индексы, количество отфильтрованных частей и количество отфильтрованных гранул для каждого применённого индекса. По умолчанию: 0. Поддерживается для таблицMergeTree. Начиная с ClickHouse >= v25.9, эта команда даёт содержательный вывод только при использовании вместе сSETTINGS use_query_condition_cache = 0, use_skip_indexes_on_data_read = 0.
- projections— Показывает все проанализированные проекции и их влияние на фильтрацию на уровне частей на основе условий по первичному ключу проекции. Для каждой проекции этот раздел включает статистику, такую как количество частей, строк, меток и диапазонов, которые были обработаны с использованием её первичного ключа. Также показывает, сколько частей данных было пропущено благодаря этой фильтрации, без чтения из самой проекции. То, была ли проекция фактически использована для чтения или только проанализирована для фильтрации, можно определить по полюdescription. По умолчанию: 0. Поддерживается для таблицMergeTree.
- actions— Печатает подробную информацию о действиях шага. По умолчанию: 0.
- sorting— Печатает описание сортировки для каждого шага плана, который выдаёт отсортированный результат. По умолчанию: 0.
- keep_logical_steps— Сохраняет логические шаги плана для JOIN вместо преобразования их в физические реализации JOIN. По умолчанию: 0.
- json— Печатает шаги плана запроса как строку в форматеJSON. По умолчанию: 0. Рекомендуется использовать форматTabSeparatedRaw (TSVRaw), чтобы избежать лишнего экранирования.
- input_headers— Печатает входные заголовки для шага. По умолчанию: 0. В основном полезно только разработчикам для отладки проблем, связанных с несоответствием входных и выходных заголовков.
- column_structure— Дополнительно печатает структуру столбцов в заголовках, помимо их имени и типа. По умолчанию: 0. В основном полезно только разработчикам для отладки проблем, связанных с несоответствием входных и выходных заголовков.
- distributed— Показывает планы запросов, выполняемые на удалённых узлах для distributed таблиц или параллельных реплик. По умолчанию: 0.
- compact— Если параметр включён, скрывает из плана шаги выражений и подробную информацию о действиях (входы, функции, псевдонимы и позиции вывода). Действует только приactions = 1. По умолчанию: 0.
- pretty— Печатает дерево плана с использованием символов рисования линий (├──, └──, │) вместо отступов для визуализации иерархии. Также форматирует свойства шага JOIN в одной строке. По умолчанию: 0.
Когдаjson=1, имена шагов будут содержать дополнительный суффикс с уникальным идентификатором шага.

Пример:


```
EXPLAIN SELECT sum(number) FROM numbers(10) GROUP BY number % 4;

```


```
Union
  Expression (Projection)
  Expression (Before ORDER BY and SELECT)
    Aggregating
      Expression (Before GROUP BY)
        SettingQuotaAndLimits (Set limits and quota after reading from storage)
          ReadFromStorage (SystemNumbers)

```

Оценка стоимости шагов и запросов не поддерживается.

Когдаjson = 1, план запроса представляется в формате JSON. Каждый узел представляет собой словарь, который всегда содержит ключиNode TypeиPlans.Node Type— строка с именем шага.Plans— массив с описаниями дочерних шагов. В зависимости от типа узла и настроек могут быть добавлены дополнительные необязательные ключи.

Пример:


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

При значенииdescription= 1 к шагу добавляется ключDescription:


```
{
  "Node Type": "ReadFromStorage",
  "Description": "SystemOne"
}

```

Еслиheader= 1, к шагу добавляется ключHeader, содержащий массив столбцов.

Пример:


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

Еслиindexes= 1, добавляется ключIndexes. Он содержит массив использованных индексов. Каждый индекс описывается как JSON с ключомType(строкаMinMax,Partition,PrimaryKeyилиSkip) и дополнительными (необязательными) ключами:

- Name— имя индекса (в настоящее время используется только для индексовSkip).
- Keys— массив столбцов, используемых индексом.
- Condition— используемое условие.
- Description— описание индекса (в настоящее время используется только для индексовSkip).
- Parts— количество частей после/до применения индекса.
- Granules— количество гранул после/до применения индекса.
- Ranges— количество диапазонов гранул после применения индекса.
Пример:


```
"Node Type": "ReadFromMergeTree",
"Indexes": [
  {
    "Type": "MinMax",
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

Приprojections= 1 добавляется ключProjections. Он содержит массив анализированных проекций. Каждая проекция описывается как JSON со следующими ключами:

- Name— имя проекции.
- Condition— используемое условие первичного ключа проекции.
- Description— описание способа использования проекции (например, фильтрация на уровне частей).
- Selected Parts— количество частей, выбранных проекцией.
- Selected Marks— количество выбранных меток.
- Selected Ranges— количество выбранных диапазонов.
- Selected Rows— количество выбранных строк.
- Filtered Parts— количество частей, пропущенных из-за фильтрации на уровне частей.
Пример:


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

Еслиactions= 1, добавляемые ключи зависят от типа шага.

Пример:


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

Приcompact = 1каждый шагExpressionубирается. Кроме того, если установленоactions = 1, строкиActionsиPositionsскрываются, и остаются только описания шагов:


```
EXPLAIN actions = 1, compact = 1 SELECT sum(number) FROM numbers(10) GROUP BY number % 4 FORMAT Raw;

```


```
Aggregating
Keys: modulo(__table1.number, 4_UInt8)
Aggregates:
    sum(__table1.number)
      Function: sum(UInt64) → UInt64
      Arguments: __table1.number
Skip merging: 0
  ReadFromSystemNumbers

```

Приdistributed= 1 вывод включает не только локальный план запроса, но и планы запросов, которые будут выполняться на удалённых узлах. Это полезно для анализа и отладки распределённых запросов.

Пример с distributed таблицей:


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

Пример с параллельными репликами:


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

В обоих примерах план запроса показывает полный процесс выполнения, включая локальные и удалённые этапы.

Приpretty= 1 дерево плана отображается с помощью символов псевдографики вместо отступов:


```
EXPLAIN pretty = 1 SELECT sum(number) FROM numbers(10) GROUP BY number % 4 FORMAT Raw;

```


```
Expression ((Project names + Projection))
└──Aggregating
   └──Expression ((Before GROUP BY + Change column names to column identifiers))
      └──ReadFromSystemNumbers

```


### EXPLAIN PIPELINE​

Настройки:

- header— Выводит заголовок для каждого выходного порта. По умолчанию: 0.
- graph— Выводит граф, описанный на языке описания графовDOT. По умолчанию: 0.
- compact— Выводит граф в компактном режиме, если настройкаgraphвключена. По умолчанию: 1.
Когдаcompact=0иgraph=1, имена процессоров будут содержать дополнительный суффикс с уникальным идентификатором процессора.

Пример:


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


### EXPLAIN ESTIMATE​

Показывает приблизительное количество строк, меток и частей, которые нужно прочитать из таблиц при обработке запроса. Работает с таблицами семействаMergeTree.

Пример

Создание таблицы:


```
CREATE TABLE ttt (i Int64) ENGINE = MergeTree() ORDER BY i SETTINGS index_granularity = 16, write_final_mark = 0;
INSERT INTO ttt SELECT number FROM numbers(128);
OPTIMIZE TABLE ttt;

```

Запрос:


```
EXPLAIN ESTIMATE SELECT * FROM ttt;

```

Результат:


```
┌─database─┬─table─┬─parts─┬─rows─┬─marks─┐
│ default  │ ttt   │     1 │  128 │     8 │
└──────────┴───────┴───────┴──────┴───────┘

```


### EXPLAIN TABLE OVERRIDE​

Показывает результат применения переопределения таблицы к схеме таблицы, доступной через табличную функцию.
Также выполняет проверку и генерирует исключение, если переопределение привело бы к какой-либо ошибке.

Пример

Предположим, у вас есть удалённая таблица MySQL следующего вида:


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

Результат:


```
┌─explain─────────────────────────────────────────────────┐
│ PARTITION BY uses columns: `created` Nullable(DateTime) │
└─────────────────────────────────────────────────────────┘

```

Проверка неполная, поэтому успешный запрос не гарантирует, что переопределение не вызовет проблем.
