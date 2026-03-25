# Быстрый старт ClickHouse OSS | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/getting-started/quick-start/oss

В этом кратком руководстве по быстрому старту вы за 8
простых шагов настроите ClickHouse OSS. Вы скачаете подходящий бинарный файл для своей ОС,
узнаете, как запускать сервер ClickHouse, и воспользуетесь клиентом ClickHouse, чтобы создать таблицу,
затем вставите в неё данные и выполните запрос для выборки этих данных.


## Загрузка ClickHouse​

ClickHouse работает нативно на Linux, FreeBSD и macOS, а на Windows — черезWSL. Самый простой способ загрузить ClickHouse локально — выполнить
следующую командуcurl. Команда определяет, поддерживается ли ваша операционная система,
и загружает соответствующий бинарный файл ClickHouse, собранный из ветки master.ПримечаниеРекомендуется запускать приведённую ниже команду из нового пустого подкаталога, поскольку при первом запуске сервера ClickHouse в каталоге, где находится исполняемый файл, будут созданы некоторые конфигурационные файлы.Приведенный ниже скрипт не рекомендуется использовать для установки ClickHouse в промышленной эксплуатации.
Если вам необходимо установить экземпляр ClickHouse для промышленной эксплуатации, обратитесь кстранице установки.curl https://clickhouse.com/ | shВы увидите:Successfully downloaded the ClickHouse binary, you can run it as:
    ./clickhouse

You can also install it:
sudo ./clickhouse installНа этом этапе можно проигнорировать предложение выполнить командуinstall.ПримечаниеДля пользователей Mac: Если вы получаете ошибки о том, что разработчик бинарного файла не может быть проверен, см."Исправление ошибки проверки разработчика в MacOS".

Рекомендуется запускать приведённую ниже команду из нового пустого подкаталога, поскольку при первом запуске сервера ClickHouse в каталоге, где находится исполняемый файл, будут созданы некоторые конфигурационные файлы.Приведенный ниже скрипт не рекомендуется использовать для установки ClickHouse в промышленной эксплуатации.
Если вам необходимо установить экземпляр ClickHouse для промышленной эксплуатации, обратитесь кстранице установки.

Приведенный ниже скрипт не рекомендуется использовать для установки ClickHouse в промышленной эксплуатации.
Если вам необходимо установить экземпляр ClickHouse для промышленной эксплуатации, обратитесь кстранице установки.


```
curl https://clickhouse.com/ | sh

```

Вы увидите:Successfully downloaded the ClickHouse binary, you can run it as:
    ./clickhouse

You can also install it:
sudo ./clickhouse installНа этом этапе можно проигнорировать предложение выполнить командуinstall.ПримечаниеДля пользователей Mac: Если вы получаете ошибки о том, что разработчик бинарного файла не может быть проверен, см."Исправление ошибки проверки разработчика в MacOS".


```
Successfully downloaded the ClickHouse binary, you can run it as:
    ./clickhouse

You can also install it:
sudo ./clickhouse install

```

На этом этапе можно проигнорировать предложение выполнить командуinstall.ПримечаниеДля пользователей Mac: Если вы получаете ошибки о том, что разработчик бинарного файла не может быть проверен, см."Исправление ошибки проверки разработчика в MacOS".

Для пользователей Mac: Если вы получаете ошибки о том, что разработчик бинарного файла не может быть проверен, см."Исправление ошибки проверки разработчика в MacOS".


## Запуск сервера​

Выполните следующую команду для запуска сервера ClickHouse:./clickhouse serverТерминал должен заполниться логами. Это ожидаемое поведение. В ClickHouseуровень логирования по умолчаниюустановлен вtrace, а не вwarning.


```
./clickhouse server

```

Терминал должен заполниться логами. Это ожидаемое поведение. В ClickHouseуровень логирования по умолчаниюустановлен вtrace, а не вwarning.


## Запуск клиента​

