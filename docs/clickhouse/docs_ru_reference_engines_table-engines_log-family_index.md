# Семейство движков Log - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/log-family/index


| Движки семейства Log |
| --- |
| [StripeLog](https://clickhouse.com/docs/ru/reference/engines/table-engines/log-family/stripelog) |
| [Log](https://clickhouse.com/docs/ru/reference/engines/table-engines/log-family/log) |
| [TinyLog](https://clickhouse.com/docs/ru/reference/engines/table-engines/log-family/tinylog) |


## Общие свойства

- Хранят данные на диске.
- При записи дописывают данные в конец файла.
- Поддерживают блокировки для одновременного доступа к данным. Во время запросов `INSERT` таблица блокируется, и другие запросы на чтение и запись данных ждут снятия блокировки. Если запросов на запись данных нет, одновременно может выполняться любое количество запросов на чтение данных.
- Не поддерживают [мутации](https://clickhouse.com/docs/ru/reference/statements/alter/index#mutations).
- Не поддерживают индексы. Это означает, что запросы `SELECT` по диапазонам данных выполняются неэффективно.
- Не записывают данные атомарно. Таблица может оказаться с поврежденными данными, если что-то прервет операцию записи, например аварийное завершение работы сервера.

## Отличия

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
