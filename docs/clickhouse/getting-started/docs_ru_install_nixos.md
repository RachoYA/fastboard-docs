# Установка ClickHouse на NixOS | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/install/nixos

ClickHouse доступен в репозитории Nixpkgs и может быть установлен с помощью Nix вLinuxиmacOS.


## Установка ClickHouse с помощью Nix​

Вы можете использовать Nix, чтобы установить ClickHouse, не добавляя его в систему на постоянной основе:# Установить последнюю стабильную версию
nix shell nixpkgs#clickhouse

# Или установить LTS-версию
nix shell nixpkgs#clickhouse-ltsПосле этого исполняемый файлclickhouseбудет доступен в текущей сессии оболочки.Пакетnixpkgs#clickhouseпредоставляет последнюю стабильную версию.Пакетnixpkgs#clickhouse-ltsпредоставляет версию с долгосрочной поддержкой (Long Term Support).Оба пакета работают в Linux и macOS.


```
# Установить последнюю стабильную версию
nix shell nixpkgs#clickhouse

# Или установить LTS-версию
nix shell nixpkgs#clickhouse-lts

```

После этого исполняемый файлclickhouseбудет доступен в текущей сессии оболочки.Пакетnixpkgs#clickhouseпредоставляет последнюю стабильную версию.Пакетnixpkgs#clickhouse-ltsпредоставляет версию с долгосрочной поддержкой (Long Term Support).Оба пакета работают в Linux и macOS.

- Пакетnixpkgs#clickhouseпредоставляет последнюю стабильную версию.
- Пакетnixpkgs#clickhouse-ltsпредоставляет версию с долгосрочной поддержкой (Long Term Support).
- Оба пакета работают в Linux и macOS.

## Постоянная установка​

Чтобы установить ClickHouse в систему на постоянной основе:Для пользователей NixOSдобавьте вconfiguration.nix:environment.systemPackages = with pkgs; [
  clickhouse
];Затем пересоберите систему:sudo nixos-rebuild switchДля пользователей, не использующих NixOS, установите с помощью профиля Nix:# Установить последнюю стабильную версию
nix profile install nixpkgs#clickhouse

# Или установить LTS-версию
nix profile install nixpkgs#clickhouse-lts

Для пользователей NixOSдобавьте вconfiguration.nix:environment.systemPackages = with pkgs; [
  clickhouse
];Затем пересоберите систему:sudo nixos-rebuild switchДля пользователей, не использующих NixOS, установите с помощью профиля Nix:# Установить последнюю стабильную версию
nix profile install nixpkgs#clickhouse

# Или установить LTS-версию
nix profile install nixpkgs#clickhouse-lts


```
environment.systemPackages = with pkgs; [
  clickhouse
];

```

Затем пересоберите систему:sudo nixos-rebuild switchДля пользователей, не использующих NixOS, установите с помощью профиля Nix:# Установить последнюю стабильную версию
nix profile install nixpkgs#clickhouse

# Или установить LTS-версию
nix profile install nixpkgs#clickhouse-lts


```
sudo nixos-rebuild switch

```

Для пользователей, не использующих NixOS, установите с помощью профиля Nix:# Установить последнюю стабильную версию
nix profile install nixpkgs#clickhouse

# Или установить LTS-версию
nix profile install nixpkgs#clickhouse-lts


```
# Установить последнюю стабильную версию
nix profile install nixpkgs#clickhouse

# Или установить LTS-версию
nix profile install nixpkgs#clickhouse-lts

```


## Запуск сервера ClickHouse​

После установки вы можете запустить сервер ClickHouse:clickhouse-serverПо умолчанию сервер запустится с базовой конфигурацией и будет принимать подключения наlocalhost:9000.Для использования в production-средах на NixOS вы можете настроить ClickHouse как системную службу. Обратитесь круководству NixOSдля доступных параметров конфигурации.


```
clickhouse-server

```

По умолчанию сервер запустится с базовой конфигурацией и будет принимать подключения наlocalhost:9000.Для использования в production-средах на NixOS вы можете настроить ClickHouse как системную службу. Обратитесь круководству NixOSдля доступных параметров конфигурации.

Для использования в production-средах на NixOS вы можете настроить ClickHouse как системную службу. Обратитесь круководству NixOSдля доступных параметров конфигурации.


## Запуск клиента ClickHouse​

Чтобы подключиться к серверу ClickHouse, откройте новый терминал и выполните:clickhouse-client


```
clickhouse-client

```


## О пакете Nix​

Пакет ClickHouse в Nixpkgs содержит:

- clickhouse-server— сервер базы данных ClickHouse
- clickhouse-client— клиент командной строки для подключения к ClickHouse
- clickhouse-local— инструмент для выполнения SQL‑запросов по локальным файлам
- Другие утилиты ClickHouse
Для получения дополнительной информации о пакете ClickHouse в Nixpkgs посетите:

- Пакет ClickHouse в Nixpkgs
- Параметры службы ClickHouse в NixOS