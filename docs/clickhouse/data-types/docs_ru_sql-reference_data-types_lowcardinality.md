# LowCardinality(T) | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/sql-reference/data-types/lowcardinality

Изменяет внутреннее представление других типов данных на представление с использованием словарной кодировки.


## Синтаксис​


```
LowCardinality(data_type)

```

Параметры

- data_type—String,FixedString,Date,DateTimeи числовые типы данных, за исключениемDecimal.LowCardinalityнеэффективен для некоторых типов данных, см. описание настройкиallow_suspicious_low_cardinality_types.

## Описание​

LowCardinality— это надстройка, которая изменяет способ хранения данных и правила их обработки. ClickHouse применяетсловарное кодированиек столбцам типаLowCardinality. Работа со словарно закодированными данными существенно повышает производительность выполнения запросовSELECTдля многих приложений.

Эффективность использования типа данныхLowCardinalityзависит от разнообразия данных. Если словарь содержит менее 10 000 различных значений, ClickHouse в большинстве случаев показывает более высокую эффективность чтения и хранения данных. Если словарь содержит более 100 000 различных значений, ClickHouse может работать хуже по сравнению с использованием обычных типов данных.

Рассмотрите возможность использованияLowCardinalityвместоEnumпри работе со строками.LowCardinalityобеспечивает большую гибкость в использовании и часто демонстрирует такую же или более высокую эффективность.


## Пример​

Создайте таблицу со столбцом типаLowCardinality:


```
CREATE TABLE lc_t
(
    `id` UInt16,
    `strings` LowCardinality(String)
)
ENGINE = MergeTree()
ORDER BY id

```


## Связанные настройки и функции​

Настройки:

- low_cardinality_max_dictionary_size
- low_cardinality_use_single_dictionary_for_part
- low_cardinality_allow_in_native_format
- allow_suspicious_low_cardinality_types
- output_format_arrow_low_cardinality_as_dictionary
Функции:

- toLowCardinality

## Связанные материалы​

- Блог:Оптимизация ClickHouse с помощью схем и кодеков
- Блог:Работа с временными рядами в ClickHouse
- Оптимизация строк (видеодоклад на русском).Слайды на английском