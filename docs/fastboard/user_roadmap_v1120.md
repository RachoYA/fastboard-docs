# 1.12.0 | 06.02.2026 | Документация Fastboard

Source: https://help.fastboard.online/user/roadmap/v1120/


## **Настройки визуализации**[​](#настройки-визуализации)


### **Свободный режим SQL-редактора (редактор со встроенным языком структурированных запросов)**[​](#свободный-режим-sql-редактора-редактор-со-встроенным-языком-структурированных-запросов)

Добавлен новый режим работы с визуализациями — Свободный режим SQL-редактора, предоставляющий расширенные возможности работы с SQL (язык структурированных запросов). [Подробная инструкция по работе с новым режимом SQL-редактора](https://help.fastboard.online/osobennosti-sql-redaktora/svobodnyi-rezim-sql-redaktora/).

![Frame 11.png](https://book.winsolutions.ru/uploads/images/gallery/2025-12/scaled-1680-/frame-11.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2025-12/scaled-1680-/frame-11.png)):
> 1) Редактор Кода  
> Карта модели  
> Поиск  
> ik  
> ik_week  
> calendar  
> Свободный режим  
> Выражение  
> SELECT  
>     calendar.id AS "calendar.id",  
>     calendar.key_date AS "calendar.key_date",  
>     calendar.date AS "calendar.date",  
>     calendar.index_day AS "calendar.index_day",  
>     calendar.day AS "calendar.day",  
>     calendar.week AS "calendar.week",  
>     calendar.quarter AS "calendar.quarter",  
>     calendar.year AS "calendar.year",  
>     calendar.index_month AS "calendar.index_month",  
>     calendar.month AS "calendar.month"  
> FROM  
>     calendar AS calendar  
> GROUP BY  
>     calendar.id,  
>     calendar.key_date,  
>     calendar.date,  
>     calendar.index_day,  
>     calendar.day,  
>     calendar.week,  
>     calendar.quarter,  
>     calendar.year,  
>     calendar.index_month,  
>     calendar.month  
> ORDER BY  
>     calendar.id DESC,  
>     calendar.key_date DESC,  
>     calendar.index_day ASC  
> LIMIT  
>     25  
> Добавить в текст  
> Форматировать  
> Отменить  
> Сохранить  
> Разрезы:  
> calendar.id  
> calendar.key_date  
> calendar.date  
> calendar.index_day  
> calendar.day  
> calendar.week  
> calendar.quarter  
> calendar.year  
> calendar.index_month  
> calendar.month  
> 2) Скриншот показывает интерфейс редактора SQL-запросов в BI-платформе Fastboard с отображением структуры запроса, списка полей таблицы calendar и элементов управления для редактирования и сохранения.



#### Описание функциональности[​](#описание-функциональности)

В настройке визуальных компонентов SQL-редактора появился переключатель «Свободный режим», открывающий доступ к сплошному редактору SQL.

Пользователь может вручную писать полноценный SQL-запрос с использованием:

- подзапросов (запрос, использующийся в другом SQL запросе),
- CTE (WITH),
- оконных функций,
- ручного формирования секций, SELECT, FROM, GROUP BY.
Используется синтаксис ClickHouse, соответствующий версии стенда.

Подсветка синтаксиса, автодополнение, форматирование и словарь. ![Frame 12.png](https://book.winsolutions.ru/uploads/images/gallery/2025-12/scaled-1680-/frame-12.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2025-12/scaled-1680-/frame-12.png)):
> 1)  
> Свободный режим  
> Выражение  
> SELECT  
> calendar.id AS "calendar.id",  
> calendar.key_date AS "calendar.key_date",  
> calendar.date AS "calendar.date",  
> calendar.index_day AS "calendar.index_day",  
> calendar.day AS "calendar.day",  
> calendar.week AS "calendar.week",  
> calendar.quarter AS "calendar.quarter",  
> calendar.year AS "calendar.year",  
> calendar.index_month AS "calendar.index_month",  
> calendar.month AS "calendar.month"  
> FROM  
> calendar AS calendar  
> GROUP BY  
> calendar.id,  
> calendar.key_date,  
> calendar.date,  
> calendar.index_day,  
> calendar.day,  
> calendar.week,  
> calendar.quarter,  
> header keyword  
> height keyword  
> check keyword  
> checkpoint keyword  
> shell_in keyword  
> shell_out keyword  
> then keyword  
> thesaurus_init keyword  
> 31 hej  
> ОШИБКИ СИНТАКСИСА SQL  
> FREE MODE SQL  
> Expected "#", ";", ":", "-", "/", "*", "EXCEPT", "FOR", "GO", "INTERSECT", "INTO", "LIMIT", "LOCK", "MINUS", "OFFSET", "ORDER", "UNION", "WINDOW", [ \t\n\v], or end of input but "h" found.
> 2) Скриншот показывает редактор SQL-запроса в BI-платформе Fastboard с ошибкой синтаксиса из-за незавершённого ввода на строке 31.


