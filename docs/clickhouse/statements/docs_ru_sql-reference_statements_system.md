# Операторы SYSTEM | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/sql-reference/statements/system


## SYSTEM RELOAD EMBEDDED DICTIONARIES​

Перезагружает всевнутренние словари.
По умолчанию внутренние словари отключены.
Всегда возвращаетOk.независимо от результата обновления внутреннего словаря.


## SYSTEM RELOAD DICTIONARIES​

ЗапросSYSTEM RELOAD DICTIONARIESперезагружает словари со статусомLOADED(см. столбецstatusвsystem.dictionaries), то есть словари, которые ранее были успешно загружены.
По умолчанию словари загружаются по требованию (см.dictionaries_lazy_load), поэтому вместо автоматической загрузки при запуске они инициализируются при первом обращении через функциюdictGetили при выполненииSELECTиз таблиц сENGINE = Dictionary.

Синтаксис


```
SYSTEM RELOAD DICTIONARIES [ON CLUSTER cluster_name]

```


## SYSTEM RELOAD DICTIONARY​

Полностью перезагружает словарьdictionary_nameвне зависимости от его состояния (LOADED / NOT_LOADED / FAILED).
Всегда возвращаетOk.независимо от того, удалось обновить словарь или нет.


```
SYSTEM RELOAD DICTIONARY [ON CLUSTER cluster_name] dictionary_name

```

Статус словаря можно проверить, выполнив запрос к таблицеsystem.dictionaries.


```
SELECT name, status FROM system.dictionaries;

```


## SYSTEM RELOAD MODELS​

Эта команда иSYSTEM RELOAD MODELтолько выгружают модели CatBoost из clickhouse-library-bridge. ФункцияcatboostEvaluate()загружает модель при первом обращении, если она ещё не загружена.

Выгружает все модели CatBoost.

Синтаксис


```
SYSTEM RELOAD MODELS [ON CLUSTER cluster_name]

```


## SYSTEM RELOAD MODEL​

Выгружает модель CatBoost, расположенную по путиmodel_path.

Синтаксис


```
SYSTEM RELOAD MODEL [ON CLUSTER cluster_name] <model_path>

```


## SYSTEM RELOAD FUNCTIONS​

Перезагружает все зарегистрированныеисполняемые пользовательские функцииили одну из них из конфигурационного файла.

Синтаксис


```
SYSTEM RELOAD FUNCTIONS [ON CLUSTER cluster_name]
SYSTEM RELOAD FUNCTION [ON CLUSTER cluster_name] function_name

```


## SYSTEM RELOAD ASYNCHRONOUS METRICS​

Повторно вычисляет всеасинхронные метрики. Поскольку асинхронные метрики периодически обновляются на основе настройкиasynchronous_metrics_update_period_s, их ручное обновление с помощью этой команды, как правило, не требуется.


```
SYSTEM RELOAD ASYNCHRONOUS METRICS [ON CLUSTER cluster_name]

```


## SYSTEM CLEAR|DROP DNS CACHE​

Очищает внутренний DNS‑кэш ClickHouse. Иногда, в старых версиях ClickHouse, при изменении инфраструктуры (например, при смене IP‑адреса другого сервера ClickHouse или сервера, используемого словарями) необходимо использовать эту команду.

Для более удобного (автоматического) управления кэшем см. параметрыdisable_internal_dns_cache,dns_cache_max_entries,dns_cache_update_period.


## SYSTEM CLEAR|DROP MARK CACHE​

Очищает кеш меток.


## SYSTEM CLEAR|DROP ICEBERG METADATA CACHE​

Очищает кеш метаданных Iceberg.


## SYSTEM DROP PARQUET METADATA CACHE​

Очищает кеш метаданных Parquet.


## SYSTEM CLEAR|DROP TEXT INDEX CACHES​

Очищает кеш заголовков текстового индекса, кеш словаря и кеш постингов.

Если вы хотите очистить один из этих кешей по отдельности, выполните:

- SYSTEM CLEAR TEXT INDEX HEADER CACHE,
- SYSTEM CLEAR TEXT INDEX DICTIONARY CACHEили
- SYSTEM CLEAR TEXT INDEX POSTINGS CACHE

