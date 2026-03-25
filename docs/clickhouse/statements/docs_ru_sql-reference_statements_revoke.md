# Оператор REVOKE | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/sql-reference/statements/revoke

Отзывает привилегии у пользователей или ролей.


## Синтаксис​

Отмена привилегий для пользователей


```
REVOKE [ON CLUSTER cluster_name] privilege[(column_name [,...])] [,...] ON {db.table|db.*|*.*|table|*} FROM {user | CURRENT_USER} [,...] | ALL | ALL EXCEPT {user | CURRENT_USER} [,...]

```

Отзыв ролей у пользователей


```
REVOKE [ON CLUSTER cluster_name] [ADMIN OPTION FOR] role [,...] FROM {user | role | CURRENT_USER} [,...] | ALL | ALL EXCEPT {user_name | role_name | CURRENT_USER} [,...]

```


## Описание​

Чтобы отозвать какую‑либо привилегию, вы можете использовать привилегию более широкого уровня, чем та, которую планируете отозвать. Например, если у пользователя есть привилегияSELECT (x,y), администратор может выполнить запросREVOKE SELECT(x,y) ..., илиREVOKE SELECT * ..., или дажеREVOKE ALL PRIVILEGES ..., чтобы отозвать эту привилегию.


### Частичный отзыв привилегий​

Вы можете отозвать часть привилегии. Например, если у пользователя есть привилегияSELECT *.*, вы можете отозвать у него привилегию на чтение данных из некоторой таблицы или базы данных.


## Примеры​

Предоставьте учётной записи пользователяjohnпривилегию SELECT для всех баз данных, кроме базы данныхaccounts:


```
GRANT SELECT ON *.* TO john;
REVOKE SELECT ON accounts.* FROM john;

```

Предоставьте пользователюmiraпривилегию на выборку данных из всех столбцов таблицыaccounts.staff, кроме столбцаwage.


```
GRANT SELECT ON accounts.staff TO mira;
REVOKE SELECT(wage) ON accounts.staff FROM mira;

```

Оригинал статьи
