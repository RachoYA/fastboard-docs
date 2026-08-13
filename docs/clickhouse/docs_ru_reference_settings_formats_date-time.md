# Настройки формата date_time_* - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/settings/formats/date-time


## date_time_64_output_format_cut_trailing_zeros_align_to_groups_of_thousands


## date_time_input_format

- `'best_effort'` — Включает расширенный разбор. ClickHouse может разбирать базовый формат `YYYY-MM-DD HH:MM:SS` и все форматы даты и времени [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601). Например, `'2018-06-08T01:02:03.000Z'`.
- `'best_effort_us'` — Аналогично `best_effort` (см. отличие в [parseDateTimeBestEffortUS](https://clickhouse.com/docs/ru/reference/functions/regular-functions/type-conversion-functions#parseDateTimeBestEffortUS)
- `'basic'` — Использует базовый парсер. ClickHouse может разбирать только базовый формат `YYYY-MM-DD HH:MM:SS` или `YYYY-MM-DD`. Например, `2019-08-20 10:18:56` или `2019-08-20`.
- [Тип данных DateTime.](https://clickhouse.com/docs/ru/reference/data-types/datetime)
- [Функции для работы с датами и временем.](https://clickhouse.com/docs/ru/reference/functions/regular-functions/date-time-functions)

## date_time_output_format

- `simple` — Простой формат вывода. ClickHouse выводит дату и время в формате `YYYY-MM-DD hh:mm:ss`. Например, `2019-08-20 10:18:56`. Расчёт выполняется в соответствии с часовым поясом типа данных (если он задан) или часовым поясом сервера.
- `iso` — Формат вывода ISO. ClickHouse выводит дату и время в формате [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) `YYYY-MM-DDThh:mm:ssZ`. Например, `2019-08-20T10:18:56Z`. Обратите внимание, что вывод выполняется в UTC (`Z` означает UTC).
- `unix_timestamp` — Формат вывода Unix-временной метки. ClickHouse выводит дату и время в формате [Unix-временной метки](https://en.wikipedia.org/wiki/Unix_time). Например, `1566285536`.
- [Тип данных DateTime.](https://clickhouse.com/docs/ru/reference/data-types/datetime)
- [Функции для работы с датами и временем.](https://clickhouse.com/docs/ru/reference/functions/regular-functions/date-time-functions)

## date_time_overflow_behavior

- `ignore` — Переполнение игнорируется без уведомления. Результат не определён.
- `throw` — Сгенерировать исключение в случае переполнения.
- `saturate` — Ограничить результат предельными значениями. Если значение меньше минимального значения, которое может быть представлено целевым типом, в качестве результата выбирается минимальное представимое значение. Если значение больше максимального значения, которое может быть представлено целевым типом, в качестве результата выбирается максимальное представимое значение.
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
