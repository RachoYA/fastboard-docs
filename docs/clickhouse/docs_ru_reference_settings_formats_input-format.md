# настройки формата input_format_* - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/settings/formats/input-format


## input_format_allow_errors_num


## input_format_allow_errors_ratio


## input_format_allow_seeks


## input_format_arrow_allow_missing_columns


## input_format_arrow_case_insensitive_column_matching


## input_format_arrow_skip_columns_with_unsupported_types_in_schema_inference


## input_format_arrow_use_native_reader


## input_format_avro_allow_missing_fields


## input_format_avro_null_as_default


## input_format_binary_decode_types_in_binary_format


## input_format_binary_max_type_complexity


## input_format_binary_read_json_as_string


## input_format_bson_skip_fields_with_unsupported_types_in_schema_inference


## input_format_capn_proto_skip_fields_with_unsupported_types_in_schema_inference


## input_format_column_name_matching_mode

- match_case: сопоставлять с учётом регистра
- ignore_case: сопоставлять без учёта регистра
- auto: сначала пытается сопоставлять с учётом регистра; если не удаётся, пытается сопоставлять без учёта регистра.

## input_format_connection_handling


## input_format_csv_allow_cr_end_of_line


## input_format_csv_allow_variable_number_of_columns


## input_format_csv_allow_whitespace_or_tab_as_delimiter


## input_format_csv_arrays_as_nested_csv


## input_format_csv_deserialize_separate_columns_into_tuple


## input_format_csv_detect_header


## input_format_csv_empty_as_default


## input_format_csv_enum_as_number


## input_format_csv_missing_nullable_as_empty_string


## input_format_csv_skip_first_lines


## input_format_csv_skip_trailing_empty_lines


## input_format_csv_trim_whitespaces


## input_format_csv_try_infer_numbers_from_strings


## input_format_csv_try_infer_strings_from_quoted_tuples


## input_format_csv_use_best_effort_in_schema_inference


## input_format_csv_use_default_on_bad_values


## input_format_custom_allow_variable_number_of_columns


## input_format_custom_detect_header


## input_format_custom_skip_trailing_empty_lines


## input_format_defaults_for_omitted_fields

- 0 — Отключено.
- 1 — Включено.

## input_format_force_null_for_omitted_fields


## input_format_geojson_unsupported_geometry_handling

- `'throw'` (по умолчанию) — сгенерировать исключение.
- `'null'` — вставить значение `NULL` в столбец `geometry` и продолжить разбор.

## input_format_hive_text_allow_variable_number_of_columns


## input_format_hive_text_collection_items_delimiter


## input_format_hive_text_fields_delimiter


## input_format_hive_text_map_keys_delimiter


## input_format_import_nested_json

