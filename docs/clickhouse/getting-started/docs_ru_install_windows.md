# Установка ClickHouse на Windows в среде WSL | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/install/windows


## Требования​

Для установки ClickHouse на Windows вам понадобится WSL (Windows Subsystem for Linux).


## Установите WSL​

Откройте Windows PowerShell от имени администратора и выполните следующую команду:wsl --installВас попросят ввести новое имя пользователя и пароль UNIX. После того как вы
введёте желаемые имя пользователя и пароль, вы должны увидеть сообщение, похожее на:Welcome to Ubuntu 24.04.1 LTS (GNU/Linux 5.15.133.1-microsoft-WSL2 x86_64)


```
wsl --install

```

Вас попросят ввести новое имя пользователя и пароль UNIX. После того как вы
введёте желаемые имя пользователя и пароль, вы должны увидеть сообщение, похожее на:Welcome to Ubuntu 24.04.1 LTS (GNU/Linux 5.15.133.1-microsoft-WSL2 x86_64)


```
Welcome to Ubuntu 24.04.1 LTS (GNU/Linux 5.15.133.1-microsoft-WSL2 x86_64)

```


## Установите ClickHouse с помощью скрипта через curl​

Выполните следующую команду, чтобы установить ClickHouse с помощью скрипта через curl:curl https://clickhouse.com/ | shЕсли скрипт был успешно выполнен, вы увидите сообщение:Successfully downloaded the ClickHouse binary, you can run it as:
  ./clickhouse


```
curl https://clickhouse.com/ | sh

```

Если скрипт был успешно выполнен, вы увидите сообщение:Successfully downloaded the ClickHouse binary, you can run it as:
  ./clickhouse


```
Successfully downloaded the ClickHouse binary, you can run it as:
  ./clickhouse

```


## Запустите clickhouse-local​

clickhouse-localпозволяет обрабатывать локальные и удалённые файлы, используя
мощный SQL-синтаксис ClickHouse, без необходимости в конфигурации. Данные таблиц
хранятся во временном каталоге, поэтому после перезапускаclickhouse-localранее созданные таблицы больше недоступны.Выполните следующую команду, чтобы запуститьclickhouse-local:./clickhouse

Выполните следующую команду, чтобы запуститьclickhouse-local:./clickhouse


```
./clickhouse

```


## Запустите clickhouse-server​

Если вы хотите сохранять данные, вам потребуется запуститьclickhouse-server. Вы можете
запустить сервер ClickHouse с помощью следующей команды:./clickhouse server


```
./clickhouse server

```


## Start clickhouse-client​

При работающем сервере откройте новое окно терминала и выполните следующую команду
для запускаclickhouse-client:./clickhouse clientВы увидите примерно следующее:./clickhouse client
ClickHouse client version 24.5.1.117 (official build).
Connecting to localhost:9000 as user default.
Connected to ClickHouse server version 24.5.1.

local-host :)Данные таблиц хранятся в текущем каталоге и остаются доступными после перезапуска
сервера ClickHouse. При необходимости можно передать-C config.xmlв качестве дополнительного аргумента командной строки для./clickhouse serverи задать дополнительные параметры в файле
конфигурации. Все доступные параметры конфигурации описаныздесьи вшаблоне файла
конфигурации.Теперь можно отправлять SQL-команды в ClickHouse!


```
./clickhouse client

```

Вы увидите примерно следующее:./clickhouse client
ClickHouse client version 24.5.1.117 (official build).
Connecting to localhost:9000 as user default.
Connected to ClickHouse server version 24.5.1.

local-host :)Данные таблиц хранятся в текущем каталоге и остаются доступными после перезапуска
сервера ClickHouse. При необходимости можно передать-C config.xmlв качестве дополнительного аргумента командной строки для./clickhouse serverи задать дополнительные параметры в файле
конфигурации. Все доступные параметры конфигурации описаныздесьи вшаблоне файла
конфигурации.Теперь можно отправлять SQL-команды в ClickHouse!


```
./clickhouse client
ClickHouse client version 24.5.1.117 (official build).
Connecting to localhost:9000 as user default.
Connected to ClickHouse server version 24.5.1.

local-host :)

```

Данные таблиц хранятся в текущем каталоге и остаются доступными после перезапуска
сервера ClickHouse. При необходимости можно передать-C config.xmlв качестве дополнительного аргумента командной строки для./clickhouse serverи задать дополнительные параметры в файле
конфигурации. Все доступные параметры конфигурации описаныздесьи вшаблоне файла
конфигурации.Теперь можно отправлять SQL-команды в ClickHouse!

Теперь можно отправлять SQL-команды в ClickHouse!
