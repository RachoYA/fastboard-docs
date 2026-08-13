# Оператор легковесного UPDATE - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/statements/update


```
UPDATE [db.]table [ON CLUSTER cluster] SET column1 = expr1 [, ...] [IN PARTITION partition_expr] WHERE filter_expr;

```


## Примеры


```
UPDATE hits SET Title = 'Updated Title' WHERE EventDate = today();

UPDATE wikistat SET hits = hits + 1, time = now() WHERE path = 'ClickHouse';

```


## Легковесные обновления не обновляют данные сразу

- **Сразу видны** в запросах `SELECT` за счёт применения патчей
- **Физически материализуются** только во время последующих слияний и мутаций
- **Автоматически удаляются** после того, как патчи будут материализованы во всех активных частях

## Требования к легковесным обновлениям


## Легковесные удаления


## Особенности производительности

- Задержка обновления сопоставима с задержкой запроса `INSERT ... SELECT ...`
- Записываются только обновлённые столбцы и значения, а не столбцы целиком в частях данных
- Не нужно ждать завершения уже выполняющихся слияний/мутаций, поэтому задержка обновления предсказуема
- Возможно параллельное выполнение легковесных обновлений
- Добавляют накладные расходы для запросов `SELECT`, в которых нужно применять патчи
- [Индексы пропуска данных](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/mergetree#table_engine-mergetree-data_skipping-indexes) не будут использоваться для столбцов в частях данных, к которым нужно применить патчи. [Проекции](https://clickhouse.com/docs/ru/reference/engines/table-engines/mergetree-family/mergetree#projections) не будут использоваться, если у таблицы есть патч-части, в том числе для частей данных, к которым патчи применять не нужно.
- Небольшие, но слишком частые обновления могут привести к ошибке “слишком много частей”. Рекомендуется объединять несколько обновлений в один запрос, например поместив идентификаторы обновляемых строк в одно условие `IN` в `WHERE`
- Легковесные обновления рассчитаны на обновление небольшого количества строк (примерно до 10% таблицы). Если нужно обновить больший объём данных, рекомендуется использовать мутацию [`ALTER TABLE ... UPDATE`](https://clickhouse.com/docs/ru/reference/statements/alter/update)

## Параллельные операции


## Разрешения для UPDATE


```
GRANT ALTER UPDATE ON db.table TO username;

```


## Детали реализации

- `_part` - имя исходной части
- `_part_offset` - номер строки в исходной части
- `_block_number` - номер блока строки в исходной части
- `_block_offset` - смещение строки в блоке исходной части
- `_data_version` - версия обновлённых данных (номер блока, выделенный для запроса `UPDATE`)
- если `X` содержит саму часть `A`. Это происходит, если `A` не участвовала в слиянии на момент выполнения `UPDATE`.
- если `X` содержит части `B` и `C`, которые покрываются частью `A`. Это происходит, если на момент выполнения `UPDATE` выполнялось слияние (`B`, `C`) -> `A`.
- Использование слияния по отсортированным столбцам `_part`, `_part_offset`.
- Использование JOIN по столбцам `_block_number`, `_block_offset`.

## Связанные материалы

- [`ALTER UPDATE`](https://clickhouse.com/docs/ru/reference/statements/alter/update) — тяжёлые операции `UPDATE`
- [Легковесный `DELETE`](https://clickhouse.com/docs/ru/reference/statements/delete) — операции легковесного `DELETE`
- [`APPLY PATCHES`](https://clickhouse.com/docs/ru/reference/statements/alter/apply-patches) — принудительная физическая материализация патчей в частях данных (операция мутации)
Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
