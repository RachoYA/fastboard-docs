# Редактор скрипта загрузки | Документация Fastboard

Source: https://help.fastboard.online/user/dispetcer-dannyx/redaktor-skripta-zagruzki/

Скрипт загрузки генерируется автоматически после [выбора источников данных](https://help.fastboard.online/user/dispetcer-dannyx/vybor-dannyx-dlia-zagruzki/).

Этап ручного редактирования скрипта загрузки является **необязательным**, однако функциональность Fastboard позволяет при необходимости внести изменения.

![Снимок экрана 2026-02-09 в 03.27.09.png](https://book.winsolutions.ru/uploads/images/gallery/2026-02/scaled-1680-/snimok-ekrana-2026-02-09-v-03-27-09.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-02/scaled-1680-/snimok-ekrana-2026-02-09-v-03-27-09.png)):
> 1)  
> Скрипт загрузки  
> Модель данных  
> 1 Table "Biudzhets"  
> 2  
> 3 Delete @@@  
> 4 DROP TABLE IF EXISTS "Biudzhets"  
> 5 @@@  
> 6  
> 7 Create @@@  
> 8 CREATE TABLE IF NOT EXISTS "Biudzhets" (  
> 9   "Kompania_ID" Int8,  
> 10  "updated_date" Nullable(String)  
> 11 ) ENGINE = MergeTree()  
> 12 ORDER BY  
> 13 tuple()  
> 14 @@@  
> 15  
> 16 Source "Бюджет_демо"  
> 17  
> 18 Read @@@  
> Свернуть  
> 02:53:06 Получен скрипт  
> Сохранить скрипт  
> Запустить скрипт  
> Обновление данных  
> 2) Скриншот показывает интерфейс BI-платформы Fastboard с открытым SQL-скриптом для создания таблицы «Biudzhets» в ClickHouse, включая команды удаления, создания и чтения данных из источника «Бюджет_демо», а также кнопки управления скриптом.



## Правила использования редактора[​](#правила-использования-редактора)


| **Шаги** | **Ожидаемый результат** |
| --- | --- |
| В любом месте скрипта добавить строку *Source "Название коннекта"* где: Source - ключевое слово обозначающее вставку нового коннекта, "Название источника" - имя коннекта из списка источников | При вставке кода для импорта таблиц из этого источника таблицы успешно загрузятся в БД проекта |


### Добавить источник[​](#добавить-источник)


#### Добавить таблицу из источника[​](#добавить-таблицу-из-источника)


#### Удалить таблицу[​](#удалить-таблицу)


#### Добавить поле из таблицы источника в таблицу импорта[​](#добавить-поле-из-таблицы-источника-в-таблицу-импорта)


#### Удалить поле из таблицы[​](#удалить-поле-из-таблицы)


#### Изменить тип данных поля[​](#изменить-тип-данных-поля)

В настоящий момент для применения любых изменений в таблицах (создание поля, переимнование поля, изменение типа поля и т.д.) необходимо пересоздать таблицу в БД проекта. Для этого после внесения всех изменеий к имени таблицы можно добавить, например `\_1`, после этого сохранить, затем запустить скрипт. При необходимости вернуть таблице старое название тем же способом. *(Это связано с текущими ограничениями парсера. Мы над этим работаем)*


#### Создать вычисляемое поле в таблице[​](#создать-вычисляемое-поле-в-таблице)


#### Создать новую таблицу "Календарь"[​](#создать-новую-таблицу-календарь)

Вставить в скрипт загрузки следующий текст (обратите внимание на комментарии), после выполнения скрипта загрузки выполнить JOIN таблицы Calendar к вашей таблице фактов.


```
postgresql Table "calendar"Create @@@CREATE TABLE IF NOT EXISTS  "calendar" (    "id" Int32 NULL,    "key_date"   String NULL,    "date"   Date32 NULL,    "index_day"   Int32 NULL,    "day"   String NULL,    "week"   Int32 NULL,    "quarter"   Int32 NULL,    "year"   Int32 NULL,    "index_month"   Int32 NULL,    "month"   String NULL      ) ENGINE = MergeTree ()ORDER BY  tuple ()@@@ Delete @@@ALTER TABLE "calendar" DELETE WHERE 1=1@@@Source "promo_fb (RomanS)" -- Укажите любой существующий источник, чтобы сохранить в него вашу таблицуRead @@@SELECT  a."id"::text,  a."key_date"::text,  a."date"::text,  a."index_day"::text,  a."day"::text,  a."week"::text,  a."quarter"::text,  a."year"::text,  a."index_month"::text,  a."month"::textFROM(select distinct    row_number() over() as id,    date(date)::text as key_date,    date::date,    extract('isodow' from date)  as index_day,       CASE           WHEN extract('isodow' from date) = 1 then 'ПН' -- Если нужно, укажите названия дней (и месяцев ниже)           WHEN extract('isodow' from date) = 2 then 'ВТ'           WHEN extract('isodow' from date) = 3 then 'СР'           WHEN extract('isodow' from date) = 4 then 'ЧТ'           WHEN extract('isodow' from date) = 5 then 'ПТ'           WHEN extract('isodow' from date) = 6 then 'СБ'           WHEN extract('isodow' from date) = 7 then 'ВС' end as day,    extract('week' from date)     as week,    extract('quarter' from date ) as quarter,    extract('year' from date)     as year,    extract('month' from date)    as index_month,       CASE           WHEN extract('month' from date) = 1 then  'Январь'            WHEN extract('month' from date) = 2 then  'Февраль'           WHEN extract('month' from date) = 3 then  'Март'           WHEN extract('month' from date) = 4 then  'Апрель'           WHEN extract('month' from date) = 5 then  'Май'           WHEN extract('month' from date) = 6 then  'Июнь'           WHEN extract('month' from date) = 7 then  'Июль'           WHEN extract('month' from date) = 8 then  'Август'           WHEN extract('month' from date) = 9 then  'Сентябрь'           WHEN extract('month' from date) = 10 then 'Октябрь'           WHEN extract('month' from date) = 11 then 'Ноябрь'           WHEN extract('month' from date) = 12 then 'Декабрь'end as monthfrom generate_series(date'2015-01-01',date(now()),interval '1 day')as t(date) -- Выберите дату начала и интервалorder by   date desc) a@@@
```

