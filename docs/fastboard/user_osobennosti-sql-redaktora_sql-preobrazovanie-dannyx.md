# SQL-преобразование данных | Документация Fastboard

Source: https://help.fastboard.online/user/osobennosti-sql-redaktora/sql-preobrazovanie-dannyx/

![image.png](https://book.winsolutions.ru/uploads/images/gallery/2023-08/scaled-1680-/h2simage.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2023-08/scaled-1680-/h2simage.png)):
> 1)  
> Источники данных  
> Редактор скрипта загрузки  
> Конструктор моделей данных  
> Цвет по выражению (условию)  
> SQL-редактор виджета  
> Показатель "по выражению"  
> Переменная медиаблока  
> Результирующий запрос  
> сырые данные  
> импортированные данные в таблицах  
> FROM ...  
> SELECT ... WHERE ... ORDER BY ... GROUP BY ...  
> SELECT ... FROM ... WHERE ... ORDER BY ... GROUP BY ...
> 2) Скриншот показывает схему обработки данных в BI-платформе Fastboard: от источника до результирующего SQL-запроса, с этапами загрузки, моделирования и визуализации.


В Fastboard данные для визуализаций преобразуются в несколько этапов с помощью последовательно выполненных SQL-скриптов.


## **Этап 1: Редактор скрипта загрузки**[​](#этап-1-редактор-скрипта-загрузки)

![image.png](https://book.winsolutions.ru/uploads/images/gallery/2023-09/scaled-1680-/gV7image.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2023-09/scaled-1680-/gV7image.png)):
> 1)  
> Загрузить данные  
> Скрипт загрузки  
> Модель данных  
> Загрузить данные  
> Файл  
> База данных  
> Connection name  
> Host  
> Port  
> Database  
> Login  
> Password  
> Отмена  
> Подключиться  
> Подключения в проекте  
> test  
> Остальные подключения  
> Api-Test  
> Api-Test JSON  
> Api-Test JSON 2  
> Api-Test JSON 3  
> Api-Test JSON 4  
> Api-Test XML  
> Table "Brand"  
> Create @@@  
> CREATE TABLE IF NOT EXISTS  
> "Brand" (  
>     "id" String NULL,  
>     "createdAt" DateTime64 (6) NULL,  
>     "updatedAt" DateTime64 (6) NULL,  
>     "brand" String NULL  
> ) ENGINE = MergeTree ()  
> ORDER BY  
> tuple ()  
> @@@  
> Delete @@@  
> ALTER TABLE "Brand" DELETE WHERE 1=1  
> @@@  
> Source "test"  
> Read @@@  
> SELECT  
>     CAST("id" AS text),  
>     CAST(CAST("createdAt" AS timestamp) AS text),  
>     CAST(CAST("updatedAt" AS timestamp) AS text),  
>     CAST("brand" AS text)  
> FROM  
>     "Brand"  
> @@@  
> Table "Car"  
> Create @@@  
> CREATE TABLE IF NOT EXISTS  
> 11:52:51 Получен скрипт  
> Ссылка  
> Сохранить  
> Запустить  
> 2) Скриншот показывает интерфейс BI-платформы Fastboard на этапе настройки загрузки данных из базы данных через SQL-скрипт, включая создание таблицы, очистку и выборку данных.