Используйтеclickhouse-clientдля подключения к вашему сервису ClickHouse. Откройте новый
терминал, перейдите в каталог, где сохранён бинарный файлclickhouse, и
выполните следующую команду:./clickhouse clientПри успешном подключении к вашему сервису на localhost вы увидите смайлик:my-host :)


```
./clickhouse client

```

При успешном подключении к вашему сервису на localhost вы увидите смайлик:my-host :)


```
my-host :)

```


## Создание таблицы​

ИспользуйтеCREATE TABLEдля создания новой таблицы. Стандартные SQL DDL-команды работают в
ClickHouse с одним дополнением — таблицы в ClickHouse требуют
указания клаузыENGINE. ИспользуйтеMergeTree,
чтобы воспользоваться преимуществами производительности ClickHouse:CREATE TABLE my_first_table
(
    user_id UInt32,
    message String,
    timestamp DateTime,
    metric Float32
)
ENGINE = MergeTree
PRIMARY KEY (user_id, timestamp)


```
CREATE TABLE my_first_table
(
    user_id UInt32,
    message String,
    timestamp DateTime,
    metric Float32
)
ENGINE = MergeTree
PRIMARY KEY (user_id, timestamp)

```


## Вставка данных​

Вы можете использовать знакомую командуINSERT INTO TABLEс ClickHouse, но важно
понимать, что каждая вставка в таблицуMergeTreeприводит к созданию в хранилище
того, что мы называемпартом(part) в ClickHouse. Эти части впоследствии
объединяются ClickHouse в фоновом режиме.В ClickHouse рекомендуется выполнять массовую вставку большого количества строк за один раз
(десятки тысяч или даже миллионы одновременно), чтобы минимизировать количествочастей,
которые необходимо объединять в фоновом процессе.В данном руководстве мы пока не будем этим заниматься. Выполните следующую команду для вставки нескольких строк данных в таблицу:INSERT INTO my_first_table (user_id, message, timestamp, metric) VALUES
    (101, 'Hello, ClickHouse!',                                 now(),       -1.0    ),
    (102, 'Insert a lot of rows per batch',                     yesterday(), 1.41421 ),
    (102, 'Sort your data based on your commonly-used queries', today(),     2.718   ),
    (101, 'Granules are the smallest chunks of data read',      now() + 5,   3.14159 )

В ClickHouse рекомендуется выполнять массовую вставку большого количества строк за один раз
(десятки тысяч или даже миллионы одновременно), чтобы минимизировать количествочастей,
которые необходимо объединять в фоновом процессе.В данном руководстве мы пока не будем этим заниматься. Выполните следующую команду для вставки нескольких строк данных в таблицу:INSERT INTO my_first_table (user_id, message, timestamp, metric) VALUES
    (101, 'Hello, ClickHouse!',                                 now(),       -1.0    ),
    (102, 'Insert a lot of rows per batch',                     yesterday(), 1.41421 ),
    (102, 'Sort your data based on your commonly-used queries', today(),     2.718   ),
    (101, 'Granules are the smallest chunks of data read',      now() + 5,   3.14159 )

В данном руководстве мы пока не будем этим заниматься. Выполните следующую команду для вставки нескольких строк данных в таблицу:INSERT INTO my_first_table (user_id, message, timestamp, metric) VALUES
    (101, 'Hello, ClickHouse!',                                 now(),       -1.0    ),
    (102, 'Insert a lot of rows per batch',                     yesterday(), 1.41421 ),
    (102, 'Sort your data based on your commonly-used queries', today(),     2.718   ),
    (101, 'Granules are the smallest chunks of data read',      now() + 5,   3.14159 )


```
INSERT INTO my_first_table (user_id, message, timestamp, metric) VALUES
    (101, 'Hello, ClickHouse!',                                 now(),       -1.0    ),
    (102, 'Insert a lot of rows per batch',                     yesterday(), 1.41421 ),
    (102, 'Sort your data based on your commonly-used queries', today(),     2.718   ),
    (101, 'Granules are the smallest chunks of data read',      now() + 5,   3.14159 )

```


