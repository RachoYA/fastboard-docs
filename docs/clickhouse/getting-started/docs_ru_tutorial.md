# Продвинутое руководство | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/tutorial


## Overview​

Узнайте, как выполнять приём и запросы данных в ClickHouse на примере набора данных о такси Нью-Йорка.


### Prerequisites​

Для выполнения данного руководства необходим доступ к работающему сервису ClickHouse. Инструкции см. в руководствеБыстрый старт.


## Создание новой таблицы​

Набор данных о такси Нью‑Йорка содержит сведения о миллионах поездок, включая такие столбцы, как сумма чаевых, платные дороги, тип оплаты и многое другое. Создайте таблицу для хранения этих данных.Подключитесь к SQL‑консоли:Для ClickHouse Cloud выберите сервис в раскрывающемся списке, затем выберитеSQL Consoleв левой панели навигации.Для самостоятельно развернутого ClickHouse подключитесь к SQL‑консоли по адресуhttps://_hostname_:8443/play. Уточните детали у администратора ClickHouse.Создайте следующую таблицуtripsв базе данныхdefault:CREATE TABLE trips
(
    `trip_id` UInt32,
    `vendor_id` Enum8('1' = 1, '2' = 2, '3' = 3, '4' = 4, 'CMT' = 5, 'VTS' = 6, 'DDS' = 7, 'B02512' = 10, 'B02598' = 11, 'B02617' = 12, 'B02682' = 13, 'B02764' = 14, '' = 15),
    `pickup_date` Date,
    `pickup_datetime` DateTime,
    `dropoff_date` Date,
    `dropoff_datetime` DateTime,
    `store_and_fwd_flag` UInt8,
    `rate_code_id` UInt8,
    `pickup_longitude` Float64,
    `pickup_latitude` Float64,
    `dropoff_longitude` Float64,
    `dropoff_latitude` Float64,
    `passenger_count` UInt8,
    `trip_distance` Float64,
    `fare_amount` Float32,
    `extra` Float32,
    `mta_tax` Float32,
    `tip_amount` Float32,
    `tolls_amount` Float32,
    `ehail_fee` Float32,
    `improvement_surcharge` Float32,
    `total_amount` Float32,
    `payment_type` Enum8('UNK' = 0, 'CSH' = 1, 'CRE' = 2, 'NOC' = 3, 'DIS' = 4),
    `trip_type` UInt8,
    `pickup` FixedString(25),
    `dropoff` FixedString(25),
    `cab_type` Enum8('yellow' = 1, 'green' = 2, 'uber' = 3),
    `pickup_nyct2010_gid` Int8,
    `pickup_ctlabel` Float32,
    `pickup_borocode` Int8,
    `pickup_ct2010` String,
    `pickup_boroct2010` String,
    `pickup_cdeligibil` String,
    `pickup_ntacode` FixedString(4),
    `pickup_ntaname` String,
    `pickup_puma` UInt16,
    `dropoff_nyct2010_gid` UInt8,
    `dropoff_ctlabel` Float32,
    `dropoff_borocode` UInt8,
    `dropoff_ct2010` String,
    `dropoff_boroct2010` String,
    `dropoff_cdeligibil` String,
    `dropoff_ntacode` FixedString(4),
    `dropoff_ntaname` String,
    `dropoff_puma` UInt16
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(pickup_date)
ORDER BY pickup_datetime;

- Подключитесь к SQL‑консоли:Для ClickHouse Cloud выберите сервис в раскрывающемся списке, затем выберитеSQL Consoleв левой панели навигации.Для самостоятельно развернутого ClickHouse подключитесь к SQL‑консоли по адресуhttps://_hostname_:8443/play. Уточните детали у администратора ClickHouse.
Подключитесь к SQL‑консоли:

- Для ClickHouse Cloud выберите сервис в раскрывающемся списке, затем выберитеSQL Consoleв левой панели навигации.
- Для самостоятельно развернутого ClickHouse подключитесь к SQL‑консоли по адресуhttps://_hostname_:8443/play. Уточните детали у администратора ClickHouse.
- Создайте следующую таблицуtripsв базе данныхdefault:CREATE TABLE trips
(
    `trip_id` UInt32,
    `vendor_id` Enum8('1' = 1, '2' = 2, '3' = 3, '4' = 4, 'CMT' = 5, 'VTS' = 6, 'DDS' = 7, 'B02512' = 10, 'B02598' = 11, 'B02617' = 12, 'B02682' = 13, 'B02764' = 14, '' = 15),
    `pickup_date` Date,
    `pickup_datetime` DateTime,
    `dropoff_date` Date,
    `dropoff_datetime` DateTime,
    `store_and_fwd_flag` UInt8,
    `rate_code_id` UInt8,
    `pickup_longitude` Float64,
    `pickup_latitude` Float64,
    `dropoff_longitude` Float64,
    `dropoff_latitude` Float64,
    `passenger_count` UInt8,
    `trip_distance` Float64,
    `fare_amount` Float32,
    `extra` Float32,
    `mta_tax` Float32,
    `tip_amount` Float32,
    `tolls_amount` Float32,
    `ehail_fee` Float32,
    `improvement_surcharge` Float32,
    `total_amount` Float32,
    `payment_type` Enum8('UNK' = 0, 'CSH' = 1, 'CRE' = 2, 'NOC' = 3, 'DIS' = 4),
    `trip_type` UInt8,
    `pickup` FixedString(25),
    `dropoff` FixedString(25),
    `cab_type` Enum8('yellow' = 1, 'green' = 2, 'uber' = 3),
    `pickup_nyct2010_gid` Int8,
    `pickup_ctlabel` Float32,
    `pickup_borocode` Int8,
    `pickup_ct2010` String,
    `pickup_boroct2010` String,
    `pickup_cdeligibil` String,
    `pickup_ntacode` FixedString(4),
    `pickup_ntaname` String,
    `pickup_puma` UInt16,
    `dropoff_nyct2010_gid` UInt8,
    `dropoff_ctlabel` Float32,
    `dropoff_borocode` UInt8,
    `dropoff_ct2010` String,
    `dropoff_boroct2010` String,
    `dropoff_cdeligibil` String,
    `dropoff_ntacode` FixedString(4),
    `dropoff_ntaname` String,
    `dropoff_puma` UInt16
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(pickup_date)
ORDER BY pickup_datetime;
Создайте следующую таблицуtripsв базе данныхdefault:


```
CREATE TABLE trips
(
    `trip_id` UInt32,
    `vendor_id` Enum8('1' = 1, '2' = 2, '3' = 3, '4' = 4, 'CMT' = 5, 'VTS' = 6, 'DDS' = 7, 'B02512' = 10, 'B02598' = 11, 'B02617' = 12, 'B02682' = 13, 'B02764' = 14, '' = 15),
    `pickup_date` Date,
    `pickup_datetime` DateTime,
    `dropoff_date` Date,
    `dropoff_datetime` DateTime,
    `store_and_fwd_flag` UInt8,
    `rate_code_id` UInt8,
    `pickup_longitude` Float64,
    `pickup_latitude` Float64,
    `dropoff_longitude` Float64,
    `dropoff_latitude` Float64,
    `passenger_count` UInt8,
    `trip_distance` Float64,
    `fare_amount` Float32,
    `extra` Float32,
    `mta_tax` Float32,
    `tip_amount` Float32,
    `tolls_amount` Float32,
    `ehail_fee` Float32,
    `improvement_surcharge` Float32,
    `total_amount` Float32,
    `payment_type` Enum8('UNK' = 0, 'CSH' = 1, 'CRE' = 2, 'NOC' = 3, 'DIS' = 4),
    `trip_type` UInt8,
    `pickup` FixedString(25),
    `dropoff` FixedString(25),
    `cab_type` Enum8('yellow' = 1, 'green' = 2, 'uber' = 3),
    `pickup_nyct2010_gid` Int8,
    `pickup_ctlabel` Float32,
    `pickup_borocode` Int8,
    `pickup_ct2010` String,
    `pickup_boroct2010` String,
    `pickup_cdeligibil` String,
    `pickup_ntacode` FixedString(4),
    `pickup_ntaname` String,
    `pickup_puma` UInt16,
    `dropoff_nyct2010_gid` UInt8,
    `dropoff_ctlabel` Float32,
    `dropoff_borocode` UInt8,
    `dropoff_ct2010` String,
    `dropoff_boroct2010` String,
    `dropoff_cdeligibil` String,
    `dropoff_ntacode` FixedString(4),
    `dropoff_ntaname` String,
    `dropoff_puma` UInt16
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(pickup_date)
ORDER BY pickup_datetime;

```


## Добавьте датасет​

Теперь, когда вы создали таблицу, добавьте данные о такси Нью‑Йорка из CSV‑файлов в S3.Следующая команда вставляет примерно 2 000 000 строк в таблицуtripsиз двух разных файлов в S3:trips_1.tsv.gzиtrips_2.tsv.gz:INSERT INTO trips
SELECT * FROM s3(
    'https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/trips_{1..2}.gz',
    'TabSeparatedWithNames', "
    `trip_id` UInt32,
    `vendor_id` Enum8('1' = 1, '2' = 2, '3' = 3, '4' = 4, 'CMT' = 5, 'VTS' = 6, 'DDS' = 7, 'B02512' = 10, 'B02598' = 11, 'B02617' = 12, 'B02682' = 13, 'B02764' = 14, '' = 15),
    `pickup_date` Date,
    `pickup_datetime` DateTime,
    `dropoff_date` Date,
    `dropoff_datetime` DateTime,
    `store_and_fwd_flag` UInt8,
    `rate_code_id` UInt8,
    `pickup_longitude` Float64,
    `pickup_latitude` Float64,
    `dropoff_longitude` Float64,
    `dropoff_latitude` Float64,
    `passenger_count` UInt8,
    `trip_distance` Float64,
    `fare_amount` Float32,
    `extra` Float32,
    `mta_tax` Float32,
    `tip_amount` Float32,
    `tolls_amount` Float32,
    `ehail_fee` Float32,
    `improvement_surcharge` Float32,
    `total_amount` Float32,
    `payment_type` Enum8('UNK' = 0, 'CSH' = 1, 'CRE' = 2, 'NOC' = 3, 'DIS' = 4),
    `trip_type` UInt8,
    `pickup` FixedString(25),
    `dropoff` FixedString(25),
    `cab_type` Enum8('yellow' = 1, 'green' = 2, 'uber' = 3),
    `pickup_nyct2010_gid` Int8,
    `pickup_ctlabel` Float32,
    `pickup_borocode` Int8,
    `pickup_ct2010` String,
    `pickup_boroct2010` String,
    `pickup_cdeligibil` String,
    `pickup_ntacode` FixedString(4),
    `pickup_ntaname` String,
    `pickup_puma` UInt16,
    `dropoff_nyct2010_gid` UInt8,
    `dropoff_ctlabel` Float32,
    `dropoff_borocode` UInt8,
    `dropoff_ct2010` String,
    `dropoff_boroct2010` String,
    `dropoff_cdeligibil` String,
    `dropoff_ntacode` FixedString(4),
    `dropoff_ntaname` String,
    `dropoff_puma` UInt16
") SETTINGS input_format_try_infer_datetimes = 0Дождитесь завершения выполнения командыINSERT. Загрузка 150 МБ данных может занять некоторое время.После завершения вставки убедитесь, что она прошла успешно:SELECT count() FROM tripsЭтот запрос должен вернуть 1 999 657 строк.

- Следующая команда вставляет примерно 2 000 000 строк в таблицуtripsиз двух разных файлов в S3:trips_1.tsv.gzиtrips_2.tsv.gz:INSERT INTO trips
SELECT * FROM s3(
    'https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/trips_{1..2}.gz',
    'TabSeparatedWithNames', "
    `trip_id` UInt32,
    `vendor_id` Enum8('1' = 1, '2' = 2, '3' = 3, '4' = 4, 'CMT' = 5, 'VTS' = 6, 'DDS' = 7, 'B02512' = 10, 'B02598' = 11, 'B02617' = 12, 'B02682' = 13, 'B02764' = 14, '' = 15),
    `pickup_date` Date,
    `pickup_datetime` DateTime,
    `dropoff_date` Date,
    `dropoff_datetime` DateTime,
    `store_and_fwd_flag` UInt8,
    `rate_code_id` UInt8,
    `pickup_longitude` Float64,
    `pickup_latitude` Float64,
    `dropoff_longitude` Float64,
    `dropoff_latitude` Float64,
    `passenger_count` UInt8,
    `trip_distance` Float64,
    `fare_amount` Float32,
    `extra` Float32,
    `mta_tax` Float32,
    `tip_amount` Float32,
    `tolls_amount` Float32,
    `ehail_fee` Float32,
    `improvement_surcharge` Float32,
    `total_amount` Float32,
    `payment_type` Enum8('UNK' = 0, 'CSH' = 1, 'CRE' = 2, 'NOC' = 3, 'DIS' = 4),
    `trip_type` UInt8,
    `pickup` FixedString(25),
    `dropoff` FixedString(25),
    `cab_type` Enum8('yellow' = 1, 'green' = 2, 'uber' = 3),
    `pickup_nyct2010_gid` Int8,
    `pickup_ctlabel` Float32,
    `pickup_borocode` Int8,
    `pickup_ct2010` String,
    `pickup_boroct2010` String,
    `pickup_cdeligibil` String,
    `pickup_ntacode` FixedString(4),
    `pickup_ntaname` String,
    `pickup_puma` UInt16,
    `dropoff_nyct2010_gid` UInt8,
    `dropoff_ctlabel` Float32,
    `dropoff_borocode` UInt8,
    `dropoff_ct2010` String,
    `dropoff_boroct2010` String,
    `dropoff_cdeligibil` String,
    `dropoff_ntacode` FixedString(4),
    `dropoff_ntaname` String,
    `dropoff_puma` UInt16
") SETTINGS input_format_try_infer_datetimes = 0
Следующая команда вставляет примерно 2 000 000 строк в таблицуtripsиз двух разных файлов в S3:trips_1.tsv.gzиtrips_2.tsv.gz:


```
INSERT INTO trips
SELECT * FROM s3(
    'https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/trips_{1..2}.gz',
    'TabSeparatedWithNames', "
    `trip_id` UInt32,
    `vendor_id` Enum8('1' = 1, '2' = 2, '3' = 3, '4' = 4, 'CMT' = 5, 'VTS' = 6, 'DDS' = 7, 'B02512' = 10, 'B02598' = 11, 'B02617' = 12, 'B02682' = 13, 'B02764' = 14, '' = 15),
    `pickup_date` Date,
    `pickup_datetime` DateTime,
    `dropoff_date` Date,
    `dropoff_datetime` DateTime,
    `store_and_fwd_flag` UInt8,
    `rate_code_id` UInt8,
    `pickup_longitude` Float64,
    `pickup_latitude` Float64,
    `dropoff_longitude` Float64,
    `dropoff_latitude` Float64,
    `passenger_count` UInt8,
    `trip_distance` Float64,
    `fare_amount` Float32,
    `extra` Float32,
    `mta_tax` Float32,
    `tip_amount` Float32,
    `tolls_amount` Float32,
    `ehail_fee` Float32,
    `improvement_surcharge` Float32,
    `total_amount` Float32,
    `payment_type` Enum8('UNK' = 0, 'CSH' = 1, 'CRE' = 2, 'NOC' = 3, 'DIS' = 4),
    `trip_type` UInt8,
    `pickup` FixedString(25),
    `dropoff` FixedString(25),
    `cab_type` Enum8('yellow' = 1, 'green' = 2, 'uber' = 3),
    `pickup_nyct2010_gid` Int8,
    `pickup_ctlabel` Float32,
    `pickup_borocode` Int8,
    `pickup_ct2010` String,
    `pickup_boroct2010` String,
    `pickup_cdeligibil` String,
    `pickup_ntacode` FixedString(4),
    `pickup_ntaname` String,
    `pickup_puma` UInt16,
    `dropoff_nyct2010_gid` UInt8,
    `dropoff_ctlabel` Float32,
    `dropoff_borocode` UInt8,
    `dropoff_ct2010` String,
    `dropoff_boroct2010` String,
    `dropoff_cdeligibil` String,
    `dropoff_ntacode` FixedString(4),
    `dropoff_ntaname` String,
    `dropoff_puma` UInt16
") SETTINGS input_format_try_infer_datetimes = 0

```

- Дождитесь завершения выполнения командыINSERT. Загрузка 150 МБ данных может занять некоторое время.
Дождитесь завершения выполнения командыINSERT. Загрузка 150 МБ данных может занять некоторое время.

- После завершения вставки убедитесь, что она прошла успешно:SELECT count() FROM tripsЭтот запрос должен вернуть 1 999 657 строк.
После завершения вставки убедитесь, что она прошла успешно:


```
SELECT count() FROM trips

```

Этот запрос должен вернуть 1 999 657 строк.


## Анализ данных​

Выполните несколько запросов для анализа данных. Изучите следующие примеры или попробуйте свой собственный SQL-запрос.Рассчитайте среднюю сумму чаевых:SELECT round(avg(tip_amount), 2) FROM tripsОжидаемый результат┌─round(avg(tip_amount), 2)─┐
│                      1.68 │
└───────────────────────────┘Рассчитайте среднюю стоимость поездки в зависимости от количества пассажиров:SELECT
    passenger_count,
    ceil(avg(total_amount),2) AS average_total_amount
FROM trips
GROUP BY passenger_countОжидаемый результатПолеpassenger_countпринимает значения от 0 до 9:┌─passenger_count─┬─average_total_amount─┐
│               0 │                22.69 │
│               1 │                15.97 │
│               2 │                17.15 │
│               3 │                16.76 │
│               4 │                17.33 │
│               5 │                16.35 │
│               6 │                16.04 │
│               7 │                 59.8 │
│               8 │                36.41 │
│               9 │                 9.81 │
└─────────────────┴──────────────────────┘Рассчитайте ежедневное число посадок такси по районам:SELECT
    pickup_date,
    pickup_ntaname,
    SUM(1) AS number_of_trips
FROM trips
GROUP BY pickup_date, pickup_ntaname
ORDER BY pickup_date ASCОжидаемый результат┌─pickup_date─┬─pickup_ntaname───────────────────────────────────────────┬─number_of_trips─┐
│  2015-07-01 │ Brooklyn Heights-Cobble Hill                             │              13 │
│  2015-07-01 │ Old Astoria                                              │               5 │
│  2015-07-01 │ Flushing                                                 │               1 │
│  2015-07-01 │ Yorkville                                                │             378 │
│  2015-07-01 │ Gramercy                                                 │             344 │
│  2015-07-01 │ Fordham South                                            │               2 │
│  2015-07-01 │ SoHo-TriBeCa-Civic Center-Little Italy                   │             621 │
│  2015-07-01 │ Park Slope-Gowanus                                       │              29 │
│  2015-07-01 │ Bushwick South                                           │               5 │Вычислите продолжительность каждой поездки в минутах, затем сгруппируйте результаты по длительности поездки:SELECT
    avg(tip_amount) AS avg_tip,
    avg(fare_amount) AS avg_fare,
    avg(passenger_count) AS avg_passenger,
    count() AS count,
    truncate(date_diff('second', pickup_datetime, dropoff_datetime)/60) as trip_minutes
FROM trips
WHERE trip_minutes > 0
GROUP BY trip_minutes
ORDER BY trip_minutes DESCОжидаемый результат┌──────────────avg_tip─┬───────────avg_fare─┬──────avg_passenger─┬──count─┬─trip_minutes─┐
│   1.9600000381469727 │                  8 │                  1 │      1 │        27511 │
│                    0 │                 12 │                  2 │      1 │        27500 │
│    0.542166673981895 │ 19.716666666666665 │ 1.9166666666666667 │     60 │         1439 │
│    0.902499997522682 │ 11.270625001192093 │            1.95625 │    160 │         1438 │
│   0.9715789457909146 │ 13.646616541353383 │ 2.0526315789473686 │    133 │         1437 │
│   0.9682692398245518 │ 14.134615384615385 │  2.076923076923077 │    104 │         1436 │
│   1.1022105210705808 │ 13.778947368421052 │  2.042105263157895 │     95 │         1435 │Выведите количество посадок такси в каждом районе с разбивкой по часам суток:SELECT
    pickup_ntaname,
    toHour(pickup_datetime) as pickup_hour,
    SUM(1) AS pickups
FROM trips
WHERE pickup_ntaname != ''
GROUP BY pickup_ntaname, pickup_hour
ORDER BY pickup_ntaname, pickup_hourОжидаемый результат┌─pickup_ntaname───────────────────────────────────────────┬─pickup_hour─┬─pickups─┐
│ Airport                                                  │           0 │    3509 │
│ Airport                                                  │           1 │    1184 │
│ Airport                                                  │           2 │     401 │
│ Airport                                                  │           3 │     152 │
│ Airport                                                  │           4 │     213 │
│ Airport                                                  │           5 │     955 │
│ Airport                                                  │           6 │    2161 │
│ Airport                                                  │           7 │    3013 │
│ Airport                                                  │           8 │    3601 │
│ Airport                                                  │           9 │    3792 │
│ Airport                                                  │          10 │    4546 │
│ Airport                                                  │          11 │    4659 │
│ Airport                                                  │          12 │    4621 │
│ Airport                                                  │          13 │    5348 │
│ Airport                                                  │          14 │    5889 │
│ Airport                                                  │          15 │    6505 │
│ Airport                                                  │          16 │    6119 │
│ Airport                                                  │          17 │    6341 │
│ Airport                                                  │          18 │    6173 │
│ Airport                                                  │          19 │    6329 │
│ Airport                                                  │          20 │    6271 │
│ Airport                                                  │          21 │    6649 │
│ Airport                                                  │          22 │    6356 │
│ Airport                                                  │          23 │    6016 │
│ Allerton-Pelham Gardens                                  │           4 │       1 │
│ Allerton-Pelham Gardens                                  │           6 │       1 │
│ Allerton-Pelham Gardens                                  │           7 │       1 │
│ Allerton-Pelham Gardens                                  │           9 │       5 │
│ Allerton-Pelham Gardens                                  │          10 │       3 │
│ Allerton-Pelham Gardens                                  │          15 │       1 │
│ Allerton-Pelham Gardens                                  │          20 │       2 │
│ Allerton-Pelham Gardens                                  │          23 │       1 │
│ Annadale-Huguenot-Prince's Bay-Eltingville               │          23 │       1 │
│ Arden Heights                                            │          11 │       1 │Извлеките  записи о поездках в аэропорты Ла‑Гуардия или JFK:SELECT
    pickup_datetime,
    dropoff_datetime,
    total_amount,
    pickup_nyct2010_gid,
    dropoff_nyct2010_gid,
    CASE
        WHEN dropoff_nyct2010_gid = 138 THEN 'LGA'
        WHEN dropoff_nyct2010_gid = 132 THEN 'JFK'
    END AS airport_code,
    EXTRACT(YEAR FROM pickup_datetime) AS year,
    EXTRACT(DAY FROM pickup_datetime) AS day,
    EXTRACT(HOUR FROM pickup_datetime) AS hour
FROM trips
WHERE dropoff_nyct2010_gid IN (132, 138)
ORDER BY pickup_datetimeОжидаемый результат┌─────pickup_datetime─┬────dropoff_datetime─┬─total_amount─┬─pickup_nyct2010_gid─┬─dropoff_nyct2010_gid─┬─airport_code─┬─year─┬─day─┬─hour─┐
│ 2015-07-01 00:04:14 │ 2015-07-01 00:15:29 │         13.3 │                 -34 │                  132 │ JFK          │ 2015 │   1 │    0 │
│ 2015-07-01 00:09:42 │ 2015-07-01 00:12:55 │          6.8 │                  50 │                  138 │ LGA          │ 2015 │   1 │    0 │
│ 2015-07-01 00:23:04 │ 2015-07-01 00:24:39 │          4.8 │                -125 │                  132 │ JFK          │ 2015 │   1 │    0 │
│ 2015-07-01 00:27:51 │ 2015-07-01 00:39:02 │        14.72 │                -101 │                  138 │ LGA          │ 2015 │   1 │    0 │
│ 2015-07-01 00:32:03 │ 2015-07-01 00:55:39 │        39.34 │                  48 │                  138 │ LGA          │ 2015 │   1 │    0 │
│ 2015-07-01 00:34:12 │ 2015-07-01 00:40:48 │         9.95 │                 -93 │                  132 │ JFK          │ 2015 │   1 │    0 │
│ 2015-07-01 00:38:26 │ 2015-07-01 00:49:00 │         13.3 │                 -11 │                  138 │ LGA          │ 2015 │   1 │    0 │
│ 2015-07-01 00:41:48 │ 2015-07-01 00:44:45 │          6.3 │                 -94 │                  132 │ JFK          │ 2015 │   1 │    0 │
│ 2015-07-01 01:06:18 │ 2015-07-01 01:14:43 │        11.76 │                  37 │                  132 │ JFK          │ 2015 │   1 │    1 │

- Рассчитайте среднюю сумму чаевых:SELECT round(avg(tip_amount), 2) FROM tripsОжидаемый результат┌─round(avg(tip_amount), 2)─┐
│                      1.68 │
└───────────────────────────┘
Рассчитайте среднюю сумму чаевых:


```
SELECT round(avg(tip_amount), 2) FROM trips

```

┌─round(avg(tip_amount), 2)─┐
│                      1.68 │
└───────────────────────────┘


```
┌─round(avg(tip_amount), 2)─┐
│                      1.68 │
└───────────────────────────┘

```

- Рассчитайте среднюю стоимость поездки в зависимости от количества пассажиров:SELECT
    passenger_count,
    ceil(avg(total_amount),2) AS average_total_amount
FROM trips
GROUP BY passenger_countОжидаемый результатПолеpassenger_countпринимает значения от 0 до 9:┌─passenger_count─┬─average_total_amount─┐
│               0 │                22.69 │
│               1 │                15.97 │
│               2 │                17.15 │
│               3 │                16.76 │
│               4 │                17.33 │
│               5 │                16.35 │
│               6 │                16.04 │
│               7 │                 59.8 │
│               8 │                36.41 │
│               9 │                 9.81 │
└─────────────────┴──────────────────────┘
Рассчитайте среднюю стоимость поездки в зависимости от количества пассажиров:


```
SELECT
    passenger_count,
    ceil(avg(total_amount),2) AS average_total_amount
FROM trips
GROUP BY passenger_count

```

Полеpassenger_countпринимает значения от 0 до 9:┌─passenger_count─┬─average_total_amount─┐
│               0 │                22.69 │
│               1 │                15.97 │
│               2 │                17.15 │
│               3 │                16.76 │
│               4 │                17.33 │
│               5 │                16.35 │
│               6 │                16.04 │
│               7 │                 59.8 │
│               8 │                36.41 │
│               9 │                 9.81 │
└─────────────────┴──────────────────────┘

Полеpassenger_countпринимает значения от 0 до 9:┌─passenger_count─┬─average_total_amount─┐
│               0 │                22.69 │
│               1 │                15.97 │
│               2 │                17.15 │
│               3 │                16.76 │
│               4 │                17.33 │
│               5 │                16.35 │
│               6 │                16.04 │
│               7 │                 59.8 │
│               8 │                36.41 │
│               9 │                 9.81 │
└─────────────────┴──────────────────────┘


```
┌─passenger_count─┬─average_total_amount─┐
│               0 │                22.69 │
│               1 │                15.97 │
│               2 │                17.15 │
│               3 │                16.76 │
│               4 │                17.33 │
│               5 │                16.35 │
│               6 │                16.04 │
│               7 │                 59.8 │
│               8 │                36.41 │
│               9 │                 9.81 │
└─────────────────┴──────────────────────┘

```

- Рассчитайте ежедневное число посадок такси по районам:SELECT
    pickup_date,
    pickup_ntaname,
    SUM(1) AS number_of_trips
FROM trips
GROUP BY pickup_date, pickup_ntaname
ORDER BY pickup_date ASCОжидаемый результат┌─pickup_date─┬─pickup_ntaname───────────────────────────────────────────┬─number_of_trips─┐
│  2015-07-01 │ Brooklyn Heights-Cobble Hill                             │              13 │
│  2015-07-01 │ Old Astoria                                              │               5 │
│  2015-07-01 │ Flushing                                                 │               1 │
│  2015-07-01 │ Yorkville                                                │             378 │
│  2015-07-01 │ Gramercy                                                 │             344 │
│  2015-07-01 │ Fordham South                                            │               2 │
│  2015-07-01 │ SoHo-TriBeCa-Civic Center-Little Italy                   │             621 │
│  2015-07-01 │ Park Slope-Gowanus                                       │              29 │
│  2015-07-01 │ Bushwick South                                           │               5 │
Рассчитайте ежедневное число посадок такси по районам:


```
SELECT
    pickup_date,
    pickup_ntaname,
    SUM(1) AS number_of_trips
FROM trips
GROUP BY pickup_date, pickup_ntaname
ORDER BY pickup_date ASC

```

┌─pickup_date─┬─pickup_ntaname───────────────────────────────────────────┬─number_of_trips─┐
│  2015-07-01 │ Brooklyn Heights-Cobble Hill                             │              13 │
│  2015-07-01 │ Old Astoria                                              │               5 │
│  2015-07-01 │ Flushing                                                 │               1 │
│  2015-07-01 │ Yorkville                                                │             378 │
│  2015-07-01 │ Gramercy                                                 │             344 │
│  2015-07-01 │ Fordham South                                            │               2 │
│  2015-07-01 │ SoHo-TriBeCa-Civic Center-Little Italy                   │             621 │
│  2015-07-01 │ Park Slope-Gowanus                                       │              29 │
│  2015-07-01 │ Bushwick South                                           │               5 │


```
┌─pickup_date─┬─pickup_ntaname───────────────────────────────────────────┬─number_of_trips─┐
│  2015-07-01 │ Brooklyn Heights-Cobble Hill                             │              13 │
│  2015-07-01 │ Old Astoria                                              │               5 │
│  2015-07-01 │ Flushing                                                 │               1 │
│  2015-07-01 │ Yorkville                                                │             378 │
│  2015-07-01 │ Gramercy                                                 │             344 │
│  2015-07-01 │ Fordham South                                            │               2 │
│  2015-07-01 │ SoHo-TriBeCa-Civic Center-Little Italy                   │             621 │
│  2015-07-01 │ Park Slope-Gowanus                                       │              29 │
│  2015-07-01 │ Bushwick South                                           │               5 │

```

- Вычислите продолжительность каждой поездки в минутах, затем сгруппируйте результаты по длительности поездки:SELECT
    avg(tip_amount) AS avg_tip,
    avg(fare_amount) AS avg_fare,
    avg(passenger_count) AS avg_passenger,
    count() AS count,
    truncate(date_diff('second', pickup_datetime, dropoff_datetime)/60) as trip_minutes
FROM trips
WHERE trip_minutes > 0
GROUP BY trip_minutes
ORDER BY trip_minutes DESCОжидаемый результат┌──────────────avg_tip─┬───────────avg_fare─┬──────avg_passenger─┬──count─┬─trip_minutes─┐
│   1.9600000381469727 │                  8 │                  1 │      1 │        27511 │
│                    0 │                 12 │                  2 │      1 │        27500 │
│    0.542166673981895 │ 19.716666666666665 │ 1.9166666666666667 │     60 │         1439 │
│    0.902499997522682 │ 11.270625001192093 │            1.95625 │    160 │         1438 │
│   0.9715789457909146 │ 13.646616541353383 │ 2.0526315789473686 │    133 │         1437 │
│   0.9682692398245518 │ 14.134615384615385 │  2.076923076923077 │    104 │         1436 │
│   1.1022105210705808 │ 13.778947368421052 │  2.042105263157895 │     95 │         1435 │
Вычислите продолжительность каждой поездки в минутах, затем сгруппируйте результаты по длительности поездки:


```
SELECT
    avg(tip_amount) AS avg_tip,
    avg(fare_amount) AS avg_fare,
    avg(passenger_count) AS avg_passenger,
    count() AS count,
    truncate(date_diff('second', pickup_datetime, dropoff_datetime)/60) as trip_minutes
FROM trips
WHERE trip_minutes > 0
GROUP BY trip_minutes
ORDER BY trip_minutes DESC

```

┌──────────────avg_tip─┬───────────avg_fare─┬──────avg_passenger─┬──count─┬─trip_minutes─┐
│   1.9600000381469727 │                  8 │                  1 │      1 │        27511 │
│                    0 │                 12 │                  2 │      1 │        27500 │
│    0.542166673981895 │ 19.716666666666665 │ 1.9166666666666667 │     60 │         1439 │
│    0.902499997522682 │ 11.270625001192093 │            1.95625 │    160 │         1438 │
│   0.9715789457909146 │ 13.646616541353383 │ 2.0526315789473686 │    133 │         1437 │
│   0.9682692398245518 │ 14.134615384615385 │  2.076923076923077 │    104 │         1436 │
│   1.1022105210705808 │ 13.778947368421052 │  2.042105263157895 │     95 │         1435 │


```
┌──────────────avg_tip─┬───────────avg_fare─┬──────avg_passenger─┬──count─┬─trip_minutes─┐
│   1.9600000381469727 │                  8 │                  1 │      1 │        27511 │
│                    0 │                 12 │                  2 │      1 │        27500 │
│    0.542166673981895 │ 19.716666666666665 │ 1.9166666666666667 │     60 │         1439 │
│    0.902499997522682 │ 11.270625001192093 │            1.95625 │    160 │         1438 │
│   0.9715789457909146 │ 13.646616541353383 │ 2.0526315789473686 │    133 │         1437 │
│   0.9682692398245518 │ 14.134615384615385 │  2.076923076923077 │    104 │         1436 │
│   1.1022105210705808 │ 13.778947368421052 │  2.042105263157895 │     95 │         1435 │

```

- Выведите количество посадок такси в каждом районе с разбивкой по часам суток:SELECT
    pickup_ntaname,
    toHour(pickup_datetime) as pickup_hour,
    SUM(1) AS pickups
FROM trips
WHERE pickup_ntaname != ''
GROUP BY pickup_ntaname, pickup_hour
ORDER BY pickup_ntaname, pickup_hourОжидаемый результат┌─pickup_ntaname───────────────────────────────────────────┬─pickup_hour─┬─pickups─┐
│ Airport                                                  │           0 │    3509 │
│ Airport                                                  │           1 │    1184 │
│ Airport                                                  │           2 │     401 │
│ Airport                                                  │           3 │     152 │
│ Airport                                                  │           4 │     213 │
│ Airport                                                  │           5 │     955 │
│ Airport                                                  │           6 │    2161 │
│ Airport                                                  │           7 │    3013 │
│ Airport                                                  │           8 │    3601 │
│ Airport                                                  │           9 │    3792 │
│ Airport                                                  │          10 │    4546 │
│ Airport                                                  │          11 │    4659 │
│ Airport                                                  │          12 │    4621 │
│ Airport                                                  │          13 │    5348 │
│ Airport                                                  │          14 │    5889 │
│ Airport                                                  │          15 │    6505 │
│ Airport                                                  │          16 │    6119 │
│ Airport                                                  │          17 │    6341 │
│ Airport                                                  │          18 │    6173 │
│ Airport                                                  │          19 │    6329 │
│ Airport                                                  │          20 │    6271 │
│ Airport                                                  │          21 │    6649 │
│ Airport                                                  │          22 │    6356 │
│ Airport                                                  │          23 │    6016 │
│ Allerton-Pelham Gardens                                  │           4 │       1 │
│ Allerton-Pelham Gardens                                  │           6 │       1 │
│ Allerton-Pelham Gardens                                  │           7 │       1 │
│ Allerton-Pelham Gardens                                  │           9 │       5 │
│ Allerton-Pelham Gardens                                  │          10 │       3 │
│ Allerton-Pelham Gardens                                  │          15 │       1 │
│ Allerton-Pelham Gardens                                  │          20 │       2 │
│ Allerton-Pelham Gardens                                  │          23 │       1 │
│ Annadale-Huguenot-Prince's Bay-Eltingville               │          23 │       1 │
│ Arden Heights                                            │          11 │       1 │
Выведите количество посадок такси в каждом районе с разбивкой по часам суток:


```
SELECT
    pickup_ntaname,
    toHour(pickup_datetime) as pickup_hour,
    SUM(1) AS pickups
FROM trips
WHERE pickup_ntaname != ''
GROUP BY pickup_ntaname, pickup_hour
ORDER BY pickup_ntaname, pickup_hour

```

┌─pickup_ntaname───────────────────────────────────────────┬─pickup_hour─┬─pickups─┐
│ Airport                                                  │           0 │    3509 │
│ Airport                                                  │           1 │    1184 │
│ Airport                                                  │           2 │     401 │
│ Airport                                                  │           3 │     152 │
│ Airport                                                  │           4 │     213 │
│ Airport                                                  │           5 │     955 │
│ Airport                                                  │           6 │    2161 │
│ Airport                                                  │           7 │    3013 │
│ Airport                                                  │           8 │    3601 │
│ Airport                                                  │           9 │    3792 │
│ Airport                                                  │          10 │    4546 │
│ Airport                                                  │          11 │    4659 │
│ Airport                                                  │          12 │    4621 │
│ Airport                                                  │          13 │    5348 │
│ Airport                                                  │          14 │    5889 │
│ Airport                                                  │          15 │    6505 │
│ Airport                                                  │          16 │    6119 │
│ Airport                                                  │          17 │    6341 │
│ Airport                                                  │          18 │    6173 │
│ Airport                                                  │          19 │    6329 │
│ Airport                                                  │          20 │    6271 │
│ Airport                                                  │          21 │    6649 │
│ Airport                                                  │          22 │    6356 │
│ Airport                                                  │          23 │    6016 │
│ Allerton-Pelham Gardens                                  │           4 │       1 │
│ Allerton-Pelham Gardens                                  │           6 │       1 │
│ Allerton-Pelham Gardens                                  │           7 │       1 │
│ Allerton-Pelham Gardens                                  │           9 │       5 │
│ Allerton-Pelham Gardens                                  │          10 │       3 │
│ Allerton-Pelham Gardens                                  │          15 │       1 │
│ Allerton-Pelham Gardens                                  │          20 │       2 │
│ Allerton-Pelham Gardens                                  │          23 │       1 │
│ Annadale-Huguenot-Prince's Bay-Eltingville               │          23 │       1 │
│ Arden Heights                                            │          11 │       1 │


```
┌─pickup_ntaname───────────────────────────────────────────┬─pickup_hour─┬─pickups─┐
│ Airport                                                  │           0 │    3509 │
│ Airport                                                  │           1 │    1184 │
│ Airport                                                  │           2 │     401 │
│ Airport                                                  │           3 │     152 │
│ Airport                                                  │           4 │     213 │
│ Airport                                                  │           5 │     955 │
│ Airport                                                  │           6 │    2161 │
│ Airport                                                  │           7 │    3013 │
│ Airport                                                  │           8 │    3601 │
│ Airport                                                  │           9 │    3792 │
│ Airport                                                  │          10 │    4546 │
│ Airport                                                  │          11 │    4659 │
│ Airport                                                  │          12 │    4621 │
│ Airport                                                  │          13 │    5348 │
│ Airport                                                  │          14 │    5889 │
│ Airport                                                  │          15 │    6505 │
│ Airport                                                  │          16 │    6119 │
│ Airport                                                  │          17 │    6341 │
│ Airport                                                  │          18 │    6173 │
│ Airport                                                  │          19 │    6329 │
│ Airport                                                  │          20 │    6271 │
│ Airport                                                  │          21 │    6649 │
│ Airport                                                  │          22 │    6356 │
│ Airport                                                  │          23 │    6016 │
│ Allerton-Pelham Gardens                                  │           4 │       1 │
│ Allerton-Pelham Gardens                                  │           6 │       1 │
│ Allerton-Pelham Gardens                                  │           7 │       1 │
│ Allerton-Pelham Gardens                                  │           9 │       5 │
│ Allerton-Pelham Gardens                                  │          10 │       3 │
│ Allerton-Pelham Gardens                                  │          15 │       1 │
│ Allerton-Pelham Gardens                                  │          20 │       2 │
│ Allerton-Pelham Gardens                                  │          23 │       1 │
│ Annadale-Huguenot-Prince's Bay-Eltingville               │          23 │       1 │
│ Arden Heights                                            │          11 │       1 │

```

- Извлеките  записи о поездках в аэропорты Ла‑Гуардия или JFK:SELECT
    pickup_datetime,
    dropoff_datetime,
    total_amount,
    pickup_nyct2010_gid,
    dropoff_nyct2010_gid,
    CASE
        WHEN dropoff_nyct2010_gid = 138 THEN 'LGA'
        WHEN dropoff_nyct2010_gid = 132 THEN 'JFK'
    END AS airport_code,
    EXTRACT(YEAR FROM pickup_datetime) AS year,
    EXTRACT(DAY FROM pickup_datetime) AS day,
    EXTRACT(HOUR FROM pickup_datetime) AS hour
FROM trips
WHERE dropoff_nyct2010_gid IN (132, 138)
ORDER BY pickup_datetimeОжидаемый результат┌─────pickup_datetime─┬────dropoff_datetime─┬─total_amount─┬─pickup_nyct2010_gid─┬─dropoff_nyct2010_gid─┬─airport_code─┬─year─┬─day─┬─hour─┐
│ 2015-07-01 00:04:14 │ 2015-07-01 00:15:29 │         13.3 │                 -34 │                  132 │ JFK          │ 2015 │   1 │    0 │
│ 2015-07-01 00:09:42 │ 2015-07-01 00:12:55 │          6.8 │                  50 │                  138 │ LGA          │ 2015 │   1 │    0 │
│ 2015-07-01 00:23:04 │ 2015-07-01 00:24:39 │          4.8 │                -125 │                  132 │ JFK          │ 2015 │   1 │    0 │
│ 2015-07-01 00:27:51 │ 2015-07-01 00:39:02 │        14.72 │                -101 │                  138 │ LGA          │ 2015 │   1 │    0 │
│ 2015-07-01 00:32:03 │ 2015-07-01 00:55:39 │        39.34 │                  48 │                  138 │ LGA          │ 2015 │   1 │    0 │
│ 2015-07-01 00:34:12 │ 2015-07-01 00:40:48 │         9.95 │                 -93 │                  132 │ JFK          │ 2015 │   1 │    0 │
│ 2015-07-01 00:38:26 │ 2015-07-01 00:49:00 │         13.3 │                 -11 │                  138 │ LGA          │ 2015 │   1 │    0 │
│ 2015-07-01 00:41:48 │ 2015-07-01 00:44:45 │          6.3 │                 -94 │                  132 │ JFK          │ 2015 │   1 │    0 │
│ 2015-07-01 01:06:18 │ 2015-07-01 01:14:43 │        11.76 │                  37 │                  132 │ JFK          │ 2015 │   1 │    1 │
Извлеките  записи о поездках в аэропорты Ла‑Гуардия или JFK:


```
SELECT
    pickup_datetime,
    dropoff_datetime,
    total_amount,
    pickup_nyct2010_gid,
    dropoff_nyct2010_gid,
    CASE
        WHEN dropoff_nyct2010_gid = 138 THEN 'LGA'
        WHEN dropoff_nyct2010_gid = 132 THEN 'JFK'
    END AS airport_code,
    EXTRACT(YEAR FROM pickup_datetime) AS year,
    EXTRACT(DAY FROM pickup_datetime) AS day,
    EXTRACT(HOUR FROM pickup_datetime) AS hour
FROM trips
WHERE dropoff_nyct2010_gid IN (132, 138)
ORDER BY pickup_datetime

```

┌─────pickup_datetime─┬────dropoff_datetime─┬─total_amount─┬─pickup_nyct2010_gid─┬─dropoff_nyct2010_gid─┬─airport_code─┬─year─┬─day─┬─hour─┐
│ 2015-07-01 00:04:14 │ 2015-07-01 00:15:29 │         13.3 │                 -34 │                  132 │ JFK          │ 2015 │   1 │    0 │
│ 2015-07-01 00:09:42 │ 2015-07-01 00:12:55 │          6.8 │                  50 │                  138 │ LGA          │ 2015 │   1 │    0 │
│ 2015-07-01 00:23:04 │ 2015-07-01 00:24:39 │          4.8 │                -125 │                  132 │ JFK          │ 2015 │   1 │    0 │
│ 2015-07-01 00:27:51 │ 2015-07-01 00:39:02 │        14.72 │                -101 │                  138 │ LGA          │ 2015 │   1 │    0 │
│ 2015-07-01 00:32:03 │ 2015-07-01 00:55:39 │        39.34 │                  48 │                  138 │ LGA          │ 2015 │   1 │    0 │
│ 2015-07-01 00:34:12 │ 2015-07-01 00:40:48 │         9.95 │                 -93 │                  132 │ JFK          │ 2015 │   1 │    0 │
│ 2015-07-01 00:38:26 │ 2015-07-01 00:49:00 │         13.3 │                 -11 │                  138 │ LGA          │ 2015 │   1 │    0 │
│ 2015-07-01 00:41:48 │ 2015-07-01 00:44:45 │          6.3 │                 -94 │                  132 │ JFK          │ 2015 │   1 │    0 │
│ 2015-07-01 01:06:18 │ 2015-07-01 01:14:43 │        11.76 │                  37 │                  132 │ JFK          │ 2015 │   1 │    1 │


```
┌─────pickup_datetime─┬────dropoff_datetime─┬─total_amount─┬─pickup_nyct2010_gid─┬─dropoff_nyct2010_gid─┬─airport_code─┬─year─┬─day─┬─hour─┐
│ 2015-07-01 00:04:14 │ 2015-07-01 00:15:29 │         13.3 │                 -34 │                  132 │ JFK          │ 2015 │   1 │    0 │
│ 2015-07-01 00:09:42 │ 2015-07-01 00:12:55 │          6.8 │                  50 │                  138 │ LGA          │ 2015 │   1 │    0 │
│ 2015-07-01 00:23:04 │ 2015-07-01 00:24:39 │          4.8 │                -125 │                  132 │ JFK          │ 2015 │   1 │    0 │
│ 2015-07-01 00:27:51 │ 2015-07-01 00:39:02 │        14.72 │                -101 │                  138 │ LGA          │ 2015 │   1 │    0 │
│ 2015-07-01 00:32:03 │ 2015-07-01 00:55:39 │        39.34 │                  48 │                  138 │ LGA          │ 2015 │   1 │    0 │
│ 2015-07-01 00:34:12 │ 2015-07-01 00:40:48 │         9.95 │                 -93 │                  132 │ JFK          │ 2015 │   1 │    0 │
│ 2015-07-01 00:38:26 │ 2015-07-01 00:49:00 │         13.3 │                 -11 │                  138 │ LGA          │ 2015 │   1 │    0 │
│ 2015-07-01 00:41:48 │ 2015-07-01 00:44:45 │          6.3 │                 -94 │                  132 │ JFK          │ 2015 │   1 │    0 │
│ 2015-07-01 01:06:18 │ 2015-07-01 01:14:43 │        11.76 │                  37 │                  132 │ JFK          │ 2015 │   1 │    1 │

```


## Создайте словарь​

Словарь — это хранящееся в памяти отображение пар ключ-значение. Подробности см. в разделеСловариСоздайте словарь, связанный с таблицей в вашем сервисе ClickHouse.
Таблица и словарь основаны на CSV-файле, который содержит строку для каждого района Нью-Йорка.Районы сопоставлены с названиями пяти районов (боро) Нью‑Йорка (Бронкс, Бруклин, Манхэттен, Куинс и Статен‑Айленд), а также с аэропортом Ньюарк (EWR).Вот фрагмент используемого CSV-файла в табличном формате. СтолбецLocationIDв файле соответствует столбцамpickup_nyct2010_gidиdropoff_nyct2010_gidв таблицеtrips:LocationIDBoroughZoneservice_zone1EWRNewark AirportEWR2QueensJamaica BayBoro Zone3BronxAllerton/Pelham GardensBoro Zone4ManhattanAlphabet CityYellow Zone5Staten IslandArden HeightsBoro ZoneВыполните следующий SQL‑запрос, который создаёт словарь с именемtaxi_zone_dictionaryи заполняет его данными из CSV‑файла в S3. URL файла:https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/taxi_zone_lookup.csv.CREATE DICTIONARY taxi_zone_dictionary
(
  `LocationID` UInt16 DEFAULT 0,
  `Borough` String,
  `Zone` String,
  `service_zone` String
)
PRIMARY KEY LocationID
SOURCE(HTTP(URL 'https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/taxi_zone_lookup.csv' FORMAT 'CSVWithNames'))
LIFETIME(MIN 0 MAX 0)
LAYOUT(HASHED_ARRAY())ПримечаниеУстановкаLIFETIMEв 0 отключает автоматические обновления, чтобы избежать ненужного трафика к нашему S3 бакету. В других случаях вы можете настроить это по‑другому. Подробности см. в разделеОбновление данных словаря с помощью LIFETIME.Убедитесь, что всё работает. Следующий запрос должен вернуть 265 строк — по одной для каждого района:SELECT * FROM taxi_zone_dictionaryИспользуйте функциюdictGet(или её варианты), чтобы извлечь значение из словаря. Вы передаёте имя словаря, значение, которое нужно получить, и ключ (в нашем примере это столбецLocationIDсловаряtaxi_zone_dictionary).Например, следующий запрос возвращаетBorough, для которогоLocationIDравен 132, что соответствует аэропорту JFK):SELECT dictGet('taxi_zone_dictionary', 'Borough', 132)JFK находится в Куинсе. Обратите внимание, что время выборки значения практически равно 0:┌─dictGet('taxi_zone_dictionary', 'Borough', 132)─┐
│ Queens                                          │
└─────────────────────────────────────────────────┘

1 rows in set. Elapsed: 0.004 sec.Используйте функциюdictHas, чтобы проверить, присутствует ли ключ в словаре. Например, следующий запрос возвращает1(что соответствует значению "true" в ClickHouse):SELECT dictHas('taxi_zone_dictionary', 132)Следующий запрос вернёт 0, потому что 4567 не является значениемLocationIDв словаре:SELECT dictHas('taxi_zone_dictionary', 4567)Используйте функциюdictGet, чтобы получить название боро в запросе. Например:SELECT
    count(1) AS total,
    dictGetOrDefault('taxi_zone_dictionary','Borough', toUInt64(pickup_nyct2010_gid), 'Unknown') AS borough_name
FROM trips
WHERE dropoff_nyct2010_gid = 132 OR dropoff_nyct2010_gid = 138
GROUP BY borough_name
ORDER BY total DESCЭтот запрос подсчитывает общее количество поездок на такси по районам для поездок, которые заканчиваются либо в аэропорту LaGuardia, либо в аэропорту JFK. Результат выглядит следующим образом — обратите внимание, что есть довольно много поездок с неизвестным районом отправления:┌─total─┬─borough_name──┐
│ 23683 │ Unknown       │
│  7053 │ Manhattan     │
│  6828 │ Brooklyn      │
│  4458 │ Queens        │
│  2670 │ Bronx         │
│   554 │ Staten Island │
│    53 │ EWR           │
└───────┴───────────────┘

7 rows in set. Elapsed: 0.019 sec. Processed 2.00 million rows, 4.00 MB (105.70 million rows/s., 211.40 MB/s.)

Создайте словарь, связанный с таблицей в вашем сервисе ClickHouse.
Таблица и словарь основаны на CSV-файле, который содержит строку для каждого района Нью-Йорка.Районы сопоставлены с названиями пяти районов (боро) Нью‑Йорка (Бронкс, Бруклин, Манхэттен, Куинс и Статен‑Айленд), а также с аэропортом Ньюарк (EWR).Вот фрагмент используемого CSV-файла в табличном формате. СтолбецLocationIDв файле соответствует столбцамpickup_nyct2010_gidиdropoff_nyct2010_gidв таблицеtrips:LocationIDBoroughZoneservice_zone1EWRNewark AirportEWR2QueensJamaica BayBoro Zone3BronxAllerton/Pelham GardensBoro Zone4ManhattanAlphabet CityYellow Zone5Staten IslandArden HeightsBoro ZoneВыполните следующий SQL‑запрос, который создаёт словарь с именемtaxi_zone_dictionaryи заполняет его данными из CSV‑файла в S3. URL файла:https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/taxi_zone_lookup.csv.CREATE DICTIONARY taxi_zone_dictionary
(
  `LocationID` UInt16 DEFAULT 0,
  `Borough` String,
  `Zone` String,
  `service_zone` String
)
PRIMARY KEY LocationID
SOURCE(HTTP(URL 'https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/taxi_zone_lookup.csv' FORMAT 'CSVWithNames'))
LIFETIME(MIN 0 MAX 0)
LAYOUT(HASHED_ARRAY())ПримечаниеУстановкаLIFETIMEв 0 отключает автоматические обновления, чтобы избежать ненужного трафика к нашему S3 бакету. В других случаях вы можете настроить это по‑другому. Подробности см. в разделеОбновление данных словаря с помощью LIFETIME.Убедитесь, что всё работает. Следующий запрос должен вернуть 265 строк — по одной для каждого района:SELECT * FROM taxi_zone_dictionaryИспользуйте функциюdictGet(или её варианты), чтобы извлечь значение из словаря. Вы передаёте имя словаря, значение, которое нужно получить, и ключ (в нашем примере это столбецLocationIDсловаряtaxi_zone_dictionary).Например, следующий запрос возвращаетBorough, для которогоLocationIDравен 132, что соответствует аэропорту JFK):SELECT dictGet('taxi_zone_dictionary', 'Borough', 132)JFK находится в Куинсе. Обратите внимание, что время выборки значения практически равно 0:┌─dictGet('taxi_zone_dictionary', 'Borough', 132)─┐
│ Queens                                          │
└─────────────────────────────────────────────────┘

1 rows in set. Elapsed: 0.004 sec.Используйте функциюdictHas, чтобы проверить, присутствует ли ключ в словаре. Например, следующий запрос возвращает1(что соответствует значению "true" в ClickHouse):SELECT dictHas('taxi_zone_dictionary', 132)Следующий запрос вернёт 0, потому что 4567 не является значениемLocationIDв словаре:SELECT dictHas('taxi_zone_dictionary', 4567)Используйте функциюdictGet, чтобы получить название боро в запросе. Например:SELECT
    count(1) AS total,
    dictGetOrDefault('taxi_zone_dictionary','Borough', toUInt64(pickup_nyct2010_gid), 'Unknown') AS borough_name
FROM trips
WHERE dropoff_nyct2010_gid = 132 OR dropoff_nyct2010_gid = 138
GROUP BY borough_name
ORDER BY total DESCЭтот запрос подсчитывает общее количество поездок на такси по районам для поездок, которые заканчиваются либо в аэропорту LaGuardia, либо в аэропорту JFK. Результат выглядит следующим образом — обратите внимание, что есть довольно много поездок с неизвестным районом отправления:┌─total─┬─borough_name──┐
│ 23683 │ Unknown       │
│  7053 │ Manhattan     │
│  6828 │ Brooklyn      │
│  4458 │ Queens        │
│  2670 │ Bronx         │
│   554 │ Staten Island │
│    53 │ EWR           │
└───────┴───────────────┘

7 rows in set. Elapsed: 0.019 sec. Processed 2.00 million rows, 4.00 MB (105.70 million rows/s., 211.40 MB/s.)

Районы сопоставлены с названиями пяти районов (боро) Нью‑Йорка (Бронкс, Бруклин, Манхэттен, Куинс и Статен‑Айленд), а также с аэропортом Ньюарк (EWR).Вот фрагмент используемого CSV-файла в табличном формате. СтолбецLocationIDв файле соответствует столбцамpickup_nyct2010_gidиdropoff_nyct2010_gidв таблицеtrips:LocationIDBoroughZoneservice_zone1EWRNewark AirportEWR2QueensJamaica BayBoro Zone3BronxAllerton/Pelham GardensBoro Zone4ManhattanAlphabet CityYellow Zone5Staten IslandArden HeightsBoro ZoneВыполните следующий SQL‑запрос, который создаёт словарь с именемtaxi_zone_dictionaryи заполняет его данными из CSV‑файла в S3. URL файла:https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/taxi_zone_lookup.csv.CREATE DICTIONARY taxi_zone_dictionary
(
  `LocationID` UInt16 DEFAULT 0,
  `Borough` String,
  `Zone` String,
  `service_zone` String
)
PRIMARY KEY LocationID
SOURCE(HTTP(URL 'https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/taxi_zone_lookup.csv' FORMAT 'CSVWithNames'))
LIFETIME(MIN 0 MAX 0)
LAYOUT(HASHED_ARRAY())ПримечаниеУстановкаLIFETIMEв 0 отключает автоматические обновления, чтобы избежать ненужного трафика к нашему S3 бакету. В других случаях вы можете настроить это по‑другому. Подробности см. в разделеОбновление данных словаря с помощью LIFETIME.Убедитесь, что всё работает. Следующий запрос должен вернуть 265 строк — по одной для каждого района:SELECT * FROM taxi_zone_dictionaryИспользуйте функциюdictGet(или её варианты), чтобы извлечь значение из словаря. Вы передаёте имя словаря, значение, которое нужно получить, и ключ (в нашем примере это столбецLocationIDсловаряtaxi_zone_dictionary).Например, следующий запрос возвращаетBorough, для которогоLocationIDравен 132, что соответствует аэропорту JFK):SELECT dictGet('taxi_zone_dictionary', 'Borough', 132)JFK находится в Куинсе. Обратите внимание, что время выборки значения практически равно 0:┌─dictGet('taxi_zone_dictionary', 'Borough', 132)─┐
│ Queens                                          │
└─────────────────────────────────────────────────┘

1 rows in set. Elapsed: 0.004 sec.Используйте функциюdictHas, чтобы проверить, присутствует ли ключ в словаре. Например, следующий запрос возвращает1(что соответствует значению "true" в ClickHouse):SELECT dictHas('taxi_zone_dictionary', 132)Следующий запрос вернёт 0, потому что 4567 не является значениемLocationIDв словаре:SELECT dictHas('taxi_zone_dictionary', 4567)Используйте функциюdictGet, чтобы получить название боро в запросе. Например:SELECT
    count(1) AS total,
    dictGetOrDefault('taxi_zone_dictionary','Borough', toUInt64(pickup_nyct2010_gid), 'Unknown') AS borough_name
FROM trips
WHERE dropoff_nyct2010_gid = 132 OR dropoff_nyct2010_gid = 138
GROUP BY borough_name
ORDER BY total DESCЭтот запрос подсчитывает общее количество поездок на такси по районам для поездок, которые заканчиваются либо в аэропорту LaGuardia, либо в аэропорту JFK. Результат выглядит следующим образом — обратите внимание, что есть довольно много поездок с неизвестным районом отправления:┌─total─┬─borough_name──┐
│ 23683 │ Unknown       │
│  7053 │ Manhattan     │
│  6828 │ Brooklyn      │
│  4458 │ Queens        │
│  2670 │ Bronx         │
│   554 │ Staten Island │
│    53 │ EWR           │
└───────┴───────────────┘

7 rows in set. Elapsed: 0.019 sec. Processed 2.00 million rows, 4.00 MB (105.70 million rows/s., 211.40 MB/s.)

Вот фрагмент используемого CSV-файла в табличном формате. СтолбецLocationIDв файле соответствует столбцамpickup_nyct2010_gidиdropoff_nyct2010_gidв таблицеtrips:LocationIDBoroughZoneservice_zone1EWRNewark AirportEWR2QueensJamaica BayBoro Zone3BronxAllerton/Pelham GardensBoro Zone4ManhattanAlphabet CityYellow Zone5Staten IslandArden HeightsBoro ZoneВыполните следующий SQL‑запрос, который создаёт словарь с именемtaxi_zone_dictionaryи заполняет его данными из CSV‑файла в S3. URL файла:https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/taxi_zone_lookup.csv.CREATE DICTIONARY taxi_zone_dictionary
(
  `LocationID` UInt16 DEFAULT 0,
  `Borough` String,
  `Zone` String,
  `service_zone` String
)
PRIMARY KEY LocationID
SOURCE(HTTP(URL 'https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/taxi_zone_lookup.csv' FORMAT 'CSVWithNames'))
LIFETIME(MIN 0 MAX 0)
LAYOUT(HASHED_ARRAY())ПримечаниеУстановкаLIFETIMEв 0 отключает автоматические обновления, чтобы избежать ненужного трафика к нашему S3 бакету. В других случаях вы можете настроить это по‑другому. Подробности см. в разделеОбновление данных словаря с помощью LIFETIME.Убедитесь, что всё работает. Следующий запрос должен вернуть 265 строк — по одной для каждого района:SELECT * FROM taxi_zone_dictionaryИспользуйте функциюdictGet(или её варианты), чтобы извлечь значение из словаря. Вы передаёте имя словаря, значение, которое нужно получить, и ключ (в нашем примере это столбецLocationIDсловаряtaxi_zone_dictionary).Например, следующий запрос возвращаетBorough, для которогоLocationIDравен 132, что соответствует аэропорту JFK):SELECT dictGet('taxi_zone_dictionary', 'Borough', 132)JFK находится в Куинсе. Обратите внимание, что время выборки значения практически равно 0:┌─dictGet('taxi_zone_dictionary', 'Borough', 132)─┐
│ Queens                                          │
└─────────────────────────────────────────────────┘

