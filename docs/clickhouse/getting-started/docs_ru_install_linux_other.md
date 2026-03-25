# Установка ClickHouse с использованием архивов tgz | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/install/linux_other

Рекомендуется использовать официальные предварительно скомпилированные архивыtgzдля всех дистрибутивов Linux, где установка пакетовdebилиrpmневозможна.


## Загрузка и установка последней стабильной версии​

Необходимую версию можно загрузить с помощьюcurlилиwgetиз репозиторияhttps://packages.clickhouse.com/tgz/.
После этого загруженные архивы нужно распаковать и установить с помощью установочных скриптов.Ниже приведён пример установки последней стабильной версии.ПримечаниеДля продакшн-сред рекомендуется использовать последнюю версиюstable.
Найти номер релиза можно на этойстранице GitHubс постфиксом-stable.

Ниже приведён пример установки последней стабильной версии.ПримечаниеДля продакшн-сред рекомендуется использовать последнюю версиюstable.
Найти номер релиза можно на этойстранице GitHubс постфиксом-stable.

Для продакшн-сред рекомендуется использовать последнюю версиюstable.
Найти номер релиза можно на этойстранице GitHubс постфиксом-stable.


## Получение последней версии ClickHouse​

Получите последнюю версию ClickHouse с GitHub и сохраните её в переменнуюLATEST_VERSION.LATEST_VERSION=$(curl -s https://raw.githubusercontent.com/ClickHouse/ClickHouse/master/utils/list-versions/version_date.tsv | \
    grep -Eo '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | sort -V -r | head -n 1)
export LATEST_VERSION


```
LATEST_VERSION=$(curl -s https://raw.githubusercontent.com/ClickHouse/ClickHouse/master/utils/list-versions/version_date.tsv | \
    grep -Eo '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | sort -V -r | head -n 1)
export LATEST_VERSION

```


## Определение архитектуры системы​

Определите архитектуру системы и соответствующим образом задайте переменную ARCH:case $(uname -m) in
  x86_64) ARCH=amd64 ;;         # Для 64-битных процессоров Intel/AMD
  aarch64) ARCH=arm64 ;;        # Для 64-битных процессоров ARM
  *) echo "Unknown architecture $(uname -m)"; exit 1 ;; # Завершить работу, если архитектура не поддерживается
esac


```
case $(uname -m) in
  x86_64) ARCH=amd64 ;;         # Для 64-битных процессоров Intel/AMD
  aarch64) ARCH=arm64 ;;        # Для 64-битных процессоров ARM
  *) echo "Unknown architecture $(uname -m)"; exit 1 ;; # Завершить работу, если архитектура не поддерживается
esac

```


## Загрузка tar-архивов для каждого компонента ClickHouse​

Загрузите tar-архивы для каждого компонента ClickHouse. Цикл сначала пытается скачать архитектурно-специфичные
пакеты, затем при необходимости переходит к универсальным.for PKG in clickhouse-common-static clickhouse-common-static-dbg clickhouse-server clickhouse-client clickhouse-keeper
do
  curl -fO "https://packages.clickhouse.com/tgz/stable/$PKG-$LATEST_VERSION-${ARCH}.tgz" \
    || curl -fO "https://packages.clickhouse.com/tgz/stable/$PKG-$LATEST_VERSION.tgz"
done


```
for PKG in clickhouse-common-static clickhouse-common-static-dbg clickhouse-server clickhouse-client clickhouse-keeper
do
  curl -fO "https://packages.clickhouse.com/tgz/stable/$PKG-$LATEST_VERSION-${ARCH}.tgz" \
    || curl -fO "https://packages.clickhouse.com/tgz/stable/$PKG-$LATEST_VERSION.tgz"
done

```


## Распаковка и установка пакетов​

Выполните приведённые ниже команды для распаковки и установки следующих пакетов:clickhouse-common-static# Распаковать и установить пакет clickhouse-common-static
tar -xzvf "clickhouse-common-static-$LATEST_VERSION-${ARCH}.tgz" \
  || tar -xzvf "clickhouse-common-static-$LATEST_VERSION.tgz"
sudo "clickhouse-common-static-$LATEST_VERSION/install/doinst.sh"clickhouse-common-static-dbg# Распаковать и установить пакет с отладочными символами
tar -xzvf "clickhouse-common-static-dbg-$LATEST_VERSION-${ARCH}.tgz" \
  || tar -xzvf "clickhouse-common-static-dbg-$LATEST_VERSION.tgz"
sudo "clickhouse-common-static-dbg-$LATEST_VERSION/install/doinst.sh"clickhouse-server# Распаковать и установить серверный пакет с конфигурацией
tar -xzvf "clickhouse-server-$LATEST_VERSION-${ARCH}.tgz" \
  || tar -xzvf "clickhouse-server-$LATEST_VERSION.tgz"
sudo "clickhouse-server-$LATEST_VERSION/install/doinst.sh" configure
sudo /etc/init.d/clickhouse-server start  # Запустить серверclickhouse-client# Распаковать и установить клиентский пакет
tar -xzvf "clickhouse-client-$LATEST_VERSION-${ARCH}.tgz" \
  || tar -xzvf "clickhouse-client-$LATEST_VERSION.tgz"
sudo "clickhouse-client-$LATEST_VERSION/install/doinst.sh"

- clickhouse-common-static

```
# Распаковать и установить пакет clickhouse-common-static
tar -xzvf "clickhouse-common-static-$LATEST_VERSION-${ARCH}.tgz" \
  || tar -xzvf "clickhouse-common-static-$LATEST_VERSION.tgz"
sudo "clickhouse-common-static-$LATEST_VERSION/install/doinst.sh"

```

- clickhouse-common-static-dbg

```
# Распаковать и установить пакет с отладочными символами
tar -xzvf "clickhouse-common-static-dbg-$LATEST_VERSION-${ARCH}.tgz" \
  || tar -xzvf "clickhouse-common-static-dbg-$LATEST_VERSION.tgz"
sudo "clickhouse-common-static-dbg-$LATEST_VERSION/install/doinst.sh"

```

- clickhouse-server

```
# Распаковать и установить серверный пакет с конфигурацией
tar -xzvf "clickhouse-server-$LATEST_VERSION-${ARCH}.tgz" \
  || tar -xzvf "clickhouse-server-$LATEST_VERSION.tgz"
sudo "clickhouse-server-$LATEST_VERSION/install/doinst.sh" configure
sudo /etc/init.d/clickhouse-server start  # Запустить сервер

```

- clickhouse-client

```
# Распаковать и установить клиентский пакет
tar -xzvf "clickhouse-client-$LATEST_VERSION-${ARCH}.tgz" \
  || tar -xzvf "clickhouse-client-$LATEST_VERSION.tgz"
sudo "clickhouse-client-$LATEST_VERSION/install/doinst.sh"

```