## Запросы к новой таблице​

ЗапросSELECTможно написать так же, как в любой другой SQL-базе данных:SELECT *
FROM my_first_table
ORDER BY timestampОбратите внимание, что ответ возвращается в виде таблицы:┌─user_id─┬─message────────────────────────────────────────────┬───────────timestamp─┬──metric─┐
│     102 │ Insert a lot of rows per batch                     │ 2022-03-21 00:00:00 │ 1.41421 │
│     102 │ Sort your data based on your commonly-used queries │ 2022-03-22 00:00:00 │   2.718 │
│     101 │ Hello, ClickHouse!                                 │ 2022-03-22 14:04:09 │      -1 │
│     101 │ Granules are the smallest chunks of data read      │ 2022-03-22 14:04:14 │ 3.14159 │
└─────────┴────────────────────────────────────────────────────┴─────────────────────┴─────────┘

4 rows in set. Elapsed: 0.008 sec.


```
SELECT *
FROM my_first_table
ORDER BY timestamp

```

Обратите внимание, что ответ возвращается в виде таблицы:┌─user_id─┬─message────────────────────────────────────────────┬───────────timestamp─┬──metric─┐
│     102 │ Insert a lot of rows per batch                     │ 2022-03-21 00:00:00 │ 1.41421 │
│     102 │ Sort your data based on your commonly-used queries │ 2022-03-22 00:00:00 │   2.718 │
│     101 │ Hello, ClickHouse!                                 │ 2022-03-22 14:04:09 │      -1 │
│     101 │ Granules are the smallest chunks of data read      │ 2022-03-22 14:04:14 │ 3.14159 │
└─────────┴────────────────────────────────────────────────────┴─────────────────────┴─────────┘

4 rows in set. Elapsed: 0.008 sec.


```
┌─user_id─┬─message────────────────────────────────────────────┬───────────timestamp─┬──metric─┐
│     102 │ Insert a lot of rows per batch                     │ 2022-03-21 00:00:00 │ 1.41421 │
│     102 │ Sort your data based on your commonly-used queries │ 2022-03-22 00:00:00 │   2.718 │
│     101 │ Hello, ClickHouse!                                 │ 2022-03-22 14:04:09 │      -1 │
│     101 │ Granules are the smallest chunks of data read      │ 2022-03-22 14:04:14 │ 3.14159 │
└─────────┴────────────────────────────────────────────────────┴─────────────────────┴─────────┘

4 rows in set. Elapsed: 0.008 sec.

```


## Вставка собственных данных​

Следующий шаг — загрузить ваши данные в ClickHouse. Для приёма данных доступно множествотабличных функцийиинтеграций. Примеры приведены на вкладках
ниже. Полный список технологий, которые интегрируются с ClickHouse, представлен на страницеИнтеграции.S3GCSВебЛокальныйPostgreSQLMySQLODBC/JDBCОчереди сообщенийОзера данныхДругоеИспользуйте табличную функциюs3,
чтобы читать файлы из S3. Это табличная функция — то есть результатом является таблица,
которую можно:использовать как источник для запросаSELECT(что позволяет выполнять разовые запросы и
оставлять данные в S3), иливставить результат в таблицуMergeTree(когда вы будете готовы
перенести данные в ClickHouse).Пример разового (ad hoc) запроса:SELECT
passenger_count,
avg(toFloat32(total_amount))
FROM s3(
'https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/trips_0.gz',
'TabSeparatedWithNames'
)
GROUP BY passenger_count
ORDER BY passenger_count;Перемещение данных в таблицу ClickHouse будет выглядеть следующим образом, гдеnyc_taxi— это таблицаMergeTree:INSERT INTO nyc_taxi
SELECT * FROM s3(
'https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/trips_0.gz',
'TabSeparatedWithNames'
)
SETTINGS input_format_allow_errors_num=25000;Ознакомьтесь с нашейколлекцией страниц документации по AWS S3, где приведена подробная информация и многочисленные примеры использования S3 с ClickHouse.Табличная функцияs3, используемая для
чтения данных из AWS S3, также работает с файлами в Google Cloud Storage.Например:SELECT
*
FROM s3(
'https://storage.googleapis.com/my-bucket/trips.parquet',
'MY_GCS_HMAC_KEY',
'MY_GCS_HMAC_SECRET_KEY',
'Parquet'
)
LIMIT 1000Дополнительные сведения см. настранице табличной функцииs3.Табличная функцияurlчитает
файлы, доступные в интернете:--By default, ClickHouse prevents redirects to protect from SSRF attacks.
--The URL below requires a redirect, so we must set max_http_get_redirects > 0.
SET max_http_get_redirects=10;