1 rows in set. Elapsed: 0.004 sec.Используйте функциюdictHas, чтобы проверить, присутствует ли ключ в словаре. Например, следующий запрос возвращает1(что соответствует значению "true" в ClickHouse):SELECT dictHas('taxi_zone_dictionary', 132)Следующий запрос вернёт 0, потому что 4567 не является значениемLocationIDв словаре:SELECT dictHas('taxi_zone_dictionary', 4567)Используйте функциюdictGet, чтобы получить название боро в запросе. Например:SELECT
    count(1) AS total,
    dictGetOrDefault('taxi_zone_dictionary','Borough', toUInt64(pickup_nyct2010_gid), 'Unknown') AS borough_name
FROM trips
WHERE dropoff_nyct2010_gid = 132 OR dropoff_nyct2010_gid = 138
GROUP BY borough_name
ORDER BY total DESCЭтот запрос подсчитывает общее количество поездок на такси по районам для поездок, которые заканчиваются либо в аэропорту LaGuardia, либо в аэропорту JFK. Результат выглядит следующим образом — обратите внимание, что есть довольно много поездок с неизвестным районом отправления:┌─total─┬─borough_name──┐
│ 23683 │ Unknown       │
│  7053 │ Manhattan     │
│  6828 │ Brooklyn      │
│  4458 │ Queens        │
│  2670 │ Bronx         │
│   554 │ Staten Island │
│    53 │ EWR           │
└───────┴───────────────┘

