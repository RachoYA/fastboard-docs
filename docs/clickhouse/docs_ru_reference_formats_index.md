# Форматы ввода и вывода данных - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/formats/index


## Форматы ввода

- Разбора данных, передаваемых в операторы `INSERT`
- Выполнения запросов `SELECT` к таблицам с файловой поддержкой, таким как `File`, `URL` или `HDFS`
- Чтения словарей
- **Формат [Native](https://clickhouse.com/docs/ru/reference/formats/Native) — самый эффективный формат ввода**, он обеспечивает лучшее сжатие, минимальное потребление ресурсов и минимальные накладные расходы на обработку на стороне сервера.
- **Сжатие крайне важно** — LZ4 уменьшает размер данных при минимальных затратах CPU, тогда как ZSTD обеспечивает более высокую степень сжатия ценой дополнительной нагрузки на CPU.
- **Предварительная сортировка влияет умеренно**, поскольку ClickHouse и без того сортирует эффективно.
- **Формирование батчей значительно повышает эффективность** — более крупные батчи уменьшают накладные расходы на вставку и повышают пропускную способность.

## Форматы вывода

- Представления результатов запроса `SELECT`
- Выполнения операций `INSERT` в таблицы с файловой поддержкой

## Обзор форматов


| Формат | Вход | Выход |
| --- | --- | --- |
| [TabSeparated](https://clickhouse.com/docs/ru/reference/formats/TabSeparated/TabSeparated) | ✔ | ✔ |
| [TabSeparatedRaw](https://clickhouse.com/docs/ru/reference/formats/TabSeparated/TabSeparatedRaw) | ✔ | ✔ |
| [TabSeparatedWithNames](https://clickhouse.com/docs/ru/reference/formats/TabSeparated/TabSeparatedWithNames) | ✔ | ✔ |
| [TabSeparatedWithNamesAndTypes](https://clickhouse.com/docs/ru/reference/formats/TabSeparated/TabSeparatedWithNamesAndTypes) | ✔ | ✔ |
| [TabSeparatedRawWithNames](https://clickhouse.com/docs/ru/reference/formats/TabSeparated/TabSeparatedRawWithNames) | ✔ | ✔ |
| [TabSeparatedRawWithNamesAndTypes](https://clickhouse.com/docs/ru/reference/formats/TabSeparated/TabSeparatedRawWithNamesAndTypes) | ✔ | ✔ |
| [Template](https://clickhouse.com/docs/ru/reference/formats/Template/Template) | ✔ | ✔ |
| [TemplateIgnoreSpaces](https://clickhouse.com/docs/ru/reference/formats/Template/TemplateIgnoreSpaces) | ✔ | ✗ |
| [CSV](https://clickhouse.com/docs/ru/reference/formats/CSV/CSV) | ✔ | ✔ |
| [CSVWithNames](https://clickhouse.com/docs/ru/reference/formats/CSV/CSVWithNames) | ✔ | ✔ |
| [CSVWithNamesAndTypes](https://clickhouse.com/docs/ru/reference/formats/CSV/CSVWithNamesAndTypes) | ✔ | ✔ |
| [CustomSeparated](https://clickhouse.com/docs/ru/reference/formats/CustomSeparated/CustomSeparated) | ✔ | ✔ |
| [CustomSeparatedIgnoreSpaces](https://clickhouse.com/docs/ru/reference/formats/CustomSeparated/CustomSeparatedIgnoreSpaces) | ✔ | ✗ |
| [CustomSeparatedIgnoreSpacesWithNames](https://clickhouse.com/docs/ru/reference/formats/CustomSeparated/CustomSeparatedIgnoreSpacesWithNames) | ✔ | ✗ |
| [CustomSeparatedIgnoreSpacesWithNamesAndTypes](https://clickhouse.com/docs/ru/reference/formats/CustomSeparated/CustomSeparatedIgnoreSpacesWithNamesAndTypes) | ✔ | ✗ |
| [CustomSeparatedWithNames](https://clickhouse.com/docs/ru/reference/formats/CustomSeparated/CustomSeparatedWithNames) | ✔ | ✔ |
| [CustomSeparatedWithNamesAndTypes](https://clickhouse.com/docs/ru/reference/formats/CustomSeparated/CustomSeparatedWithNamesAndTypes) | ✔ | ✔ |
| [HiveText](https://clickhouse.com/docs/ru/reference/formats/HiveText) | ✔ | ✗ |
| [SQLInsert](https://clickhouse.com/docs/ru/reference/formats/SQLInsert) | ✗ | ✔ |
| [Values](https://clickhouse.com/docs/ru/reference/formats/Values) | ✔ | ✔ |
| [Vertical](https://clickhouse.com/docs/ru/reference/formats/Vertical) | ✗ | ✔ |
| [JSON](https://clickhouse.com/docs/ru/reference/formats/JSON/JSON) | ✔ | ✔ |
| [JSONAsString](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONAsString) | ✔ | ✗ |
| [JSONAsObject](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONAsObject) | ✔ | ✗ |
| [JSONStrings](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONStrings) | ✗ | ✔ |
| [JSONColumns](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONColumns) | ✔ | ✔ |
| [JSONColumnsWithMetadata](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONColumnsWithMetadata) | ✔ | ✔ |
| [JSONCompact](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONCompact) | ✔ | ✔ |
| [JSONCompactStrings](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONCompactStrings) | ✗ | ✔ |
| [JSONCompactColumns](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONCompactColumns) | ✔ | ✔ |
| [JSONEachRow](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONEachRow) | ✔ | ✔ |
| [JSONLines](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONLines) | ✔ | ✔ |
| [PrettyJSONEachRow](https://clickhouse.com/docs/ru/reference/formats/JSON/PrettyJSONEachRow) | ✗ | ✔ |
| [JSONEachRowWithProgress](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONEachRowWithProgress) | ✗ | ✔ |
| [JSONStringsEachRow](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONStringsEachRow) | ✔ | ✔ |
| [JSONStringsEachRowWithProgress](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONStringsEachRowWithProgress) | ✗ | ✔ |
| [JSONCompactEachRow](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONCompactEachRow) | ✔ | ✔ |
| [JSONCompactEachRowWithNames](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONCompactEachRowWithNames) | ✔ | ✔ |
| [JSONCompactEachRowWithNamesAndTypes](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONCompactEachRowWithNamesAndTypes) | ✔ | ✔ |
| [JSONCompactEachRowWithProgress](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONCompactEachRowWithProgress) | ✗ | ✔ |
| [JSONCompactStringsEachRow](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONCompactStringsEachRow) | ✔ | ✔ |
| [JSONCompactStringsEachRowWithNames](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONCompactStringsEachRowWithNames) | ✔ | ✔ |
| [JSONCompactStringsEachRowWithNamesAndTypes](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONCompactStringsEachRowWithNamesAndTypes) | ✔ | ✔ |
| [JSONCompactStringsEachRowWithProgress](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONCompactStringsEachRowWithProgress) | ✗ | ✔ |
| [JSONObjectEachRow](https://clickhouse.com/docs/ru/reference/formats/JSON/JSONObjectEachRow) | ✔ | ✔ |
| [BSONEachRow](https://clickhouse.com/docs/ru/reference/formats/BSONEachRow) | ✔ | ✔ |
| [TSKV](https://clickhouse.com/docs/ru/reference/formats/TabSeparated/TSKV) | ✔ | ✔ |
| [Pretty](https://clickhouse.com/docs/ru/reference/formats/Pretty/Pretty) | ✗ | ✔ |
| [PrettyNoEscapes](https://clickhouse.com/docs/ru/reference/formats/Pretty/PrettyNoEscapes) | ✗ | ✔ |
| [PrettyMonoBlock](https://clickhouse.com/docs/ru/reference/formats/Pretty/PrettyMonoBlock) | ✗ | ✔ |
| [PrettyNoEscapesMonoBlock](https://clickhouse.com/docs/ru/reference/formats/Pretty/PrettyNoEscapesMonoBlock) | ✗ | ✔ |
| [PrettyCompact](https://clickhouse.com/docs/ru/reference/formats/Pretty/PrettyCompact) | ✗ | ✔ |
| [PrettyCompactNoEscapes](https://clickhouse.com/docs/ru/reference/formats/Pretty/PrettyCompactNoEscapes) | ✗ | ✔ |
| [PrettyCompactMonoBlock](https://clickhouse.com/docs/ru/reference/formats/Pretty/PrettyCompactMonoBlock) | ✗ | ✔ |
| [PrettyCompactNoEscapesMonoBlock](https://clickhouse.com/docs/ru/reference/formats/Pretty/PrettyCompactNoEscapesMonoBlock) | ✗ | ✔ |
| [PrettySpace](https://clickhouse.com/docs/ru/reference/formats/Pretty/PrettySpace) | ✗ | ✔ |
| [PrettySpaceNoEscapes](https://clickhouse.com/docs/ru/reference/formats/Pretty/PrettySpaceNoEscapes) | ✗ | ✔ |
| [PrettySpaceMonoBlock](https://clickhouse.com/docs/ru/reference/formats/Pretty/PrettySpaceMonoBlock) | ✗ | ✔ |
| [PrettySpaceNoEscapesMonoBlock](https://clickhouse.com/docs/ru/reference/formats/Pretty/PrettySpaceNoEscapesMonoBlock) | ✗ | ✔ |
| [Prometheus](https://clickhouse.com/docs/ru/reference/formats/Prometheus) | ✗ | ✔ |
| [Protobuf](https://clickhouse.com/docs/ru/reference/formats/Protobuf/Protobuf) | ✔ | ✔ |
| [ProtobufSingle](https://clickhouse.com/docs/ru/reference/formats/Protobuf/ProtobufSingle) | ✔ | ✔ |
| [ProtobufList](https://clickhouse.com/docs/ru/reference/formats/Protobuf/ProtobufList) | ✔ | ✔ |
| [Avro](https://clickhouse.com/docs/ru/reference/formats/Avro/Avro) | ✔ | ✔ |
| [AvroConfluent](https://clickhouse.com/docs/ru/reference/formats/Avro/AvroConfluent) | ✔ | ✔ |
| [Parquet](https://clickhouse.com/docs/ru/reference/formats/Parquet/Parquet) | ✔ | ✔ |
| [ParquetMetadata](https://clickhouse.com/docs/ru/reference/formats/Parquet/ParquetMetadata) | ✔ | ✗ |
| [Arrow](https://clickhouse.com/docs/ru/reference/formats/Arrow/Arrow) | ✔ | ✔ |
| [ArrowStream](https://clickhouse.com/docs/ru/reference/formats/Arrow/ArrowStream) | ✔ | ✔ |
| [ORC](https://clickhouse.com/docs/ru/reference/formats/ORC) | ✔ | ✔ |
| [One](https://clickhouse.com/docs/ru/reference/formats/One) | ✔ | ✗ |
| [Npy](https://clickhouse.com/docs/ru/reference/formats/Npy) | ✔ | ✔ |
| [RowBinary](https://clickhouse.com/docs/ru/reference/formats/RowBinary/RowBinary) | ✔ | ✔ |
| [RowBinaryWithNames](https://clickhouse.com/docs/ru/reference/formats/RowBinary/RowBinaryWithNames) | ✔ | ✔ |
| [RowBinaryWithNamesAndTypes](https://clickhouse.com/docs/ru/reference/formats/RowBinary/RowBinaryWithNamesAndTypes) | ✔ | ✔ |
| [RowBinaryWithDefaults](https://clickhouse.com/docs/ru/reference/formats/RowBinary/RowBinaryWithDefaults) | ✔ | ✗ |
| [RowBinaryWithNamesAndTypesAndDefaults](https://clickhouse.com/docs/ru/reference/formats/RowBinary/RowBinaryWithNamesAndTypesAndDefaults) | ✔ | ✗ |
| [Native](https://clickhouse.com/docs/ru/reference/formats/Native) | ✔ | ✔ |
| [Buffers](https://clickhouse.com/docs/ru/reference/formats/Buffers) | ✔ | ✔ |
| [Null](https://clickhouse.com/docs/ru/reference/formats/Null) | ✗ | ✔ |
| [Hash](https://clickhouse.com/docs/ru/reference/formats/Hash) | ✗ | ✔ |
| [XML](https://clickhouse.com/docs/ru/reference/formats/XML) | ✗ | ✔ |
| [CapnProto](https://clickhouse.com/docs/ru/reference/formats/CapnProto) | ✔ | ✔ |
| [LineAsString](https://clickhouse.com/docs/ru/reference/formats/LineAsString/LineAsString) | ✔ | ✔ |
| [LineAsStringWithNames](https://clickhouse.com/docs/ru/reference/formats/LineAsString/LineAsStringWithNames) | ✗ | ✔ |
| [LineAsStringWithNamesAndTypes](https://clickhouse.com/docs/ru/reference/formats/LineAsString/LineAsStringWithNamesAndTypes) | ✗ | ✔ |
| [Regexp](https://clickhouse.com/docs/ru/reference/formats/Regexp) | ✔ | ✗ |
| [RawBLOB](https://clickhouse.com/docs/ru/reference/formats/RawBLOB) | ✔ | ✔ |
| [MsgPack](https://clickhouse.com/docs/ru/reference/formats/MsgPack) | ✔ | ✔ |
| [MySQLDump](https://clickhouse.com/docs/ru/reference/formats/MySQLDump) | ✔ | ✗ |
| [MySQLWire](https://clickhouse.com/docs/ru/reference/formats/MySQLWire) | ✗ | ✔ |
| [PostgreSQLWire](https://clickhouse.com/docs/ru/reference/formats/PostgreSQLWire) | ✗ | ✔ |
| [ODBCDriver2](https://clickhouse.com/docs/ru/reference/formats/ODBCDriver2) | ✗ | ✔ |
| [GeoJSON](https://clickhouse.com/docs/ru/reference/formats/GeoJSON) | ✔ | ✔ |
| [DWARF](https://clickhouse.com/docs/ru/reference/formats/DWARF) | ✔ | ✗ |
| [Markdown](https://clickhouse.com/docs/ru/reference/formats/Markdown) | ✗ | ✔ |
| [Form](https://clickhouse.com/docs/ru/reference/formats/Form) | ✔ | ✗ |


## Схема формата


## Пропуск ошибок

- При ошибке разбора `JSONEachRow` пропускает все данные до символа новой строки (или EOF), поэтому для корректного подсчета ошибок строки должны разделяться символом `\n`.
- `Template` и `CustomSeparated` используют разделитель после последнего столбца и разделитель между строками, чтобы находить начало следующей строки, поэтому пропуск ошибок работает только в том случае, если хотя бы один из них не пуст.
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
