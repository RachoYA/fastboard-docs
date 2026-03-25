# Оператор ATTACH | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/sql-reference/statements/attach

Подключает таблицу или словарь, например, при переносе базы данных на другой сервер.

Синтаксис


```
ATTACH TABLE|DICTIONARY|DATABASE [IF NOT EXISTS] [db.]name [ON CLUSTER cluster] ...

```

Запрос не создаёт данные на диске, а предполагает, что данные уже размещены в соответствующих местах, и просто добавляет на сервер информацию об указанной таблице, словаре или базе данных. После выполнения запросаATTACHсервер будет знать о существовании таблицы, словаря или базы данных.

Если таблица ранее была отсоединена (запросDETACH), то есть её структура уже известна, можно использовать сокращённую форму без определения структуры.


## Подключить существующую таблицу​

Синтаксис


```
ATTACH TABLE [IF NOT EXISTS] [db.]name [ON CLUSTER cluster]

```

Этот запрос используется при запуске сервера. Сервер хранит метаданные таблиц в виде файлов с запросамиATTACH, которые он просто выполняет при старте (за исключением некоторых системных таблиц, которые создаются на сервере явно).

Если таблица была отсоединена окончательно, она не будет повторно присоединена при запуске сервера, поэтому вам нужно явно выполнить запросATTACH.


## Создание новой таблицы и подключение данных​


### С указанием пути к данным таблицы​

Запрос создает новую таблицу с заданной структурой и подключает данные таблицы из указанного каталога в директорииuser_files.

Синтаксис


```
ATTACH TABLE name FROM 'path/to/data/' (col1 Type1, ...)

```

Пример

Запрос:


```
DROP TABLE IF EXISTS test;
INSERT INTO TABLE FUNCTION file('01188_attach/test/data.TSV', 'TSV', 's String, n UInt8') VALUES ('test', 42);
ATTACH TABLE test FROM '01188_attach/test' (s String, n UInt8) ENGINE = File(TSV);
SELECT * FROM test;

```

Результат:


```
┌─s────┬──n─┐
│ test │ 42 │
└──────┴────┘

```


### С заданным UUID таблицы​

Этот запрос создает новую таблицу с заданной структурой и присоединяет данные из таблицы с указанным UUID.
Поддерживается в движке базы данныхAtomic.

Синтаксис


```
ATTACH TABLE name UUID '<uuid>' (col1 Type1, ...)

```


## Подключение таблицы MergeTree как ReplicatedMergeTree​

Позволяет подключить нереплицируемую таблицу MergeTree как ReplicatedMergeTree. Таблица ReplicatedMergeTree будет создана с использованием значений настроекdefault_replica_pathиdefault_replica_name. Также возможно подключить реплицируемую таблицу как обычную MergeTree.

Обратите внимание, что данные таблицы в ZooKeeper этим запросом не изменяются. Это означает, что вам необходимо либо добавить метаданные в ZooKeeper с помощьюSYSTEM RESTORE REPLICA, либо очистить их с помощьюSYSTEM DROP REPLICA ... FROM ZKPATH ...после выполнения операции ATTACH.

Если вы пытаетесь добавить реплику к уже существующей таблице ReplicatedMergeTree, имейте в виду, что все локальные данные в преобразованной таблице MergeTree будут отсоединены.

Синтаксис


```
ATTACH TABLE [db.]name AS [NOT] REPLICATED

```

Преобразование таблицы в реплицируемую таблицу


```
DETACH TABLE test;
ATTACH TABLE test AS REPLICATED;
SYSTEM RESTORE REPLICA test;

```

Преобразовать таблицу в нереплицируемую

Определите путь в ZooKeeper и имя реплики таблицы:


```
SELECT replica_name, zookeeper_path FROM system.replicas WHERE table='test';

```

Результат:


```
┌─replica_name─┬─zookeeper_path─────────────────────────────────────────────┐
│ r1           │ /clickhouse/tables/401e6a1f-9bf2-41a3-a900-abb7e94dff98/s1 │
└──────────────┴────────────────────────────────────────────────────────────┘

```

Подключите таблицу как нереплицируемую и удалите данные этой реплики из ZooKeeper:


```
DETACH TABLE test;
ATTACH TABLE test AS NOT REPLICATED;
SYSTEM DROP REPLICA 'r1' FROM ZKPATH '/clickhouse/tables/401e6a1f-9bf2-41a3-a900-abb7e94dff98/s1';

```


## Подключить существующий словарь​

Подключает ранее отключённый словарь.

Синтаксис


```
ATTACH DICTIONARY [IF NOT EXISTS] [db.]name [ON CLUSTER cluster]

```


## Подключить существующую базу данных​

Подключает ранее отсоединённую базу данных.

Синтаксис


```
ATTACH DATABASE [IF NOT EXISTS] name [ENGINE=<database engine>] [ON CLUSTER cluster]

```
