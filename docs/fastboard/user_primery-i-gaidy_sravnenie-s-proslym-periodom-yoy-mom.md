# Сравнение с прошлым периодом (YoY, MoM) | Документация Fastboard

Source: https://help.fastboard.online/user/primery-i-gaidy/sravnenie-s-proslym-periodom-yoy-mom/


## **Задача**[​](#задача)

Сравнить продажи **текущего периода** с продажами **предыдущего месяца** и **аналогичным месяцем прошлого года** на одном графике **(три линии).**


## **Проблема**[​](#проблема)

Без сложных подзапросов или оконных функций со сдвигом (LAG) трудно подтянуть данные за другой период, динамически привязанный к текущей дате.


## **Решение**[​](#решение)

Для сдвига по дате создадим **таблицу с календарем**, **подключим к данным** и **реализуем расчеты со сдвигом**

- Создаем **новую таблицу календаря**
![Снимок экрана 2026-07-22 в 01.41.09.png](https://book.winsolutions.ru/uploads/images/gallery/2026-07/scaled-1680-/snimok-ekrana-2026-07-22-v-01-41-09.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-07/scaled-1680-/snimok-ekrana-2026-07-22-v-01-41-09.png)):
> 1)  
> Table "calendar"  
> Create @@@  
> CREATE TABLE IF NOT EXISTS "calendar"  
> (  
>     "offset"          String,  
>     "date_id"         UInt32,  
>     "date"            Date,  
>     "date_rus"        String  
> ) ENGINE = MergeTree()  
> ORDER BY  
>     tuple ()  
> @@@  
> Delete @@@  
> DROP TABLE IF EXISTS "calendar"  
> @@@  
> Source "ClickHouse common"  
> Read @@@  
> -- тут будет запрос  
> @@@  
> Optimize @@@  
> OPTIMIZE TABLE "calendar"  
> @@@  
> 2) Скриншот показывает фрагмент SQL-скрипта для создания, удаления и оптимизации таблицы «calendar» в ClickHouse с указанием структуры полей и движка MergeTree.


Добавим **запрос для заполнения календаря в секцию Read**

В данном запросе мы создаем **CTE** с датами начиная с 2010 года и **на 2 года вперед** от текущего момента. **Дальше** для каждой даты получаем ее id формулой **toYYYYMMDD** и добавим поле для форматированного вывода даты. **Дальше** **объединяем 3 раза** и указываем разный offset.

- **offset = ‘0’:** Даты без преобразования берутся из CTE. Данная часть будет ссылаться на текущие данные
- **offset = ‘-1Y’:** Даты берутся такие же, но id даты указывает на дату с прошлогодним id
- **offset = ‘-1M’:** Аналогично с -1Y, но id указывает на id прошлого месяца
Далее необходимо **добавить поле для связи** в нашу таблицу с продажами. В качестве этого поля выступает **id даты** (функция - toYYYYMMDD(<поле с датой>)

![Frame 334.png](https://book.winsolutions.ru/uploads/images/gallery/2026-07/scaled-1680-/frame-334.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-07/scaled-1680-/frame-334.png)):
> 1)  
> Read  
> SELECT  
> "Row_ID",  
> "Order_ID",  
> "Order_Date",  
> toYYYYMMDD("Order_Date"),  
> "Ship_Date",  
> "Ship_Mode",  
> "Customer_ID",  
> "Customer_Name",  
> "Segment",  
> "Country",  
> "City",  
> "State",  
> "Postal_Code",  
> "Region",  
> "Product_ID",  
> "Category",  
> "Sub_Category",  
> "Product_Name",  
> "Sales",  
> "Quantity",  
> "Discount",  
> "Profit",  
> "file_name",  
> "updated_date",  
> "fb_created_date"  
> FROM  
> "Sample_Superstore"  
> 2) Скриншот показывает SQL-запрос для выборки данных из таблицы "Sample_Superstore" с преобразованием поля "Order_Date" в формат YYYYMMDD.


В модели данных **основной датасет** (с фактами) **связывается с календарем** по полю даты (LEFT JOIN).

