# Маркер динамики в таблице | Документация Fastboard

Source: https://help.fastboard.online/gostech/primery-i-gaidy/marker-dinamiki-v-tablice/


## **Задача**[​](#задача)

Подсветить товары с **отрицательной** выручкой.


## **Решение**[​](#решение)

Создадим таблицу и добавим маркер **к столбцу выручки,** который будет виден только при отрицательной выручке.

- Создание таблицы с разрезами **Категория** и **Название товара**, добавить показатели **по количеству продаж**, **сумме продаж** и **выручке:**
![](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-jpt4b46r.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-jpt4b46r.png)):
> Категория  
> Количество покупок  
> Сумма продаж  
> Выручка  
> Office Supplies  
> 17 971  
> 2 146 995  
> 364 467  
> Furniture  
> 6 326  
> 2 208 879  
> 54 924  
> Technology  
> 5 513  
> 2 485 390  
> 431 504  
> Итого  
> 29 810  
> 6 841 264  
> 850 896  
> Скриншот показывает таблицу с агрегированными данными по категориям товаров: количество покупок, сумма продаж и выручка, включая итоговые значения.


- Включим отображение маркера **в настройках показателя** “Выручка”:
![](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-purz6dis.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-purz6dis.png)):
> Маркер динамики  
> Позиционирование  
> Слева Справа Отступ 10 пикс  
> Размер 10 пикс  
> Режим настройки  
> По диапазонам Раздельно  
> Настроить  
> Скриншот показывает панель настроек маркера динамики в BI-платформе Fastboard, включая параметры позиционирования, размера и режима настройки.


- Настроим **условия для маркера**. Для отрицательных значений будем выводить красный треугольник, для положительных не будем выводить маркер:
![](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-cefjkxwi.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-cefjkxwi.png)):
> 1)  
> Настроить маркер динамики  
> Значение <= 0 и < 100 то Цвет ● Фигура ▼ 🗑️  
> Показывать по умолчанию ○ Цвет ○ Фигура ● ▼  
> Добавить условие Отменить Сохранить  
> Изображение  
> Сортировать по этому столбцу  
> По возрастанию По убыванию  
> Рассчитать итог  
> Маркер динамики  
> Позиционирование Слева Справа Отступ 10 пикс  
> Размер 10 пикс  
> Режим настройки По диапазонам Раздельно  
> Настроить  
> 2) Настройка маркера динамики в BI-платформе Fastboard: условия отображения, цвет, фигура, позиционирование, размер и режим настройки.



## **Итог**[​](#итог)

Получили таблицу с подсветкой товаров у которых отрицательная выручка:

![](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-x0jcqvkb.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-x0jcqvkb.png)):
> 1)  
> Категория  
> Группы ▲  
> Количество покупок ▼  
> Сумма продаж  
> Выручка  
> Anderson Hickey Conga Table Tops & Accessories  
> 6  
> 155  
> ▼ -53  
> Artistic Insta-Plaque  
> 9  
> 470  
> 183  
> Atlantic Metals Mobile 2-Shelf Bookcases, Custom Colors  
> 6  
> 1 200  
> ▼ -340  
> Atlantic Metals Mobile 3-Shelf Bookcases, Custom Colors  
> 23  
> 21 066  
> 2 140  
> Atlantic Metals Mobile 4-Shelf Bookcases, Custom Colors  
> 18  
> 15 552  
> ▼ -379  
> Atlantic Metals Mobile 5-Shelf Bookcases, Custom Colors  
> 24  
> 16 479  
> 45  
> BPI Conference Tables  
> 15  
> 6 726  
> ▼ -2 388  
> Balt Solid Wood Rectangular Table  
> 12  
> 2 484  
> ▼ -649  
> Balt Solid Wood Round Tables  
> 12  
> 19 556  
> ▼ -3 603  
> Balt Split Level Computer Training Table  
> 14  
> 3 053  
> ▼ -1 027  
> Итого  
> 29 810  
> 6 841 264  
> 850 896  
> 2) Скриншот показывает таблицу с данными по продажам: категории товаров, количество покупок, сумма продаж и выручка (с индикаторами роста/падения), включая итоговые значения.

