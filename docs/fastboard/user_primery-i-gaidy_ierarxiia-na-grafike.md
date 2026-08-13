# Иерархия на графике | Документация Fastboard

Source: https://help.fastboard.online/user/primery-i-gaidy/ierarxiia-na-grafike/


## **Задача**[​](#задача)

Добавить **несколько уровней** **детализации** на график.


## **Проблема**[​](#проблема)

Полезно смотреть не только на отдельные названия продуктов, но и на их категории, но делать 2 графика избыточно.


## **Решение**[​](#решение)

Создадим несколько разрезов **для линейчатого графика** и таблицы.

- Добавим таблицу по продажам и выручке. В качестве разреза будет **категория** и **название товара**:
![Добавим таблицу по продажам и выручке. В качестве разреза будет категория и название товара :](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-v8obnqeo.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-v8obnqeo.png)):
> Категория  
> Товар  
> Количество покупок  
> Сумма продаж  
> Выручка  
> Office Supplies  
> Staple envelope  
> 143  
> 5 037  
> 2 243  
> Office Supplies  
> Easy-staple paper  
> 137  
> 7 456  
> 3 260  
> Office Supplies  
> Staples  
> 137  
> 2 255  
> 871  
> Office Supplies  
> Avery Non-Stick Binders  
> 60  
> 652  
> 131  
> Office Supplies  
> Staples in misc. colors  
> 57  
> 1 436  
> 372  
> Furniture  
> KI Adjustable-Height Table  
> 54  
> 13 658  
> -745  
> Office Supplies  
> Staple remover  
> 54  
> 789  
> 72  
> Office Supplies  
> Storex Dura Pro Binders  
> 50  
> 832  
> 158  
> Furniture  
> Staple-based wall hangings  
> 48  
> 1 267  
> 366  
> Technology  
> Logitech 910-002974 M325 Wireless Mouse for Web Scrolling  
> 45  
> 4 229  
> 1 609  
> Итоги  
> 29 810  
> 6 841 264  
> 850 896  
> Скриншот показывает таблицу с данными по продажам товаров, сгруппированным по категориям, включая количество покупок, сумму продаж и выручку, а также итоговые значения.


- Перейдем в настройки разреза **“Категория”**. Включим настройку **“Группировать”**:
![Перейдем в настройки разреза “Категория” . Включим настройку “Группировать” :](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-eedxyspb.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-eedxyspb.png)):
> 1) Настроить  
> Пустые значения  
> Группировать  
> Параметры текста  
> Изменить свойства текста  
> Надчеркивание B I U  
> Размер 12 пикс  
> Межстрочный интервал 120 %  
> Межбуквенный интервал 0 пикс  
> Выравнивание (иконки: по левому краю, по центру, по правому краю, вверх, по вертикали, вниз)  
> Локальный шрифт  
> Изменить цвет текста  
> Вручную SQL  
> Реальные данные  
> Модель данных  
> Модель 1  
> Группировать все разрезы  
> Разрезы в шапке  
> + Добавить разрез  
> Разрезы в колонках  
> Категория  
> Sample_Superstore.Category  
> Товар  
> + Добавить разрез  
> 2) Скриншот показывает панель настроек визуализации в BI-платформе Fastboard с вкладками «Реальные данные» и настройками текста, группировки и разрезов.



## **Итог**[​](#итог)

Получили таблицу группировкой и возможностью раскрытия категорий для детального изучения товаров внутри нее:

![Получили таблицу группировкой и возможностью раскрытия категорий для детального изучения товаров](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-krswrwf0.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-krswrwf0.png)):
> 1)  
> Категория  
> Товар  
> Количество покупок  
> Сумма продаж  
> Выручка  
> Office Supplies  
> Furniture  
> Technology  
> Logitech 910-002974 M325 Wireless Mouse for Web Scrolling  
> Kingston Digital DataTraveler 16GB USB 2.0  
> Logitech Desktop MK120 Mouse and keyboard Combo  
> SanDisk Ultra 32 GB MicroSDHC Class 10 Memory Card  
> Geemarc AmpliPOWER60  
> Maxell 4.7GB DVD-R  
> Microsoft Sculpt Comfort Mouse  
> Итоги  
> 2) Скриншот показывает таблицу с данными по продажам товаров, сгруппированным по категориям (Office Supplies, Furniture, Technology), включая количество покупок, сумму продаж и выручку по каждому товару и в целом.



## **Иерархия в столбчатом графике:**[​](#иерархия-в-столбчатом-графике)

- Добавим график, в качестве разреза будет **категория**, а в качестве показателя **сумма продаж**:
![Добавим график, в качестве разреза будет категория , а в качестве показателя сумма продаж :](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-uz41rpon.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-uz41rpon.png)):
> Сумма продаж  
> 500,000  
> 400,000  
> 300,000  
> 200,000  
> 100,000  
> 0  
> Technology  
> Office Supplies  
> Furniture  
> Скриншот показывает столбчатую диаграмму «Сумма продаж» по трём категориям: Technology, Office Supplies и Furniture.


- Добавим еще один разрез по **подкатегории товара**. Появляется **переключатель** уровня детализации. При выборе нужного разреза график будет строиться на разных разрезах. Также можно проваливаться в категорию при нажатии на интересующую категорию:
![Добавим еще один разрез по подкатегории товара . Появляется переключатель уровня детализации. Пр](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-fbe03oix.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-04/embedded-image-fbe03oix.png)):
> 1)  
> Сумма продаж  
> Категория Подкатегория  
> 000,000  
> 800,000  
> 600,000  
> 400,000  
> 200,000  
> 0  
> Phones Paper Supplies Labels Appliances Envelopes  
> 2)  
> Скриншот показывает столбчатую диаграмму «Сумма продаж» по подкатегориям товаров (Phones, Paper, Supplies, Labels, Appliances, Envelopes), с переключателем между «Категория» и «Подкатегория», где активна вкладка «Подкатегория».



## **Итог**[​](#итог-1)

Построены графики с поддержкой иерархий