![В модели данных основной датасет (с фактами) связывается с календарем по полю даты (LEFT JOIN).](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-cmgoaljk.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-cmgoaljk.png)):
> 1)  
> Fit  
> +  
> -  
> 1:1  
> 76%  
> Sample_Superstore  
> date_id  
> calendar  
> date_id  
> Sample_Superstore  
> Связи  
> Sample_Superstore  
> Вид JOIN  
> LEFT  
> =  
> calendar  
> date_id  
> + Новая связь  
> 2) Скриншот показывает настройку связи между таблицами Sample_Superstore и calendar по полю date_id с использованием LEFT JOIN в BI-платформе Fastboard.


На дашборде **создаем 3 показателя** с разным условием для поля offset

![Снимок экрана 2026-07-22 в 01.51.40.png](https://book.winsolutions.ru/uploads/images/gallery/2026-07/scaled-1680-/snimok-ekrana-2026-07-22-v-01-51-40.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-07/scaled-1680-/snimok-ekrana-2026-07-22-v-01-51-40.png)):
> 1)  
> sumIf (Sample_Superstore.Sales, calendar.offset = '0') AS "Текущее значение",  
> sumIf (Sample_Superstore.Sales, calendar.offset = '-1M') AS "Прошлый месяц",  
> sumIf (Sample_Superstore.Sales, calendar.offset = '-1Y') AS "Прошлый год"
> 2) Скриншот показывает три SQL-подобные формулы для вычисления продаж за текущий период, прошлый месяц и прошлый год с использованием функции sumIf и фильтрации по полю calendar.offset.


- В качестве разреза используем **название месяца**
![Снимок экрана 2026-07-22 в 01.52.29.png](https://book.winsolutions.ru/uploads/images/gallery/2026-07/scaled-1680-/snimok-ekrana-2026-07-22-v-01-52-29.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-07/scaled-1680-/snimok-ekrana-2026-07-22-v-01-52-29.png)):
> 1) месяцName (calendar.date) AS "Месяц"  
> 2) Скриншот показывает SQL-выражение для получения названия месяца из поля calendar.date с псевдонимом "Месяц".



## **Итог**[​](#итог)

Получили график с возможностью сравнивать значения с прошлым месяцем или годом.

![Получили график с возможностью сравнивать значения с прошлым месяцем или годом.](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-9ogqfnzh.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-9ogqfnzh.png)):
> 1) Динамика фактов по месяцам  
> January March May July September November  
> Текущее значение Прошлый месяц Прошлый год  
> 2) График показывает динамику трёх показателей (текущее значение, прошлый месяц, прошлый год) по месяцам с января по ноябрь.


Также такую формулу можно использовать **в KPI карточке**:

- Используем те же формулы в переменных, и **рассчитаем отклонение в процентах**
![Снимок экрана 2026-07-22 в 01.47.53.png](https://book.winsolutions.ru/uploads/images/gallery/2026-07/scaled-1680-/snimok-ekrana-2026-07-22-v-01-47-53.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-07/scaled-1680-/snimok-ekrana-2026-07-22-v-01-47-53.png)):
> 1)  
> sumIf (Sample_Superstore.Sales, calendar.offset = '0') / 1e3 AS val,  
> sumIf (Sample_Superstore.Sales, calendar.offset = '-1M') / 1e3 AS prev_val,  
> (val - prev_val) / prev_val AS dev  
> 2) Скриншот показывает фрагмент SQL-запроса с вычислением текущих и предыдущих продаж в тысячах единиц и их относительного изменения.


- В блоке текста указываем переменные
![В блоке текста указываем переменные](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-am4ok6wo.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-am4ok6wo.png)):
> 1) Текст:  
> T  
> Текст  
> Выручка  
> {{val}}  
> {{dev}}  
> 2) Скриншот показывает интерфейс редактора текстового поля в BI-платформе Fastboard с шаблоном для отображения метрики «Выручка» и её отклонения.



## **Результат**[​](#результат)

Получили простую карточку с сравнение текущей выручки с выручкой в прошлом месяце

![Получили простую карточку с сравнение текущей выручки с выручкой в прошлом месяце](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-cngj4r5k.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-cngj4r5k.png)):
> Выручка  
> $ 57,0 тыс.  
> +50% MoM  
> Скриншот показывает показатель выручки в размере 57,0 тысяч долларов США с ростом на 50% по сравнению с предыдущим месяцем (MoM).