На этом этапе данные загружаются из источника данных во внутреннее хранилище Fastboard. В [скрипте загрузки](https://users-docs-dev.fb-dev.winsolutions.ru/dispetcer-dannyx/redaktor-skripta-zagruzki/). Данные, полученные с помощью скрипта загрузки хранятся в проекте в виде несвязанных таблиц.

Чтобы таблицу можно было добавить в проект, подключение к источнику этой таблицы должно находиться в списке "Подключения в проекте". Добавить его туда можно создав новое подключение, либо выбрав уже существующее из списка "Остальные подключения.

По умолчанию импорт каждой таблицы состоит из заголовка (например, *Table "Brand"*) и трех секций:

*Create @@@* - создает в clickhouse таблицу с указанными столбцами и типами данных

*Delete @@@* - удаляет существующую таблицу из clickhouse при повторном запуске скрипта загрузки для корректной перезаписи данных

*Read @@@* - считывает данные из источника, приводит типы данных к указанным и записывает в созданную ранее таблицу.

**Отладочная информация**

Если при в коде скрипта загрузки были допущены ошибки, после сохранения и запуска скрипта они отобразятся в консоли:

![image.png](https://book.winsolutions.ru/uploads/images/gallery/2023-09/scaled-1680-/8Gyimage.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2023-09/scaled-1680-/8Gyimage.png)):
> 1)  
> Login  
> Password  
> Отмена  
> Подключиться  
> Подключения в проекте  
> AzureDevourer  
> Остальные подключения  
> Api-Test  
> Api-Test JSON  
> Api-Test JSON 2  
> Read @@  
> SELECT  
>     "date_create"::text,  
>     "date_end"::text,  
>     "type"::text,  
>     "genre"::text,  
>     "genre_2"::text,  
>     "genre_3"::text,  
>     "id"::text,  
>     "country"::text,  
>     "name"::text,  
>     "count_voice"::text,  
>     "time"::text,  
> 12:23:23 Скрипт запущен  
> 12:23:24 Error: Syntax error: failed at position 181 ("genre_3") (line 8, col 5): "genre_3" String NULL, "id" Int32 NULL, "country" String NULL, "name" String NULL, "count_voice" Int32 NULL, "time" Int32 NULL, "avg_rat. Expected one of: DEFAULT, MATERIALIZED, ALIAS, EPHEMERAL, AUTO_INCREMENT, COMMENT, CODEC, TTL, PRIMARY KEY, token, Comma, ClosingRoundBracket.  
> 12:23:48 Скрипт сохранен  
> Ссылка  
> Сохранить  
> Запустить  
> 2) Скриншот показывает интерфейс BI-платформы Fastboard с формой подключения к базе данных, списком подключений в проекте и редактором SQL-запроса с ошибкой синтаксиса при выполнении скрипта.



### **Этап 2: Конструктор моделей данных**[​](#этап-2-конструктор-моделей-данных)

Модель данных заменяет собой секцию FROM у запросов, по которым в конструкторе дашбордов (отчётов) строятся визуализации. Она строится в визуальном конструкторе и представляет собой набор таблиц проекта, соединенных операторами JOIN в одну. Моделей может быть произвольное количество, в зависимости от потребностей пользователя. ![image.png](https://book.winsolutions.ru/uploads/images/gallery/2023-06/scaled-1680-/4Enimage.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2023-06/scaled-1680-/4Enimage.png)):
> 1)  
> Загрузить данные  
> Скрипт загрузки  
> Модель данных  
> Сохранить  
> +  
> –  
> Таблицы  
> Brand  
> Car  
> area  
> items  
> orders  
> shops  
> users_shops  
> Заказы/товары/клиенты  
> Магазины/адреса  
> Модель 2  
> +  
> shops  
> id  
> store guid  
> name  
> address  
> description  
> area  
> id area  
> full address  
> area type  
> area value  
> 2) Скриншот показывает интерфейс настройки модели данных в BI-платформе Fastboard, где отображены таблицы «shops» и «area» с их полями и связью между ними.



### **Этап 3: Конструктор дашбордов**[​](#этап-3-конструктор-дашбордов)

В конструкторе дашбордов пользователь оперирует данными, обработанными в скрипте загрузки и объединенными в модель данных. На этом этапе доступны кастомные SQL-запросы (запросы на структурированном языке) в следующих блоках:

**SQL-редактор визуального компонента** Формирует набор данных для отдельно взятой визуализации. В редакторе доступны для редактирования три поля: Разрезы, Показатели, Группировки и фильтры.

