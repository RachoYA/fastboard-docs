# Раздельное обновление источников | Документация Fastboard

Source: https://help.fastboard.online/user/dispetcer-dannyx/razdelnoe-obnovlenie-istocnikov/

В Fastboard есть возможность ссылаться на другой проект, и как следствие этого, вы можете настроить раздельное обновление источников, что дает гибкость системе. С помощью него вы можете управлять обновлением как набором независимых модулей.

Рассмотрим практический пример. У нас имеется крупный проект (А), который включает множество источников, среди которых присутствует таблица данных, из которой необходимо извлекать информацию каждый час. Обновление всего проекта со всеми источниками создает значительную нагрузку на сервер. В данной ситуации целесообразно создать вспомогательный проект для отдельного обновления (Б).

![Frame 215.png](https://book.winsolutions.ru/uploads/images/gallery/2026-02/scaled-1680-/frame-215.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-02/scaled-1680-/frame-215.png)):
> А  
> Большой проект  
> Б  
> П. для раздельного обнов...  
> Скриншот показывает два элемента интерфейса BI-платформы Fastboard: слева — дашборд с графиками и метриками под названием «Большой проект», справа — загрузочный или пустой блок с подписью «П. для раздельного обнов...» (вероятно, сокращение от «Панель для раздельного обновления»).



## Создание стороннего проекта для раздельного обновления[​](#создание-стороннего-проекта-для-раздельного-обновления)

Подключаем необходимые данные в проект Б.

Подробнее о [создании проекта.](https://help.fastboard.online/rabota-s-proektami/sozdanie-i-upravlenie-proektami/)

Подробнее о [подключении источников](https://help.fastboard.online/dispetcer-dannyx/istocniki-dannyx/konnektory/).

![Frame 217.png](https://book.winsolutions.ru/uploads/images/gallery/2026-02/scaled-1680-/frame-217.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-02/scaled-1680-/frame-217.png)):
> 1)  
> Б  
> Скрипт загрузки  
> Модель данных  
> 21 "Natsenka_PERCENT" Float32,  
> 22 "Marzhinal_nost_rub" Float32,  
> 23 "Vozrastnaia_kategorii" String,  
> 24 "Aksiiio_skidka_PERCENT" Int8,  
> 25 "Skladskie_ostatki" Float32,  
> 26 "Vremia_dostavki_dnei" Int8,  
> 27 "file_name" Nullable (String),  
> 28 "updated_date" Nullable (String),  
> 29 "fb_created_date" Nullable (String)  
> 30 ) ENGINE = MergeTree ()  
> 31 ORDER BY  
> 32 tuple ()  
> 33 ===  
> 34  
> 35 Source "курс по FB"  
> 36 Read ===  
> 37 SELECT  
> 38 "Period",  
> 39 "Region",  
> 40 "FIO",  
> 41 "FIO_sokrashchenno",  
> 42 "Tovarnia_gruppa",  
> 43 "Konkretnyi_tovar",  
> 44 "Brend",  
> 45 "Prodano_sht",  
> 46 "Isena_sht",  
> 47 "Plan_prodazh_sht",  
> 48 "Sebestoimost_rub",  
> 49 "Natsenka_PERCENT",  
> 50 "Marzhinal_nost_rub",  
> 51 "Vozrastnaia_kategorii",  
> 52 "Aksiiio_skidka_PERCENT",  
> 53 "Skladskie_ostatki",  
> 54 "Vremia_dostavki_dnei",  
> 55 "file_name",  
> 56 "updated_date",  
> 57 "fb_created_date"  
> 58 FROM  
> 59 "Sheet1"  
> 60 WHERE "Period" > '2025-01-01'  
> 61 ===  
> 62  
> 63 Optimize ===  
> 64 OPTIMIZE TABLE "Sheet1"  
> 65 ===  
> 66  
> Развернуть  
> 14.09.24 Получен скрипт  
> Сохранить скрипт Запустить скрипт  
> Обновление данных  
> 2) Скриншот показывает интерфейс BI-платформы Fastboard с открытым SQL-скриптом загрузки данных, включающим определение таблицы, SELECT-запрос из источника "Sheet1" и команду оптимизации.



### Внесение изменений в скрипт загрузки[​](#внесение-изменений-в-скрипт-загрузки)

Копируем скрипт из проекта Б в скрипт загрузки проекта А. Далее со скриптом **работаем в проекте А**. Нужно не создать такую же таблицу, а сослаться на проект Б.

Удаляем лишние поля

![Frame 221 (1).png](https://book.winsolutions.ru/uploads/images/gallery/2026-02/scaled-1680-/frame-221-1.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-02/scaled-1680-/frame-221-1.png)):
> 1)  
> A  
> Скрипт загрузки  
> Модель данных  
> 1 Table "Sheet1"  
> 2   
> 3 Delete @@@  
> 4 DROP TABLE IF EXISTS "Sheet1"  
> 5   
> 6   
> 7 Create @@@  
> 8 CREATE TABLE IF NOT EXISTS "Sheet1" (  
> 9   "Period" Date,  
> 10  "Region" String,  
> 11  "FID" String,  
> 12  "FID_sokrashchenno" String,  
> 13  "Tovarnaya_gruppa" String,  
> 14  "Konkretniy_tovar" Nullable (String),  
> 15  "Brand" String,  
> 16  "Prodano_sht" Float32,  
> 17  "Tsen_sht" Float32,  
> 18  "Plan_prodazh_sht" Float32,  
> 19  "Sebestoimost_rub" Float32,  
> 20  "Natsenka_PERCENT" Float32,  
> 21  "Marzhal_nost_rub" Float32,  
> 22  "Vozrastnaya_kategoriya" String,  
> 23  "Aksiya_aksiyka_PERCENT" Int8,  
> 24  "Skladskie_ostatki" Float32,  
> 25  "Vremya_dostavki_dnei" Int8,  
> 26  "file_name" Nullable (String),  
> 27  "updated_date" Nullable (String),  
> 28  "fb_created_date" Nullable (String)  
> 29 ) ENGINE = MergeTree ()  
> 30 ORDER BY  
> 31   tuple ()  
> 32   
> 33 @@@  
> 34 Source "хурс по FB"  
> 35 Read @@@  
> 36 SELECT  
> 37   "Period",  
> 38   "Region",  
> 39   "FID",  
> 40   "FID_sokrashchenno",  
> 41   "Tovarnaya_gruppa",  
> 42   "Konkretniy_tovar",  
> 43   "Brand",  
> 44   "Prodano_sht",  
> 45  "Tsen_sht",  
> 14:36:43 Получен скрипт  
> 2) Скриншот показывает интерфейс редактора SQL-скриптов в BI-платформе Fastboard с вкладками «Скрипт загрузки» и «Модель данных», где отображается код создания таблицы «Sheet1» и выборки данных из источника «хурс по FB».