SELECT *
FROM url(
'http://prod2.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-complete.csv',
'CSV'
);Дополнительную информацию см. настранице табличной функцииurl.Используйтеfileтабличный движок, чтобы
читать локальный файл. Для простоты скопируйте файл в каталогuser_files(он находится в каталоге, куда вы загрузили бинарный файл ClickHouse).DESCRIBE TABLE file('comments.tsv')

Query id: 8ca9b2f9-65a2-4982-954a-890de710a336

┌─name──────┬─type────────────────────┐
│ id        │ Nullable(Int64)         │
│ type      │ Nullable(String)        │
│ author    │ Nullable(String)        │
│ timestamp │ Nullable(DateTime64(9)) │
│ comment   │ Nullable(String)        │
│ children  │ Array(Nullable(Int64))  │
└───────────┴─────────────────────────┘Обратите внимание, что ClickHouse определяет имена и типы данных столбцов, анализируя
большой пакет строк. Если ClickHouse не может определить формат файла по его имени,
вы можете указать его вторым аргументом:SELECT count()
FROM file(
'comments.tsv',
'TabSeparatedWithNames'
)Подробнее см. страницу документации по табличной функцииfile.Используйтетабличную функциюpostgresql,
чтобы читать данные из таблицы в PostgreSQL:SELECT *
FROM
postgresql(
'localhost:5432',
'my_database',
'my_table',
'postgresql_user',
'password')
;Подробности см. на странице документации потабличной функцииpostgresql.Используйтетабличную функциюmysql,
чтобы читать данные из таблицы в MySQL:SELECT *
FROM
mysql(
'localhost:3306',
'my_database',
'my_table',
'mysql_user',
'password')
;Подробнее см. страницу документации потабличной функцииmysql.ClickHouse может читать данные из любого ODBC- или JDBC-источника данных:SELECT *
FROM
odbc(
'DSN=mysqlconn',
'my_database',
'my_table'
);Ознакомьтесь со страницами документации по табличной функцииodbcи табличной функцииjdbcдля получения более подробной информации.Очереди сообщений могут передавать данные в ClickHouse с помощью соответствующего табличного движка, в том числе:Kafka: интегрируйте с Kafka с помощьютабличного движкаKafkaAmazon MSK: интегрируйте сAmazon Managed Streaming for Apache Kafka (MSK)RabbitMQ: интегрируйте с RabbitMQ с помощьютабличного движкаRabbitMQВ ClickHouse есть табличные функции для чтения данных из следующих источников:Hadoop: интеграция с Apache Hadoop с использованием табличной функцииhdfsHudi: чтение из существующих таблиц Apache Hudi в S3 с использованием табличной функцииhudiIceberg: чтение из существующих таблиц Apache Iceberg в S3 с использованием табличной функцииicebergDeltaLake: чтение из существующих таблиц Delta Lake в S3 с использованием табличной функцииdeltaLakeОзнакомьтесь с нашимобширным списком интеграций ClickHouse, чтобы узнать, как подключить имеющиеся фреймворки и источники данных к ClickHouse.

