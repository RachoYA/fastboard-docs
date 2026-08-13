# Бета- и экспериментальные возможности - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/settings/beta-and-experimental-features


## бета-функции

- Находятся в активной разработке и готовятся к выходу в GA
- Основные известные проблемы можно отслеживать на GitHub
- Функциональность может измениться в будущем
- Могут быть включены в ClickHouse Cloud
- Команда ClickHouse поддерживает бета-функции

## Экспериментальные возможности

- Могут никогда не выйти в GA
- Могут быть удалены
- Могут вносить несовместимые изменения
- Функциональность может измениться
- Требуют явного включения
- Команда ClickHouse **не поддерживает** экспериментальные возможности
- Могут не иметь важных функций и документации
- Нельзя включить в ClickHouse Cloud

## Бета-настройки


| Название | По умолчанию |
| --- | --- |
| [enable_join_transitive_predicates](https://clickhouse.com/docs/ru/reference/settings/session-settings#enable_join_transitive_predicates) | `1` |
| [geotoh3_argument_order](https://clickhouse.com/docs/ru/reference/settings/session-settings#geotoh3_argument_order) | `lat_lon` |
| [enable_lightweight_update](https://clickhouse.com/docs/ru/reference/settings/session-settings#enable_lightweight_update) | `1` |
| [allow_experimental_correlated_subqueries](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_correlated_subqueries) | `1` |
| [allow_experimental_delta_lake_writes](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_delta_lake_writes) | `0` |
| [parallel_replicas_count](https://clickhouse.com/docs/ru/reference/settings/session-settings#parallel_replicas_count) | `0` |
| [parallel_replica_offset](https://clickhouse.com/docs/ru/reference/settings/session-settings#parallel_replica_offset) | `0` |
| [parallel_replicas_custom_key](https://clickhouse.com/docs/ru/reference/settings/session-settings#parallel_replicas_custom_key) | “ |
| [parallel_replicas_custom_key_range_lower](https://clickhouse.com/docs/ru/reference/settings/session-settings#parallel_replicas_custom_key_range_lower) | `0` |
| [parallel_replicas_custom_key_range_upper](https://clickhouse.com/docs/ru/reference/settings/session-settings#parallel_replicas_custom_key_range_upper) | `0` |
| [parallel_replicas_filter_pushdown](https://clickhouse.com/docs/ru/reference/settings/session-settings#parallel_replicas_filter_pushdown) | `0` |
| [parallel_replicas_allow_view_over_mergetree](https://clickhouse.com/docs/ru/reference/settings/session-settings#parallel_replicas_allow_view_over_mergetree) | `0` |
| [allow_experimental_database_iceberg](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_database_iceberg) | `0` |
| [allow_experimental_database_unity_catalog](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_database_unity_catalog) | `0` |
| [allow_experimental_database_glue_catalog](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_database_glue_catalog) | `0` |
| [session_timezone](https://clickhouse.com/docs/ru/reference/settings/session-settings#session_timezone) | “ |
| [low_priority_query_wait_time_ms](https://clickhouse.com/docs/ru/reference/settings/session-settings#low_priority_query_wait_time_ms) | `1000` |
| [allow_experimental_nullable_tuple_type](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_nullable_tuple_type) | `0` |
| [allow_experimental_delta_kernel_rs](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_delta_kernel_rs) | `1` |
| [allow_insert_into_iceberg](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_insert_into_iceberg) | `0` |
| [enable_join_runtime_filters](https://clickhouse.com/docs/ru/reference/settings/session-settings#enable_join_runtime_filters) | `1` |


## Экспериментальные настройки


| Название | По умолчанию |
| --- | --- |
| [allow_commit_order_projection](https://clickhouse.com/docs/ru/reference/settings/merge-tree-settings#allow_commit_order_projection) | `0` |
| [allow_experimental_replacing_merge_with_cleanup](https://clickhouse.com/docs/ru/reference/settings/merge-tree-settings#allow_experimental_replacing_merge_with_cleanup) | `0` |
| [allow_experimental_text_index_phrase_search](https://clickhouse.com/docs/ru/reference/settings/merge-tree-settings#allow_experimental_text_index_phrase_search) | `0` |
| [allow_remote_fs_zero_copy_replication](https://clickhouse.com/docs/ru/reference/settings/merge-tree-settings#allow_remote_fs_zero_copy_replication) | `0` |
| [compute_exact_num_defaults_for_sparse_columns](https://clickhouse.com/docs/ru/reference/settings/merge-tree-settings#compute_exact_num_defaults_for_sparse_columns) | `0` |
| [distributed_index_analysis_min_indexes_bytes_to_activate](https://clickhouse.com/docs/ru/reference/settings/merge-tree-settings#distributed_index_analysis_min_indexes_bytes_to_activate) | `1073741824` |
| [distributed_index_analysis_min_parts_to_activate](https://clickhouse.com/docs/ru/reference/settings/merge-tree-settings#distributed_index_analysis_min_parts_to_activate) | `10` |
| [enable_replacing_merge_with_cleanup_for_min_age_to_force_merge](https://clickhouse.com/docs/ru/reference/settings/merge-tree-settings#enable_replacing_merge_with_cleanup_for_min_age_to_force_merge) | `0` |
| [force_read_through_cache_for_merges](https://clickhouse.com/docs/ru/reference/settings/merge-tree-settings#force_read_through_cache_for_merges) | `0` |
| [merge_selector_algorithm](https://clickhouse.com/docs/ru/reference/settings/merge-tree-settings#merge_selector_algorithm) | `Simple` |
| [merge_selector_heuristic_to_lower_max_parts_to_merge_at_once_exponent](https://clickhouse.com/docs/ru/reference/settings/merge-tree-settings#merge_selector_heuristic_to_lower_max_parts_to_merge_at_once_exponent) | `5` |
| [notify_newest_block_number](https://clickhouse.com/docs/ru/reference/settings/merge-tree-settings#notify_newest_block_number) | `0` |
| [packed_skip_index_max_bytes](https://clickhouse.com/docs/ru/reference/settings/merge-tree-settings#packed_skip_index_max_bytes) | `0` |
| [part_moves_between_shards_delay_seconds](https://clickhouse.com/docs/ru/reference/settings/merge-tree-settings#part_moves_between_shards_delay_seconds) | `30` |
| [part_moves_between_shards_enable](https://clickhouse.com/docs/ru/reference/settings/merge-tree-settings#part_moves_between_shards_enable) | `0` |
| [remote_fs_zero_copy_path_compatible_mode](https://clickhouse.com/docs/ru/reference/settings/merge-tree-settings#remote_fs_zero_copy_path_compatible_mode) | `0` |
| [remote_fs_zero_copy_zookeeper_path](https://clickhouse.com/docs/ru/reference/settings/merge-tree-settings#remote_fs_zero_copy_zookeeper_path) | `/clickhouse/zero_copy` |
| [remove_rolled_back_parts_immediately](https://clickhouse.com/docs/ru/reference/settings/merge-tree-settings#remove_rolled_back_parts_immediately) | `1` |
| [use_reader_executor](https://clickhouse.com/docs/ru/reference/settings/session-settings#use_reader_executor) | `0` |
| [reader_executor_use_long_connections](https://clickhouse.com/docs/ru/reference/settings/session-settings#reader_executor_use_long_connections) | `0` |
| [reader_executor_min_bytes_for_seek](https://clickhouse.com/docs/ru/reference/settings/session-settings#reader_executor_min_bytes_for_seek) | `2097152` |
| [reader_executor_max_tail_for_drain](https://clickhouse.com/docs/ru/reference/settings/session-settings#reader_executor_max_tail_for_drain) | `1048576` |
| [query_plan_optimize_join_order_max_searched_plans](https://clickhouse.com/docs/ru/reference/settings/session-settings#query_plan_optimize_join_order_max_searched_plans) | `100000` |
| [query_plan_optimize_join_order_randomize](https://clickhouse.com/docs/ru/reference/settings/session-settings#query_plan_optimize_join_order_randomize) | `0` |
| [ast_fuzzer_runs](https://clickhouse.com/docs/ru/reference/settings/session-settings#ast_fuzzer_runs) | `0` |
| [ast_fuzzer_any_query](https://clickhouse.com/docs/ru/reference/settings/session-settings#ast_fuzzer_any_query) | `0` |
| [allow_fuzz_query_functions](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_fuzz_query_functions) | `0` |
| [reserve_memory](https://clickhouse.com/docs/ru/reference/settings/session-settings#reserve_memory) | `0` |
| [allow_experimental_url_wildcard_from_index_pages](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_url_wildcard_from_index_pages) | `0` |
| [optimize_trivial_count_with_sparsity_filter](https://clickhouse.com/docs/ru/reference/settings/session-settings#optimize_trivial_count_with_sparsity_filter) | `0` |
| [enable_materialized_cte](https://clickhouse.com/docs/ru/reference/settings/session-settings#enable_materialized_cte) | `0` |
| [analyzer_inline_views](https://clickhouse.com/docs/ru/reference/settings/session-settings#analyzer_inline_views) | `0` |
| [allow_experimental_kafka_offsets_storage_in_keeper](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_kafka_offsets_storage_in_keeper) | `0` |
| [automatic_parallel_replicas_mode](https://clickhouse.com/docs/ru/reference/settings/session-settings#automatic_parallel_replicas_mode) | `0` |
| [automatic_parallel_replicas_min_bytes_per_replica](https://clickhouse.com/docs/ru/reference/settings/session-settings#automatic_parallel_replicas_min_bytes_per_replica) | `1048576` |
| [parallel_replicas_plan_based](https://clickhouse.com/docs/ru/reference/settings/session-settings#parallel_replicas_plan_based) | `0` |
| [distributed_index_analysis](https://clickhouse.com/docs/ru/reference/settings/session-settings#distributed_index_analysis) | `0` |
| [allow_experimental_materialized_postgresql_table](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_materialized_postgresql_table) | `0` |
| [allow_experimental_funnel_functions](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_funnel_functions) | `0` |
| [allow_experimental_nlp_functions](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_nlp_functions) | `0` |
| [allow_experimental_hash_functions](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_hash_functions) | `0` |
| [allow_experimental_time_series_table](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_time_series_table) | `0` |
| [unique_key_max_encoded_size](https://clickhouse.com/docs/ru/reference/settings/session-settings#unique_key_max_encoded_size) | `256` |
| [allow_experimental_unique_key](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_unique_key) | `0` |
| [allow_experimental_codecs](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_codecs) | `0` |
| [throw_on_unsupported_query_inside_transaction](https://clickhouse.com/docs/ru/reference/settings/session-settings#throw_on_unsupported_query_inside_transaction) | `1` |
| [wait_changes_become_visible_after_commit_mode](https://clickhouse.com/docs/ru/reference/settings/session-settings#wait_changes_become_visible_after_commit_mode) | `wait_unknown` |
| [implicit_transaction](https://clickhouse.com/docs/ru/reference/settings/session-settings#implicit_transaction) | `0` |
| [grace_hash_join_initial_buckets](https://clickhouse.com/docs/ru/reference/settings/session-settings#grace_hash_join_initial_buckets) | `1` |
| [grace_hash_join_max_buckets](https://clickhouse.com/docs/ru/reference/settings/session-settings#grace_hash_join_max_buckets) | `1024` |
| [join_to_sort_minimum_perkey_rows](https://clickhouse.com/docs/ru/reference/settings/session-settings#join_to_sort_minimum_perkey_rows) | `40` |
| [join_to_sort_maximum_table_rows](https://clickhouse.com/docs/ru/reference/settings/session-settings#join_to_sort_maximum_table_rows) | `10000` |
| [allow_experimental_join_right_table_sorting](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_join_right_table_sorting) | `0` |
| [allow_experimental_json_lazy_type_hints](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_json_lazy_type_hints) | `0` |
| [enable_streaming_queries](https://clickhouse.com/docs/ru/reference/settings/session-settings#enable_streaming_queries) | `0` |
| [allow_experimental_window_view](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_window_view) | `0` |
| [window_view_clean_interval](https://clickhouse.com/docs/ru/reference/settings/session-settings#window_view_clean_interval) | `60` |
| [window_view_heartbeat_interval](https://clickhouse.com/docs/ru/reference/settings/session-settings#window_view_heartbeat_interval) | `15` |
| [wait_for_window_view_fire_signal_timeout](https://clickhouse.com/docs/ru/reference/settings/session-settings#wait_for_window_view_fire_signal_timeout) | `10` |
| [stop_refreshable_materialized_views_on_startup](https://clickhouse.com/docs/ru/reference/settings/session-settings#stop_refreshable_materialized_views_on_startup) | `0` |
| [allow_experimental_database_materialized_postgresql](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_database_materialized_postgresql) | `0` |
| [allow_experimental_database_hms_catalog](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_database_hms_catalog) | `0` |
| [allow_experimental_kusto_dialect](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_kusto_dialect) | `0` |
| [allow_experimental_prql_dialect](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_prql_dialect) | `0` |
| [allow_experimental_polyglot_dialect](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_polyglot_dialect) | `0` |
| [polyglot_dialect](https://clickhouse.com/docs/ru/reference/settings/session-settings#polyglot_dialect) | “ |
| [enable_adaptive_memory_spill_scheduler](https://clickhouse.com/docs/ru/reference/settings/session-settings#enable_adaptive_memory_spill_scheduler) | `0` |
| [allow_experimental_cleanup_old_data_files_compaction](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_cleanup_old_data_files_compaction) | `0` |
| [allow_experimental_iceberg_compaction](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_iceberg_compaction) | `0` |
| [iceberg_manifest_min_count_to_compact](https://clickhouse.com/docs/ru/reference/settings/session-settings#iceberg_manifest_min_count_to_compact) | `30` |
| [allow_iceberg_remove_orphan_files](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_iceberg_remove_orphan_files) | `0` |
| [iceberg_orphan_files_older_than_seconds](https://clickhouse.com/docs/ru/reference/settings/session-settings#iceberg_orphan_files_older_than_seconds) | `259200` |
| [allow_experimental_expire_snapshots](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_expire_snapshots) | `0` |
| [write_full_path_in_iceberg_metadata](https://clickhouse.com/docs/ru/reference/settings/session-settings#write_full_path_in_iceberg_metadata) | `0` |
| [iceberg_metadata_compression_method](https://clickhouse.com/docs/ru/reference/settings/session-settings#iceberg_metadata_compression_method) | “ |
| [make_distributed_plan](https://clickhouse.com/docs/ru/reference/settings/session-settings#make_distributed_plan) | `0` |
| [distributed_plan_execute_locally](https://clickhouse.com/docs/ru/reference/settings/session-settings#distributed_plan_execute_locally) | `0` |
| [distributed_plan_default_shuffle_join_bucket_count](https://clickhouse.com/docs/ru/reference/settings/session-settings#distributed_plan_default_shuffle_join_bucket_count) | `8` |
| [distributed_plan_default_reader_bucket_count](https://clickhouse.com/docs/ru/reference/settings/session-settings#distributed_plan_default_reader_bucket_count) | `8` |
| [distributed_plan_workers_num](https://clickhouse.com/docs/ru/reference/settings/session-settings#distributed_plan_workers_num) | `0` |
| [distributed_plan_force_exchange_kind](https://clickhouse.com/docs/ru/reference/settings/session-settings#distributed_plan_force_exchange_kind) | “ |
| [distributed_plan_max_rows_to_broadcast](https://clickhouse.com/docs/ru/reference/settings/session-settings#distributed_plan_max_rows_to_broadcast) | `20000` |
| [distributed_plan_prefer_replicas_over_workers](https://clickhouse.com/docs/ru/reference/settings/session-settings#distributed_plan_prefer_replicas_over_workers) | `0` |
| [allow_experimental_ytsaurus_table_engine](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_ytsaurus_table_engine) | `0` |
| [allow_experimental_ytsaurus_table_function](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_ytsaurus_table_function) | `0` |
| [allow_experimental_ytsaurus_dictionary_source](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_ytsaurus_dictionary_source) | `0` |
| [distributed_plan_force_shuffle_aggregation](https://clickhouse.com/docs/ru/reference/settings/session-settings#distributed_plan_force_shuffle_aggregation) | `0` |
| [join_runtime_filter_exact_values_limit](https://clickhouse.com/docs/ru/reference/settings/session-settings#join_runtime_filter_exact_values_limit) | `10000` |
| [join_runtime_bloom_filter_bytes](https://clickhouse.com/docs/ru/reference/settings/session-settings#join_runtime_bloom_filter_bytes) | `524288` |
| [join_runtime_bloom_filter_hash_functions](https://clickhouse.com/docs/ru/reference/settings/session-settings#join_runtime_bloom_filter_hash_functions) | `3` |
| [join_runtime_filter_pass_ratio_threshold_for_disabling](https://clickhouse.com/docs/ru/reference/settings/session-settings#join_runtime_filter_pass_ratio_threshold_for_disabling) | `0.7` |
| [join_runtime_filter_blocks_to_skip_before_reenabling](https://clickhouse.com/docs/ru/reference/settings/session-settings#join_runtime_filter_blocks_to_skip_before_reenabling) | `30` |
| [join_runtime_bloom_filter_max_ratio_of_set_bits](https://clickhouse.com/docs/ru/reference/settings/session-settings#join_runtime_bloom_filter_max_ratio_of_set_bits) | `0.7` |
| [enable_join_runtime_filters_index_analysis](https://clickhouse.com/docs/ru/reference/settings/session-settings#enable_join_runtime_filters_index_analysis) | `0` |
| [rewrite_in_to_join](https://clickhouse.com/docs/ru/reference/settings/session-settings#rewrite_in_to_join) | `0` |
| [allow_experimental_time_series_aggregate_functions](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_time_series_aggregate_functions) | `0` |
| [promql_database](https://clickhouse.com/docs/ru/reference/settings/session-settings#promql_database) | “ |
| [promql_table](https://clickhouse.com/docs/ru/reference/settings/session-settings#promql_table) | “ |
| [promql_evaluation_time](https://clickhouse.com/docs/ru/reference/settings/session-settings#promql_evaluation_time) | `auto` |
| [allow_experimental_paimon_storage_engine](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_paimon_storage_engine) | `0` |
| [paimon_target_snapshot_id](https://clickhouse.com/docs/ru/reference/settings/session-settings#paimon_target_snapshot_id) | `-1` |
| [max_consume_snapshots](https://clickhouse.com/docs/ru/reference/settings/session-settings#max_consume_snapshots) | `0` |
| [use_paimon_partition_pruning](https://clickhouse.com/docs/ru/reference/settings/session-settings#use_paimon_partition_pruning) | `0` |
| [allow_experimental_object_storage_queue_hive_partitioning](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_object_storage_queue_hive_partitioning) | `0` |
| [query_plan_optimize_join_order_algorithm](https://clickhouse.com/docs/ru/reference/settings/session-settings#query_plan_optimize_join_order_algorithm) | `greedy` |
| [allow_experimental_database_paimon_rest_catalog](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_database_paimon_rest_catalog) | `0` |
| [webassembly_udf_max_fuel](https://clickhouse.com/docs/ru/reference/settings/session-settings#webassembly_udf_max_fuel) | `100000` |
| [webassembly_udf_max_memory](https://clickhouse.com/docs/ru/reference/settings/session-settings#webassembly_udf_max_memory) | `134217728` |
| [webassembly_udf_max_input_block_size](https://clickhouse.com/docs/ru/reference/settings/session-settings#webassembly_udf_max_input_block_size) | `0` |
| [webassembly_udf_max_instances](https://clickhouse.com/docs/ru/reference/settings/session-settings#webassembly_udf_max_instances) | `32` |
| [allow_experimental_eval_table_function](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_eval_table_function) | `0` |
| [allow_experimental_ai_functions](https://clickhouse.com/docs/ru/reference/settings/session-settings#allow_experimental_ai_functions) | `0` |
| [ai_function_request_timeout_sec](https://clickhouse.com/docs/ru/reference/settings/session-settings#ai_function_request_timeout_sec) | `60` |
| [ai_function_max_retries](https://clickhouse.com/docs/ru/reference/settings/session-settings#ai_function_max_retries) | `0` |
| [ai_function_retry_initial_delay_ms](https://clickhouse.com/docs/ru/reference/settings/session-settings#ai_function_retry_initial_delay_ms) | `1000` |
| [ai_function_throw_on_error](https://clickhouse.com/docs/ru/reference/settings/session-settings#ai_function_throw_on_error) | `1` |
| [ai_function_max_input_tokens_per_query](https://clickhouse.com/docs/ru/reference/settings/session-settings#ai_function_max_input_tokens_per_query) | `1000000` |
| [ai_function_max_output_tokens_per_query](https://clickhouse.com/docs/ru/reference/settings/session-settings#ai_function_max_output_tokens_per_query) | `500000` |
| [ai_function_max_api_calls_per_query](https://clickhouse.com/docs/ru/reference/settings/session-settings#ai_function_max_api_calls_per_query) | `0` |
| [ai_function_throw_on_quota_exceeded](https://clickhouse.com/docs/ru/reference/settings/session-settings#ai_function_throw_on_quota_exceeded) | `1` |
| [ai_function_embedding_max_batch_size](https://clickhouse.com/docs/ru/reference/settings/session-settings#ai_function_embedding_max_batch_size) | `100` |
| [ai_function_text_default_credentials](https://clickhouse.com/docs/ru/reference/settings/session-settings#ai_function_text_default_credentials) | “ |
| [ai_function_embedding_default_credentials](https://clickhouse.com/docs/ru/reference/settings/session-settings#ai_function_embedding_default_credentials) | “ |

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
