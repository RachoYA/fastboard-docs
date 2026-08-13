# Семейство движков MergeTree - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/index


| Страница | Описание |
| --- | --- |
| [Движок таблицы MergeTree](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/mergetree) | Движки таблиц семейства `MergeTree` предназначены для высокой скорости приёма данных и работы с огромными объёмами данных. |
| [Движки таблиц Replicated*](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/replication) | Обзор репликации данных в ClickHouse с использованием семейства движков таблиц Replicated* |
| [Пользовательский ключ партиционирования](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/custom-partitioning-key) | Узнайте, как добавить пользовательский ключ партиционирования в таблицы MergeTree. |
| [Движок таблицы ReplacingMergeTree](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/replacingmergetree) | Отличается от MergeTree тем, что удаляет повторяющиеся записи с одинаковым значением ключа сортировки (раздел таблицы `ORDER BY`, а не `PRIMARY KEY`). |
| [Движок таблицы CoalescingMergeTree](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/coalescingmergetree) | CoalescingMergeTree наследуется от движка MergeTree. Его ключевая возможность — автоматически сохранять последнее ненулевое значение каждого столбца при слиянии частей. |
| [Движок таблицы SummingMergeTree](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/summingmergetree) | SummingMergeTree наследуется от движка MergeTree. Его ключевая возможность — автоматически суммировать числовые данные при слиянии частей. |
| [Движок таблицы AggregatingMergeTree](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/aggregatingmergetree) | Заменяет все строки с одинаковым первичным ключом (или, точнее, с одинаковым [ключом сортировки](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/mergetree)) одной строкой (в пределах одной части данных), которая хранит комбинацию состояний агрегатных функций. |
| [Движок таблицы CollapsingMergeTree](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/collapsingmergetree) | Наследуется от MergeTree, но добавляет логику схлопывания строк в процессе слияния. |
| [Движок таблицы VersionedCollapsingMergeTree](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/versionedcollapsingmergetree) | Позволяет быстро записывать постоянно изменяющиеся состояния объектов и удалять старые состояния объектов в фоновом режиме. |
| [Движок таблицы GraphiteMergeTree](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/graphitemergetree) | Предназначен для прореживания и агрегирования/усреднения (rollup) данных Graphite. |
| [Точный и приблизительный векторный поиск](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/annindexes) | Документация по точному и приблизительному векторному поиску |
| [Полнотекстовый поиск с текстовыми индексами](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/textindexes) | Быстрый поиск терминов в тексте. |

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