7 rows in set. Elapsed: 0.019 sec. Processed 2.00 million rows, 4.00 MB (105.70 million rows/s., 211.40 MB/s.)

- Выполните следующий SQL‑запрос, который создаёт словарь с именемtaxi_zone_dictionaryи заполняет его данными из CSV‑файла в S3. URL файла:https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/taxi_zone_lookup.csv.

```
CREATE DICTIONARY taxi_zone_dictionary
(
  `LocationID` UInt16 DEFAULT 0,
  `Borough` String,
  `Zone` String,
  `service_zone` String
)
PRIMARY KEY LocationID
SOURCE(HTTP(URL 'https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/taxi_zone_lookup.csv' FORMAT 'CSVWithNames'))
LIFETIME(MIN 0 MAX 0)
LAYOUT(HASHED_ARRAY())

```

УстановкаLIFETIMEв 0 отключает автоматические обновления, чтобы избежать ненужного трафика к нашему S3 бакету. В других случаях вы можете настроить это по‑другому. Подробности см. в разделеОбновление данных словаря с помощью LIFETIME.

- Убедитесь, что всё работает. Следующий запрос должен вернуть 265 строк — по одной для каждого района:SELECT * FROM taxi_zone_dictionary
Убедитесь, что всё работает. Следующий запрос должен вернуть 265 строк — по одной для каждого района:


```
SELECT * FROM taxi_zone_dictionary

```

- Используйте функциюdictGet(или её варианты), чтобы извлечь значение из словаря. Вы передаёте имя словаря, значение, которое нужно получить, и ключ (в нашем примере это столбецLocationIDсловаряtaxi_zone_dictionary).Например, следующий запрос возвращаетBorough, для которогоLocationIDравен 132, что соответствует аэропорту JFK):SELECT dictGet('taxi_zone_dictionary', 'Borough', 132)JFK находится в Куинсе. Обратите внимание, что время выборки значения практически равно 0:┌─dictGet('taxi_zone_dictionary', 'Borough', 132)─┐
│ Queens                                          │
└─────────────────────────────────────────────────┘

1 rows in set. Elapsed: 0.004 sec.
Используйте функциюdictGet(или её варианты), чтобы извлечь значение из словаря. Вы передаёте имя словаря, значение, которое нужно получить, и ключ (в нашем примере это столбецLocationIDсловаряtaxi_zone_dictionary).

Например, следующий запрос возвращаетBorough, для которогоLocationIDравен 132, что соответствует аэропорту JFK):


```
SELECT dictGet('taxi_zone_dictionary', 'Borough', 132)

```

JFK находится в Куинсе. Обратите внимание, что время выборки значения практически равно 0:


```
┌─dictGet('taxi_zone_dictionary', 'Borough', 132)─┐
│ Queens                                          │
└─────────────────────────────────────────────────┘

1 rows in set. Elapsed: 0.004 sec.

```

- Используйте функциюdictHas, чтобы проверить, присутствует ли ключ в словаре. Например, следующий запрос возвращает1(что соответствует значению "true" в ClickHouse):SELECT dictHas('taxi_zone_dictionary', 132)
Используйте функциюdictHas, чтобы проверить, присутствует ли ключ в словаре. Например, следующий запрос возвращает1(что соответствует значению "true" в ClickHouse):


```
SELECT dictHas('taxi_zone_dictionary', 132)

```

- Следующий запрос вернёт 0, потому что 4567 не является значениемLocationIDв словаре:SELECT dictHas('taxi_zone_dictionary', 4567)
Следующий запрос вернёт 0, потому что 4567 не является значениемLocationIDв словаре:


```
SELECT dictHas('taxi_zone_dictionary', 4567)

```

- Используйте функциюdictGet, чтобы получить название боро в запросе. Например:SELECT
    count(1) AS total,
    dictGetOrDefault('taxi_zone_dictionary','Borough', toUInt64(pickup_nyct2010_gid), 'Unknown') AS borough_name
FROM trips
WHERE dropoff_nyct2010_gid = 132 OR dropoff_nyct2010_gid = 138
GROUP BY borough_name
ORDER BY total DESCЭтот запрос подсчитывает общее количество поездок на такси по районам для поездок, которые заканчиваются либо в аэропорту LaGuardia, либо в аэропорту JFK. Результат выглядит следующим образом — обратите внимание, что есть довольно много поездок с неизвестным районом отправления:┌─total─┬─borough_name──┐
│ 23683 │ Unknown       │
│  7053 │ Manhattan     │
│  6828 │ Brooklyn      │
│  4458 │ Queens        │
│  2670 │ Bronx         │
│   554 │ Staten Island │
│    53 │ EWR           │
└───────┴───────────────┘