## SYSTEM DROP REPLICA​

Неактивные реплики таблицReplicatedMergeTreeможно удалить с помощью следующего синтаксиса:


```
SYSTEM DROP REPLICA 'replica_name' FROM TABLE database.table;
SYSTEM DROP REPLICA 'replica_name' FROM DATABASE database;
SYSTEM DROP REPLICA 'replica_name';
SYSTEM DROP REPLICA 'replica_name' FROM ZKPATH '/path/to/table/in/zk';

```

Запросы удаляют путь репликиReplicatedMergeTreeв Zookeeper. Это полезно, когда реплика «мертвая» и её метаданные не могут быть удалены из Zookeeper командойDROP TABLE, потому что такой таблицы больше не существует. Будет удалена только неактивная или устаревшая реплика; локальную реплику этим способом удалить нельзя, для этого используйтеDROP TABLE.DROP REPLICAне удаляет никакие таблицы и не удаляет данные или метаданные с диска.

Первый вариант удаляет метаданные реплики'replica_name'таблицыdatabase.table.
Второй делает то же самое для всех реплицированных таблиц в базе данных.
Третий делает то же самое для всех реплицированных таблиц на локальном сервере.
Четвёртый полезен для удаления метаданных мёртвой реплики, когда все остальные реплики таблицы были удалены. Он требует явного указания пути таблицы. Путь должен совпадать с тем, который был передан в первый аргумент движкаReplicatedMergeTreeпри создании таблицы.


## SYSTEM DROP DATABASE REPLICA​

Мёртвые реплики баз данных типаReplicatedможно удалить с помощью следующего синтаксиса:


```
SYSTEM DROP DATABASE REPLICA 'replica_name' [FROM SHARD 'shard_name'] FROM DATABASE database;
SYSTEM DROP DATABASE REPLICA 'replica_name' [FROM SHARD 'shard_name'];
SYSTEM DROP DATABASE REPLICA 'replica_name' [FROM SHARD 'shard_name'] FROM ZKPATH '/path/to/table/in/zk';

```

АналогичноSYSTEM DROP REPLICA, но удаляет путь реплики базы данныхReplicatedиз ZooKeeper, когда нет базы данных, к которой можно применитьDROP DATABASE. Обратите внимание, что эта команда не удаляет репликиReplicatedMergeTree(поэтому вам также может понадобитьсяSYSTEM DROP REPLICA). Имена сегмента и реплики — это имена, которые были указаны в аргументах движкаReplicatedпри создании базы данных. Также эти имена можно получить из столбцовdatabase_shard_nameиdatabase_replica_nameвsystem.clusters. Если предложениеFROM SHARDотсутствует, тоreplica_nameдолжен быть полным именем реплики в форматеshard_name|replica_name.


## SYSTEM CLEAR|DROP UNCOMPRESSED CACHE​

Очищает кэш несжатых данных.
Кэш несжатых данных включается и отключается с помощью настройки на уровне запроса, USER или профиляuse_uncompressed_cache.
Его размер можно настроить с помощью серверной настройкиuncompressed_cache_size.


## SYSTEM CLEAR|DROP COMPILED EXPRESSION CACHE​

Очищает кеш скомпилированных выражений.
Кеш скомпилированных выражений включается и отключается с помощью настройкиcompile_expressionsна уровне запроса, USER или профиля.


## SYSTEM CLEAR|DROP QUERY CONDITION CACHE​

Очищает кеш условий запроса.


## SYSTEM CLEAR|DROP QUERY CACHE​


```
SYSTEM CLEAR QUERY CACHE;
SYSTEM CLEAR QUERY CACHE TAG '<tag>'

```

Очищаеткеш запросов.
Если указан тег, удаляются только записи кеша запросов, помеченные этим тегом.


## SYSTEM CLEAR|DROP FORMAT SCHEMA CACHE​

Очищает кэш для схем, загруженных изformat_schema_path.

Поддерживаемые варианты:

- Protobuf: Удаляет из памяти импортированные определения сообщений Protobuf.
- Files: Удаляет из кэша локально сохранённые файлы схем вformat_schema_path, которые были сгенерированы, когда дляformat_schema_sourceустановлено значениеquery.
Примечание: если вариант не указан, оба кэша очищаются.

