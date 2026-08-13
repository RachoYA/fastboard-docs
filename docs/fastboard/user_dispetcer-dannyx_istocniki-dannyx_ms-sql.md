# MS SQL: особенности загрузки | Документация Fastboard

Source: https://help.fastboard.online/user/dispetcer-dannyx/istocniki-dannyx/ms-sql/

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


- Excel. Вместо даты может прийти непонятное число (например, 45565). Это внутренний способ excel хранить даты. Если чисто без дробной части это Дата. Нужно сделать следующее:
![Excel. Вместо даты может прийти непонятное число (например, 45565). Это внутренний способ excel](https://book.winsolutions.ru/uploads/images/gallery/2026-02/embedded-image-tjbrs89a.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-02/embedded-image-tjbrs89a.png)):
> 1) toDate(toInt32(trim("дата")) - 25569)  
> 2) Формула для преобразования строкового значения поля "дата" в числовой формат даты с вычитанием константы 25569, вероятно, для коррекции смещения дат (например, из Excel-формата).


- Если число дробное, то его нужно перевести еще к количеству миллисекунд:
![Если число дробное, то его нужно перевести еще к количеству миллисекунд:](https://book.winsolutions.ru/uploads/images/gallery/2026-02/embedded-image-ehba4uyd.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2026-02/embedded-image-ehba4uyd.png)):
> 1) toDateTIme ({"data" - 25569) * 86400),  
> 2) Формула для преобразования числового значения даты в формат DateTime, используемая в BI-платформе Fastboard.


Для csv файлов, в случае, неверного распознования надо задать разделитель и кодировку

Запрос в разделе Read при обращении к сторонней СУБД надо писать на запросе СУБД
