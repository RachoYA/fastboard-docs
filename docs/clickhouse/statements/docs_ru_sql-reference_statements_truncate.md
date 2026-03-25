# Команды TRUNCATE | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/sql-reference/statements/truncate

КомандаTRUNCATEв ClickHouse используется для быстрого удаления всех данных из таблицы или базы данных при сохранении их структуры.


## TRUNCATE TABLE​


```
TRUNCATE TABLE [IF EXISTS] [db.]name [ON CLUSTER cluster] [SYNC]

```

Вы можете использовать настройкуalter_syncдля ожидания выполнения действий на репликах.

Вы можете указать, как долго (в секундах) ждать выполнения запросовTRUNCATEнеактивными репликами с помощью настройкиreplication_wait_for_inactive_replica_timeout.

Если параметрalter_syncустановлен в значение2и некоторые реплики неактивны дольше времени, указанного в настройкеreplication_wait_for_inactive_replica_timeout, будет выброшено исключениеUNFINISHED.

ЗапросTRUNCATE TABLEне поддерживаетсядля следующих движков таблиц:

- View
- File
- URL
- Buffer
- Null

## TRUNCATE ALL TABLES​


```
TRUNCATE [ALL] TABLES FROM [IF EXISTS] db [LIKE | ILIKE | NOT LIKE '<pattern>'] [ON CLUSTER cluster]

```

Удаляет все данные из всех таблиц базы данных.


## TRUNCATE DATABASE​


```
TRUNCATE DATABASE [IF EXISTS] db [ON CLUSTER cluster]

```

Удаляет все таблицы из базы данных, но сохраняет саму базу данных. Если опустить условиеIF EXISTS, запрос вернёт ошибку, если база данных не существует.

TRUNCATE DATABASEне поддерживается для баз данныхReplicated. Вместо этого просто выполнитеDROPиCREATEдля базы данных.