**Таблица в результате:**

![image.png](https://book.winsolutions.ru/uploads/images/gallery/2023-09/scaled-1680-/FLEimage.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2023-09/scaled-1680-/FLEimage.png)):
> 1)  
> calendar  
> Предварительный просмотр  
> calendar  
> INNER  
> data2  
> =  
> Таблица  
> + Связать  
> id  
> key_date  
> date  
> index_day  
> day  
> week  
> quarter  
> year  
> index_month  
> month  
> 3183  
> 2023-09-18  
> 2023-09-18  
> 1  
> ПН  
> 38  
> 3  
> 2023  
> 9  
> Сентябрь  
> 3182  
> 2023-09-17  
> 2023-09-17  
> 7  
> ВС  
> 37  
> 3  
> 2023  
> 9  
> Сентябрь  
> 3181  
> 2023-09-16  
> 2023-09-16  
> 6  
> СБ  
> 37  
> 3  
> 2023  
> 9  
> Сентябрь  
> 2) Скриншот показывает интерфейс настройки соединения таблиц в BI-платформе Fastboard, где таблица «calendar» соединяется с другой таблицей через INNER JOIN по полю key_date, и отображается предварительный просмотр данных календаря с датами, днями недели, номерами недель, кварталов, годов и месяцев.



#### Загрузка данных из другого проекта[​](#загрузка-данных-из-другого-проекта)


### Некоторые особенности работы разными типами источников[​](#некоторые-особенности-работы-разными-типами-источников)


#### MS SQL[​](#ms-sql)

- При импорте данных с типом «Дата» нужно будет поля с датами в секции READ для этой таблицы сконвертировать в строку. КХ сам сконвертирует тип дата при создании таблицы у себя и они снова станут датами
![image.png](https://book.winsolutions.ru/uploads/images/gallery/2023-11/scaled-1680-/qS6image.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2023-11/scaled-1680-/qS6image.png)):
> Read  
> SELECT  
> "CreatedDate" ::text,  
> "ActivatedDate" ::text,  
> "PlannedEndDate" ::text;  
> Скриншот показывает фрагмент SQL-запроса для выборки трёх полей с приведением их типов к тексту.


- Поля с кодировкой UTF16 (тип varchar) нужно будет обернуть в cast. В той же секции @READ для этой таблицы. Иначе русскоязычные значения не распознаются в этих полях и появятся вопросительные знаки
![image.png](https://book.winsolutions.ru/uploads/images/gallery/2023-11/scaled-1680-/LiPimage.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2023-11/scaled-1680-/LiPimage.png)):
> Read 000
> SELECT
> "id"
> "cast("name" as nvarchar) as "name""
> Скриншот показывает фрагмент SQL-запроса с использованием функции CAST для преобразования типа данных поля name в nvarchar.


Excel. Вместо даты может прийти непонятное число (например, 45565). Это внутренний способ excel хранить даты. Если чисто без дробной части это Дата. Нужно сделать следующее: ![Excel. Вместо даты может прийти непонятное число (например, 45565). Это внутренний способ excel](https://book.winsolutions.ru/uploads/images/gallery/2026-02/embedded-image-tjbrs89a.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-02/embedded-image-tjbrs89a.png)):
> 1) toDate(toInt32(trim("дата")) - 25569)  
> 2) Формула для преобразования строкового значения поля "дата" в числовой формат даты с вычитанием константы 25569, вероятно, для коррекции смещения дат (например, из Excel-формата).


Если число дробное, то его нужно перевести еще к количеству миллисекунд:

![Если число дробное, то его нужно перевести еще к количеству миллисекунд:](https://book.winsolutions.ru/uploads/images/gallery/2026-02/embedded-image-ehba4uyd.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-02/embedded-image-ehba4uyd.png)):
> 1) toDateTIme ({"data" - 25569) * 86400),  
> 2) Формула для преобразования числового значения даты в формат DateTime, используемая в BI-платформе Fastboard.


Для csv файлов, в случае, неверного распознования надо задать разделитель и кодировку

Запрос в разделе Read при обращении к сторонней СУБД надо писать на запросе СУБД
