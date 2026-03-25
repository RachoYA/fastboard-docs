# Установка ClickHouse на Debian/Ubuntu | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/install/debian_ubuntu

Рекомендуется использовать официальные предварительно скомпилированные пакетыdebдляDebianилиUbuntu.


## Настройка репозитория Debian​

Чтобы установить ClickHouse, выполните следующие команды:# Установите необходимые пакеты
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg

# Скачайте GPG-ключ ClickHouse и сохраните его в хранилище ключей
curl -fsSL 'https://packages.clickhouse.com/rpm/lts/repodata/repomd.xml.key' | sudo gpg --dearmor -o /usr/share/keyrings/clickhouse-keyring.gpg

# Определите архитектуру системы
ARCH=$(dpkg --print-architecture)

# Добавьте репозиторий ClickHouse в источники apt
echo "deb [signed-by=/usr/share/keyrings/clickhouse-keyring.gpg arch=${ARCH}] https://packages.clickhouse.com/deb stable main" | sudo tee /etc/apt/sources.list.d/clickhouse.list

# Обновите списки пакетов apt
sudo apt-get updateВы можете заменитьstableнаlts, чтобы использовать другойтип релизав зависимости от ваших потребностей.Вы можете скачать и установить пакеты вручную сpackages.clickhouse.com.Устаревший способ установки deb-пакетов через дистрибутивы# Установите необходимые пакеты
sudo apt-get install apt-transport-https ca-certificates dirmngr

# Добавьте GPG-ключ ClickHouse для аутентификации пакетов
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 8919F6BD2B48D754

# Добавьте репозиторий ClickHouse в источники apt
echo "deb https://packages.clickhouse.com/deb stable main" | sudo tee \
    /etc/apt/sources.list.d/clickhouse.list
    
# Обновите списки пакетов apt
sudo apt-get update

# Установите пакеты сервера и клиента ClickHouse
sudo apt-get install -y clickhouse-server clickhouse-client

# Запустите службу сервера ClickHouse
sudo service clickhouse-server start

# Запустите клиент командной строки ClickHouse
clickhouse-client # или "clickhouse-client --password", если вы задали пароль.


```
# Установите необходимые пакеты
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg

# Скачайте GPG-ключ ClickHouse и сохраните его в хранилище ключей
curl -fsSL 'https://packages.clickhouse.com/rpm/lts/repodata/repomd.xml.key' | sudo gpg --dearmor -o /usr/share/keyrings/clickhouse-keyring.gpg

# Определите архитектуру системы
ARCH=$(dpkg --print-architecture)

# Добавьте репозиторий ClickHouse в источники apt
echo "deb [signed-by=/usr/share/keyrings/clickhouse-keyring.gpg arch=${ARCH}] https://packages.clickhouse.com/deb stable main" | sudo tee /etc/apt/sources.list.d/clickhouse.list

# Обновите списки пакетов apt
sudo apt-get update

```

- Вы можете заменитьstableнаlts, чтобы использовать другойтип релизав зависимости от ваших потребностей.
- Вы можете скачать и установить пакеты вручную сpackages.clickhouse.com.

```
# Установите необходимые пакеты
sudo apt-get install apt-transport-https ca-certificates dirmngr

# Добавьте GPG-ключ ClickHouse для аутентификации пакетов
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 8919F6BD2B48D754

# Добавьте репозиторий ClickHouse в источники apt
echo "deb https://packages.clickhouse.com/deb stable main" | sudo tee \
    /etc/apt/sources.list.d/clickhouse.list
    
# Обновите списки пакетов apt
sudo apt-get update

# Установите пакеты сервера и клиента ClickHouse
sudo apt-get install -y clickhouse-server clickhouse-client

# Запустите службу сервера ClickHouse
sudo service clickhouse-server start

# Запустите клиент командной строки ClickHouse
clickhouse-client # или "clickhouse-client --password", если вы задали пароль.

```


## Установка сервера и клиента ClickHouse​


```
sudo apt-get install -y clickhouse-server clickhouse-client

```


## Запуск ClickHouse​

Чтобы запустить сервер ClickHouse, выполните:sudo service clickhouse-server startЧтобы запустить клиент ClickHouse, выполните:clickhouse-clientЕсли вы задали пароль для сервера, вам нужно выполнить:clickhouse-client --password


```
sudo service clickhouse-server start

```

Чтобы запустить клиент ClickHouse, выполните:clickhouse-clientЕсли вы задали пароль для сервера, вам нужно выполнить:clickhouse-client --password


```
clickhouse-client

```

Если вы задали пароль для сервера, вам нужно выполнить:clickhouse-client --password


```
clickhouse-client --password

```


## Установка автономного ClickHouse Keeper​

В продакшн-средах мы настоятельно рекомендуем запускать ClickHouse Keeper на выделенных узлах.
В тестовых средах, если вы решили запускать ClickHouse Server и ClickHouse Keeper на одном сервере,
то вам не нужно устанавливать ClickHouse Keeper отдельно, так как он включён в состав сервера ClickHouse.

Чтобы установитьclickhouse-keeperна автономные серверы ClickHouse Keeper, выполните:sudo apt-get install -y clickhouse-keeper


```
sudo apt-get install -y clickhouse-keeper

```


## Включение и запуск ClickHouse Keeper​


```
sudo systemctl enable clickhouse-keeper
sudo systemctl start clickhouse-keeper
sudo systemctl status clickhouse-keeper

```


## Пакеты​

Доступные deb-пакеты описаны ниже:

Если вам нужно установить определенную версию ClickHouse, необходимо установить все пакеты одной и той же версии:sudo apt-get install clickhouse-server=21.8.5.7 clickhouse-client=21.8.5.7 clickhouse-common-static=21.8.5.7
