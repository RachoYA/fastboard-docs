# Другие настройки формата - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/settings/formats/other


## allow_special_bool_values_inside_variant


## check_conversion_from_numbers_to_enum

- 0 — Отключено.
- 1 — Включено.

```
CREATE TABLE tab (
  val Enum('first' = 1, 'second' = 2, 'third' = 3)
) ENGINE = Memory;

INSERT INTO tab SETTINGS check_conversion_from_numbers_to_enum = 1 VALUES (4); -- returns an error

```


## column_names_for_schema_inference


## errors_output_format


## insert_distributed_one_random_shard

- 0 — Вставка отклоняется, если имеется несколько сегментов и не задан распределённый ключ.
- 1 — Вставка выполняется случайным образом в один из всех доступных сегментов, если распределённый ключ не задан.

## interval_output_format

- `kusto` - Формат вывода в стиле KQL. ClickHouse выводит интервалы в [формате KQL](https://learn.microsoft.com/en-us/dotnet/standard/base-types/standard-timespan-format-strings#the-constant-c-format-specifier). Например, `toIntervalDay(2)` будет отформатирован как `2.00:00:00`. Обратите внимание, что для типов interval переменной длины (то есть `IntervalMonth` и `IntervalYear`) учитывается среднее количество секунд в интервале.
- `numeric` - Числовой формат вывода. ClickHouse выводит интервалы в виде их числового представления. Например, `toIntervalDay(2)` будет отформатирован как `2`.
- [Interval](https://clickhouse.com/docs/ru/reference/data-types/special-data-types/interval)

## into_outfile_create_parent_directories


## json_type_escape_dots_in_keys


## max_dynamic_subcolumns_in_json_type_parsing


## precise_float_parsing


## validate_experimental_and_suspicious_types_inside_nested_types

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