В режиме «Свободный режим» SQL-код (код, написанный на структурированном языке запросов) становится **основным источником данных** для визуализации, а выбор данных через интерфейс блокируется. При этом настройки отображения визуализации (цвета, шрифты, подписи, легенды и другие визуальные параметры) остаются доступными и не зависят от режима работы редактора.


## **Диспетчер данных**[​](#диспетчер-данных)


### **Нумерация строк в SQL-редакторах**[​](#нумерация-строк-в-sql-редакторах)

Во всех SQL-редакторах добавлена **нумерация строк** для удобства навигации и анализа кода.

![Frame 10 (2).png](https://book.winsolutions.ru/uploads/images/gallery/2025-12/scaled-1680-/frame-10-2.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2025-12/scaled-1680-/frame-10-2.png)):
> 1)  
> Подключения  
> Все типы  
> Поиск  
> В проекте  
> AzureDevourer  
> Все подключения  
> + Создать подключение  
> Скрипт загрузки  
> Модель данных  
> Разделы  
> Table "attributes"  
> Delete @@@  
> DROP TABLE IF EXISTS "attributes"  
> @@@  
> Create @@@  
> CREATE TABLE IF NOT EXISTS "attributes" (  
> "udt_catalog" String,  
> "udt_schema" String,  
> "udt_name" String,  
> "attribute_name" String,  
> "ordinal_position" Int32,  
> "attribute_default" String,  
> "is_nullable" String,  
> "data_type" String,  
> "character_maximum_length" Int32,  
> "character_octet_length" Int32,  
> "character_set_catalog" String,  
> "character_set_schema" String,  
> "character_set_name" String,  
> "collation_catalog" String,  
> "collation_schema" String,  
> "collation_name" String,  
> "numeric_precision" Int32,  
> "numeric_precision_radix" Int32,  
> "numeric_scale" Int32,  
> "datetime_precision" Int32,  
> "interval_type" String,  
> "interval_precision" Int32,  
> "attribute_udt_catalog" String,  
> "attribute_udt_schema" String,  
> "attribute_udt_name" String,  
> Table "attributes"  
> Delete @@@  
> DROP TABLE IF EXISTS "attributes"  
> @@@  
> 13:13:35 Получен скрипт  
> Развернуть  
> Сохранить скрипт  
> Запустить скрипт  
> Обновление данных  
> 2) Скриншот показывает интерфейс BI-платформы Fastboard с открытым редактором SQL-скрипта для создания таблицы «attributes», включая её структуру и команды удаления/создания, а также панель подключений слева и кнопки управления скриптом внизу.



## **Багфикс (устранение дефектов)**[​](#багфикс-устранение-дефектов)

Изменили формулировку ошибки в **медиаблоке**

Восстановлена работа **Page Level Security (механизм безопасности на уровне строк)**.

**Диспетчере данных**

- корректно работает параметр **«Загружать с N строки»**;
- добавлен **прелоадер (индикатор предзагрузки)** при загрузке данных.
Исправлена работа **SVG-визуализаций**:

- корректно применяется **кросс-фильтрация (перекрестная фильтрация)** — элементы вне фильтра больше не окрашиваются ошибочно;
- восстановлена работа **правил непрозрачности**;
- исправлена настройка **обводки**;
- устранена проблема, при которой нельзя было отключить название области при отсутствии данных по path (элемента SVG);
- исправлен цвет при наведении на области без данных — теперь используется цвет, заданный в настройках.
Исправлено **градиентное окрашивание пузырьков**.

Исправлена ошибка **календаря** при работе в режиме фильтрации без параметра «Дни».

В **KPI-визуальном компоненте** исправлено применение правил окраски для всех исходных переменных.