- S3GCSВебЛокальныйPostgreSQLMySQLODBC/JDBCОчереди сообщенийОзера данныхДругое
- GCSВебЛокальныйPostgreSQLMySQLODBC/JDBCОчереди сообщенийОзера данныхДругое
- ВебЛокальныйPostgreSQLMySQLODBC/JDBCОчереди сообщенийОзера данныхДругое
- ЛокальныйPostgreSQLMySQLODBC/JDBCОчереди сообщенийОзера данныхДругое
- PostgreSQLMySQLODBC/JDBCОчереди сообщенийОзера данныхДругое
- MySQLODBC/JDBCОчереди сообщенийОзера данныхДругое
- ODBC/JDBCОчереди сообщенийОзера данныхДругое
- Очереди сообщенийОзера данныхДругое
- Озера данныхДругое
- Другое
Используйте табличную функциюs3,
чтобы читать файлы из S3. Это табличная функция — то есть результатом является таблица,
которую можно:использовать как источник для запросаSELECT(что позволяет выполнять разовые запросы и
оставлять данные в S3), иливставить результат в таблицуMergeTree(когда вы будете готовы
перенести данные в ClickHouse).Пример разового (ad hoc) запроса:SELECT
passenger_count,
avg(toFloat32(total_amount))
FROM s3(
'https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/trips_0.gz',
'TabSeparatedWithNames'
)
GROUP BY passenger_count
ORDER BY passenger_count;Перемещение данных в таблицу ClickHouse будет выглядеть следующим образом, гдеnyc_taxi— это таблицаMergeTree:INSERT INTO nyc_taxi
SELECT * FROM s3(
'https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/trips_0.gz',
'TabSeparatedWithNames'
)
SETTINGS input_format_allow_errors_num=25000;Ознакомьтесь с нашейколлекцией страниц документации по AWS S3, где приведена подробная информация и многочисленные примеры использования S3 с ClickHouse.

- использовать как источник для запросаSELECT(что позволяет выполнять разовые запросы и
оставлять данные в S3), или
- вставить результат в таблицуMergeTree(когда вы будете готовы
перенести данные в ClickHouse).
Пример разового (ad hoc) запроса:SELECT
passenger_count,
avg(toFloat32(total_amount))
FROM s3(
'https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/trips_0.gz',
'TabSeparatedWithNames'
)
GROUP BY passenger_count
ORDER BY passenger_count;Перемещение данных в таблицу ClickHouse будет выглядеть следующим образом, гдеnyc_taxi— это таблицаMergeTree:INSERT INTO nyc_taxi
SELECT * FROM s3(
'https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/trips_0.gz',
'TabSeparatedWithNames'
)
SETTINGS input_format_allow_errors_num=25000;Ознакомьтесь с нашейколлекцией страниц документации по AWS S3, где приведена подробная информация и многочисленные примеры использования S3 с ClickHouse.


```
SELECT
passenger_count,
avg(toFloat32(total_amount))
FROM s3(
'https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/trips_0.gz',
'TabSeparatedWithNames'
)
GROUP BY passenger_count
ORDER BY passenger_count;

```

Перемещение данных в таблицу ClickHouse будет выглядеть следующим образом, гдеnyc_taxi— это таблицаMergeTree:INSERT INTO nyc_taxi
SELECT * FROM s3(
'https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/trips_0.gz',
'TabSeparatedWithNames'
)
SETTINGS input_format_allow_errors_num=25000;Ознакомьтесь с нашейколлекцией страниц документации по AWS S3, где приведена подробная информация и многочисленные примеры использования S3 с ClickHouse.


```
INSERT INTO nyc_taxi
SELECT * FROM s3(
'https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/trips_0.gz',
'TabSeparatedWithNames'
)
SETTINGS input_format_allow_errors_num=25000;

```

Ознакомьтесь с нашейколлекцией страниц документации по AWS S3, где приведена подробная информация и многочисленные примеры использования S3 с ClickHouse.

