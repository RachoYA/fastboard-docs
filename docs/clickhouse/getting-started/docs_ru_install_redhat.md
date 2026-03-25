# Установка ClickHouse в дистрибутивах Linux, основанных на RPM | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/install/redhat

Рекомендуется использовать официальные предварительно скомпилированные пакетыrpmдляCentOS,RedHatи всех других Linux-дистрибутивов на основе RPM.


## Настройка RPM-репозитория​

Добавьте официальный репозиторий, выполнив следующие команды:sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://packages.clickhouse.com/rpm/clickhouse.repoДля систем с пакетным менеджеромzypper(openSUSE, SLES) выполните:sudo zypper addrepo -r https://packages.clickhouse.com/rpm/clickhouse.repo -g
sudo zypper --gpg-auto-import-keys refresh clickhouse-stableВ последующих шагах командуyum installможно заменить наzypper installв зависимости
от используемого пакетного менеджера.


```
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://packages.clickhouse.com/rpm/clickhouse.repo

```

Для систем с пакетным менеджеромzypper(openSUSE, SLES) выполните:sudo zypper addrepo -r https://packages.clickhouse.com/rpm/clickhouse.repo -g
sudo zypper --gpg-auto-import-keys refresh clickhouse-stableВ последующих шагах командуyum installможно заменить наzypper installв зависимости
от используемого пакетного менеджера.


```
sudo zypper addrepo -r https://packages.clickhouse.com/rpm/clickhouse.repo -g
sudo zypper --gpg-auto-import-keys refresh clickhouse-stable

```

В последующих шагах командуyum installможно заменить наzypper installв зависимости
от используемого пакетного менеджера.


## Установка сервера и клиента ClickHouse​

Установите ClickHouse, выполнив следующие команды:sudo yum install -y clickhouse-server clickhouse-clientВы можете заменитьstableнаlts, чтобы использовать другойтип релизав зависимости от ваших потребностей.Вы можете загрузить и установить пакеты вручную по адресуpackages.clickhouse.com/rpm.Чтобы указать конкретную версию, добавьте-$versionв конец имени пакета,
например:sudo yum install clickhouse-server-22.8.7.34


```
sudo yum install -y clickhouse-server clickhouse-client

```

- Вы можете заменитьstableнаlts, чтобы использовать другойтип релизав зависимости от ваших потребностей.
- Вы можете загрузить и установить пакеты вручную по адресуpackages.clickhouse.com/rpm.
- Чтобы указать конкретную версию, добавьте-$versionв конец имени пакета,
например:

```
sudo yum install clickhouse-server-22.8.7.34

```


## Запуск сервера ClickHouse​

Чтобы запустить сервер ClickHouse, выполните:sudo systemctl enable clickhouse-server
sudo systemctl start clickhouse-server
sudo systemctl status clickhouse-serverЧтобы запустить клиент ClickHouse, выполните:clickhouse-clientЕсли вы задали пароль для вашего сервера, вам потребуется выполнить:clickhouse-client --password


```
sudo systemctl enable clickhouse-server
sudo systemctl start clickhouse-server
sudo systemctl status clickhouse-server

```

Чтобы запустить клиент ClickHouse, выполните:clickhouse-clientЕсли вы задали пароль для вашего сервера, вам потребуется выполнить:clickhouse-client --password


```
clickhouse-client

```

Если вы задали пароль для вашего сервера, вам потребуется выполнить:clickhouse-client --password


```
clickhouse-client --password

```


## Установка автономного ClickHouse Keeper​

В продуктивных средах мы настоятельно рекомендуем запускать ClickHouse Keeper на отдельных узлах.
В тестовых средах, если вы решите запускать ClickHouse Server и ClickHouse Keeper на одном и том же сервере,
то вам не нужно устанавливать ClickHouse Keeper отдельно, так как он включен в состав ClickHouse Server.

Чтобы установитьclickhouse-keeperна отдельных серверах ClickHouse Keeper, выполните:sudo yum install -y clickhouse-keeper


```
sudo yum install -y clickhouse-keeper

```


## Включение и запуск ClickHouse Keeper​


```
sudo systemctl enable clickhouse-keeper
sudo systemctl start clickhouse-keeper
sudo systemctl status clickhouse-keeper

```