Копируем из адресной строки id проекта Б и вставляем скрипт проекта А. ![Frame 219.png](https://book.winsolutions.ru/uploads/images/gallery/2026-02/scaled-1680-/frame-219.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-02/scaled-1680-/frame-219.png)):
> fb.winsolutions.ru/7816327a-5bd4-47fe-887c-05f8a10c5801/console  
> Скрипт загрузки  
> Модель данных  
> Разделы  
> Разделен  
> Table "Sheet1"  
> Delete @@@  
> DROP TABLE IF EXISTS "Sheet1"  
> @@@  
> Create @@@  
> CREATE TABLE IF NOT EXISTS "Sheet1" AS "7816327a_5bd4_47fe_887c_05f8a10c5801".Sheet1  
> Source "ClickHouse common"  
> Read @@@  
> SELECT  
> Б  
> А  
> Скриншот показывает интерфейс BI-платформы Fastboard с вкладкой «Скрипт загрузки», где отображается SQL-код для создания таблицы из источника ClickHouse, а также URL-адрес консоли и структура проекта с разделами.


В id проекта заменить дефисы "-" на нижнее подчеркивание "_" и в конце строки добавить название таблицы. ![Frame 220 (1).png](https://book.winsolutions.ru/uploads/images/gallery/2026-02/scaled-1680-/frame-220-1.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-02/scaled-1680-/frame-220-1.png)):
> 8 Create  
> 9 CREATE TABLE IF NOT EXISTS "Sheet1" AS '761827a_5bd4_47fe_887c_05f8a10c5801'.Sheet1  
> 10  
> Скриншот показывает SQL-запрос для создания таблицы в BI-платформе Fastboard.


Указываем что создаем такую же таблицу как в исходном проекте

![Frame 222 (1).png](https://book.winsolutions.ru/uploads/images/gallery/2026-02/scaled-1680-/frame-222-1.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-02/scaled-1680-/frame-222-1.png)):
> 1)  
> A  
> Скрипт загрузки  
> Модель данных  
> 1 Table "Sheet1"  
> 2   
> 3 Delete @@@  
> 4 DROP TABLE IF EXISTS "Sheet1"  
> 5 @@@  
> 6   
> 7 Create @@@  
> 8 CREATE TABLE IF NOT EXISTS "Sheet1" AS "7816327a_5bd4_47fe_887c_05f8a10c5801".Sheet1  
> 9 @@@  
> 10   
> 11 Source "курс по FB"  
> 12   
> 13 Read @@@  
> 14 SELECT  
> 15 "Period",  
> 16 "Region",  
> 17 "FIO",  
> 18 "FIO_sokrashchenno",  
> 19 "Tovarnaya_gruppa",  
> 20 "Konkretnyi_tovar",  
> 21 "Brand",  
> 22 "Prodano_sht",  
> 23 "Tsena_sht",  
> 24 "Plan_prodazh_sht",  
> 25 "Sebestoimost_rub",  
> 26 "Natsenka_PERCENT",  
> 27 "Marzhdinal_nost_rub",  
> 28 "Vozrastnaya_kategoriiya",  
> 29 "Aktivnost_aktivno_PERCENT",  
> 30 "Skhldskie_ostatki",  
> 31 "Vremia_dostavki_dnei",  
> 32 "file_name",  
> 33 "updated_date",  
> 34 "fb_created_date"  
> 35 FROM  
> 36 "Sheet1"  
> 37 WHERE "Period" > '2025-01-01'  
> 38 @@@  
> 39   
> 40 Optimize @@@  
> 41 OPTIMIZE TABLE "Sheet1"  
> 42 @@@  
> 43   
> 44  
> Развернуть  
> 14:51:01 Получен скрипт  
> 2) Скриншот показывает интерфейс BI-платформы Fastboard с вкладкой «Скрипт загрузки», где отображается SQL-скрипт для создания, очистки и оптимизации таблицы "Sheet1" из источника данных "курс по FB", включая выборку строк за период после 2025-01-01.
 ![Frame 223.png](https://book.winsolutions.ru/uploads/images/gallery/2026-02/scaled-1680-/frame-223.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-02/scaled-1680-/frame-223.png)):
> 1)  
> A  
> Table "Sheet1"  
> Delete  
> DROP TABLE IF EXISTS "Sheet1"  
> Create  
> CREATE TABLE IF NOT EXISTS "Sheet1" AS "7816327a_5bd4_47fe_887c_05f8a10c5081".Sheet1  
> Source "kypc no FB"  
> Read  
> SELECT *  
> FROM "Sheet1"  
> WHERE "Period" > '2025-01-01'  
> Optimize  
> OPTIMIZE TABLE "Sheet1"  
> 2) Скриншот показывает SQL-запросы для управления таблицей "Sheet1" в BI-платформе Fastboard: удаление, создание, чтение с фильтром по дате и оптимизация.