7 rows in set. Elapsed: 0.019 sec. Processed 2.00 million rows, 4.00 MB (105.70 million rows/s., 211.40 MB/s.)
Используйте функциюdictGet, чтобы получить название боро в запросе. Например:


```
SELECT
    count(1) AS total,
    dictGetOrDefault('taxi_zone_dictionary','Borough', toUInt64(pickup_nyct2010_gid), 'Unknown') AS borough_name
FROM trips
WHERE dropoff_nyct2010_gid = 132 OR dropoff_nyct2010_gid = 138
GROUP BY borough_name
ORDER BY total DESC

```

Этот запрос подсчитывает общее количество поездок на такси по районам для поездок, которые заканчиваются либо в аэропорту LaGuardia, либо в аэропорту JFK. Результат выглядит следующим образом — обратите внимание, что есть довольно много поездок с неизвестным районом отправления:


```
┌─total─┬─borough_name──┐
│ 23683 │ Unknown       │
│  7053 │ Manhattan     │
│  6828 │ Brooklyn      │
│  4458 │ Queens        │
│  2670 │ Bronx         │
│   554 │ Staten Island │
│    53 │ EWR           │
└───────┴───────────────┘

7 rows in set. Elapsed: 0.019 sec. Processed 2.00 million rows, 4.00 MB (105.70 million rows/s., 211.40 MB/s.)

```


