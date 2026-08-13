# Инкрементное обновление | Документация Fastboard

Source: https://help.fastboard.online/user/dispetcer-dannyx/inkrementnoe-obnovlenie/

Инкрементальное обновление данных подразумевает загрузку данных в базу данных без полной перезаписи.

Необходимо настроить скрипт так, чтобы он дополнял данные в таблице, а не перезаписывал их полностью. Это сократит время выполнения скрипта и минимизирует простой системы.

По умолчанию скрипт работает в режиме полной перезаписи: при каждом запуске таблица удаляется (`DROP`) и создаётся заново. Для больших таблиц это занимает много времени.

Далее вы узнаете как изменить настройки скрипта вместо полной перезаписи удалять данные только за последние 7 дней и дописывать новые.


## **Настройка инкрементального обновления**[​](#настройка-инкрементального-обновления)

**Шаг 1. Переместить секцию `DELETE` под секцию `CREATE`**

В коде скрипта найдите блоки `CREATE` (создание таблицы) и `DELETE` (удаление данных). Поменяйте их порядок: сначала должен идти `CREATE`, затем — `DELETE`.

![В коде скрипта найдите блоки CREATE (создание таблицы) и DELETE (удаление данных). Поменяйте их](https://help.fastboard.online/assets/images/frame-212-c6dd9929db0bb1c354cb2a0aa0883825.png)

> **Со скриншота** ([изображение](https://help.fastboard.online/assets/images/frame-212-c6dd9929db0bb1c354cb2a0aa0883825.png)):
> 1)  
> Скрипт загрузки  
> Модель данных  
> 1 Table "Biudzhets"  
> 2   
> 3 Delete ===  
> 4 DROP TABLE IF EXISTS "Biudzhets"  
> 5 ===  
> 6   
> 7 Create ===  
> 8 CREATE TABLE IF NOT EXISTS "Biudzhets" (  
> 9   "Biudzhets_ID" Int16,  
> 10  "Schet_ID" Int16,  
> 11  "Summa_Biudzhets" Float32,  
> 12  "Podrazdelenie_ID" Int8,  
> 13  "Period_ID" Int8,  
> 14  "ID" Int16,  
> 15  "Kompania_ID" Int8,  
> 16  "file_name" Nullable (String),  
> 17  "updated_date" Nullable (String),  
> 18  "fb_created_date" Nullable (String)  
> 19 ) ENGINE = MergeTree ()  
> 20 ORDER BY  
> 21   tuple ()  
> 22 ===  
> 23   
> 24 Source "Бюджет_демо"  
> 25   
> 26 Read ===  
> 27 SELECT  
> 28  "Biudzhets_ID",  
> 29  "Schet_ID",  
> 30  "Summa_Biudzhets",  
> 31  "Podrazdelenie_ID",  
> 32  "Period_ID",  
> 33  "ID",  
> 34  "Kompania_ID",  
> 35  "file_name",  
> 36  "updated_date",  
> 37  "fb_created_date"  
> 38 FROM  
> 39  "Biudzhets"  
> Развернуть  
> 05:03:29 Получен скрипт  
> Сохранить скрипт  
> Запустить скрипт  
> Обновление данных  
> 2) Скриншот показывает интерфейс BI-платформы Fastboard с открытым SQL-скриптом для создания и чтения таблицы «Biudzhets» из источника «Бюджет_демо», включая команды DROP, CREATE TABLE и SELECT, а также кнопки управления скриптом.


**Шаг 2. Заменить команду `DROP` на `ALTER`**

- Найдите в секции `DELETE` команду `DROP TABLE`. Вместе полного удаления таблицы (DROP) укажем конструкцию `ALTER` и удалим данные за последние 7 дней.
- Замените `DROP TABLE` на `ALTER TABLE`.
![Замените DROP TABLE на ALTER TABLE .](https://help.fastboard.online/assets/images/frame-213-34160b19f7a85a12fac685124be051cc.png)

> **Со скриншота** ([изображение](https://help.fastboard.online/assets/images/frame-213-34160b19f7a85a12fac685124be051cc.png)):
> 1)  
> Скрипт загрузки  
> Модель данных  
> 1 Table "Biudzhet"  
> 2   
> 3   
> 4   
> 5 Create ###  
> 6 CREATE TABLE IF NOT EXISTS "Biudzhet" (  
> 7   "Biudzhet_ID" Int16,  
> 8   "Schet_ID" Int16,  
> 9   "Summa_Biudzhet" Float32,  
> 10  "Podrazdelenie_ID" Int8,  
> 11  "Period_ID" Int8,  
> 12  "ID" Int16,  
> 13  "Kompania_ID" Int8,  
> 14  "file_name" Nullable (String),  
> 15  "updated_date" Nullable (String),  
> 16  "fb_created_date" Nullable (String)  
> 17 ) ENGINE = MergeTree ()  
> 18 ORDER BY  
> 19   tuple ()  
> 20 ###  
> 21   
> 22 Delete ###  
> 23 alter Table "Biudzhet" Delete WHERE 1=0  
> 24 ###  
> 25   
> 26   
> 27 Source "Бюджет_демо"  
> 28   
> 29 Read ###  
> 30 SELECT  
> 31   "Biudzhet_ID",  
> 32   "Schet_ID",  
> 33   "Summa_Biudzhet"  
> 34   "Podrazdelenie_ID",  
> 35   "Period_ID",  
> 36   "ID",  
> 37   "Kompania_ID"  
> Развернуть  
> 05:18:16 Получен скрипт  
> Сохранить скрипт Запустить скрипт  
> Обновление данных  
> 2) Скриншот показывает интерфейс редактора SQL-скриптов в BI-платформе Fastboard с кодом создания, очистки и чтения таблицы "Biudzhet", а также панелью управления скриптом.


Alter @@@

ALTER TABLE "Biudzhet"

DELETE WHERE "Order_Date" >= today() - interval 7 day

**После внесения изменений** в скрипт, нажмите сначала "Сохранить скрипт", затем "Запустить скрипт".

![После внесения изменений в скрипт, нажмите сначала &#39;Сохранить скрипт&#39;, затем &#39;Запустить скрипт&#39;.](data:image/png;base64,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)