```
SYSTEM CLEAR|DROP FORMAT SCHEMA CACHE [FOR Protobuf/Files]

```


## SYSTEM FLUSH LOGS​

Сбрасывает буферизованные сообщения журнала в системные таблицы, например system.query_log. В основном полезно для отладки, так как большинство системных таблиц имеют интервал сброса по умолчанию 7,5 секунды.
Команда также создаёт системные таблицы, даже если очередь сообщений пуста.


```
SYSTEM FLUSH LOGS [ON CLUSTER cluster_name] [log_name|[database.table]] [, ...]

```

Если не требуется сбрасывать все логи, можно сбросить один или несколько отдельных, указав либо их имя, либо целевую таблицу:


```
SYSTEM FLUSH LOGS query_log, system.query_views_log;

```


## SYSTEM RELOAD CONFIG​

Перезагружает конфигурацию ClickHouse. Используется, когда конфигурация хранится в ZooKeeper. Обратите внимание, чтоSYSTEM RELOAD CONFIGне перезагружает конфигурациюUSER, хранящуюся в ZooKeeper, а только конфигурациюUSER, которая хранится вusers.xml. Чтобы перезагрузить всю конфигурациюUSER, используйтеSYSTEM RELOAD USERS.


```
SYSTEM RELOAD CONFIG [ON CLUSTER cluster_name]

```


## SYSTEM RELOAD USERS​

Перезагружает все хранилища доступа, включая users.xml, хранилище доступа на локальном диске и реплицируемое (в ZooKeeper) хранилище доступа.


```
SYSTEM RELOAD USERS [ON CLUSTER cluster_name]

```


## SYSTEM SHUTDOWN​

Обычно завершает работу сервера ClickHouse (аналогичноservice clickhouse-server stop/kill {$pid_clickhouse-server})


## SYSTEM KILL​

Принудительно завершает процесс ClickHouse (например, какkill -9 {$ pid_clickhouse-server})


## SYSTEM INSTRUMENT​

Управляет точками инструментирования с помощью функции XRay в LLVM, доступной, когда ClickHouse собран с параметромENABLE_XRAY=1.
Это позволяет выполнять отладку и профилирование в продакшене без изменения исходного кода и с минимальными накладными расходами.
Когда не добавлено ни одной точки инструментирования, штраф по производительности пренебрежимо мал, поскольку добавляется лишь один дополнительный переход
на близкий адрес в прологе и эпилоге тех функций, которые содержат более 200 инструкций.


### SYSTEM INSTRUMENT ADD​

Добавляет новую точку инструментирования. Инструментированные функции можно просмотреть в системной таблицеsystem.instrumentation. Для одной и той же функции можно добавить более одного обработчика, и они будут выполняться в том же порядке, в котором было добавлено инструментирование.
Функции для инструментирования можно получить из системной таблицыsystem.symbols.

Существует три разных типа обработчиков, которые можно добавить к функциям:

Синтаксис


```
SYSTEM INSTRUMENT ADD FUNCTION HANDLER [PARAMETERS]

```

гдеFUNCTION— любая функция или подстрока имени функции, напримерQueryMetricLog::startQuery, а обработчик — один из следующих вариантов


#### LOG​

Выводит переданный в аргументе текст и стек вызовов приENTRYилиEXITфункции.


```
SYSTEM INSTRUMENT ADD 'QueryMetricLog::startQuery' LOG ENTRY 'this is a log printed at entry'
SYSTEM INSTRUMENT ADD 'QueryMetricLog::startQuery' LOG EXIT 'this is a log printed at exit'

```


#### SLEEP​

Приостанавливает выполнение на фиксированное число секунд приENTRYилиEXIT:


```
SYSTEM INSTRUMENT ADD 'QueryMetricLog::startQuery' SLEEP ENTRY 0.5

```

или — для равномерно распределённого случайного интервала в секундах, указав минимум и максимум через пробел:


```
SYSTEM INSTRUMENT ADD 'QueryMetricLog::startQuery' SLEEP ENTRY 0 1

```


