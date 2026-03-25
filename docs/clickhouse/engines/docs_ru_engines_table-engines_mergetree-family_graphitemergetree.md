# Движок таблицы GraphiteMergeTree | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/engines/table-engines/mergetree-family/graphitemergetree

Этот движок предназначен для прореживания и агрегирования/усреднения (rollup) данныхGraphite. Он может быть полезен разработчикам, которые хотят использовать ClickHouse в качестве хранилища данных для Graphite.

Вы можете использовать любой движок таблицы ClickHouse для хранения данных Graphite, если вам не нужен rollup, но если rollup необходим, используйтеGraphiteMergeTree. Движок уменьшает объем хранимых данных и повышает эффективность выполнения запросов Graphite.

Движок наследует свойства отMergeTree.


## Создание таблицы​


```
CREATE TABLE [IF NOT EXISTS] [db.]table_name [ON CLUSTER cluster]
(
    Path String,
    Time DateTime,
    Value Float64,
    Version <Numeric_type>
    ...
) ENGINE = GraphiteMergeTree(config_section)
[PARTITION BY expr]
[ORDER BY expr]
[SAMPLE BY expr]
[SETTINGS name=value, ...]

```

См. подробное описание запросаCREATE TABLE.

Таблица для данных Graphite должна иметь следующие столбцы:

- Имя метрики (датчика Graphite). Тип данных:String.
Имя метрики (датчика Graphite). Тип данных:String.

- Время измерения метрики. Тип данных:DateTime.
Время измерения метрики. Тип данных:DateTime.

- Значение метрики. Тип данных:Float64.
Значение метрики. Тип данных:Float64.

- Версия метрики. Тип данных: любой числовой тип (ClickHouse сохраняет строки с наибольшей версией или последнюю записанную, если версии совпадают. Остальные строки удаляются при слиянии частей данных).
Версия метрики. Тип данных: любой числовой тип (ClickHouse сохраняет строки с наибольшей версией или последнюю записанную, если версии совпадают. Остальные строки удаляются при слиянии частей данных).

Имена этих столбцов должны быть указаны в конфигурации rollup.

Параметры GraphiteMergeTree

- config_section— Имя раздела в файле конфигурации, где заданы правила rollup.
Части запроса

При создании таблицыGraphiteMergeTreeтребуются те жечасти запроса, что и при создании таблицыMergeTree.

Не используйте этот способ в новых проектах и, по возможности, переведите старые проекты на способ, описанный выше.


```
CREATE TABLE [IF NOT EXISTS] [db.]table_name [ON CLUSTER cluster]
(
  EventDate Date,
  Path String,
  Time DateTime,
  Value Float64,
  Version <Numeric_type>
  ...
) ENGINE [=] GraphiteMergeTree(date-column [, sampling_expression], (primary, key), index_granularity, config_section)

```

Все параметры, кромеconfig_section, имеют то же значение, что и вMergeTree.config_section— Имя раздела в файле конфигурации, где заданы правила rollup.

- config_section— Имя раздела в файле конфигурации, где заданы правила rollup.

## Конфигурация rollup​

Настройки rollup задаются параметромgraphite_rollupв конфигурации сервера. Имя параметра может быть любым. Вы можете создать несколько конфигураций и использовать их для разных таблиц.

Структура конфигурации rollup:

required-columns
patterns


### Обязательные столбцы​


#### path_column_name​

path_column_name— имя столбца, в котором хранится имя метрики (датчик Graphite). Значение по умолчанию:Path.


#### time_column_name​

time_column_name— имя столбца, в котором хранится время измерения метрики. Значение по умолчанию:Time.


#### value_column_name​

value_column_name— имя столбца, в котором хранится значение метрики в момент времени, указанной вtime_column_name. Значение по умолчанию:Value.


#### version_column_name​

version_column_name— имя столбца, в котором хранится версия метрики. Значение по умолчанию:Timestamp.


### Шаблоны​

Структура разделаpatterns:


```
pattern
    rule_type
    regexp
    function
pattern
    rule_type
    regexp
    age + precision
    ...
pattern
    rule_type
    regexp
    function
    age + precision
    ...
pattern
    ...
default
    function
    age + precision
    ...

```

Паттерны должны быть строго упорядочены:Паттерны безfunctionилиretention.Паттерны с обоими параметрамиfunctionиretention.Паттернdefault.

- Паттерны безfunctionилиretention.
- Паттерны с обоими параметрамиfunctionиretention.
- Паттернdefault.
При обработке строки ClickHouse проверяет правила в секцияхpattern. Каждая из секцийpattern(включаяdefault) может содержать параметрfunctionдля агрегации, параметрыretentionили оба. Если имя метрики соответствуетregexp, применяются правила из секции (или секций)pattern; в противном случае используются правила из секцииdefault.

Поля для секцийpatternиdefault:

- rule_type- тип правила. Применяется только к конкретным метрикам. Движок использует его для разделения обычных и помеченных (tagged) метрик. Необязательный параметр. Значение по умолчанию:all.
Он не нужен, когда производительность не критична или используется только один тип метрик, например обычные метрики. По умолчанию создаётся только один набор правил. В противном случае, если определён любой из специальных типов, создаются два разных набора. Один для обычных метрик (root.branch.leaf) и один для помеченных метрик (root.branch.leaf;tag1=value1).
Правила по умолчанию попадают в оба набора.
Допустимые значения:all(по умолчанию) - универсальное правило, используется, когдаrule_typeопущен.plain- правило для обычных метрик. Полеregexpобрабатывается как регулярное выражение.tagged- правило для помеченных метрик (метрики хранятся в БД в форматеsomeName?tag1=value1&tag2=value2&tag3=value3). Регулярное выражение должно быть отсортировано по именам тегов, первый тег должен быть__name__, если он существует. Полеregexpобрабатывается как регулярное выражение.tag_list- правило для помеченных метрик, простой DSL для более удобного описания метрики в формате graphitesomeName;tag1=value1;tag2=value2,someNameилиtag1=value1;tag2=value2. Полеregexpпреобразуется в правилоtagged. Сортировка по именам тегов не нужна, она будет выполнена автоматически. Значение тега (но не имя) может задаваться как регулярное выражение, напримерenv=(dev|staging).
- all(по умолчанию) - универсальное правило, используется, когдаrule_typeопущен.
- plain- правило для обычных метрик. Полеregexpобрабатывается как регулярное выражение.
- tagged- правило для помеченных метрик (метрики хранятся в БД в форматеsomeName?tag1=value1&tag2=value2&tag3=value3). Регулярное выражение должно быть отсортировано по именам тегов, первый тег должен быть__name__, если он существует. Полеregexpобрабатывается как регулярное выражение.
- tag_list- правило для помеченных метрик, простой DSL для более удобного описания метрики в формате graphitesomeName;tag1=value1;tag2=value2,someNameилиtag1=value1;tag2=value2. Полеregexpпреобразуется в правилоtagged. Сортировка по именам тегов не нужна, она будет выполнена автоматически. Значение тега (но не имя) может задаваться как регулярное выражение, напримерenv=(dev|staging).
- regexp– шаблон для имени метрики (регулярное выражение или DSL).
- age– минимальный возраст данных в секундах.
- precision– точность определения возраста данных в секундах. Должно быть делителем 86400 (количество секунд в сутках).
- function– имя агрегирующей функции, применяемой к данным, возраст которых попадает в диапазон[age, age + precision]. Допустимые функции: min / max / any / avg. Среднее значение рассчитывается неточно, как среднее от средних значений.

### Пример конфигурации без типов правил​


```
<graphite_rollup>
    <version_column_name>Version</version_column_name>
    <pattern>
        <regexp>click_cost</regexp>
        <function>any</function>
        <retention>
            <age>0</age>
            <precision>5</precision>
        </retention>
        <retention>
            <age>86400</age>
            <precision>60</precision>
        </retention>
    </pattern>
    <default>
        <function>max</function>
        <retention>
            <age>0</age>
            <precision>60</precision>
        </retention>
        <retention>
            <age>3600</age>
            <precision>300</precision>
        </retention>
        <retention>
            <age>86400</age>
            <precision>3600</precision>
        </retention>
    </default>
</graphite_rollup>

```


### Пример конфигурации с типами правил​


```
<graphite_rollup>
    <version_column_name>Version</version_column_name>
    <pattern>
        <rule_type>plain</rule_type>
        <regexp>click_cost</regexp>
        <function>any</function>
        <retention>
            <age>0</age>
            <precision>5</precision>
        </retention>
        <retention>
            <age>86400</age>
            <precision>60</precision>
        </retention>
    </pattern>
    <pattern>
        <rule_type>tagged</rule_type>
        <regexp>^((.*)|.)min\?</regexp>
        <function>min</function>
        <retention>
            <age>0</age>
            <precision>5</precision>
        </retention>
        <retention>
            <age>86400</age>
            <precision>60</precision>
        </retention>
    </pattern>
    <pattern>
        <rule_type>tagged</rule_type>
        <regexp><![CDATA[^someName\?(.*&)*tag1=value1(&|$)]]></regexp>
        <function>min</function>
        <retention>
            <age>0</age>
            <precision>5</precision>
        </retention>
        <retention>
            <age>86400</age>
            <precision>60</precision>
        </retention>
    </pattern>
    <pattern>
        <rule_type>tag_list</rule_type>
        <regexp>someName;tag2=value2</regexp>
        <retention>
            <age>0</age>
            <precision>5</precision>
        </retention>
        <retention>
            <age>86400</age>
            <precision>60</precision>
        </retention>
    </pattern>
    <default>
        <function>max</function>
        <retention>
            <age>0</age>
            <precision>60</precision>
        </retention>
        <retention>
            <age>3600</age>
            <precision>300</precision>
        </retention>
        <retention>
            <age>86400</age>
            <precision>3600</precision>
        </retention>
    </default>
</graphite_rollup>

```

Агрегация (rollup) данных выполняется во время слияний. Обычно для старых партиций слияния не запускаются, поэтому для выполнения rollup необходимо инициировать внеплановое слияние с помощью командыOPTIMIZE. Также можно использовать дополнительные инструменты, напримерgraphite-ch-optimizer.
