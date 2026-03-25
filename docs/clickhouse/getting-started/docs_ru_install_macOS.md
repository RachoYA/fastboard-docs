# Установка ClickHouse с помощью Homebrew | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/install/macOS

Установка с использованием формулы Homebrew устарела и будет отключена 2026-09-01.
Мы рекомендуем вместо этого использовать методбыстрой установки, который работает на любой платформе.


## Установка с использованием community-формулы Homebrew​

Чтобы установить ClickHouse на macOS с помощьюHomebrew, вы можете использоватьформулу Homebrew, поддерживаемую сообществом ClickHouse.brew install --cask clickhouse


```
brew install --cask clickhouse

```


## Исправление ошибки проверки разработчика в macOS​

Если вы устанавливаете ClickHouse с помощьюbrew, вы можете столкнуться с ошибкой со стороны macOS.
По умолчанию macOS не запускает приложения или инструменты, созданные разработчиком, подлинность которого не может быть подтверждена.При попытке выполнить любую командуclickhouseвы можете увидеть такую ошибку:Чтобы обойти эту ошибку проверки, нужно убрать приложение из карантина macOS — либо найдя соответствующую настройку в окнеSystem Settings, используя терминал, либо переустановив ClickHouse.Процесс через системные настройки​Самый простой способ убрать исполняемый файлclickhouseиз карантина:ОткройтеSystem Settings.Перейдите вPrivacy & Security:Пролистайте окно вниз до сообщения вида"clickhouse-macos-aarch64" was blocked from use because it is not from an identified developer".НажмитеAllow Anyway.Введите пароль пользователя macOS.Теперь вы должны иметь возможность запускать командыclickhouseв терминале.Процесс через терминал​Иногда нажатие кнопкиAllow Anywayне решает эту проблему, и в этом случае вы можете выполнить этот процесс через командную строку.
Или вы можете просто предпочитать использовать командную строку!Сначала выясните, куда Homebrew установил исполняемый файлclickhouse:which clickhouseДолжно получиться что-то вроде этого:/opt/homebrew/bin/clickhouseУдалите файлclickhouseиз карантина, выполнивxattr -d com.apple.quarantineс путем, полученным из предыдущей команды:xattr -d com.apple.quarantine /opt/homebrew/bin/clickhouseТеперь вы можете запустить исполняемый файлclickhouse:clickhouseДолжно получиться примерно следующее:Use one of the following commands:
clickhouse local [args]
clickhouse client [args]
clickhouse benchmark [args]

При попытке выполнить любую командуclickhouseвы можете увидеть такую ошибку:Чтобы обойти эту ошибку проверки, нужно убрать приложение из карантина macOS — либо найдя соответствующую настройку в окнеSystem Settings, используя терминал, либо переустановив ClickHouse.Процесс через системные настройки​Самый простой способ убрать исполняемый файлclickhouseиз карантина:ОткройтеSystem Settings.Перейдите вPrivacy & Security:Пролистайте окно вниз до сообщения вида"clickhouse-macos-aarch64" was blocked from use because it is not from an identified developer".НажмитеAllow Anyway.Введите пароль пользователя macOS.Теперь вы должны иметь возможность запускать командыclickhouseв терминале.Процесс через терминал​Иногда нажатие кнопкиAllow Anywayне решает эту проблему, и в этом случае вы можете выполнить этот процесс через командную строку.
Или вы можете просто предпочитать использовать командную строку!Сначала выясните, куда Homebrew установил исполняемый файлclickhouse:which clickhouseДолжно получиться что-то вроде этого:/opt/homebrew/bin/clickhouseУдалите файлclickhouseиз карантина, выполнивxattr -d com.apple.quarantineс путем, полученным из предыдущей команды:xattr -d com.apple.quarantine /opt/homebrew/bin/clickhouseТеперь вы можете запустить исполняемый файлclickhouse:clickhouseДолжно получиться примерно следующее:Use one of the following commands:
clickhouse local [args]
clickhouse client [args]
clickhouse benchmark [args]

