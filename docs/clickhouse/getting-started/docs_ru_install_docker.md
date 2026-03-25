# Установка ClickHouse с помощью Docker | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/install/docker

Руководство наDocker Hubприведено ниже для удобства. Доступные Docker-образы используют
официальные deb-пакеты ClickHouse.

Команда docker pull:


```
docker pull clickhouse/clickhouse-server

```


## Versions​

- Тегlatestуказывает на последний релиз последней стабильной ветки.
- Теги веток, такие как22.2, указывают на последний релиз соответствующей ветки.
- Полные теги версий, такие как22.2.3и22.2.3.5, указывают на соответствующий релиз.
- Тегheadсобирается из последнего коммита в ветке по умолчанию.
- У каждого тега есть необязательный суффикс-alpine, который указывает на то, что образ собран на базе Alpine.

### Совместимость​

- Образ amd64 требует поддержкиинструкций SSE3.
Практически все x86-процессоры, выпущенные после 2005 года, поддерживают SSE3.
- Образ arm64 требует поддержкиархитектуры ARMv8.2-Aи
дополнительно регистра Load-Acquire RCpc. Этот регистр является необязательным в версии ARMv8.2-A и обязательным вARMv8.3-A. Поддерживается в Graviton >=2, инстансах Azure и GCP.
Примеры неподдерживаемых устройств: Raspberry Pi 4 (ARMv8.0-A) и Jetson AGX Xavier/Orin (ARMv8.2-A).
- Начиная с ClickHouse 24.11 образы для Ubuntu стали использоватьubuntu:22.04в качестве базового образа. Для этого требуется версия Docker >=20.10.10,
содержащаяпатч. В качестве обходного пути вы можете
использоватьdocker run --security-opt seccomp=unconfined, однако это имеет последствия для безопасности.

## Как использовать этот образ Docker​


### Запуск экземпляра сервера​


```
docker run -d --name some-clickhouse-server --ulimit nofile=262144:262144 clickhouse/clickhouse-server

```

По умолчанию ClickHouse будет доступен только через сеть Docker. См. ниже раздел о сетевом взаимодействии.

По умолчанию запущенный выше экземпляр сервера будет работать от имени пользователяdefaultбез пароля.


### Подключение к нему с помощью нативного клиента​


```
docker run -it --rm --network=container:some-clickhouse-server --entrypoint clickhouse-client clickhouse/clickhouse-server
# OR
docker exec -it some-clickhouse-server clickhouse-client

```

Дополнительные сведения о клиенте ClickHouse см. в разделеClickHouse client.


### Подключитесь к нему через curl​


```
echo "SELECT 'Hello, ClickHouse!'" | docker run -i --rm --network=container:some-clickhouse-server buildpack-deps:curl curl 'http://localhost:8123/?query=' -s --data-binary @-

```

Дополнительные сведения об HTTP‑интерфейсе см. в разделеClickHouse HTTP Interface.


### Остановка и удаление контейнера​


```
docker stop some-clickhouse-server
docker rm some-clickhouse-server

```


### Сетевое взаимодействие​

предопределённый пользовательdefaultне имеет сетевого доступа до тех пор, пока не задан пароль,
см. ниже разделы «How to create default database and user on starting» и «Managingdefaultuser»

Вы можете открыть доступ к вашему ClickHouse, запущенному в Docker,пробросив определённый портизнутри контейнера на порт хоста:


```
docker run -d -p 18123:8123 -p19000:9000 -e CLICKHOUSE_PASSWORD=changeme --name some-clickhouse-server --ulimit nofile=262144:262144 clickhouse/clickhouse-server
echo 'SELECT version()' | curl 'http://localhost:18123/?password=changeme' --data-binary @-

```

Или можно разрешить контейнеру использоватьпорты хоста напрямуюс помощью--network=host(что также позволяет добиться более высокой сетевой производительности):


```
docker run -d --network=host --name some-clickhouse-server --ulimit nofile=262144:262144 clickhouse/clickhouse-server
echo 'SELECT version()' | curl 'http://localhost:8123/' --data-binary @-

```

Пользователь по умолчанию в приведённом выше примере доступен только для запросов с localhost.


### Томa​

Обычно для обеспечения сохранности данных вы можете подключить к контейнеру следующие каталоги:

- /var/lib/clickhouse/— основной каталог, где ClickHouse хранит данные
- /var/log/clickhouse-server/— логи

```
docker run -d \
    -v "$PWD/ch_data:/var/lib/clickhouse/" \
    -v "$PWD/ch_logs:/var/log/clickhouse-server/" \
    --name some-clickhouse-server --ulimit nofile=262144:262144 clickhouse/clickhouse-server

```

Вы также можете смонтировать:

- /etc/clickhouse-server/config.d/*.xml— файлы с дополнительными настройками конфигурации сервера
- /etc/clickhouse-server/users.d/*.xml— файлы с дополнительными настройками пользователей
- /docker-entrypoint-initdb.d/— каталог со скриптами инициализации базы данных (см. ниже).

## Возможности Linux​

ClickHouse обладает некоторыми расширенными возможностями, для которых требуется включение несколькихвозможностей Linux.

Они необязательны и могут быть включены с помощью следующихпараметров командной строки Docker:


```
docker run -d \
    --cap-add=SYS_NICE --cap-add=NET_ADMIN --cap-add=IPC_LOCK \
    --name some-clickhouse-server --ulimit nofile=262144:262144 clickhouse/clickhouse-server

```

Дополнительные сведения см. в разделе"Настройка возможностей CAP_IPC_LOCK и CAP_SYS_NICE в Docker"


## Конфигурация​

Контейнер открывает порт 8123 дляHTTP-интерфейсаи порт 9000 длянативного клиентского протокола.

Конфигурация ClickHouse задаётся файлом «config.xml» (документация)


### Запуск экземпляра сервера с собственной конфигурацией​


```
docker run -d --name some-clickhouse-server --ulimit nofile=262144:262144 -v /path/to/your/config.xml:/etc/clickhouse-server/config.xml clickhouse/clickhouse-server

```


### Запуск сервера от имени другого пользователя​


```
# $PWD/data/clickhouse should exist and be owned by current user
docker run --rm --user "${UID}:${GID}" --name some-clickhouse-server --ulimit nofile=262144:262144 -v "$PWD/logs/clickhouse:/var/log/clickhouse-server" -v "$PWD/data/clickhouse:/var/lib/clickhouse" clickhouse/clickhouse-server

```

При использовании образа с примонтированными локальными каталогами вам, скорее всего, нужно указать пользователя, чтобы сохранить корректные права собственности на файлы. Используйте аргумент--userи примонтируйте/var/lib/clickhouseи/var/log/clickhouse-serverвнутрь контейнера. В противном случае образ будет выдавать ошибку и не запустится.


### Запуск сервера от имени пользователя root​

Запуск сервера от имени пользователя root полезен в случаях, когда включено пространство имен пользователей.
Для этого выполните:


```
docker run --rm -e CLICKHOUSE_RUN_AS_ROOT=1 --name clickhouse-server-userns -v "$PWD/logs/clickhouse:/var/log/clickhouse-server" -v "$PWD/data/clickhouse:/var/lib/clickhouse" clickhouse/clickhouse-server

```


### Как создать базу данных и пользователя по умолчанию при запуске​

Иногда вам может понадобиться создать пользователя (по умолчанию используется пользователь с именемdefault) и базу данных при запуске контейнера. Это можно сделать с помощью переменных окруженияCLICKHOUSE_DB,CLICKHOUSE_USER,CLICKHOUSE_DEFAULT_ACCESS_MANAGEMENTиCLICKHOUSE_PASSWORD:


```
docker run --rm -e CLICKHOUSE_DB=my_database -e CLICKHOUSE_USER=username -e CLICKHOUSE_DEFAULT_ACCESS_MANAGEMENT=1 -e CLICKHOUSE_PASSWORD=password -p 9000:9000/tcp clickhouse/clickhouse-server

```


#### Управление пользователемdefault​

Пользовательdefaultпо умолчанию не имеет сетевого доступа, если ни одна из переменныхCLICKHOUSE_USER,CLICKHOUSE_PASSWORDилиCLICKHOUSE_DEFAULT_ACCESS_MANAGEMENTне установлена.

Существует способ небезопасно сделать пользователяdefaultдоступным, установив переменную окруженияCLICKHOUSE_SKIP_USER_SETUPв значение 1:


```
docker run --rm -e CLICKHOUSE_SKIP_USER_SETUP=1 -p 9000:9000/tcp clickhouse/clickhouse-server

```


## Как расширить этот образ​

Чтобы выполнить дополнительную инициализацию в образе, созданном на основе этого, добавьте один или несколько скриптов*.sql,*.sql.gzили*.shв каталог/docker-entrypoint-initdb.d. После того как точка входа (entrypoint) вызоветinitdb, она запустит все файлы*.sql, выполнит все исполняемые скрипты*.shи подключит (source) все неисполняемые скрипты*.sh, найденные в этом каталоге, для дальнейшей инициализации перед запуском сервиса.

Скрипты в каталоге/docker-entrypoint-initdb.dвыполняются валфавитном порядкепо имени файла. Если ваши скрипты зависят друг от друга (например, скрипт, создающий представления, должен выполняться после скрипта, создающего соответствующие таблицы), убедитесь, что их имена сортируются в правильном порядке.

Также вы можете задать переменные окруженияCLICKHOUSE_USER&CLICKHOUSE_PASSWORD, которые будут использоваться клиентом clickhouse-client во время инициализации.

Например, чтобы добавить ещё одного пользователя и базу данных, добавьте следующее в/docker-entrypoint-initdb.d/init-db.sh:


```
#!/bin/bash
set -e

clickhouse client -n <<-EOSQL
    CREATE DATABASE docker;
    CREATE TABLE docker.docker (x Int32) ENGINE = MergeTree
    ORDER BY ();
EOSQL

```