![image.png](https://book.winsolutions.ru/uploads/images/gallery/2023-11/scaled-1680-/w3oimage.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2023-11/scaled-1680-/w3oimage.png)):
> 1) Весь видимый текст дословно:
> Редактор Кода  
> Карта модели  
> Поиск  
> Kinopoisk  
> Разрезы ⓘ  
> Kinopoisk.date_create AS "Год_создания"  
> Модель данных  
> Разрезы (неагрегируемые данные)  
> Показатели ⓘ  
> COUNT(  
>   CASE  
>     WHEN Kinopoisk.type = 'фильм' THEN Kinopoisk.id  
>     ELSE NULL  
>   END  
> ) AS "Фильмы",  
> COUNT(  
>   CASE  
>     WHEN Kinopoisk.type = 'сериал' THEN Kinopoisk.id  
>     ELSE NULL  
>   END  
> ) AS "Сериалы"  
> Показатели (агрегируемые данные)  
> Группировки и фильтры ⓘ  
> order by  
> date_create asc  
> Группировки и фильтры  
> Добавить в текст  
> Отменить  
> Сохранить  
> Разрезы:  
> Год_создания  
> Показатели:  
> Фильмы  
> Сериалы  
> SELECT  
> FROM  
> WHERE  
> GROUP BY (если не указан, формируется автоматически)  
> ORDER BY  
> SQL запрос виджета  
> SELECT  
>   Kinopoisk.date_create AS "Год_создания",  
>   COUNT(  
>     CASE  
>       WHEN Kinopoisk.type = 'фильм' THEN Kinopoisk.id  
>       ELSE NULL  
>     END  
>   ) AS "Фильмы",  
>   COUNT(  
>     CASE  
>       WHEN Kinopoisk.type = 'сериал' THEN Kinopoisk.id  
>       ELSE NULL  
>     END  
>   ) AS "Сериалы"  
> FROM  
>   Kinopoisk AS Kinopoisk  
> WHERE  
>   Kinopoisk.country IN (  
>     'США',  
>     'Австралия',  
>     'Австрия',  
>     'Азербайджан',  
>     'Албания',  
>     'Ангола',  
>     'Афганистан',  
>     'Андорра'  
>   )  
> GROUP BY  
>   Kinopoisk.date_create  
> ORDER BY  
>   date_create ASC  
> 2) Скриншот показывает интерфейс редактора SQL-запроса в BI-платформе Fastboard, где пользователь настраивает выборку данных из таблицы Kinopoisk с разрезами по году создания, показателями количества фильмов и сериалов, фильтрацией по странам и сортировкой по дате.


Разрезы и показатели определяют секцию SELECT запроса и разделены для того, чтобы правильно построить диаграмму. Разрезы представляют собой измерения, а показатели -- меры(агрегируемые данные).

Группировки и фильтры определяют секции WHERE, ORDER BY и GROUP BY запроса.

![image.png](https://book.winsolutions.ru/uploads/images/gallery/2023-11/scaled-1680-/wbximage.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2023-11/scaled-1680-/wbximage.png)):
> Группировки и фильтры  
> WHERE  
> Organisation.id > 5  
> GROUP BY  
> Organisation.name  
> ORDER BY  
> Organisation.name|  
> Скриншот показывает интерфейс настройки SQL-запроса в BI-платформе Fastboard с фильтрацией, группировкой и сортировкой по полю Organisation.name.


Для агрегации показателей существуют встроенные функции (SUM, COUNT, AVG, MIN, MAX), а также "По выражению":

**Показатель по выражению**

![image.png](https://book.winsolutions.ru/uploads/images/gallery/2023-08/scaled-1680-/TMLimage.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2023-08/scaled-1680-/TMLimage.png)):
> 1)  
> Настроить  
> Название из источника  
> Доп. показатель  
> Тип элемента  
> Столбик Линия  
> Показать значения  
> Расположение  
> В конце В центре В начале Снаружи  
> Ориентация  
> Горизонтально Вертикально  
> Свойства  
> Начертание B I  
> Размер 12 пикс  
> Цвет  
> Выражение  
> Формат  
> 12 % $ ½ 10²  
> T ←.0 →.0 000  
> Данные Вид События  
> Показатели  
> Оценка по шкале APDEX  
> Оценка по шкале APDEX  
> По выраже...  
> Отлично  
> Хорошо  
> Плохо  
> Очень плохо  
> + Добавить показатель  
> SQL  
> Лимит  
> 2)  
> Скриншот показывает интерфейс настройки визуализации данных в BI-платформе Fastboard, включая параметры отображения столбиков/линий, форматирование значений и выбор показателей (в т.ч. APDEX-оценка), с возможностью привязки к выражению или SQL.