Чтобы обойти эту ошибку проверки, нужно убрать приложение из карантина macOS — либо найдя соответствующую настройку в окнеSystem Settings, используя терминал, либо переустановив ClickHouse.Процесс через системные настройки​Самый простой способ убрать исполняемый файлclickhouseиз карантина:ОткройтеSystem Settings.Перейдите вPrivacy & Security:Пролистайте окно вниз до сообщения вида"clickhouse-macos-aarch64" was blocked from use because it is not from an identified developer".НажмитеAllow Anyway.Введите пароль пользователя macOS.Теперь вы должны иметь возможность запускать командыclickhouseв терминале.Процесс через терминал​Иногда нажатие кнопкиAllow Anywayне решает эту проблему, и в этом случае вы можете выполнить этот процесс через командную строку.
Или вы можете просто предпочитать использовать командную строку!Сначала выясните, куда Homebrew установил исполняемый файлclickhouse:which clickhouseДолжно получиться что-то вроде этого:/opt/homebrew/bin/clickhouseУдалите файлclickhouseиз карантина, выполнивxattr -d com.apple.quarantineс путем, полученным из предыдущей команды:xattr -d com.apple.quarantine /opt/homebrew/bin/clickhouseТеперь вы можете запустить исполняемый файлclickhouse:clickhouseДолжно получиться примерно следующее:Use one of the following commands:
clickhouse local [args]
clickhouse client [args]
clickhouse benchmark [args]


### Процесс через системные настройки​

Самый простой способ убрать исполняемый файлclickhouseиз карантина:ОткройтеSystem Settings.Перейдите вPrivacy & Security:Пролистайте окно вниз до сообщения вида"clickhouse-macos-aarch64" was blocked from use because it is not from an identified developer".НажмитеAllow Anyway.Введите пароль пользователя macOS.Теперь вы должны иметь возможность запускать командыclickhouseв терминале.Процесс через терминал​Иногда нажатие кнопкиAllow Anywayне решает эту проблему, и в этом случае вы можете выполнить этот процесс через командную строку.
Или вы можете просто предпочитать использовать командную строку!Сначала выясните, куда Homebrew установил исполняемый файлclickhouse:which clickhouseДолжно получиться что-то вроде этого:/opt/homebrew/bin/clickhouseУдалите файлclickhouseиз карантина, выполнивxattr -d com.apple.quarantineс путем, полученным из предыдущей команды:xattr -d com.apple.quarantine /opt/homebrew/bin/clickhouseТеперь вы можете запустить исполняемый файлclickhouse:clickhouseДолжно получиться примерно следующее:Use one of the following commands:
clickhouse local [args]
clickhouse client [args]
clickhouse benchmark [args]

- ОткройтеSystem Settings.
ОткройтеSystem Settings.

- Перейдите вPrivacy & Security:
Перейдите вPrivacy & Security:

- Пролистайте окно вниз до сообщения вида"clickhouse-macos-aarch64" was blocked from use because it is not from an identified developer".
Пролистайте окно вниз до сообщения вида"clickhouse-macos-aarch64" was blocked from use because it is not from an identified developer".

- НажмитеAllow Anyway.
НажмитеAllow Anyway.

- Введите пароль пользователя macOS.
Введите пароль пользователя macOS.

Теперь вы должны иметь возможность запускать командыclickhouseв терминале.Процесс через терминал​Иногда нажатие кнопкиAllow Anywayне решает эту проблему, и в этом случае вы можете выполнить этот процесс через командную строку.
Или вы можете просто предпочитать использовать командную строку!Сначала выясните, куда Homebrew установил исполняемый файлclickhouse:which clickhouseДолжно получиться что-то вроде этого:/opt/homebrew/bin/clickhouseУдалите файлclickhouseиз карантина, выполнивxattr -d com.apple.quarantineс путем, полученным из предыдущей команды:xattr -d com.apple.quarantine /opt/homebrew/bin/clickhouseТеперь вы можете запустить исполняемый файлclickhouse:clickhouseДолжно получиться примерно следующее:Use one of the following commands:
clickhouse local [args]
clickhouse client [args]
clickhouse benchmark [args]