#### PROFILE​

Измеряет время, прошедшее междуENTRYиEXITфункции.
Результаты профилирования сохраняются вsystem.trace_logи могут быть преобразованы
вChrome Event Trace Format.


```
SYSTEM INSTRUMENT ADD 'QueryMetricLog::startQuery' PROFILE

```


### SYSTEM INSTRUMENT REMOVE​

Удаляет одну точку инструментирования с помощью:


```
SYSTEM INSTRUMENT REMOVE ID

```

для удаления всех используйте параметрALL:


```
SYSTEM INSTRUMENT REMOVE ALL

```

набор идентификаторов из подзапроса:


```
SYSTEM INSTRUMENT REMOVE (SELECT id FROM system.instrumentation WHERE handler = 'log')

```

или все точки инструментирования, соответствующие заданному параметруfunction_name:


```
SYSTEM INSTRUMENT REMOVE 'QueryMetricLog::startQuery'

```

Информацию о точке инструментирования можно получить из системной таблицыsystem.instrumentation.


## Управление distributed таблицами​

ClickHouse может работать сdistributedтаблицами. При вставке данных в такие таблицы ClickHouse сначала создаёт очередь данных для отправки на узлы кластера, а затем асинхронно отправляет их. Вы можете управлять обработкой очереди с помощью запросовSTOP DISTRIBUTED SENDS,FLUSH DISTRIBUTEDиSTART DISTRIBUTED SENDS. Вы также можете выполнять синхронную вставку данных в distributed таблицы с помощью настройкиdistributed_foreground_insert.


### SYSTEM STOP DISTRIBUTED SENDS​

Отключает фоновое распределение данных при вставке данных в distributed таблицы.


```
SYSTEM STOP DISTRIBUTED SENDS [db.]<distributed_table_name> [ON CLUSTER cluster_name]

```

Если параметрprefer_localhost_replicaвключён (по умолчанию), данные всё равно будут вставляться в локальный сегмент.


### SYSTEM FLUSH DISTRIBUTED​

Принудительно инициирует синхронную отправку данных на узлы кластера в ClickHouse. Если какие-либо узлы недоступны, ClickHouse выбрасывает исключение и останавливает выполнение запроса. Вы можете повторять запрос до тех пор, пока он не выполнится успешно, то есть когда все узлы снова будут доступны.

Вы также можете переопределить некоторые настройки с помощью предложенияSETTINGS— это может быть полезно для обхода временных ограничений, таких какmax_concurrent_queries_for_all_usersилиmax_memory_usage.


```
SYSTEM FLUSH DISTRIBUTED [db.]<distributed_table_name> [ON CLUSTER cluster_name] [SETTINGS ...]

```

Каждый ожидающий отправки блок хранится на диске с настройками из исходного запроса INSERT, поэтому иногда может потребоваться переопределить эти настройки.


### SYSTEM START DISTRIBUTED SENDS​

Включает фоновую отправку данных при вставке в distributed таблицы.


```
SYSTEM START DISTRIBUTED SENDS [db.]<distributed_table_name> [ON CLUSTER cluster_name]

```


### SYSTEM STOP LISTEN​

Закрывает сокет и корректно завершает активные подключения к серверу на указанном порту с указанным протоколом.

Однако, если соответствующие настройки протокола не заданы в конфигурации clickhouse-server, эта команда не окажет эффекта.


```
SYSTEM STOP LISTEN [ON CLUSTER cluster_name] [QUERIES ALL | QUERIES DEFAULT | QUERIES CUSTOM | TCP | TCP WITH PROXY | TCP SECURE | HTTP | HTTPS | MYSQL | GRPC | POSTGRESQL | PROMETHEUS | CUSTOM 'protocol']

```

- Если указан модификаторCUSTOM 'protocol', будет остановлен пользовательский протокол с указанным именем, определённый в разделеprotocolsконфигурации сервера.
- Если указан модификаторQUERIES ALL [EXCEPT .. [,..]], будут остановлены все протоколы, за исключением протоколов, перечисленных в выраженииEXCEPT.
- Если указан модификаторQUERIES DEFAULT [EXCEPT .. [,..]], будут остановлены все протоколы по умолчанию, за исключением протоколов, перечисленных в выраженииEXCEPT.
- Если указан модификаторQUERIES CUSTOM [EXCEPT .. [,..]], будут остановлены все пользовательские протоколы, за исключением протоколов, перечисленных в выраженииEXCEPT.