![image.png](https://book.winsolutions.ru/uploads/images/gallery/2023-08/scaled-1680-/FnGimage.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2023-08/scaled-1680-/FnGimage.png)):
> Редактор Кода  
> SUM(if(toFloat64(replace(assumeNotNull(fact.execution_time), ',', '.')) <= 0.006, 1, 0)) / SUM(if(toFloat64(replace(assumeNotNull(fact.execution_time), ',', '.')) > 0, 1, 0)) * 100
> Скриншот показывает редактор кода в BI-платформе Fastboard с формулой для расчёта доли записей, где execution_time ≤ 0.006 от общего числа ненулевых значений execution_time, умноженной на 100.


Данная функция позволяет написать произвольное SQL-выражение для выбранного показателя. Это выражение будет добавлено в основной SQL-редактор визуального компонента, в поле "Показатели", с указанием алиаса данного показателя.

![image.png](https://book.winsolutions.ru/uploads/images/gallery/2023-08/scaled-1680-/kXLimage.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2023-08/scaled-1680-/kXLimage.png)):
> Показатели ⓘ  
> Разочарованные  
> replace(assumeNotNull (fact.execution_time), ',', '.')  
> ) > 0,  
> 1,  
> 0  
> )  
> ) * 100 AS "Довольные",  
> SUM(  
> if (  
> Группировки и фильтры ⓘ  
> WHERE  
> Скриншот показывает фрагмент SQL-запроса в BI-платформе Fastboard с логикой расчёта метрики «Довольные» на основе времени выполнения, а также заголовки разделов интерфейса: «Показатели», «Группировки и фильтры».


**Цвет по условию**

Данная функция позволяет написать SQL-выражение для расчета и выбора цвета показателя из палитры. Например,


```
postgresqlcase when Car.BRAND = 'Toyota' then '1'when Car.BRAND = 'Mitsubishi' then '2'else '3'end
```

где цифры в одинарных кавычках это выбранные образцы цвета ![image.png](https://book.winsolutions.ru/uploads/images/gallery/2023-08/scaled-1680-/W0fimage.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2023-08/scaled-1680-/W0fimage.png)):
> Изменить условие  
> 1 2 3 +  
> case  
> when Car.BRAND = 'Toyota' then '1'  
> when Car.BRAND = 'Mitsubishi' then '2'  
> else '3'  
> end  
> Скриншот показывает интерфейс настройки условного форматирования в BI-платформе Fastboard, где по цвету (фиолетовый — 1, зелёный — 2, белый — 3) отображаются значения поля Car.BRAND: Toyota → 1, Mitsubishi → 2, остальные → 3.


**SQL-редактор медиаблока**

![SQL-редактор медиаблока](https://book.winsolutions.ru/uploads/images/gallery/2023-05/scaled-1680-/image-1685434111053.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2023-05/scaled-1680-/image-1685434111053.png)):
> 1)  
> Страница 1  
> Страница 2  
> Страница 3  
> Редактор Кода  
> Переменные ⓘ  
> COUNT(Car.id) AS var1, SUM(Car.lcr) AS var2  
> Группировки и фильтры ⓘ  
> WHERE  
> CAST(Car.DATE_RELEASE as date) > '2022-01-01'|  
> Переменные:  
> var1  
> var2  
> 2) Скриншот показывает интерфейс редактора SQL-запросов в BI-платформе Fastboard с заданными переменными и условием фильтрации по дате.


Медиаблок - визуальный компонент, позволяющий использовать текст с переменными, значение которых определяется SQL-выражением, а также картинки, также подставляющиеся с помощью SQL-запроса.

SQL-редактор медиаблока не имеет полей "Разрезы" и "Показатели", вместо них одно поле "Переменные", аналогично определяющее секцию SELECT, и поле "Группировки и фильтры", аналогично стандартному редактору определяющее секции WHERE, ORDER BY и GROUP BY

**Переменные в медиаблоке** Имена переменных назначаются на основной вкладке параметров медиаблока. Можно увеличить их количество кнопкой "Добавить переменную" или удалить выбранную переменную с помощью кнопки "Корзина". Переименовать переменную можно нажав на ее название.

Рядом с названием переменной находится кнопка, открывающая дополнительное окно параметров:

![Рядом с названием переменной находится кнопка, открывающая дополнительное окно параметров:](https://book.winsolutions.ru/uploads/images/gallery/2023-05/scaled-1680-/image-1685433446841.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2023-05/scaled-1680-/image-1685433446841.png)):
> 1) Переменные  
> var1  
> var2  
> + Добавить переменную  
> 2) Скриншот показывает интерфейс управления переменными в BI-платформе Fastboard, включая список переменных (var1, var2), кнопку добавления новой переменной и иконку настроек/связей рядом с var1.


Это окно содержит стандартный блок, позволяющий включить, отключить а также выбрать тип форматирования для значения переменной.

![Это окно содержит стандартный блок, позволяющий включить, отключить а также выбрать тип форматир](https://book.winsolutions.ru/uploads/images/gallery/2023-05/scaled-1680-/image-1685433585026.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2023-05/scaled-1680-/image-1685433585026.png)):
> Настроить  
> Формат  
> 12 % $ ½ 10³  
> T <0 >0 000  
> Выражение  
> Скриншот показывает окно настройки формата отображения данных в BI-платформе Fastboard, включая переключатель формата и варианты числового представления.


Также в нем можно открыть редактор запросов для ввода выражения, которое определит значение переменной. Если для переменной не указано выражение, значением будет "undefined".

**Картинки в медиаблоке** В режиме "Ссылка - По условию" работает аналогично функции "Цвет по условию".

![image.png](https://book.winsolutions.ru/uploads/images/gallery/2023-09/scaled-1680-/Oobimage.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2023-09/scaled-1680-/Oobimage.png)):
> Изменить условие  
> 1 2 3 4 +  
> I  
> Сохранить  
> case  
> When Car.CAR_MODEL = '911' then '1'  
> Скриншот показывает интерфейс редактирования условия в BI-платформе Fastboard, где пользователь может задать логическое правило (например, для категоризации или фильтрации данных) с использованием SQL-подобного синтаксиса.


В режиме "База данных" ссылка на картинку должна содержаться в столбце модели данных, который необходимо указать в параметрах визуального компонента.

**Отладочная информация** Если в процессе написания скрипта допущены ошибки, сообщения о них отобразятся во всплывающем окне. Наведите курсор мыши на это окно, чтобы оно не исчезло по таймауту.

![image.png](https://book.winsolutions.ru/uploads/images/gallery/2023-09/scaled-1680-/kFFimage.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2023-09/scaled-1680-/kFFimage.png)):
> 1)  
> Редактор Кода  
> Разрезы ⓘ  
> Expected "#", " ", "\t", "\r\n", "/", "*", "FETCH", "FROM", "GROUP", "HAVING", "OFFSET", "ORDER", "UNION", "WHERE", { \n\r }, or end of input but "C" found.  
> Разрезы:  
> Год_создания  
> 2) Скриншот показывает ошибку синтаксического анализа SQL-запроса в редакторе кода BI-платформы Fastboard, где вместо ожидаемых ключевых слов или символов найден символ «C».


**Этап 4: Результирующий SQL-запрос**

После создания и настройки визуальных компонентов на листе дашборда формируется итоговый запрос, просмотреть который можно с помощью кнопки " " на правой панели инструментов. В нем будут содержаться все секци, что может быть полезно при отладке. Если выбран визуальный компонент, то будет отображаться запрос только для него, если ничего не выбрано -- отобразится запрос для всех элементов листа.

Отредактировать результирующий запрос нельзя, для этого необходимо вернуться на предыдущие этапы.

![image.png](https://book.winsolutions.ru/uploads/images/gallery/2023-09/scaled-1680-/qttimage.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2023-09/scaled-1680-/qttimage.png)):
> 1)  
> Дата ▼  
> ия  
> Max врем  
> за  
> 13  
> ика структуры пользовате  
> ольные Удовлетворенные  
> 34 18 15 14 13 10 17 31 31 22  
> SELECT fact.essence AS "Сущность" FROM  
> fact AS fact LEFT JOIN percentile AS percentile  
> ON percentile.key_percentile =  
> fact.key_percentile LEFT JOIN user AS user  
> ON user.key_user = fact.key_user LEFT JOIN  
> calendar AS calendar ON  
> calendar.key_calendar = fact.key_calendar  
> LEFT JOIN release AS release ON  
> release.key_calendar = fact.key_calendar LEFT  
> JOIN company AS company ON  
> company.key_company = fact.key_company  
> GROUP BY fact.essence  
> SELECT company.branch AS "Филиал",  
> median(toFloat64(replace(assumeNotNull(fact.ex  
> ', ','))) AS "Время проведения заказа (MDP)",  
> 0 AS "Довольные", 3 AS "Удовл-ные", CASE  
> WHEN  
> median(toFloat64(replace(assumeNotNull(fact.ex  
> ', ','))) <= 3 THEN '#36B685' WHEN  
> median(toFloat64(replace(assumeNotNull(fact.ex  
> ', ','))) <= 12 THEN '#6CCA6' ELSE  
> '#D05A50' END AS colors FROM fact AS fact  
> LEFT JOIN percentile AS percentile ON  
> 2) Скриншот показывает интерфейс BI-платформы Fastboard с открытым редактором SQL-запросов, содержащим два SELECT-выражения для агрегации данных по сущностям и филиалам, а также визуализацию в виде столбчатой диаграммы с цветовой кодировкой по медианному времени выполнения заказа.

