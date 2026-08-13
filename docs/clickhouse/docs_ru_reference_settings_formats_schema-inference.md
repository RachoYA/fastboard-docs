# schema_inference_*: настройки формата - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/settings/formats/schema-inference


## schema_inference_hints


```
desc format(JSONEachRow, '{"x" : 1, "y" : "String", "z" : "0.0.0.0" }') settings schema_inference_hints='x UInt8, z IPv4';

```


```
x   UInt8
y   Nullable(String)
z   IPv4

```


## schema_inference_make_columns_nullable

- 0 - определённый тип никогда не будет `Nullable` (используйте input_format_null_as_default, чтобы указать, что делать со значениями null в этом случае),
- 1 - все определённые типы будут `Nullable`,
- 2 или `auto` - определённый тип будет `Nullable`, только если столбец содержит `NULL` в выборке, разбираемой при определении схемы, или метаданные файла содержат информацию о допустимости null для столбца,
- 3 - допустимость null для определённого типа будет соответствовать метаданным файла, если формат их поддерживает (например, Parquet); в противном случае тип всегда будет `Nullable` (например, CSV).

## schema_inference_make_json_columns_nullable


## schema_inference_mode

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