Указываем другой источник ![Frame 224 (1).png](https://book.winsolutions.ru/uploads/images/gallery/2026-02/scaled-1680-/frame-224-1.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-02/scaled-1680-/frame-224-1.png)):
> 1)  
> A  
> Table "Sheet1"  
> Delete @@@  
> DROP TABLE IF EXISTS "Sheet1"  
> Create @@@  
> CREATE TABLE IF NOT EXISTS "Sheet1" AS "7816327a_5bd4_47fe_887c_05f8a10c5801".Sheet1  
> Source 'kypc no FB' ← Source "ClickHouse common"  
> Read @@@  
> SELECT  
> *  
> FROM  
> "Sheet1"  
> WHERE "Period" > '2025-01-01'  
> Optimize @@@  
> OPTIMIZE TABLE "Sheet1"  
> 2) Скриншот показывает фрагмент SQL-кода в BI-платформе Fastboard, где создаётся таблица "Sheet1", указывается источник данных ("ClickHouse common"), выполняется выборка с фильтром по дате и оптимизация таблицы.


После внесения изменений в скрипт, нажмите сначала "Сохранить скрипт", затем "Запустить скрипт". ![Frame 226.png](https://book.winsolutions.ru/uploads/images/gallery/2026-02/scaled-1680-/frame-226.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-02/scaled-1680-/frame-226.png)):
> 1)  
> 1  
> Сохранить скрипт  
> 2  
> Запустить скрипт  
> 2) Скриншот показывает два пронумерованных действия: сохранение и запуск скрипта в интерфейсе BI-платформы Fastboard.

