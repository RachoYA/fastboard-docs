# Движок таблицы MongoDB - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/integrations/mongodb


## Создание таблицы


```
CREATE TABLE [IF NOT EXISTS] [db.]table_name
(
    name1 [type1],
    name2 [type2],
    ...
) ENGINE = MongoDB(host:port, database, collection, user, password[, options[, oid_columns]]);

```


| Параметр | Описание |
| --- | --- |
| `host:port` | Адрес сервера MongoDB. |
| `database` | Имя удалённой базы данных. |
| `collection` | Имя удалённой коллекции. |
| `user` | Пользователь MongoDB. |
| `password` | Пароль пользователя. |
| `options` | Необязательно. [Параметры](https://www.mongodb.com/docs/manual/reference/connection-string-options/#connection-options) строки подключения MongoDB в виде строки в формате URL. Например: `'authSource=admin&ssl=true'` |
| `oid_columns` | Список столбцов, разделённых запятыми, которые следует обрабатывать как `oid` в предложении WHERE. По умолчанию — `_id`. |


```
ENGINE = MongoDB(uri, collection[, oid_columns]);

```


| Параметр | Описание |
| --- | --- |
| `uri` | URI подключения к серверу MongoDB. |
| `collection` | Имя удалённой коллекции. |
| `oid_columns` | Список столбцов, разделённых запятыми, которые следует обрабатывать как `oid` в предложении WHERE. По умолчанию — `_id`. |


## Сопоставление типов


| MongoDB | ClickHouse |
| --- | --- |
| bool, int32, int64 | *любой числовой тип, кроме Decimals*, Boolean, String |
| double | Float64, String |
| date | Date, Date32, DateTime, DateTime64, String |
| string | String, *любой числовой тип (кроме Decimals) при корректном формате* |
| document | String (как JSON) |
| array | Array, String (как JSON) |
| oid | String |
| binary | String, если в столбце; строка в кодировке base64, если в массиве или документе |
| uuid (binary subtype 4) | UUID |
| *любой другой* | String |


### OID


```
db.sample_oid.insertMany([
    {"another_oid_column": ObjectId()},
]);

db.sample_oid.find();
[
    {
        "_id": {"$oid": "67bf6cc44ebc466d33d42fb2"},
        "another_oid_column": {"$oid": "67bf6cc40000000000ea41b1"}
    }
]

```


```
CREATE TABLE sample_oid
(
    _id String,
    another_oid_column String
) ENGINE = MongoDB('mongodb://user:pass@host/db', 'sample_oid');

SELECT count() FROM sample_oid WHERE _id = '67bf6cc44ebc466d33d42fb2'; --выведет 1.
SELECT count() FROM sample_oid WHERE another_oid_column = '67bf6cc40000000000ea41b1'; --выведет 0

```


```
CREATE TABLE sample_oid
(
    _id String,
    another_oid_column String
) ENGINE = MongoDB('mongodb://user:pass@host/db', 'sample_oid', '_id,another_oid_column');

-- или

CREATE TABLE sample_oid
(
    _id String,
    another_oid_column String
) ENGINE = MongoDB('host', 'db', 'sample_oid', 'user', 'pass', '', '_id,another_oid_column');

SELECT count() FROM sample_oid WHERE another_oid_column = '67bf6cc40000000000ea41b1'; -- теперь выведет 1

```


## Поддерживаемые секции


```
SELECT * FROM mongo_table WHERE date = '2024-01-01'

```


```
SELECT * FROM mongo_table WHERE date = '2024-01-01'::Date OR date = toDate('2024-01-01')

```


## Пример использования


```
CREATE TABLE sample_mflix_table
(
    _id String,
    title String,
    plot String,
    genres Array(String),
    directors Array(String),
    writers Array(String),
    released Date,
    imdb String,
    year String
) ENGINE = MongoDB('mongodb://<USERNAME>:<PASSWORD>@atlas-sql-6634be87cefd3876070caf96-98lxs.a.query.mongodb.net/sample_mflix?ssl=true&authSource=admin', 'movies');

```


```
SELECT count() FROM sample_mflix_table

```


```
┌─count()─┐
│   21349 │
└─────────┘

```


```
-- JSONExtractString cannot be pushed down to MongoDB
SET mongodb_throw_on_unsupported_query = 0;

-- Find all 'Back to the Future' sequels with rating > 7.5
SELECT title, plot, genres, directors, released FROM sample_mflix_table
WHERE title IN ('Back to the Future', 'Back to the Future Part II', 'Back to the Future Part III')
    AND toFloat32(JSONExtractString(imdb, 'rating')) > 7.5
ORDER BY year
FORMAT Vertical;

```


```
Row 1:
──────
title:     Back to the Future
plot:      A young man is accidentally sent 30 years into the past in a time-traveling DeLorean invented by his friend, Dr. Emmett Brown, and must make sure his high-school-age parents unite in order to save his own existence.
genres:    ['Adventure','Comedy','Sci-Fi']
directors: ['Robert Zemeckis']
released:  1985-07-03

Row 2:
──────
title:     Back to the Future Part II
plot:      After visiting 2015, Marty McFly must repeat his visit to 1955 to prevent disastrous changes to 1985... without interfering with his first trip.
genres:    ['Action','Adventure','Comedy']
directors: ['Robert Zemeckis']
released:  1989-11-22

```


```
-- Find top 3 movies based on Cormac McCarthy's books
SELECT title, toFloat32(JSONExtractString(imdb, 'rating')) AS rating
FROM sample_mflix_table
WHERE arrayExists(x -> x LIKE 'Cormac McCarthy%', writers)
ORDER BY rating DESC
LIMIT 3;

```


```
┌─title──────────────────┬─rating─┐
│ No Country for Old Men │    8.1 │
│ The Sunset Limited     │    7.4 │
│ The Road               │    7.3 │
└────────────────────────┴────────┘

```


## Устранение неполадок

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
