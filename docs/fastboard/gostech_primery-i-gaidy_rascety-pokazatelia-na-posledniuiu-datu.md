# Расчеты показателя на последнюю дату | Документация Fastboard

Source: https://help.fastboard.online/gostech/primery-i-gaidy/rascety-pokazatelia-na-posledniuiu-datu/


## **Задача**[​](#задача)

Найти сумму остатков или платежей только на последнюю дату в выбранном периоде, **игнорируя остальные дни**.


## **Проблема**[​](#проблема)

Данные хранятся ежедневно, но нужен итог именно на конец периода. BI-система часто **не позволяет использовать простые подзапросы** (вроде WHERE date = MAX(date)) в стандартных агрегациях.


## **Решение**[​](#решение)

Использовать **ClickHouse функцию sumArgMax**.

Функция принимает **два параметра**:

- столбец со значениями для суммирования
- и столбец, по которому определяется максимум
В результате будут просуммированы все значения из первого столбца, соответствующие строкам с максимальным значением во втором столбце.


## **Реализуем решение**[​](#реализуем-решение)

Добавим карточку KPI и добавим **2 переменные:**

- **date** для хранения максимальной даты в периоде
- **val** для хранения значения суммы продаж
Добавим их в шаблон карточки:

![](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-a2k7lsu3.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-a2k7lsu3.png)):
> 1) Текст:  
> T  
> Текст  
> Выручка {{date}}  
> {{val}}  
> 2) Скриншот показывает редактор шаблона текста в BI-платформе Fastboard с переменными для даты и значения выручки.
![](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-ycvqv7q6.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-ycvqv7q6.png)):
> Переменные  
> f date  
> f val  
> + Добавить переменную  
> Скриншот показывает интерфейс раздела «Переменные» в BI-платформе Fastboard, где отображены две переменные (date и val) и кнопка для добавления новой переменной.


- Для даты найдем **максимальную дату в периоде** и приведем к удобному формату. Для расчета значений продаж используем **sumArgMax** (<столбец с продажами>, <столбец с датой>)
![](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-d2lelctg.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-d2lelctg.png)):
> 1)  
> formatDateTime (MAX(Sample_Superstore.Order_Date), '%d.%m.%y') AS date,  
> sumArgMax (  
>     Sample_Superstore.Profit,  
>     Sample_Superstore.Order_Date  
> ) AS val  
> 2) Скриншот показывает фрагмент SQL-запроса для агрегации данных: получение последней даты заказа и соответствующей ей максимальной прибыли из таблицы Sample_Superstore.



## **Итог**[​](#итог)

Получаем карточку KPI с рассчитанным значением на последнюю дату в произвольном периоде:

![](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-7heaurh4.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-7heaurh4.png)):
> 04.12.2017 - 14.12.2017 ×  
> Выручка на 14.12.17  
> $ 646  
> Скриншот показывает выручку за период с 04.12.2017 по 14.12.2017, равную $646, с акцентом на значение за 14.12.17.