### SYSTEM START LISTEN​

Включает приём новых подключений по указанным протоколам.

Однако если сервер на указанном порту и протоколе не был остановлен с помощью команды SYSTEM STOP LISTEN, эта команда не будет иметь эффекта.


```
SYSTEM START LISTEN [ON CLUSTER cluster_name] [QUERIES ALL | QUERIES DEFAULT | QUERIES CUSTOM | TCP | TCP WITH PROXY | TCP SECURE | HTTP | HTTPS | MYSQL | GRPC | POSTGRESQL | PROMETHEUS | CUSTOM 'protocol']

```


## Управление таблицами MergeTree​

ClickHouse может управлять фоновыми процессами в таблицахMergeTree.


### SYSTEM STOP MERGES​

Позволяет остановить фоновые слияния для таблиц семейства MergeTree:


```
SYSTEM STOP MERGES [ON CLUSTER cluster_name] [ON VOLUME <volume_name> | [db.]merge_tree_family_table_name]

```

ВыполнениеDETACH / ATTACHтаблицы запустит фоновые слияния для этой таблицы, даже если слияния ранее были остановлены для всех таблиц MergeTree.


### SYSTEM START MERGES​

Команда позволяет запускать фоновые слияния для таблиц семейства MergeTree:


```
SYSTEM START MERGES [ON CLUSTER cluster_name] [ON VOLUME <volume_name> | [db.]merge_tree_family_table_name]

```


### SYSTEM STOP TTL MERGES​

Позволяет остановить фоновое удаление старых данных в соответствии свыражением TTLдля таблиц семейства MergeTree.
ВозвращаетOk.даже если таблица не существует или таблица не использует движок MergeTree. Возвращает ошибку, если база данных не существует.


```
SYSTEM STOP TTL MERGES [ON CLUSTER cluster_name] [[db.]merge_tree_family_table_name]

```


### SYSTEM START TTL MERGES​

Позволяет запустить фоновое удаление устаревших данных в соответствии свыражением TTLдля таблиц семейства MergeTree.
ВозвращаетOk.даже если таблица не существует. Возвращает ошибку, если база данных не существует.


```
SYSTEM START TTL MERGES [ON CLUSTER cluster_name] [[db.]merge_tree_family_table_name]

```


### SYSTEM STOP MOVES​

Позволяет остановить фоновое перемещение данных в соответствии сTTL-выражением таблицы с оператором TO VOLUME или TO DISKдля таблиц семейства MergeTree:
ВозвращаетOk.даже если таблица не существует. Возвращает ошибку, если база данных не существует:


```
SYSTEM STOP MOVES [ON CLUSTER cluster_name] [[db.]merge_tree_family_table_name]

```


### SYSTEM START MOVES​

Предоставляет возможность запустить фоновое перемещение данных в соответствии сTTL-выражением таблицы с предложениями TO VOLUME и TO DISKдля таблиц семейства MergeTree.
ВозвращаетOk.даже в случае, если таблица не существует. Возвращает ошибку, если база данных не существует.


```
SYSTEM START MOVES [ON CLUSTER cluster_name] [[db.]merge_tree_family_table_name]

```


### SYSTEM SYSTEM UNFREEZE​

Очищает замороженный бэкап с указанным именем на всех дисках. Подробнее о разморозке отдельных частей см. вALTER TABLE table_name UNFREEZE WITH NAME


```
SYSTEM UNFREEZE WITH NAME <backup_name>

```


### SYSTEM WAIT LOADING PARTS​

Ожидает, пока все асинхронно загружаемые части таблицы (устаревшие части данных) не будут загружены.


```
SYSTEM WAIT LOADING PARTS [ON CLUSTER cluster_name] [db.]merge_tree_family_table_name

```


## Управление таблицами ReplicatedMergeTree​

ClickHouse может управлять процессами фоновой репликации в таблицахReplicatedMergeTree.


