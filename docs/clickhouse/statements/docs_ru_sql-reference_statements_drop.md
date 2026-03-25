# Операторы DROP | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/sql-reference/statements/drop

Удаляют существующую сущность. Если указано предложениеIF EXISTS, запрос не приводит к ошибке, даже если сущность не существует. Если указан модификаторSYNC, сущность удаляется без задержки.


## DROP DATABASE​

Удаляет все таблицы в базе данныхdb, а затем удаляет саму базу данныхdb.

Синтаксис:


```
DROP DATABASE [IF EXISTS] db [ON CLUSTER cluster] [SYNC]

```


## DROP TABLE​

Удаляет одну или несколько таблиц.

Чтобы отменить удаление таблицы, используйте операторUNDROP TABLE

Синтаксис:


```
DROP [TEMPORARY] TABLE [IF EXISTS] [IF EMPTY]  [db1.]name_1[, [db2.]name_2, ...] [ON CLUSTER cluster] [SYNC]

```

Ограничения:

- Если указано условиеIF EMPTY, сервер проверяет, пуста ли таблица, только на реплике, которая получила запрос.
- Удаление нескольких таблиц одновременно не является атомарной операцией, т.е. если удаление одной таблицы завершается с ошибкой, последующие таблицы не будут удалены.

## DROP DICTIONARY​

Удаляет словарь.

Синтаксис:


```
DROP DICTIONARY [IF EXISTS] [db.]name [SYNC]

```


## DROP USER​

Удаляет пользователя.

Синтаксис:


```
DROP USER [IF EXISTS] name [,...] [ON CLUSTER cluster_name] [FROM access_storage_type]

```


## DROP ROLE​

Удаляет роль. Удалённая роль автоматически отзывается у всех объектов, которым она была назначена.

Синтаксис:


```
DROP ROLE [IF EXISTS] name [,...] [ON CLUSTER cluster_name] [FROM access_storage_type]

```


## DROP ROW POLICY​

Удаляет политику строк. Удалённая политика перестаёт действовать для всех сущностей, которым она была назначена.

Синтаксис:


```
DROP [ROW] POLICY [IF EXISTS] name [,...] ON [database.]table [,...] [ON CLUSTER cluster_name] [FROM access_storage_type]

```


## DROP MASKING POLICY​

Удаляет политику маскирования.

Синтаксис:


```
DROP MASKING POLICY [IF EXISTS] name ON [database.]table [ON CLUSTER cluster_name] [FROM access_storage_type]

```


## DROP QUOTA​

Удаляет квоту. Удалённая квота отзывается у всех объектов, которым она была назначена.

Синтаксис:


```
DROP QUOTA [IF EXISTS] name [,...] [ON CLUSTER cluster_name] [FROM access_storage_type]

```


## DROP SETTINGS PROFILE​

Удаляет профиль настроек. Удалённый профиль настроек будет снят со всех объектов, которым он был назначен.

Синтаксис:


```
DROP [SETTINGS] PROFILE [IF EXISTS] name [,...] [ON CLUSTER cluster_name] [FROM access_storage_type]

```


## DROP VIEW​

Удаляет представление. Представления можно удалить и с помощью командыDROP TABLE, ноDROP VIEWпроверяет, что[db.]nameдействительно является представлением.

Синтаксис:


```
DROP VIEW [IF EXISTS] [db.]name [ON CLUSTER cluster] [SYNC]

```


## DROP FUNCTION​

Удаляет функцию, определяемую пользователем, созданную с помощьюCREATE FUNCTION.
Системные функции удалить невозможно.

Синтаксис


```
DROP FUNCTION [IF EXISTS] function_name [on CLUSTER cluster]

```

Пример


```
CREATE FUNCTION linear_equation AS (x, k, b) -> k*x + b;
DROP FUNCTION linear_equation;

```


## DROP NAMED COLLECTION​

Удаляет именованную коллекцию.

Синтаксис


```
DROP NAMED COLLECTION [IF EXISTS] name [on CLUSTER cluster]

```

Пример


```
CREATE NAMED COLLECTION foobar AS a = '1', b = '2';
DROP NAMED COLLECTION foobar;

```