### Процесс через терминал​

Иногда нажатие кнопкиAllow Anywayне решает эту проблему, и в этом случае вы можете выполнить этот процесс через командную строку.
Или вы можете просто предпочитать использовать командную строку!Сначала выясните, куда Homebrew установил исполняемый файлclickhouse:which clickhouseДолжно получиться что-то вроде этого:/opt/homebrew/bin/clickhouseУдалите файлclickhouseиз карантина, выполнивxattr -d com.apple.quarantineс путем, полученным из предыдущей команды:xattr -d com.apple.quarantine /opt/homebrew/bin/clickhouseТеперь вы можете запустить исполняемый файлclickhouse:clickhouseДолжно получиться примерно следующее:Use one of the following commands:
clickhouse local [args]
clickhouse client [args]
clickhouse benchmark [args]

Сначала выясните, куда Homebrew установил исполняемый файлclickhouse:which clickhouseДолжно получиться что-то вроде этого:/opt/homebrew/bin/clickhouseУдалите файлclickhouseиз карантина, выполнивxattr -d com.apple.quarantineс путем, полученным из предыдущей команды:xattr -d com.apple.quarantine /opt/homebrew/bin/clickhouseТеперь вы можете запустить исполняемый файлclickhouse:clickhouseДолжно получиться примерно следующее:Use one of the following commands:
clickhouse local [args]
clickhouse client [args]
clickhouse benchmark [args]


```
which clickhouse

```

Должно получиться что-то вроде этого:/opt/homebrew/bin/clickhouseУдалите файлclickhouseиз карантина, выполнивxattr -d com.apple.quarantineс путем, полученным из предыдущей команды:xattr -d com.apple.quarantine /opt/homebrew/bin/clickhouseТеперь вы можете запустить исполняемый файлclickhouse:clickhouseДолжно получиться примерно следующее:Use one of the following commands:
clickhouse local [args]
clickhouse client [args]
clickhouse benchmark [args]


```
/opt/homebrew/bin/clickhouse

```

Удалите файлclickhouseиз карантина, выполнивxattr -d com.apple.quarantineс путем, полученным из предыдущей команды:xattr -d com.apple.quarantine /opt/homebrew/bin/clickhouseТеперь вы можете запустить исполняемый файлclickhouse:clickhouseДолжно получиться примерно следующее:Use one of the following commands:
clickhouse local [args]
clickhouse client [args]
clickhouse benchmark [args]


```
xattr -d com.apple.quarantine /opt/homebrew/bin/clickhouse

```

Теперь вы можете запустить исполняемый файлclickhouse:clickhouseДолжно получиться примерно следующее:Use one of the following commands:
clickhouse local [args]
clickhouse client [args]
clickhouse benchmark [args]


```
clickhouse

```

Должно получиться примерно следующее:Use one of the following commands:
clickhouse local [args]
clickhouse client [args]
clickhouse benchmark [args]


```
Use one of the following commands:
clickhouse local [args]
clickhouse client [args]
clickhouse benchmark [args]

```


## Устранение проблемы путем повторной установки ClickHouse​

В brew есть параметр командной строки, который изначально предотвращает помещение установленных бинарных файлов в карантин.Сначала удалите ClickHouse:brew uninstall clickhouseТеперь переустановите ClickHouse с параметром--no-quarantine:brew install --no-quarantine clickhouse

Сначала удалите ClickHouse:brew uninstall clickhouseТеперь переустановите ClickHouse с параметром--no-quarantine:brew install --no-quarantine clickhouse


```
brew uninstall clickhouse

```

Теперь переустановите ClickHouse с параметром--no-quarantine:brew install --no-quarantine clickhouse


```
brew install --no-quarantine clickhouse

```