### SYSTEM STOP FETCHES​

Позволяет остановить фоновую загрузку вставленных частей для таблиц семействаReplicatedMergeTree:
Всегда возвращаетOk.независимо от движка таблицы и даже если таблица или база данных не существует.


```
SYSTEM STOP FETCHES [ON CLUSTER cluster_name] [[db.]replicated_merge_tree_family_table_name]

```


### SYSTEM START FETCHES​

Предоставляет возможность запустить фоновые операции FETCH для вставленных частей в таблицах семействаReplicatedMergeTree.
Всегда возвращаетOk.независимо от движка таблицы и даже если таблица или база данных не существует.


```
SYSTEM START FETCHES [ON CLUSTER cluster_name] [[db.]replicated_merge_tree_family_table_name]

```


### SYSTEM STOP REPLICATED SENDS​

Позволяет остановить фоновую отправку на другие реплики в кластере новых частей, вставляемых в таблицы семействаReplicatedMergeTree:


```
SYSTEM STOP REPLICATED SENDS [ON CLUSTER cluster_name] [[db.]replicated_merge_tree_family_table_name]

```


### SYSTEM START REPLICATED SENDS​

Позволяет запустить фоновые отправки новых вставленных частей другим репликам кластера для таблиц семействаReplicatedMergeTree:


```
SYSTEM START REPLICATED SENDS [ON CLUSTER cluster_name] [[db.]replicated_merge_tree_family_table_name]

```


### SYSTEM STOP REPLICATION QUEUES​

Позволяет остановить фоновые задачи выборки из очередей репликации, которые хранятся в ZooKeeper для таблиц семействаReplicatedMergeTree. Возможные типы фоновых задач — слияния, выборки, мутации, DDL-команды с предложением ON CLUSTER:


```
SYSTEM STOP REPLICATION QUEUES [ON CLUSTER cluster_name] [[db.]replicated_merge_tree_family_table_name]

```


### SYSTEM START REPLICATION QUEUES​

Позволяет запустить фоновые задачи выборки из очередей репликации, которые хранятся в ZooKeeper для таблиц семействаReplicatedMergeTree. Возможные типы фоновых задач — слияния, выборки, мутации, DDL‑команды с предложением ON CLUSTER:


```
SYSTEM START REPLICATION QUEUES [ON CLUSTER cluster_name] [[db.]replicated_merge_tree_family_table_name]

```


### SYSTEM STOP PULLING REPLICATION LOG​

Прекращает чтение новых записей из журнала репликации и помещение их в очередь репликации в таблицеReplicatedMergeTree.


```
SYSTEM STOP PULLING REPLICATION LOG [ON CLUSTER cluster_name] [[db.]replicated_merge_tree_family_table_name]

```


### SYSTEM START PULLING REPLICATION LOG​

Отменяет командуSYSTEM STOP PULLING REPLICATION LOG.


```
SYSTEM START PULLING REPLICATION LOG [ON CLUSTER cluster_name] [[db.]replicated_merge_tree_family_table_name]

```


### SYSTEM SYNC REPLICA​

Ожидает синхронизации таблицыReplicatedMergeTreeс другими репликами в кластере, но не болееreceive_timeoutсекунд.


```
SYSTEM SYNC REPLICA [ON CLUSTER cluster_name] [db.]replicated_merge_tree_family_table_name [IF EXISTS] [STRICT | LIGHTWEIGHT [FROM 'srcReplica1'[, 'srcReplica2'[, ...]]] | PULL]

```

После выполнения этого оператора[db.]replicated_merge_tree_family_table_nameзагружает команды из общего журнала репликации в свою собственную очередь репликации, после чего запрос ожидает, пока реплика обработает все полученные команды. Поддерживаются следующие модификаторы:

