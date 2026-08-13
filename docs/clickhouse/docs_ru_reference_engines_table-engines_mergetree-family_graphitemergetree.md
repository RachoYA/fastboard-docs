# Движок таблицы GraphiteMergeTree - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/graphitemergetree


## Создание таблицы


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

- Имя метрики (Graphite sensor). Тип данных: `String`.
- Время измерения метрики. Тип данных: `DateTime`.
- Значение метрики. Тип данных: `Float64`.
- Версия метрики. Тип данных: любой числовой тип (ClickHouse сохраняет строки с наибольшей версией или последнюю записанную строку, если версии совпадают. Остальные строки удаляются при слиянии частей данных).
- `config_section` — имя секции в файле конфигурации, где заданы правила rollup.

## Конфигурация rollup

- required-columns
- patterns

### Обязательные столбцы


#### `path_column_name`


#### `time_column_name`


#### `value_column_name`


#### `version_column_name`


### Шаблоны


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

- Шаблоны без `function` или `retention`.
- Шаблоны с `function` и `retention`.
- Шаблон `default`.
- `rule_type` - тип правила. Он применяется только к определённому типу метрик. Движок использует его, чтобы разделять обычные метрики и метрики с тегами. Необязательный параметр. Значение по умолчанию: `all`. Он не нужен, если производительность не критична или используется только один тип метрик, например обычные метрики. По умолчанию создаётся только один набор правил. В противном случае, если определён любой из специальных типов, создаются два разных набора. Один для обычных метрик (root.branch.leaf) и один для метрик с тегами (root.branch.leaf;tag1=value1). Правила по умолчанию в итоге попадают в оба набора. Допустимые значения:
- `all` (по умолчанию) - универсальное правило, используется, когда `rule_type` не указан.
- `plain` - правило для обычных метрик. Поле `regexp` обрабатывается как регулярное выражение.
- `tagged` - правило для метрик с тегами (метрики хранятся в БД в формате `someName?tag1=value1&tag2=value2&tag3=value3`). Регулярное выражение должно быть отсортировано по именам тегов; первым тегом должен быть `__name__`, если он есть. Поле `regexp` обрабатывается как регулярное выражение.
- `tag_list` - правило для метрик с тегами, простой DSL для более удобного описания метрики в формате Graphite: `someName;tag1=value1;tag2=value2`, `someName` или `tag1=value1;tag2=value2`. Поле `regexp` преобразуется в правило `tagged`. Сортировка по именам тегов не требуется, это будет сделано автоматически. Значение тега (но не имя) можно задать как регулярное выражение, например `env=(dev|staging)`.
- `regexp` – Шаблон регулярного выражения для имени метрики (обычный или DSL).
- `age` – Минимальный возраст данных в секундах.
- `precision`– Насколько точно определять возраст данных в секундах. Должен быть делителем 86400 (количество секунд в сутках).
- `function` – Имя агрегирующей функции, применяемой к данным, возраст которых попадает в диапазон `[age, age + precision]`. Допустимые функции: min / max / any / avg. Среднее вычисляется неточно, как среднее от средних.

### Пример конфигурации без типов правил


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


### Пример конфигурации с типами правил


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

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