Табличная функцияs3, используемая для
чтения данных из AWS S3, также работает с файлами в Google Cloud Storage.Например:SELECT
*
FROM s3(
'https://storage.googleapis.com/my-bucket/trips.parquet',
'MY_GCS_HMAC_KEY',
'MY_GCS_HMAC_SECRET_KEY',
'Parquet'
)
LIMIT 1000Дополнительные сведения см. настранице табличной функцииs3.

Например:SELECT
*
FROM s3(
'https://storage.googleapis.com/my-bucket/trips.parquet',
'MY_GCS_HMAC_KEY',
'MY_GCS_HMAC_SECRET_KEY',
'Parquet'
)
LIMIT 1000Дополнительные сведения см. настранице табличной функцииs3.


```
SELECT
*
FROM s3(
'https://storage.googleapis.com/my-bucket/trips.parquet',
'MY_GCS_HMAC_KEY',
'MY_GCS_HMAC_SECRET_KEY',
'Parquet'
)
LIMIT 1000

```

Дополнительные сведения см. настранице табличной функцииs3.

Табличная функцияurlчитает
файлы, доступные в интернете:--By default, ClickHouse prevents redirects to protect from SSRF attacks.
--The URL below requires a redirect, so we must set max_http_get_redirects > 0.
SET max_http_get_redirects=10;

SELECT *
FROM url(
'http://prod2.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-complete.csv',
'CSV'
);Дополнительную информацию см. настранице табличной функцииurl.


```
--By default, ClickHouse prevents redirects to protect from SSRF attacks.
--The URL below requires a redirect, so we must set max_http_get_redirects > 0.
SET max_http_get_redirects=10;

SELECT *
FROM url(
'http://prod2.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-complete.csv',
'CSV'
);

```

Дополнительную информацию см. настранице табличной функцииurl.

Используйтеfileтабличный движок, чтобы
читать локальный файл. Для простоты скопируйте файл в каталогuser_files(он находится в каталоге, куда вы загрузили бинарный файл ClickHouse).DESCRIBE TABLE file('comments.tsv')

Query id: 8ca9b2f9-65a2-4982-954a-890de710a336

┌─name──────┬─type────────────────────┐
│ id        │ Nullable(Int64)         │
│ type      │ Nullable(String)        │
│ author    │ Nullable(String)        │
│ timestamp │ Nullable(DateTime64(9)) │
│ comment   │ Nullable(String)        │
│ children  │ Array(Nullable(Int64))  │
└───────────┴─────────────────────────┘Обратите внимание, что ClickHouse определяет имена и типы данных столбцов, анализируя
большой пакет строк. Если ClickHouse не может определить формат файла по его имени,
вы можете указать его вторым аргументом:SELECT count()
FROM file(
'comments.tsv',
'TabSeparatedWithNames'
)Подробнее см. страницу документации по табличной функцииfile.


```
DESCRIBE TABLE file('comments.tsv')

Query id: 8ca9b2f9-65a2-4982-954a-890de710a336

┌─name──────┬─type────────────────────┐
│ id        │ Nullable(Int64)         │
│ type      │ Nullable(String)        │
│ author    │ Nullable(String)        │
│ timestamp │ Nullable(DateTime64(9)) │
│ comment   │ Nullable(String)        │
│ children  │ Array(Nullable(Int64))  │
└───────────┴─────────────────────────┘

```

Обратите внимание, что ClickHouse определяет имена и типы данных столбцов, анализируя
большой пакет строк. Если ClickHouse не может определить формат файла по его имени,
вы можете указать его вторым аргументом:SELECT count()
FROM file(
'comments.tsv',
'TabSeparatedWithNames'
)Подробнее см. страницу документации по табличной функцииfile.


```
SELECT count()
FROM file(
'comments.tsv',
'TabSeparatedWithNames'
)

```

Подробнее см. страницу документации по табличной функцииfile.

Используйтетабличную функциюpostgresql,
чтобы читать данные из таблицы в PostgreSQL:SELECT *
FROM
postgresql(
'localhost:5432',
'my_database',
'my_table',
'postgresql_user',
'password')
;Подробности см. на странице документации потабличной функцииpostgresql.