- С модификаторомIF EXISTS(доступен начиная с 25.6) запрос не будет выдавать ошибку, если таблица не существует. Это полезно при добавлении новой реплики в кластер, когда она уже является частью конфигурации кластера, но таблица ещё находится в процессе создания и синхронизации.
- Если указан модификаторSTRICT, то запрос ожидает, пока очередь репликации не станет пустой. ВариантSTRICTможет никогда не завершиться успешно, если в очереди репликации постоянно появляются новые записи.
- Если указан модификаторLIGHTWEIGHT, то запрос ожидает только обработки записейGET_PART,ATTACH_PART,DROP_RANGE,REPLACE_RANGEиDROP_PART.
Дополнительно модификаторLIGHTWEIGHTподдерживает необязательное предложениеFROM 'srcReplicas', где'srcReplicas'— это список имён исходных реплик, разделённых запятыми. Это расширение обеспечивает более точечную синхронизацию, фокусируясь только на задачах репликации, исходящих от указанных реплик-источников.
- Если указан модификаторPULL, то запрос подтягивает новые записи очереди репликации из ZooKeeper, но не ожидает обработки каких-либо записей.

### SYNC DATABASE REPLICA​

Ожидает, пока указаннаяреплицируемая база данныхне применит все изменения схемы из очереди DDL этой базы данных.

Синтаксис


```
SYSTEM SYNC DATABASE REPLICA replicated_database_name;

```


### SYSTEM RESTART REPLICA​

Позволяет повторно инициализировать состояние сессии ZooKeeper для таблицыReplicatedMergeTree: текущее состояние будет сопоставлено с ZooKeeper как источником истины, и при необходимости в очередь ZooKeeper будут добавлены задания.
Инициализация очереди репликации на основе данных ZooKeeper происходит так же, как для оператораATTACH TABLE. В течение короткого времени таблица будет недоступна для любых операций.


```
SYSTEM RESTART REPLICA [ON CLUSTER cluster_name] [db.]replicated_merge_tree_family_table_name

```


### SYSTEM RESTORE REPLICA​

Восстанавливает реплику, если данные (возможно) присутствуют, но метаданные ZooKeeper утеряны.

Работает только с таблицамиReplicatedMergeTreeв режиме только для чтения (readonly).

Запрос можно выполнить после:

- потери корня ZooKeeper/;
- потери пути реплик/replicas;
- потери пути отдельной реплики/replicas/replica_name/.
Реплика прикрепляет локально найденные части и отправляет информацию о них в ZooKeeper.
Части, присутствовавшие на реплике до потери метаданных, не загружаются повторно с других реплик, если они не устарели (то есть восстановление реплики не означает повторную загрузку всех данных по сети).

Все части во всех состояниях перемещаются в папкуdetached/. Части, которые были активны до потери данных (committed), прикрепляются.


### SYSTEM RESTORE DATABASE REPLICA​

Восстанавливает реплику, если данные, возможно, присутствуют, но метаданные Zookeeper утеряны.

Синтаксис


```
SYSTEM RESTORE DATABASE REPLICA repl_db [ON CLUSTER cluster]

```

Пример


```
CREATE DATABASE repl_db
ENGINE=Replicated("/clickhouse/repl_db", shard1, replica1);

CREATE TABLE repl_db.test_table (n UInt32)
ENGINE = ReplicatedMergeTree
ORDER BY n PARTITION BY n % 10;

-- zookeeper_delete_path("/clickhouse/repl_db", recursive=True) <- root loss.

SYSTEM RESTORE DATABASE REPLICA repl_db;

```

Синтаксис


```
SYSTEM RESTORE REPLICA [db.]replicated_merge_tree_family_table_name [ON CLUSTER cluster_name]

```

Другой синтаксис:


```
SYSTEM RESTORE REPLICA [ON CLUSTER cluster_name] [db.]replicated_merge_tree_family_table_name

```

Пример

Создание таблицы на нескольких серверах. После потери метаданных реплики в Zookeeper таблица подключится в режиме только чтения, так как метаданные отсутствуют. Последний запрос должен быть выполнен на каждой реплике.


```
CREATE TABLE test(n UInt32)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/test/', '{replica}')
ORDER BY n PARTITION BY n % 10;

INSERT INTO test SELECT * FROM numbers(1000);

-- zookeeper_delete_path("/clickhouse/tables/test", recursive=True) <- root loss.

SYSTEM RESTART REPLICA test;
SYSTEM RESTORE REPLICA test;

```

Другой способ:


