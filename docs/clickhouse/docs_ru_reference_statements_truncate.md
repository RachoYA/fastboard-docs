# Команды TRUNCATE - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/statements/truncate


## TRUNCATE TABLE


```
TRUNCATE TABLE [IF EXISTS] [db.]name [ON CLUSTER cluster] [SYNC]

```


| Параметр | Описание |
| --- | --- |
| `IF EXISTS` | Предотвращает ошибку, если таблица не существует. Если этот параметр опущен, запрос возвращает ошибку. |
| `db.name` | Необязательное имя базы данных. |
| `ON CLUSTER cluster` | Выполняет команду на указанном кластере. |
| `SYNC` | Делает усечение синхронным на репликах при использовании реплицируемых таблиц. Если этот параметр опущен, по умолчанию усечение выполняется асинхронно. |

- [`View`](https://clickhouse.com/docs/ru/reference/engines/table-engines/special/view)
- [`File`](https://clickhouse.com/docs/ru/reference/engines/table-engines/special/file)
- [`URL`](https://clickhouse.com/docs/ru/reference/engines/table-engines/special/url)
- [`Buffer`](https://clickhouse.com/docs/ru/reference/engines/table-engines/special/buffer)
- [`Null`](https://clickhouse.com/docs/ru/reference/engines/table-engines/special/null)

## TRUNCATE ВСЕХ ТАБЛИЦ


```
TRUNCATE [ALL] TABLES FROM [IF EXISTS] db [LIKE | ILIKE | NOT LIKE '<pattern>'] [ON CLUSTER cluster]

```


| Параметр | Описание |
| --- | --- |
| `ALL` | Удаляет данные из всех таблиц в базе данных. |
| `IF EXISTS` | Предотвращает ошибку, если база данных не существует. |
| `db` | Имя базы данных. |
| `LIKE \| ILIKE \| NOT LIKE '<pattern>'` | Фильтрует таблицы по шаблону. |
| `ON CLUSTER cluster` | Выполняет команду на всём кластере. |


## TRUNCATE DATABASE


```
TRUNCATE DATABASE [IF EXISTS] db [ON CLUSTER cluster]

```


| Параметр | Описание |
| --- | --- |
| `IF EXISTS` | Предотвращает ошибку, если база данных не существует. |
| `db` | Имя базы данных. |
| `ON CLUSTER cluster` | Выполняет команду на всём указанном кластере. |

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