## Выполнение соединения​

Напишите несколько запросов, которые объединяютtaxi_zone_dictionaryс вашей таблицейtrips.Начните с простогоJOIN, который будет работать аналогично предыдущему запросу к данным об аэропортах выше:SELECT
    count(1) AS total,
    Borough
FROM trips
JOIN taxi_zone_dictionary ON toUInt64(trips.pickup_nyct2010_gid) = taxi_zone_dictionary.LocationID
WHERE dropoff_nyct2010_gid = 132 OR dropoff_nyct2010_gid = 138
GROUP BY Borough
ORDER BY total DESCОтвет идентичен результату запросаdictGet:┌─total─┬─Borough───────┐
│  7053 │ Manhattan     │
│  6828 │ Brooklyn      │
│  4458 │ Queens        │
│  2670 │ Bronx         │
│   554 │ Staten Island │
│    53 │ EWR           │
└───────┴───────────────┘

6 rows in set. Elapsed: 0.034 sec. Processed 2.00 million rows, 4.00 MB (59.14 million rows/s., 118.29 MB/s.)ПримечаниеОбратите внимание, что результат приведённого выше запроса сJOINсовпадает с запросом до него, который использовалdictGetOrDefault(за исключением того, что значенияUnknownне возвращаются). Под капотом ClickHouse фактически вызывает функциюdictGetдля словаряtaxi_zone_dictionary, но синтаксисJOINболее привычен для разработчиков SQL.Этот запрос возвращает строки для 1000 поездок с наибольшей суммой чаевых, затем выполняет внутреннее соединение каждой из этих строк со словарём:SELECT *
FROM trips
JOIN taxi_zone_dictionary
    ON trips.dropoff_nyct2010_gid = taxi_zone_dictionary.LocationID
