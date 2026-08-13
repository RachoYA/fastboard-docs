# Настройки формата format_schema_* - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/settings/formats/format-schema


## format_schema


## format_schema_message_name

- Если `format_schema_message_name` не указано, имя сообщения определяется по части `message_name` в устаревшем значении `format_schema`.
- Если `format_schema_message_name` указано при использовании устаревшего формата, будет возвращена ошибка.

## format_schema_source

- ‘file’ (по умолчанию): `format_schema` — это имя файла схемы, расположенного в каталоге `format_schemas`.
- ‘string’: `format_schema` — это непосредственное содержимое схемы.
- ‘query’: `format_schema` — это запрос для получения схемы. Если `format_schema_source` имеет значение ‘query’, действуют следующие условия:
- Запрос должен возвращать ровно одно значение: одну строку с одним строковым столбцом.
- Результат запроса интерпретируется как содержимое схемы.
- Этот результат локально кэшируется в каталоге `format_schemas`.
- Локальный кэш можно очистить с помощью команды: `SYSTEM DROP FORMAT SCHEMA CACHE FOR Files`.
- После кэширования одинаковые запросы не выполняются повторно для получения схемы, пока кэш не будет явно очищен
- Помимо локальных файлов кэша, сообщения Protobuf также кэшируются в памяти. Даже после очистки локальных файлов кэша необходимо очистить кэш в памяти с помощью `SYSTEM DROP FORMAT SCHEMA CACHE [FOR Protobuf]`, чтобы полностью обновить схему.
- Выполните запрос `SYSTEM DROP FORMAT SCHEMA CACHE`, чтобы сразу очистить кэш и файлов кэша, и схем сообщений Protobuf.
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
