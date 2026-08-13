# system.asynchronous_metrics - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/system-tables/asynchronous_metrics


## Описание


## Столбцы

- `metric` ([String](https://clickhouse.com/docs/ru/reference/data-types/string)) — Название метрики.
- `value` ([Float64](https://clickhouse.com/docs/ru/reference/data-types/float)) — Значение метрики.
- `description` ([String](https://clickhouse.com/docs/ru/reference/data-types/string) - Описание метрики)

## Пример


```
SELECT * FROM system.asynchronous_metrics LIMIT 10

```


```
┌─metric──────────────────────────────────┬──────value─┬─description────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ AsynchronousMetricsCalculationTimeSpent │ 0.00179053 │ Time in seconds spent for calculation of asynchronous metrics (this is the overhead of asynchronous metrics).                                                                                                                                              │
│ NumberOfDetachedByUserParts             │          0 │ The total number of parts detached from MergeTree tables by users with the `ALTER TABLE DETACH` query (as opposed to unexpected, broken or ignored parts). The server does not care about detached parts and they can be removed.                          │
│ NumberOfDetachedParts                   │          0 │ The total number of parts detached from MergeTree tables. A part can be detached by a user with the `ALTER TABLE DETACH` query or by the server itself it the part is broken, unexpected or unneeded. The server does not care about detached parts and they can be removed. │
│ TotalRowsOfMergeTreeTables              │    2781309 │ Total amount of rows (records) stored in all tables of MergeTree family.                                                                                                                                                                                   │
│ TotalBytesOfMergeTreeTables             │    7741926 │ Total amount of bytes (compressed, including data and indices) stored in all tables of MergeTree family.                                                                                                                                                   │
│ NumberOfTables                          │         93 │ Total number of tables summed across the databases on the server, excluding the databases that cannot contain MergeTree tables. The excluded database engines are those who generate the set of tables on the fly, like `Lazy`, `MySQL`, `PostgreSQL`, `SQlite`. │
│ NumberOfDatabases                       │          6 │ Total number of databases on the server.                                                                                                                                                                                                                   │
│ MaxPartCountForPartition                │          6 │ Maximum number of parts per partition across all partitions of all tables of MergeTree family. Values larger than 300 indicates misconfiguration, overload, or massive data loading.                                                                       │
│ ReplicasSumMergesInQueue                │          0 │ Sum of merge operations in the queue (still to be applied) across Replicated tables.                                                                                                                                                                       │
│ ReplicasSumInsertsInQueue               │          0 │ Sum of INSERT operations in the queue (still to be replicated) across Replicated tables.                                                                                                                                                                   │
└─────────────────────────────────────────┴────────────┴────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

```


## Описания метрик


### AsynchronousHeavyMetricsCalculationTimeSpent


### AsynchronousHeavyMetricsUpdateInterval


### AsynchronousMetricsCalculationTimeSpent


### AsynchronousMetricsUpdateInterval


### AsyncLogging*metric_first*QueueSize


### BlockActiveTime_*name*


### BlockActiveTimePerOp_*name*


### BlockDiscardBytes_*name*


### BlockDiscardMerges_*name*


### BlockDiscardOps_*name*


### BlockDiscardTime_*name*


### BlockInFlightOps_*name*


### BlockQueueTime_*name*


### BlockQueueTimePerOp_*name*


### BlockReadBytes_*name*


### BlockReadMerges_*name*


### BlockReadOps_*name*


### BlockReadTime_*name*


### BlockWriteBytes_*name*


### BlockWriteMerges_*name*


### BlockWriteOps_*name*


### BlockWriteTime_*name*


### CGroupMaxCPU


### CGroupMemoryTotal


### CGroupMemoryUsed


### CGroupMemoryUsedWithoutPageCache


### CGroupSystemTime


### CGroupSystemTimeNormalized


### CGroupUserTime


### CGroupUserTimeNormalized


### CPUFrequencyMHz_*core_id*


### DictionaryMaxUpdateDelay


### DictionaryTotalFailedUpdates


### DiskAvailable_*name*


### DiskGetObjectThrottlerAvailable_*name*


### DiskGetObjectThrottlerRPS_*name*


### DiskPutObjectThrottlerAvailable_*name*


### DiskPutObjectThrottlerRPS_*name*


### DiskTotal_*name*


### DiskUnreserved_*name*


### DiskUsed_*name*


### EDAC*i*_Correctable


### EDAC*i*_Uncorrectable


### ExecutableUserDefinedFunctionMemoryResidentBytes


### ExecutableUserDefinedFunctionProcesses


### FilesystemCacheBytes


### FilesystemCacheCapacity


### FilesystemCacheFiles


### FilesystemLogsPathAvailableBytes


### FilesystemLogsPathAvailableINodes


### FilesystemLogsPathTotalBytes


### FilesystemLogsPathTotalINodes


### FilesystemLogsPathUsedBytes


### FilesystemLogsPathUsedINodes


### FilesystemMainPathAvailableBytes


### FilesystemMainPathAvailableINodes


### FilesystemMainPathTotalBytes


### FilesystemMainPathTotalINodes


### FilesystemMainPathUsedBytes


### FilesystemMainPathUsedINodes


### GRPCRejectedConnections


### GRPCThreads


### HashTableStatsCacheEntries


### HashTableStatsCacheHits


### HashTableStatsCacheMisses


### HTTPConnectionPool*group_name*TCPRcvBufTotalBytes


### HTTPConnectionPool*group_name*TCPSndBufTotalBytes


### HTTPRejectedConnections


### HTTPSecureRejectedConnections


### HTTPSecureThreads


### HTTPThreads


### InterserverRejectedConnections


### InterserverSecureRejectedConnections


### InterserverSecureThreads


### InterserverThreads


### jemalloc.active


### jemalloc.allocated


### jemalloc.arenas.all.dirty_purged


### jemalloc.arenas.all.muzzy_purged


### jemalloc.arenas.all.pactive


### jemalloc.arenas.all.pdirty


### jemalloc.arenas.all.pmuzzy


### jemalloc.arenas.dirty_decay_ms


### jemalloc.background_thread.num_runs


### jemalloc.background_thread.num_threads


### jemalloc.background_thread.run_intervals


### jemalloc.cache_arena.pactive


### jemalloc.cache_arena.pdirty


### jemalloc.epoch


### jemalloc.mapped


### jemalloc.mergetree_arena.active_bytes


### jemalloc.mergetree_arena.dirty_bytes


### jemalloc.mergetree_arena.pactive


### jemalloc.mergetree_arena.pdirty


### jemalloc.metadata


### jemalloc.metadata_thp


### jemalloc.prof.active


### jemalloc.prof.lg_sample


### jemalloc.prof.thread_active_init


### jemalloc.resident


### jemalloc.retained


### Jitter


### KeeperApproximateDataSize


### KeeperAvgLatency


### KeeperCommitLogsCacheEntries


### KeeperCommitLogsCacheSize


### KeeperEphemeralsCount


### KeeperFollowers


### KeeperIsExceedingMemorySoftLimitHit


### KeeperIsFollower


### KeeperIsLeader


### KeeperIsObserver


### KeeperIsStandalone


### KeeperKeyArenaSize


### KeeperLastCommittedLogIdx


### KeeperLastLogIdx


### KeeperLastLogTerm


### KeeperLastSnapshotIdx


### KeeperLatestLogsCacheEntries


### KeeperLatestLogsCacheSize


### Размер последнего снимка Keeper


### KeeperMaxFileDescriptorCount


### KeeperMaxLatency


### KeeperMinLatency


### KeeperOpenFileDescriptorCount


### KeeperPacketsReceived


### KeeperPacketsSent


### KeeperPathsWatched


### KeeperSessionWithWatches


### KeeperSyncedFollowers


### KeeperTargetCommitLogIdx


### KeeperTCPRejectedConnections


### KeeperTCPSecureRejectedConnections


### KeeperTCPSecureThreads


### KeeperTCPThreads


### KeeperWatchCount


### KeeperZnodeCount


### KeeperZxid


### LoadAverage1


### LoadAverage15


### LoadAverage5


### LongestRunningMerge


### MaxPartCountForPartition


### MemoryCode


### MemoryDataAndStack


### MemoryResident


### MemoryResidentMax


### MemoryResidentWithoutPageCache


### MemoryShared


### MemoryVirtual


### MySQLRejectedConnections


### MySQLThreads


### NetworkReceiveBytes_*interface_name*


### NetworkReceiveDrop_*interface_name*


### NetworkReceiveErrors_*interface_name*


### NetworkReceivePackets_*interface_name*


### NetworkSendBytes_*interface_name*


### NetworkSendDrop_*interface_name*


### NetworkSendErrors_*interface_name*


### NetworkSendPackets_*interface_name*


### NetworkTCPReceiveQueue


### NetworkTCPSocketRemoteAddresses


### NetworkTCPSockets


### NetworkTCPSockets_*описание*


### NetworkTCPTransmitQueue


### NetworkTCPUnrecoveredRetransmits


### NumberOfDatabases


### NumberOfDetachedByUserParts


### NumberOfDetachedParts


### NumberOfPendingMutations


### NumberOfPendingMutationsOverExecutionTime


### NumberOfTables


### NumberOfTablesSystem


### Переключения контекста ОС


### OSCPUOverload


### OSGuestNiceTime*cpu_suffix*


### OSGuestNiceTimeNormalized


### OSGuestTime*cpu_suffix*


### OSGuestTimeNormalized


### Время простоя ОС *cpu_suffix*


### OSIdleTimeNormalized


### Прерывания ОС


### OSIOWaitTime*cpu_suffix*


### OSIOWaitTimeNormalized


### OSIrqTime*cpu_suffix*


### OSIrqTimeNormalized


### Доступная память ОС


### OSMemoryBuffers


### OSMemoryCached


### OSMemoryFreePlusCached


### OSMemoryFreeWithoutCached


### OSMemorySwapCached


### OSMemoryTotal


### OSNiceTime*cpu_suffix*


### OSNiceTimeNormalized


### OSOpenFiles


### OSProcessesBlocked


### OSProcessesCreated


### OSProcessesRunning


### OSSoftIrqTime*cpu_suffix*


### OSSoftIrqTimeNormalized


### OSStealTime*cpu_suffix*


### OSStealTimeNormalized


### OSSystemTime*cpu_suffix*


### OSSystemTimeNormalized


### OSThreadsRunnable


### OSThreadsTotal


### OSUptime


### OSUserTime*cpu_suffix*


### OSUserTimeNormalized


### PageCacheMaxBytes


### PostgreSQLRejectedConnections


### PostgreSQLThreads


### ProcessSignalQueueLimit


### ProcessSignalQueueSize


### PrometheusRejectedConnections


### PrometheusThreads


### PSI_*type*_*stall_type*


### Использование памяти запросами


### QueriesPeakMemoryUsage


### ReplicasMaxAbsoluteDelay


### ReplicasMaxInsertsInQueue


### ReplicasMaxMergesInQueue


### ReplicasMaxQueueSize


### ReplicasMaxRelativeDelay


### ReplicasSumInsertsInQueue


### ReplicasSumMergesInQueue


### ReplicasSumQueueSize


### TCPRejectedConnections


### TCPSecureRejectedConnections


### TCPSecureThreads


### TCPThreads


### Температура*i*


### Температура_*hwmon_name*


### Температура_*hwmon_name*_*sensor_name*


### Общее количество байтов во всех таблицах семейства MergeTree


### TotalBytesOfMergeTreeTablesSystem


### TotalIndexGranularityBytesInMemory


### TotalIndexGranularityBytesInMemoryAllocated


### TotalPartsOfMergeTreeTables


### TotalPartsOfMergeTreeTablesSystem


### TotalPrimaryKeyBytesInMemory


### TotalPrimaryKeyBytesInMemoryAllocated


### TotalProjectionIndexGranularityBytesInMemory


### TotalProjectionIndexGranularityBytesInMemoryAllocated


### TotalProjectionPrimaryKeyBytesInMemory


### TotalProjectionPrimaryKeyBytesInMemoryAllocated


### TotalRowsOfMergeTreeTables


### TotalRowsOfMergeTreeTablesSystem


### TotalUncompressedBytesOfMergeTreeTables


### TotalUncompressedBytesOfMergeTreeTablesSystem


### TrackedMemory


### Время непрерывной работы


### VMMaxMapCount


### VMNumMaps


### ZooKeeperClientLastZXIDSeen

- [Мониторинг](https://clickhouse.com/docs/ru/guides/oss/deployment-and-scaling/monitoring/monitoring) — Основные понятия мониторинга ClickHouse.
- [system.metrics](https://clickhouse.com/docs/ru/reference/system-tables/metrics) — Содержит метрики, вычисляемые мгновенно.
- [system.events](https://clickhouse.com/docs/ru/reference/system-tables/events) — Содержит ряд произошедших событий.
- [system.metric_log](https://clickhouse.com/docs/ru/reference/system-tables/metric_log) — Содержит историю значений метрик из таблиц `system.metrics` и `system.events`.
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
