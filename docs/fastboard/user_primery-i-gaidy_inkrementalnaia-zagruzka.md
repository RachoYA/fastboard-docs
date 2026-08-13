# Инкрементальная загрузка | Документация Fastboard

Source: https://help.fastboard.online/user/primery-i-gaidy/inkrementalnaia-zagruzka/


## **Задача**[​](#задача)

Загружать данные в базу данных без переписывания имеющихся данных.


## **Проблема**[​](#проблема)

По умолчанию скрипт создается в режиме **полной перезаписи.** При каждом выполнении скрипта таблица удаляется и пересоздается. Для больших таблиц такая операция может быть **очень длительной**, xnn будет приводить к простою системы.


## **Решение**[​](#решение)

Изменить настройку скрипта, чтобы не переписывать а **дописывать** данные

- Переместим **секцию Delete под Create.** Вместе полного удаления таблицы (DROP) укажем конструкцию **ALTER** и **удалим данные за последние 7 дней.**
![Переместим секцию Delete под Create. Вместе полного удаления таблицы (DROP) укажем конструкцию A](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-0erjbyyx.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-0erjbyyx.png)):
> Alter @@@  
> ALTER TABLE "Sample_Superstore" DELETE WHERE "Order_Date" >= today() - interval 7 day  
> @@@  
> Скриншот показывает SQL-запрос для удаления записей из таблицы "Sample_Superstore", где дата заказа старше семи дней от текущей даты.


- Для запроса добавим такое же условие, будем получать данные только за последние 7 дней.
![Снимок экрана 2026-07-22 в 01.57.52.png](https://book.winsolutions.ru/uploads/images/gallery/2026-07/scaled-1680-/snimok-ekrana-2026-07-22-v-01-57-52.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-07/scaled-1680-/snimok-ekrana-2026-07-22-v-01-57-52.png)):
> 42 Read @@@  
> 43 SELECT  
> 44 "Row_ID",  
> 45 "Order_ID",  
> 46 "Order_Date",  
> 47 toYYYYMMDD(Order_Date),  
> 48 "Ship_Date",  
> 49 "Ship_Mode",  
> 50 "Customer_ID",  
> 51 "Customer_Name",  
> 52 "Segment",  
> 53 "Country",  
> 54 "City",  
> 55 "State",  
> 56 "Postal_Code",  
> 57 "Region",  
> 58 "Product_ID",  
> 59 "Category",  
> 60 "Sub_Category",  
> 61 "Product_Name",  
> 62 "Sales",  
> 63 "Quantity",  
> 64 "Discount",  
> 65 "Profit",  
> 66 "file_name",  
> 67 "updated_date",  
> 68 "fb_created_date"  
> 69 FROM  
> 70 "Sample_Superstore"  
> 71 WHERE  
> 72 "Order_Date" >= today() - interval 7 day  
> 73 @@@  
> Скриншот показывает SQL-запрос для выборки данных из таблицы Sample_Superstore с фильтрацией по дате заказа за последние 7 дней.



## **Итог**[​](#итог)

Данные не будут постоянно перезаписываться, каждый запуск скрипта будет удаляться информация за последние 7 дней и записываться заново, что при большом количестве данных сильно уменьшит время выполнения скрипта.