- [JSONEachRow](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONEachRow)
- 0 — Отключено.
- 1 — Включено.
- [Использование структур Nested](https://clickhouse.com/docs/ru/guides/clickhouse/data-formats/json/formats#accessing-nested-json-objects) в формате `JSONEachRow`.

## input_format_ipv4_default_on_conversion_error


## input_format_ipv6_default_on_conversion_error


## input_format_json_compact_allow_variable_number_of_columns


## input_format_json_defaults_for_missing_elements_in_named_tuple


## input_format_json_empty_as_default

- 0 — Отключено.
- 1 — Включено.

## input_format_json_ignore_unknown_keys_in_named_tuple


## input_format_json_ignore_unnecessary_fields


## input_format_json_infer_array_of_dynamic_from_array_of_different_types


```
SET input_format_json_infer_array_of_dynamic_from_array_of_different_types=1;
DESC format(JSONEachRow, '{"a" : [42, "hello", [1, 2, 3]]}');

```


```
┌─name─┬─type───────────┐
│ a    │ Array(Dynamic) │
└──────┴────────────────┘

```


```
SET input_format_json_infer_array_of_dynamic_from_array_of_different_types=0;
DESC format(JSONEachRow, '{"a" : [42, "hello", [1, 2, 3]]}');

```


```
┌─name─┬─type─────────────────────────────────────────────────────────────┐
│ a    │ Tuple(Nullable(Int64), Nullable(String), Array(Nullable(Int64))) │
└──────┴──────────────────────────────────────────────────────────────────┘

```


## input_format_json_infer_incomplete_types_as_strings


```
SET input_format_json_infer_incomplete_types_as_strings = 1, input_format_json_try_infer_named_tuples_from_objects = 1;
DESCRIBE format(JSONEachRow, '{"obj" : {"a" : [1,2,3], "b" : "hello", "c" : null, "d" : {}, "e" : []}}');
SELECT * FROM format(JSONEachRow, '{"obj" : {"a" : [1,2,3], "b" : "hello", "c" : null, "d" : {}, "e" : []}}');

```


```
┌─name─┬─type───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┬─default_type─┬─default_expression─┬─comment─┬─codec_expression─┬─ttl_expression─┐
│ obj  │ Tuple(a Array(Nullable(Int64)), b Nullable(String), c Nullable(String), d Nullable(String), e Array(Nullable(String))) │              │                    │         │                  │                │
└──────┴────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴──────────────┴────────────────────┴─────────┴──────────────────┴────────────────┘

┌─obj────────────────────────────┐
│ ([1,2,3],'hello',NULL,'{}',[]) │
└────────────────────────────────┘

```


## input_format_json_map_as_array_of_tuples


## input_format_json_max_depth


## input_format_json_named_tuples_as_objects


## input_format_json_read_arrays_as_strings


```
SET input_format_json_read_arrays_as_strings = 1;
SELECT arr, toTypeName(arr), JSONExtractArrayRaw(arr)[3] from format(JSONEachRow, 'arr String', '{"arr" : [1, "Hello", [1,2,3]]}');

```


```
┌─arr───────────────────┬─toTypeName(arr)─┬─arrayElement(JSONExtractArrayRaw(arr), 3)─┐
│ [1, "Hello", [1,2,3]] │ String          │ [1,2,3]                                   │
└───────────────────────┴─────────────────┴───────────────────────────────────────────┘

```


## input_format_json_read_bools_as_numbers


## input_format_json_read_bools_as_strings


## input_format_json_read_numbers_as_strings


## input_format_json_read_objects_as_strings


```
SET input_format_json_read_objects_as_strings = 1;
CREATE TABLE test (id UInt64, obj String, date Date) ENGINE=Memory();
INSERT INTO test FORMAT JSONEachRow {"id" : 1, "obj" : {"a" : 1, "b" : "Hello"}, "date" : "2020-01-01"};
SELECT * FROM test;

```


```
┌─id─┬─obj──────────────────────┬───────date─┐
│  1 │ {"a" : 1, "b" : "Hello"} │ 2020-01-01 │
└────┴──────────────────────────┴────────────┘

```


## input_format_json_throw_on_bad_escape_sequence


## input_format_json_try_infer_named_tuples_from_objects


```
SET input_format_json_try_infer_named_tuples_from_objects = 1;
DESC format(JSONEachRow, '{"obj" : {"a" : 42, "b" : "Hello"}}, {"obj" : {"a" : 43, "c" : [1, 2, 3]}}, {"obj" : {"d" : {"e" : 42}}}')

```


```
┌─name─┬─type───────────────────────────────────────────────────────────────────────────────────────────────┬─default_type─┬─default_expression─┬─comment─┬─codec_expression─┬─ttl_expression─┐
│ obj  │ Tuple(a Nullable(Int64), b Nullable(String), c Array(Nullable(Int64)), d Tuple(e Nullable(Int64))) │              │                    │         │                  │                │
└──────┴────────────────────────────────────────────────────────────────────────────────────────────────────┴──────────────┴────────────────────┴─────────┴──────────────────┴────────────────┘

```


## input_format_json_try_infer_numbers_from_strings


## input_format_json_use_string_type_for_ambiguous_paths_in_named_tuples_inference_from_objects


## input_format_json_validate_types_from_metadata


## input_format_max_block_size_bytes


## input_format_max_block_wait_ms


```
clickhouse-client --query 'CREATE TABLE wikipedia_edits (data JSON)'

curl -sS --globoff -H 'Accept: application/json' --no-buffer \
  'https://stream.wikimedia.org/v2/stream/recentchange' \
  | clickhouse-client \
      --query 'INSERT INTO wikipedia_edits FORMAT JSONAsObject' \
      --input_format_max_block_wait_ms 1000 \
      --input_format_connection_handling 1 \
      --min_insert_block_size_rows 0 \
      --min_insert_block_size_bytes 0

```


## input_format_max_bytes_to_read_for_schema_inference


## input_format_max_rows_to_read_for_schema_inference


## input_format_msgpack_number_of_columns


## input_format_mysql_dump_map_column_names


## input_format_mysql_dump_table_name


## input_format_native_allow_types_conversion


## input_format_native_decode_types_in_binary_format


## input_format_null_as_default

- 0 — Вставка `NULL` в столбец, не являющийся Nullable, вызывает исключение.
- 1 — Поля со значением `NULL` инициализируются значениями столбца по умолчанию.

## input_format_orc_allow_missing_columns


## input_format_orc_case_insensitive_column_matching


## input_format_orc_dictionary_as_low_cardinality


## input_format_orc_filter_push_down


## input_format_orc_reader_time_zone_name


## input_format_orc_row_batch_size


## input_format_orc_skip_columns_with_unsupported_types_in_schema_inference


## input_format_parallel_parsing

- 1 — Включено.
- 0 — Отключено.

## input_format_parquet_allow_geoparquet_parser


## input_format_parquet_allow_missing_columns


## input_format_parquet_bloom_filter_push_down


## input_format_parquet_case_insensitive_column_matching


## input_format_parquet_enable_json_parsing


## input_format_parquet_enable_row_group_prefetch


## input_format_parquet_filter_push_down


## input_format_parquet_local_file_min_bytes_for_seek


## input_format_parquet_local_time_as_utc


## input_format_parquet_max_block_size


## input_format_parquet_memory_high_watermark


## input_format_parquet_memory_low_watermark


## input_format_parquet_page_filter_push_down


## input_format_parquet_prefer_block_bytes


## input_format_parquet_preserve_order


## input_format_parquet_skip_columns_with_unsupported_types_in_schema_inference


## input_format_parquet_use_offset_index


## input_format_parquet_verify_checksums


## input_format_protobuf_flatten_google_wrappers


## input_format_protobuf_oneof_presence


## input_format_protobuf_skip_fields_with_unsupported_types_in_schema_inference


## input_format_record_errors_file_path


## input_format_skip_unknown_fields

- [JSONEachRow](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONEachRow) (и другие JSON-форматы)
- [BSONEachRow](https://clickhouse.com/docs/ru/reference/formats/BSONEachRow) (и другие JSON-форматы)
- [TSKV](https://clickhouse.com/docs/ru/reference/formats/TabSeparated/TSKV)
- Все форматы с суффиксами WithNames/WithNamesAndTypes
- [MySQLDump](https://clickhouse.com/docs/ru/reference/formats/MySQLDump)
- [Native](https://clickhouse.com/docs/ru/reference/formats/Native)
- 0 — Отключено.
- 1 — Включено.

## input_format_try_infer_dates


## input_format_try_infer_datetimes


## input_format_try_infer_datetimes_only_datetime64


## input_format_try_infer_exponent_floats


## input_format_try_infer_integers


## input_format_try_infer_variants

- 0 — Отключено.
- 1 — Включено.

## input_format_tsv_allow_variable_number_of_columns


## input_format_tsv_crlf_end_of_line


## input_format_tsv_detect_header


## input_format_tsv_empty_as_default


## input_format_tsv_enum_as_number


## input_format_tsv_skip_first_lines


## input_format_tsv_skip_trailing_empty_lines


## input_format_tsv_use_best_effort_in_schema_inference


## input_format_values_accurate_types_of_literals


## input_format_values_deduce_templates_of_expressions


## input_format_values_interpret_expressions


## input_format_with_names_use_header

- [CSVWithNames](https://clickhouse.com/docs/ru/reference/formats/CSV/CSVWithNames)
- [CSVWithNamesAndTypes](https://clickhouse.com/docs/ru/reference/formats/CSV/CSVWithNamesAndTypes)
- [TabSeparatedWithNames](https://clickhouse.com/docs/ru/reference/formats/TabSeparated/TabSeparatedWithNames)
- [TabSeparatedWithNamesAndTypes](https://clickhouse.com/docs/ru/reference/formats/TabSeparated/TabSeparatedWithNamesAndTypes)
- [JSONCompactEachRowWithNames](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONCompactEachRowWithNames)
- [JSONCompactEachRowWithNamesAndTypes](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONCompactEachRowWithNamesAndTypes)
- [JSONCompactStringsEachRowWithNames](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONCompactStringsEachRowWithNames)
- [JSONCompactStringsEachRowWithNamesAndTypes](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONCompactStringsEachRowWithNamesAndTypes)
- [RowBinaryWithNames](https://clickhouse.com/docs/ru/reference/formats/RowBinary/RowBinaryWithNames)
- [RowBinaryWithNamesAndTypes](https://clickhouse.com/docs/ru/reference/formats/RowBinary/RowBinaryWithNamesAndTypes)
- [CustomSeparatedWithNames](https://clickhouse.com/docs/ru/reference/formats/CustomSeparated/CustomSeparatedWithNames)
- [CustomSeparatedWithNamesAndTypes](https://clickhouse.com/docs/ru/reference/formats/CustomSeparated/CustomSeparatedWithNamesAndTypes)
- 0 — Отключено.
- 1 — Включено.

## input_format_with_types_use_header

- [CSVWithNamesAndTypes](https://clickhouse.com/docs/ru/reference/formats/CSV/CSVWithNamesAndTypes)
- [TabSeparatedWithNamesAndTypes](https://clickhouse.com/docs/ru/reference/formats/TabSeparated/TabSeparatedWithNamesAndTypes)
- [JSONCompactEachRowWithNamesAndTypes](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONCompactEachRowWithNamesAndTypes)
- [JSONCompactStringsEachRowWithNamesAndTypes](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONCompactStringsEachRowWithNamesAndTypes)
- [RowBinaryWithNamesAndTypes](https://clickhouse.com/docs/ru/reference/formats/RowBinary/RowBinaryWithNamesAndTypes)
- [CustomSeparatedWithNamesAndTypes](https://clickhouse.com/docs/ru/reference/formats/CustomSeparated/CustomSeparatedWithNamesAndTypes)
- 0 — Отключено.
- 1 — Включено.
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
