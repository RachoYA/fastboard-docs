# Настройки формата output_format_* - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/settings/formats/output-format


## output_format_always_write_decimal_point_in_float_and_decimal


## output_format_arrow_compression_method


## output_format_arrow_date_as_uint16


## output_format_arrow_fixed_string_as_fixed_byte_array


## output_format_arrow_low_cardinality_as_dictionary


## output_format_arrow_string_as_string


## output_format_arrow_unsupported_types_as_binary


## output_format_arrow_use_64_bit_indexes_for_dictionary


## output_format_arrow_use_native_writer


## output_format_arrow_use_signed_indexes_for_dictionary


## output_format_avro_codec


## output_format_avro_confluent_subject


## output_format_avro_rows_in_file


## output_format_avro_string_column_pattern


## output_format_avro_sync_interval


## output_format_binary_encode_types_in_binary_format


## output_format_binary_write_json_as_string


## output_format_bson_string_as_string


## output_format_compression_level


## output_format_compression_zstd_window_log


## output_format_csv_crlf_end_of_line


## output_format_csv_header_serialize_tuple_into_separate_columns


## output_format_csv_serialize_tuple_into_separate_columns


## output_format_decimal_trailing_zeros


## output_format_float_precision


## output_format_image_height


## output_format_image_terminal_mode

- “ (пусто) — записывать сырые байты изображения (по умолчанию).
- `iterm` — использовать inline-протокол изображений iTerm2.
- `kitty` — использовать графический протокол Kitty.
- `sixel` — использовать протокол Sixel.
- `auto` — если вывод направлен в терминал, определить его возможности и использовать `iterm`, `kitty` или `sixel` (в этом порядке); в противном случае записывать сырые байты изображения.

## output_format_image_width


## output_format_json_array_of_rows

- 1 — ClickHouse выводит все строки в виде массива, где каждая строка представлена в формате `JSONEachRow`.
- 0 — ClickHouse выводит каждую строку отдельно в формате `JSONEachRow`.

```
SET output_format_json_array_of_rows = 1;
SELECT number FROM numbers(3) FORMAT JSONEachRow;

```


```
[
{"number":"0"},
{"number":"1"},
{"number":"2"}
]

```


```
SET output_format_json_array_of_rows = 0;
SELECT number FROM numbers(3) FORMAT JSONEachRow;

```


```
{"number":"0"}
{"number":"1"}
{"number":"2"}

```


## output_format_json_escape_forward_slashes


## output_format_json_map_as_array_of_tuples


## output_format_json_named_tuples_as_objects


## output_format_json_pretty_print


```
"data":
[
  {
    "tuple": {"a":1,"b":2,"c":3},
    "array": [1,2,3],
    "map": {"a":1,"b":2,"c":3}
  }
],

```


```
"data":
[
    {
        "tuple": {
            "a": 1,
            "b": 2,
            "c": 3
        },
        "array": [
            1,
            2,
            3
        ],
        "map": {
            "a": 1,
            "b": 2,
            "c": 3
        }
    }
],

```


## output_format_json_quote_64bit_floats


## output_format_json_quote_64bit_integers

- 0 — Целые числа выводятся без кавычек.
- 1 — Целые числа заключаются в кавычки.

## output_format_json_quote_decimals


## output_format_json_quote_denormals

- 0 — Отключено.
- 1 — Включено.

```
┌─id─┬─name───┬─duration─┬─period─┬─area─┐
│  1 │ Andrew │       20 │      0 │  400 │
│  2 │ John   │       40 │      0 │    0 │
│  3 │ Bob    │       15 │      0 │ -100 │
└────┴────────┴──────────┴────────┴──────┘

```


```
SELECT area/period FROM account_orders FORMAT JSON;

```


```
{
        "meta":
        [
                {
                        "name": "divide(area, period)",
                        "type": "Float64"
                }
        ],

        "data":
        [
                {
                        "divide(area, period)": null
                },
                {
                        "divide(area, period)": null
                },
                {
                        "divide(area, period)": null
                }
        ],

        "rows": 3,

        "statistics":
        {
                "elapsed": 0.003648093,
                "rows_read": 3,
                "bytes_read": 24
        }
}

```


```
{
        "meta":
        [
                {
                        "name": "divide(area, period)",
                        "type": "Float64"
                }
        ],

        "data":
        [
                {
                        "divide(area, period)": "inf"
                },
                {
                        "divide(area, period)": "-nan"
                },
                {
                        "divide(area, period)": "-inf"
                }
        ],

        "rows": 3,

        "statistics":
        {
                "elapsed": 0.000070241,
                "rows_read": 3,
                "bytes_read": 24
        }
}

```