```
SYSTEM RESTORE REPLICA test ON CLUSTER cluster;

```


### SYSTEM RESTART REPLICAS​

Позволяет переинициализировать состояние сессий ZooKeeper для всех таблицReplicatedMergeTree, сравнивает текущее состояние с ZooKeeper как источником истины и при необходимости добавляет задания в очередь ZooKeeper.


### SYSTEM CLEAR|DROP FILESYSTEM CACHE​

Позволяет сбросить кеш файловой системы.


```
SYSTEM CLEAR FILESYSTEM CACHE [ON CLUSTER cluster_name]

```


### SYSTEM SYNC FILE CACHE​

Операция слишком ресурсоёмкая и может быть легко использована неправильно.

Вызывает системный вызов sync.


```
SYSTEM SYNC FILE CACHE [ON CLUSTER cluster_name]

```


### SYSTEM LOAD PRIMARY KEY​

Загрузить первичные ключи для заданной таблицы или для всех таблиц.


```
SYSTEM LOAD PRIMARY KEY [db.]name

```


```
SYSTEM LOAD PRIMARY KEY

```


### SYSTEM UNLOAD PRIMARY KEY​

Выгрузить первичные ключи для указанной таблицы или для всех таблиц.


```
SYSTEM UNLOAD PRIMARY KEY [db.]name

```


```
SYSTEM UNLOAD PRIMARY KEY

```


## Управление Refreshable Materialized Views​

Команды для управления фоновыми задачами, выполняемымиRefreshable Materialized Views.

При работе с ними отслеживайте таблицуsystem.view_refreshes.


### SYSTEM REFRESH VIEW​

Запускает немедленное внеплановое обновление указанного представления.


```
SYSTEM REFRESH VIEW [db.]name

```


### SYSTEM WAIT VIEW​

Ожидает завершения текущего обновления, выполняющегося в данный момент. Если обновление завершается с ошибкой, генерируется исключение. Если обновление не выполняется, немедленно завершает выполнение, генерируя исключение, если предыдущее обновление завершилось с ошибкой.


### SYSTEM STOP [REPLICATED] VIEW, STOP VIEWS​

Отключает периодическое обновление указанного представления или всех обновляемых представлений. Если обновление уже выполняется, также отменяет его.

Если представление находится в базе данных Replicated или Shared,STOP VIEWвлияет только на текущую реплику, тогда какSTOP REPLICATED VIEWвлияет на все реплики.

Остановленное состояние не сохраняется после перезапуска сервера. После перезапуска представления возобновят выполнение настроенных расписаний обновления.
В базах данных Replicated или SharedSYSTEM STOP VIEWвлияет только на текущую реплику. ИспользуйтеSYSTEM STOP REPLICATED VIEW, чтобы остановить обновления на всех репликах.


```
SYSTEM STOP VIEW [db.]name

```


```
SYSTEM STOP VIEWS

```


### SYSTEM START [REPLICATED] VIEW, START VIEWS​

Запускает периодическое обновление для указанного представления или для всех представлений с поддержкой обновления. Немедленное обновление при этом не выполняется.

Если представление находится в базе данных типа Replicated или Shared,START VIEWотменяет действиеSTOP VIEW, аSTART REPLICATED VIEWотменяет действиеSTOP REPLICATED VIEW.


```
SYSTEM START VIEW [db.]name

```


```
SYSTEM START VIEWS

```


### SYSTEM CANCEL VIEW​

Если для указанного представления на текущей реплике в данный момент выполняется обновление, команда прерывает и отменяет его; в противном случае ничего не происходит.


```
SYSTEM CANCEL VIEW [db.]name

```


### SYSTEM WAIT VIEW​

Ожидает завершения текущего обновления. Если обновление не выполняется, немедленно возвращает управление. Если последняя попытка обновления завершилась с ошибкой, генерирует ошибку.

Может использоваться сразу после создания нового refreshable materialized view (без ключевого слова EMPTY), чтобы дождаться завершения начального обновления.

Если представление находится в базе данных Replicated или Shared и обновление выполняется на другой реплике, ожидает завершения этого обновления.


```
SYSTEM WAIT VIEW [db.]name

```