```
SELECT *
FROM
postgresql(
'localhost:5432',
'my_database',
'my_table',
'postgresql_user',
'password')
;

```

Подробности см. на странице документации потабличной функцииpostgresql.

Используйтетабличную функциюmysql,
чтобы читать данные из таблицы в MySQL:SELECT *
FROM
mysql(
'localhost:3306',
'my_database',
'my_table',
'mysql_user',
'password')
;Подробнее см. страницу документации потабличной функцииmysql.


```
SELECT *
FROM
mysql(
'localhost:3306',
'my_database',
'my_table',
'mysql_user',
'password')
;

```

Подробнее см. страницу документации потабличной функцииmysql.

ClickHouse может читать данные из любого ODBC- или JDBC-источника данных:SELECT *
FROM
odbc(
'DSN=mysqlconn',
'my_database',
'my_table'
);Ознакомьтесь со страницами документации по табличной функцииodbcи табличной функцииjdbcдля получения более подробной информации.


```
SELECT *
FROM
odbc(
'DSN=mysqlconn',
'my_database',
'my_table'
);

```

Ознакомьтесь со страницами документации по табличной функцииodbcи табличной функцииjdbcдля получения более подробной информации.

Очереди сообщений могут передавать данные в ClickHouse с помощью соответствующего табличного движка, в том числе:Kafka: интегрируйте с Kafka с помощьютабличного движкаKafkaAmazon MSK: интегрируйте сAmazon Managed Streaming for Apache Kafka (MSK)RabbitMQ: интегрируйте с RabbitMQ с помощьютабличного движкаRabbitMQ

- Kafka: интегрируйте с Kafka с помощьютабличного движкаKafka
- Amazon MSK: интегрируйте сAmazon Managed Streaming for Apache Kafka (MSK)
- RabbitMQ: интегрируйте с RabbitMQ с помощьютабличного движкаRabbitMQ
В ClickHouse есть табличные функции для чтения данных из следующих источников:Hadoop: интеграция с Apache Hadoop с использованием табличной функцииhdfsHudi: чтение из существующих таблиц Apache Hudi в S3 с использованием табличной функцииhudiIceberg: чтение из существующих таблиц Apache Iceberg в S3 с использованием табличной функцииicebergDeltaLake: чтение из существующих таблиц Delta Lake в S3 с использованием табличной функцииdeltaLake

- Hadoop: интеграция с Apache Hadoop с использованием табличной функцииhdfs
- Hudi: чтение из существующих таблиц Apache Hudi в S3 с использованием табличной функцииhudi
- Iceberg: чтение из существующих таблиц Apache Iceberg в S3 с использованием табличной функцииiceberg
- DeltaLake: чтение из существующих таблиц Delta Lake в S3 с использованием табличной функцииdeltaLake
Ознакомьтесь с нашимобширным списком интеграций ClickHouse, чтобы узнать, как подключить имеющиеся фреймворки и источники данных к ClickHouse.


## Исследование​

- Ознакомьтесь с разделомОсновные концепции, чтобы разобраться в основных принципах работы ClickHouse «под капотом».
- Ознакомьтесь суглублённым руководством, которое гораздо глубже раскрывает ключевые концепции и возможности ClickHouse.
- Продолжите обучение, пройдя наши бесплатные онлайн‑курсы в удобное для вас время вClickHouse Academy.
- У нас есть списокпримеров наборов данныхс инструкциями по их загрузке.
- Если ваши данные поступают из внешнего источника, ознакомьтесь с нашейподборкой руководств по интеграциямдля подключения к очередям сообщений, базам данных, пайплайнам и другим системам.
- Если вы используете UI/BI‑инструмент визуализации, ознакомьтесь сруководствами по подключению UI к ClickHouse.
- Руководство пользователя попервичным ключамсодержит всю необходимую информацию о первичных ключах и их определении.