## output_format_json_skip_null_value_in_named_tuples


## output_format_json_validate_utf8


## output_format_markdown_escape_special_characters


```
! " # $ % & ' ( ) * + , - . / : ; < = > ? @ [ \ ] ^ _ ` { | } ~

```

- 0 — Отключено.
- 1 — Включено.

## output_format_msgpack_uuid_representation


## output_format_native_encode_types_in_binary_format


## output_format_native_use_flattened_dynamic_and_json_serialization


## output_format_native_write_json_as_string


## output_format_orc_compression_block_size


## output_format_orc_compression_method


## output_format_orc_dictionary_key_size_threshold


## output_format_orc_row_index_stride


## output_format_orc_string_as_string


## output_format_orc_writer_time_zone_name


## output_format_parallel_formatting

- 1 — Включено.
- 0 — Отключено.

## output_format_parquet_batch_size


## output_format_parquet_bloom_filter_bits_per_value

- 6 бит — 10%
- 10.5 бита — 1%
- 16.9 бита — 0.1%
- 26.4 бита — 0.01%
- 41 бит — 0.001%

## output_format_parquet_bloom_filter_flush_threshold_bytes

- если значение равно 0, bloom-фильтры каждой группы строк записываются сразу после соответствующей группы строк,
- если значение больше общего размера всех bloom-фильтров, bloom-фильтры для всех групп строк будут накапливаться в памяти, а затем записываться вместе ближе к концу файла,
- в противном случае bloom-фильтры будут накапливаться в памяти и записываться, как только их общий размер превысит это значение.

## output_format_parquet_compression_method


## output_format_parquet_data_page_size


## output_format_parquet_date_as_uint16


## output_format_parquet_datetime_as_uint32


## output_format_parquet_enum_as_byte_array


## output_format_parquet_fixed_string_as_fixed_byte_array


## output_format_parquet_geometadata


## output_format_parquet_max_dictionary_size


## output_format_parquet_parallel_encoding


## output_format_parquet_row_group_size


## output_format_parquet_row_group_size_bytes


## output_format_parquet_string_as_string


## output_format_parquet_write_bloom_filter


## output_format_parquet_write_checksums


## output_format_parquet_write_page_index


## output_format_pretty_color


## output_format_pretty_display_footer_column_names

- 0 — Имена столбцов не отображаются в нижнем колонтитуле.
- 1 — Имена столбцов отображаются в нижнем колонтитуле, если количество строк больше или равно пороговому значению, заданному в [output_format_pretty_display_footer_column_names_min_rows](https://clickhouse.com/docs/ru/reference/settings/formats/output-format#output_format_pretty_display_footer_column_names_min_rows) (по умолчанию — 50).

```
SELECT *, toTypeName(*) FROM (SELECT * FROM system.numbers LIMIT 1000);

```


```
      ┌─number─┬─toTypeName(number)─┐
   1. │      0 │ UInt64             │
   2. │      1 │ UInt64             │
   3. │      2 │ UInt64             │
   ...
 999. │    998 │ UInt64             │
1000. │    999 │ UInt64             │
      └─number─┴─toTypeName(number)─┘

```


## output_format_pretty_display_footer_column_names_min_rows


## output_format_pretty_fallback_to_vertical


## output_format_pretty_fallback_to_vertical_max_rows_per_chunk


## output_format_pretty_fallback_to_vertical_min_columns


## output_format_pretty_fallback_to_vertical_min_table_width


## output_format_pretty_glue_chunks


## output_format_pretty_grid_charset


## output_format_pretty_highlight_digit_groups


## output_format_pretty_highlight_trailing_spaces


## output_format_pretty_max_column_name_width_cut_to


## output_format_pretty_max_column_name_width_min_chars_to_cut


## output_format_pretty_max_column_pad_width


## output_format_pretty_max_rows


## output_format_pretty_max_value_width


## output_format_pretty_max_value_width_apply_for_single_value


## output_format_pretty_multiline_fields


## output_format_pretty_named_tuples_as_json


## output_format_pretty_row_numbers


## output_format_pretty_single_large_number_tip_threshold


## output_format_pretty_squash_consecutive_ms


## output_format_pretty_squash_max_wait_ms


## output_format_pretty_use_nbsp_for_padding


## output_format_protobuf_nullables_with_google_wrappers


## output_format_schema


## output_format_sql_insert_include_column_names


## output_format_sql_insert_max_batch_size


## output_format_sql_insert_quote_names


## output_format_sql_insert_table_name


## output_format_sql_insert_use_replace


## output_format_trim_fixed_string


## output_format_tsv_crlf_end_of_line


## output_format_values_escape_quote_with_quote


## output_format_write_statistics

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