WHERE tip_amount > 0
ORDER BY tip_amount DESC
LIMIT 1000ПримечаниеКак правило, в ClickHouse мы стараемся не использоватьSELECT *. Рекомендуется извлекать только те столбцы, которые вам действительно нужны.

- Начните с простогоJOIN, который будет работать аналогично предыдущему запросу к данным об аэропортах выше:SELECT
    count(1) AS total,
    Borough
FROM trips
JOIN taxi_zone_dictionary ON toUInt64(trips.pickup_nyct2010_gid) = taxi_zone_dictionary.LocationID
WHERE dropoff_nyct2010_gid = 132 OR dropoff_nyct2010_gid = 138
GROUP BY Borough
ORDER BY total DESCОтвет идентичен результату запросаdictGet:┌─total─┬─Borough───────┐
│  7053 │ Manhattan     │
│  6828 │ Brooklyn      │
│  4458 │ Queens        │
│  2670 │ Bronx         │
│   554 │ Staten Island │
│    53 │ EWR           │
└───────┴───────────────┘

6 rows in set. Elapsed: 0.034 sec. Processed 2.00 million rows, 4.00 MB (59.14 million rows/s., 118.29 MB/s.)ПримечаниеОбратите внимание, что результат приведённого выше запроса сJOINсовпадает с запросом до него, который использовалdictGetOrDefault(за исключением того, что значенияUnknownне возвращаются). Под капотом ClickHouse фактически вызывает функциюdictGetдля словаряtaxi_zone_dictionary, но синтаксисJOINболее привычен для разработчиков SQL.
Начните с простогоJOIN, который будет работать аналогично предыдущему запросу к данным об аэропортах выше:


```
SELECT
    count(1) AS total,
    Borough
FROM trips
JOIN taxi_zone_dictionary ON toUInt64(trips.pickup_nyct2010_gid) = taxi_zone_dictionary.LocationID
WHERE dropoff_nyct2010_gid = 132 OR dropoff_nyct2010_gid = 138
GROUP BY Borough
ORDER BY total DESC

```

Ответ идентичен результату запросаdictGet:


```
┌─total─┬─Borough───────┐
│  7053 │ Manhattan     │
│  6828 │ Brooklyn      │
│  4458 │ Queens        │
│  2670 │ Bronx         │
│   554 │ Staten Island │
│    53 │ EWR           │
└───────┴───────────────┘

6 rows in set. Elapsed: 0.034 sec. Processed 2.00 million rows, 4.00 MB (59.14 million rows/s., 118.29 MB/s.)

```

Обратите внимание, что результат приведённого выше запроса сJOINсовпадает с запросом до него, который использовалdictGetOrDefault(за исключением того, что значенияUnknownне возвращаются). Под капотом ClickHouse фактически вызывает функциюdictGetдля словаряtaxi_zone_dictionary, но синтаксисJOINболее привычен для разработчиков SQL.

- Этот запрос возвращает строки для 1000 поездок с наибольшей суммой чаевых, затем выполняет внутреннее соединение каждой из этих строк со словарём:SELECT *
FROM trips
JOIN taxi_zone_dictionary
    ON trips.dropoff_nyct2010_gid = taxi_zone_dictionary.LocationID
WHERE tip_amount > 0
ORDER BY tip_amount DESC
LIMIT 1000ПримечаниеКак правило, в ClickHouse мы стараемся не использоватьSELECT *. Рекомендуется извлекать только те столбцы, которые вам действительно нужны.
Этот запрос возвращает строки для 1000 поездок с наибольшей суммой чаевых, затем выполняет внутреннее соединение каждой из этих строк со словарём:


```
SELECT *
FROM trips
JOIN taxi_zone_dictionary
    ON trips.dropoff_nyct2010_gid = taxi_zone_dictionary.LocationID
WHERE tip_amount > 0
ORDER BY tip_amount DESC
LIMIT 1000

```

Как правило, в ClickHouse мы стараемся не использоватьSELECT *. Рекомендуется извлекать только те столбцы, которые вам действительно нужны.


## Дальнейшие шаги​

Узнайте больше о ClickHouse из следующих разделов документации:

- Введение в первичные индексы в ClickHouse: Узнайте, как ClickHouse использует разрежённые первичные индексы для эффективного поиска релевантных данных при выполнении запросов.
- Интеграция внешнего источника данных: Ознакомьтесь с вариантами интеграции источников данных, включая файлы, Kafka, PostgreSQL, конвейеры обработки данных и многие другие.
- Визуализация данных в ClickHouse: Подключите любимый UI/BI‑инструмент к ClickHouse.
- Справочник по SQL: Просмотрите доступные в ClickHouse функции SQL для преобразования, обработки и анализа данных.