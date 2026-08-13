# Оператор SET - ClickHouse Documentation

Source: https://clickhouse.com/docs/ru/reference/statements/set


```
SET param = value

```


```
SET profile = 'profile-name-from-the-settings-file'

```


```
-- Эти записи эквивалентны:
SET force_index_by_date = 1
SET force_index_by_date

```


## SET TIME ZONE


```
SET TIME ZONE [=] 'timezone'

```


```
SET TIME ZONE 'UTC';
SET TIME ZONE 'Europe/Amsterdam';
SET TIME ZONE 'America/New_York';

-- Проверить текущий часовой пояс сеанса
SELECT getSetting('session_timezone');

```


## Настройка параметров запроса


```
SET param_name = value

```


```
SET param_id = 42;
SET param_name = 'John';

SELECT * FROM users
WHERE id = {id: UInt32}
AND name = {name: String};

```

Была ли эта страница полезной?


![](https://clickhouse.com/docs/images/icons/icon-mcp.svg)
