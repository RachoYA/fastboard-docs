# Движок таблицы ArrowFlight - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/arrowflight


## Создание таблицы


```
CREATE TABLE [IF NOT EXISTS] [db.]table_name (name1 [type1], name2 [type2], ...)
    ENGINE = ArrowFlight('host:port', 'dataset_name' [, 'username', 'password']);

```

- `host:port` — Адрес удалённого сервера Arrow Flight. Если порт не указан, используется порт по умолчанию `8815`. [String](https://clickhouse.com/docs/ru/reference/data-types/string).
- `dataset_name` — Идентификатор набора данных на сервере Flight (используется как дескриптор PATH или в запросе `SELECT *` в зависимости от настройки `arrow_flight_request_descriptor_type`). [String](https://clickhouse.com/docs/ru/reference/data-types/string).
- `username` — Имя пользователя для HTTP-аутентификации Basic. [String](https://clickhouse.com/docs/ru/reference/data-types/string).
- `password` — Пароль для HTTP-аутентификации Basic. [String](https://clickhouse.com/docs/ru/reference/data-types/string).

## Именованные коллекции


```
CREATE TABLE remote_flight_data
    ENGINE = ArrowFlight(named_collection_name);

```


| Параметр | Обязательно | По умолчанию | Описание |
| --- | --- | --- | --- |
| `host` или `hostname` | Нет | `""` | Имя хоста сервера. |
| `port` | Да | — | Порт сервера. |
| `dataset` | Нет | `""` | Имя набора данных или дескриптор. |
| `use_basic_authentication` | Нет | `true` | Включает базовую аутентификацию. |
| `user` или `username` | Если аутентификация включена | — | Имя пользователя для аутентификации. |
| `password` | Нет | `""` | Пароль для аутентификации. |
| `enable_ssl` | Нет | `false` | Включает шифрование TLS. |
| `ssl_ca` | Нет | `""` | Путь к файлу CA‑сертификата для проверки TLS. |
| `ssl_override_hostname` | Нет | `""` | Переопределяет имя хоста, используемое при проверке TLS. |


## Настройки

- `arrow_flight_request_descriptor_type` — Определяет, как имя набора данных отправляется на сервер Flight. Возможные значения: `path` (по умолчанию, отправляется как дескриптор PATH) или `command` (отправляется как дескриптор CMD с `SELECT * FROM <dataset>`). Используйте `command` для серверов Flight, которые ожидают SQL-команды (например, Dremio).

## Пример использования


```
CREATE TABLE remote_flight_data
(
    id UInt32,
    name String,
    value Float64
) ENGINE = ArrowFlight('127.0.0.1:9005', 'sample_dataset');

SELECT * FROM remote_flight_data ORDER BY id;

```


```
┌─id─┬─name────┬─value─┐
│  1 │ foo     │ 42.1  │
│  2 │ bar     │ 13.3  │
│  3 │ baz     │ 77.0  │
└────┴─────────┴───────┘

```


```
INSERT INTO remote_flight_data VALUES (4, 'qux', 99.9);

```


## Примечания

- Если в операторе `CREATE TABLE` указаны столбцы, они должны соответствовать схеме, возвращаемой сервером Flight.
- Если столбцы не указаны, схема автоматически определяется на основе данных удалённого сервера.
- Поддерживаются как чтение (`SELECT`), так и запись (`INSERT`).
- Параметр `arrow_flight_request_descriptor_type` определяет, будет ли имя набора данных отправлено как дескриптор PATH или как дескриптор CMD, содержащий запрос `SELECT *`.

## См. также

- [Табличная функция arrowFlight](https://clickhouse.com/docs/ru/reference/functions/table-functions/arrowflight)
- [Интерфейс Arrow Flight](https://clickhouse.com/docs/ru/concepts/features/interfaces/arrowflight)
- [Apache Arrow Flight SQL](https://arrow.apache.org/docs/format/FlightSql.html)
- [Интеграция формата Arrow в ClickHouse](https://clickhouse.com/docs/ru/reference/formats/Arrow/Arrow)
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
