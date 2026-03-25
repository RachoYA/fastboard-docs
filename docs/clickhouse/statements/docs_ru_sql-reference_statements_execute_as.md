# Оператор EXECUTE AS | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/sql-reference/statements/execute_as

Позволяет выполнять запросы от имени другого пользователя.


## Синтаксис​


```
EXECUTE AS target_user;
EXECUTE AS target_user subquery;

```

Первая форма (безsubquery) означает, что все последующие запросы в текущей сессии будут выполняться от имени указанногоtarget_user.

Вторая форма (сsubquery) выполняет только указанныйsubqueryот имени указанногоtarget_user.

Для работы обеих форм необходимо, чтобы параметр конфигурацииaccess_control_improvements.allow_impersonate_userбыл установлен в значение1, а привилегияIMPERSONATEбыла выдана. Например, следующие команды


```
GRANT IMPERSONATE ON user1 TO user2;
GRANT IMPERSONATE ON * TO user3;

```

позволяет пользователюuser2выполнять командыEXECUTE AS user1 ..., а также позволяет пользователюuser3выполнять команды от имени любого пользователя.

При работе от имени другого пользователя функцияcurrentUser()возвращает имя этого пользователя,
а функцияauthenticatedUser()возвращает имя пользователя, который был фактически аутентифицирован.


## Примеры​


```
SELECT currentUser(), authenticatedUser(); -- outputs "default    default"
CREATE USER james;
EXECUTE AS james SELECT currentUser(), authenticatedUser(); -- outputs "james    default"

```
