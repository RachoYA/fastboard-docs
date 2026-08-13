# 1.9.0 | 19.09.2025 | Документация Fastboard

Source: https://help.fastboard.online/user/roadmap/v190/


## **Графический редактор**[​](#графический-редактор)


### **SVG**[​](#svg)

SVG-объект представляет собой векторный файл, состоящий из областей. В качестве примеров можно использовать карты регионов, планы помещений, здания или земельные участки. Для корректной работы в системе каждая область должна иметь уникальный идентификатор (name, title или id).

![image.png](https://book.winsolutions.ru/uploads/images/gallery/2025-08/scaled-1680-/image.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2025-08/scaled-1680-/image.png)):
> 1) Drafts Free  
> File Assets Q  
> Pages +  
> Page 1  
> Layers ≡  
> # russia (1) 1  
> H RU-KAM  
> H RU-KO  
> ∞ RU-KGD  
> H RU-KHM  
> H RU-KL  
> H RU-KK  
> H RU-KR  
> H RU-KHA  
> H RU-KLU  
> H RU-KEM  
> H RU-KDA ←  
> ∞ RU-KC  
> ∞ RU-KB  
> H RU-IVA  
> H RU-IRK  
> 9 RU-IN  
> H RU-AL  
> H RU-DA  
> H RU-CU  
> H RU-CHU  
> H RU-CHE  
> 25.03 × 22.68  
> 2) Скриншот показывает интерфейс BI-платформы Fastboard с деревом слоёв карты России, где выделен слой «RU-KDA» (Краснодарский край), и на карте отображена его граница с размерами области выделения.


Если в исходном файле идентификаторы отсутствуют (например, Figma экспортирует координаты вместо названий), то области становятся неинтерактивными и данные к ним привязать нельзя.

![image.png](https://book.winsolutions.ru/uploads/images/gallery/2025-08/scaled-1680-/rYBimage.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2025-08/scaled-1680-/rYBimage.png)):
> 1)  
> Drafts Free  
> File Assets Q  
> Pages +  
> Page 1  
> Layers ≡  
> Карта России с областями 1  
> _x41A_x443_x440_x433_x436  
> _x427_x435_x43B_x44F_x431  
> _x420_x435_x441_x43F_x443  
> _x412_x43E_x440_x43E_x43C  
> _x412_x43B_x430_x434_x43E  
> _x422_x430_x43C_x431_x43E  
> _x420_x44F_x437_x430_x43D  
> _x41F_x435_x43D_x437_x435  
> _x420_x435_x441_x43F_x443  
> _x41A_x440_x430_x441_x43D ← (выделено красной рамкой и стрелкой)  
> _x411_x435_x43B_x433_x...  
> _x412_x43E_x43B_x433_x43E  
> _x422_x443_x43B_x44C_x44  
> _x420_x43E_x441_x442_x43E  
> _x41E_x440_x43B_x43E_x432  
> _x41C_x43E_x441_x43A_x43E  
> _x41C_x43E_x441_x43A_x43E  
> _x41B_x438_x43F_x435_x446  
> _x41A_x443_x440_x441_x43A  
> _x41A_x430_x43B_x443_x436  
> 31.9 × 30.7  
> 2) Скриншот показывает интерфейс BI-платформы Fastboard с картой России, разделённой на области, где одна из областей выделена синим контуром и связана с элементом списка слева через красную стрелку.


После загрузки корректного SVG в контейнер доступно взаимодействие с областями: привязка данных из модели, настройка цветов и текста в разных состояниях, проектирование переходов по ссылкам.

![image.png](https://book.winsolutions.ru/uploads/images/gallery/2025-08/scaled-1680-/XO9image.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2025-08/scaled-1680-/XO9image.png)):
> 1) Заголовок  
> Подзаголовок  
> Murmansk 387  
> Arkhangelsk 99  
> Komi 357  
> Yakutsk 462  
> Magadan 334  
> Buryatia  
> Chita  
> Amur 203  
> Khabarovsk  
> Primorskye  
> Sakhalin 190  
> Kamchatka  
> Leningrad 45  
> Novgorod  
> Pskov  
> Tver  
> Smolensk  
> Kaliningrad  
> Moscow  
> Nizhny Novgorod  
> Vladimir  
> Ivanovo  
> Yaroslavl  
> Kostroma  
> Vologda  
> Kirov  
> Perm  
> Chelyabinsk  
> Orenburg  
> Samara  
> Saratov  
> Volgograd  
> Rostov  
> Stavropol  
> Krasnodar  
> Adygea  
> Karachay-Cherkessia  
> Kabardino-Balkaria  
> North Ossetia-Alania  
> Ingushetia  
> Chechnya  
> Dagestan  
> Astrakhan  
> Kalmykia  
> Ulyanovsk  
> Penza  
> Tambov  
> Lipetsk  
> Voronezh  
> Belgorod  
> Kursk  
> Bryansk  
> Tula  
> Ryazan  
> Oryol  
> Smolensk  
> Novgorod  
> Pskov  
> Leningrad  
> Murmansk  
> Arkhangelsk  
> Nenets Autonomous Okrug  
> Komi Republic  
> Udmurtia  
> Mari El  
> Chuvashia  
> Tatarstan  
> Bashkortostan  
> Orenburg  
> Samara  
> Saratov  
> Volgograd  
> Rostov  
> Stavropol  
> Krasnodar  
> Adygea  
> Karachay-Cherkessia  
> Kabardino-Balkaria  
> North Ossetia-Alania  
> Ingushetia  
> Chechnya  
> Dagestan  
> Astrakhan  
> Kalmykia  
> Ulyanovsk  
> Penza  
> Tambov  
> Lipetsk  
> Voronezh  
> Belgorod  
> Kursk  
> Bryansk  
> Tula  
> Ryazan  
> Oryol  
> Smolensk  
> Novgorod  
> Pskov  
> Leningrad  
> Murmansk  
> Arkhangelsk  
> Nenets Autonomous Okrug  
> Komi Republic  
> Udmurtia  
> Mari El  
> Chuvashia  
> Tatarstan  
> Bashkortostan  
> Orenburg  
> Samara  
> Saratov  
> Volgograd  
> Rostov  
> Stavropol  
> Krasnodar  
> Adygea  
> Karachay-Cherkessia  
> Kabardino-Balkaria  
> North Ossetia-Alania  
> Ingushetia  
> Chechnya  
> Dagestan  
> Astrakhan  
> Kalmykia  
> Ulyanovsk  
> Penza  
> Tambov  
> Lipetsk  
> Voronezh  
> Belgorod  
> Kursk  
> Bryansk  
> Tula  
> Ryazan  
> Oryol  
> Smolensk  
> Novgorod  
> Pskov  
> Leningrad  
> Murmansk  
> Arkhangelsk  
> Nenets Autonomous Okrug  
> Komi Republic  
> Udmurtia  
> Mari El  
> Chuvashia  
> Tatarstan  
> Bashkortostan  
> Orenburg  
> Samara



## **Обмен сообщениями между пользователями**[​](#обмен-сообщениями-между-пользователями)

Добавлена система комментариев с переписками, уведомлениями и флажками. Теперь к любой визуализации можно прикрепить комментарий, внутри которого ведётся переписка (чат). Для каждого комментария система формирует переписку, к ней можно прикреплять текст, изображения, эмодзи, а также отмечать участников с помощью тега '@'. При выборе пользователя подтягиваются его имя и фамилия из профиля.


### **Доступность функционала**[​](#доступность-функционала)


| **Функционал** | **Размещение** | **Иллюстрация** |
| --- | --- | --- |
| **Уведомления по всем проектам** | Страница менеджера проектов | [![Проекты потока.jpg](https://book.winsolutions.ru/uploads/images/gallery/2025-08/scaled-1680-/proekty-potoka.jpg)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2025-08/scaled-1680-/proekty-potoka.jpg)):
> 1)  
> A  
> 4  
> Пометить все как прочитанные  
> Серафим А: Пожалуйста, добавьте на гр... Час назад @ 4  
> Оборачиваемость запасов – Страница номер четырна...  
> Тут будет текст первого комментария столько сколько влезет в...  
> Серафим А: Пожалуйста, добавьте на гр... Час назад @ 4  
> Оборачиваемость запасов – Страница номер четырна...  
> Тут будет текст первого комментария столько сколько влезет в...  
> Серафим А: Пожалуйста, добавьте на гр... Час назад @ 4  
> Оборачиваемость запасов – Страница номер четырна...  
> Тут будет текст комментария столько ск ко влезет в одну стр...  
> Серафим А: Пожалуйста, добавьте на гр... Час назад @ 4  
> Оборачиваемость запасов – Страница номер четырна...  
> Тут будет текст первого комментария столько сколько влезет в...
> 2) Скриншот показывает интерфейс раздела уведомлений или комментариев BI-платформы Fastboard с повторяющимися записями от пользователя «Серафим А», содержащими упоминания о добавлении данных на график и ссылками на страницу по теме «Оборачиваемость запасов».
](https://book.winsolutions.ru/uploads/images/gallery/2025-08/proekty-potoka.jpg) |
| **Показываются непрочитанные сообщения и их количество по конкретному проекту** | Карточка проекта | [![Проекты потока (1).jpg](https://book.winsolutions.ru/uploads/images/gallery/2025-08/scaled-1680-/proekty-potoka-1.jpg)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2025-08/scaled-1680-/proekty-potoka-1.jpg)):
> 1)  
> Серафим А: Пожалуйста, добавьте на гр... Час назад @ 4  
> Оборачиваемость запасов – Страница номер четырна...  
> Тут будет текст первого комментария столько сколько влезет в...  
> Серафим А: Пожалуйста, добавьте на гр... Час назад @ 4  
> Оборачиваемость запасов – Страница номер четырна...  
> Тут будет текст первого комментария столько сколько влезет в...  
> Оборачиваемость запасов  
> Ставки по банковским продуктам  
> 2) Скриншот показывает интерфейс BI-платформы Fastboard с карточками дашбордов и всплывающими комментариями пользователя Серафима А.
](https://book.winsolutions.ru/uploads/images/gallery/2025-08/proekty-potoka-1.jpg) |
| **Флажки на визуализациях, доступ к перепискам, привязанным к объектам** | Страница проекта | [![Дэсктоп выкл.jpg](https://book.winsolutions.ru/uploads/images/gallery/2025-08/scaled-1680-/desktop-vykl.jpg)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2025-08/scaled-1680-/desktop-vykl.jpg)):
> 1) Тепловая карта  
> Ступенями  
> X: Разрез 1 > Разрез 2 > Разрез 3  
> Серафим Ануфриев 3 дня назад  
> Lorem ipsum dolor sit amet consectetur.  
> Aliquam massa facilisis tristique adipisci...  
> 7 ответов  
> Sunday  
> Monday  
> Tuesday  
> Wednesday  
> Thursday  
> Friday  
> Saturday  
> 12a 2a 4a 6a 8a 10a 12p 2p 4p 6p 8p 10p  
> 1 2 1 3 7 3 1 1 7 5 1  
> 1 3 1 3 1 1 1  
> 3 1 1 1  
> 1 1 1  
> 4 1 5 10 5 7 11 6 5 3 4 2  
> 2 4 4 4 14 12 1 8 5 3 7 3  
> 5 4 7 14 13 12 9 5 5 10 6 4 4 1  
> 3 2 1 9 8 10 6 5 5 5 7 4 2 4  
> 5 2 2 6 9 11 6 7 8 12 5 5 7 2  
> 2 4 1 1 3 4 6 4 4 3 3 2 5  
> 0 - 5 5 - 10 10 - 15 15 - 20  
> 2) Скриншот показывает тепловую карту активности по дням недели и часам суток с всплывающим комментарием пользователя, содержащим текст-заполнитель и количество ответов.
](https://book.winsolutions.ru/uploads/images/gallery/2025-08/desktop-vykl.jpg) |
| **Комментарии на каждой странице проекта** | Панель комментариев (чат) | [![Дэсктоп выкл (1).jpg](https://book.winsolutions.ru/uploads/images/gallery/2025-08/scaled-1680-/desktop-vykl-1.jpg)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2025-08/scaled-1680-/desktop-vykl-1.jpg)):
> 1)  
> Page 3  
> Локальный 2 ×  
> 2019 2020 2021  
> Комментарии в проекте ×  
> Q ∅ ⚙️  
> 2 часа назад  
> Серафим Ануфриев и еще 2  
> Lorem ipsum dolor sit amet consectetur. Proin nisl felis malesuada convallis nunc suspendisse lorem. Ac ligula id vel arcu.  
> 2 часа назад  
> Валерий Леонтьев  
> Подвинуть график ниже, чтобы не было наслоения.  
> 2) Скриншот показывает панель комментариев к проекту в BI-платформе Fastboard с двумя сообщениями пользователей и интерфейсом фильтрации/поиска.
](https://book.winsolutions.ru/uploads/images/gallery/2025-08/desktop-vykl-1.jpg) |
| **Переписка между пользователями** | Страница проекта | [![Дэсктоп выкл (2).jpg](https://book.winsolutions.ru/uploads/images/gallery/2025-08/scaled-1680-/pbKdesktop-vykl-2.jpg)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2025-08/scaled-1680-/pbKdesktop-vykl-2.jpg)):
> 1) Переписка  
> Оборачиваемость запасов • Страница номер четырнадцать  
> Создано: 12.10.2024  
> Применить выборку  
> Серафим Ануфриев 2 часа назад  
> Lorem ipsum dolor sit amet consectetur. Aliquam massa facilisis tristique adipiscing mi consequat pharetra.  
> 1 час назад Вы  
> Добрый день! Ваш запрос принят.  
> Тимур Алибеков 2 минуты назад  
> Lorem ipsum dolor sit amet  
> Каштан Барбитуратов минуту назад  
> Lorem ipsum dolor sit amet consectetur. Ante dictum convallis justo suspendisse et dictum tellus turpis pretium. Ut habitant at sit amet. Sapien s...  
> Закрыть  
> Ответить  
> 2) Скриншот показывает интерфейс переписки в BI-платформе Fastboard с сообщениями пользователей и системными элементами управления.
](https://book.winsolutions.ru/uploads/images/gallery/2025-08/pbKdesktop-vykl-2.jpg) |


## **Менеджер проектов**[​](#менеджер-проектов)


### **Публикация дашборда в Интернет для использования на сайтах и внутренних порталах**[​](#публикация-дашборда-в-интернет-для-использования-на-сайтах-и-внутренних-порталах)

Новый режим проекта – публичный. В этом режиме проект доступен для просмотра любому пользователю, у которого есть ссылка, но все настройки редактирования недоступны никаким образом. Запускается процесс с помощью кнопки "Опубликовать (общедоступно)", которая запускает пошаговый процесс публикации проекта, который включает в себя активацию публичного режима, формирование публичной ссылки и iFrame для подстановки в HTML-код.

![Всплывающее окно Публикации](https://help.fastboard.online/assets/images/project-context-menu-242e6a719eb81b7d2259ae08f84b7fbc.png)

> **Со скриншота** ([изображение](https://help.fastboard.online/assets/images/project-context-menu-242e6a719eb81b7d2259ae08f84b7fbc.png)):
> Копировать  
> Переместить  
> Откатить  
> Защитить  
> Переименовать  
> Изменить статус  
> О проекте  
> В корзину  
> Экспортировать проект  
> Опубликовать (общедоступно)  
> Скриншот показывает контекстное меню с действиями над проектом в BI-платформе Fastboard, включая публикацию как общедоступную.


![Frame 1764 (1).jpg](https://book.winsolutions.ru/uploads/images/gallery/2025-08/scaled-1680-/frame-1764-1.jpg)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2025-08/scaled-1680-/frame-1764-1.jpg)):
> 1)  
> Публикация проекта в общедоступном режиме  
> Готово!  
> Публичная версия проекта успешно создана и готова к совместному использованию  
> Название проекта  
> Внутренняя аналитика  
> Ширина  
> 1100  
> Высота  
> 750  
> Страница по умолчанию  
> Страница 1  
> Ссылка на публичную версию проекта  
> https://book.winsolutions.ru/books/konstruk...  
> Копировать  
> HTML-код для быстрой подстановки в веб-сайт  
> <iframe title="Внутренняя аналитика" width="300" height="200" src="https://www.openstreetmap.org/export/embed.html?bbox=-0.004017949104309083%2C51.47612752641776%2C0.00030577182769775396%2C51.478569861898606&layer=mapnik">  
> </iframe>  
> Копировать  
> Страница 1  
> Страница 2  
> Страница 3  
> Выбрать период: 1  
> Active  
> Cancelled  
> Closed  
> Completed  
> Resolved  
> Фильтр 1 ▾  
> Сброс  
> Кнопка  
> Заголовок  
> Подзаголовок  
> Период 1  
> Период 2  
> Период 3  
> Количество задач  
> Дата выполнения задачи  
> Типы задач  
> New  
> In Progress  
> Done  
> Completed  
> Resolved  
> Design  
> Test  
> Active  
> Closed  
> Cancelled  
> Сделано в Fastboard  
> Закрыть  
> Сохранить  
> 2) Скриншот показывает окно подтверждения публикации проекта «Внутренняя аналитика» в общедоступном режиме на платформе Fastboard, включая параметры отображения, ссылку и HTML-код для встраивания, а также превью дашборда с графиками и диаграммами.



## **Диспетчер данных**[​](#диспетчер-данных)


### **Разделы в скрипте загрузки**[​](#разделы-в-скрипте-загрузки)

Появилась дополнительная панель **Разделы,** на которой можно разделить скрипт загрузки на несколько частей. Для этого необходимо создать новый раздел и перенести на нее необходимую часть кода. Разделение происходит руками пользователя. Порядок разделов важен.

![Разделы в скрипте загрузки](https://help.fastboard.online/assets/images/снимок-экрана-2025-09-24-в-12.00.45-6f573e0abc4529783aee276fa4d5f3de.png)

> **Со скриншота** ([изображение](https://help.fastboard.online/assets/images/снимок-экрана-2025-09-24-в-12.00.45-6f573e0abc4529783aee276fa4d5f3de.png)):
> 1)  
> Подключения  
> Все типы  
> Поиск  
> import_dds_new_xlsx  
> 4c9e6660-9...54bd316.xlsx  
> import_dds_xlsx  
> d276937d-1...f440350.xlsx  
> import_discharge_dds  
> d6711c63-2...904de4d.xlsx  
> import_discharge_dds_xlsx  
> 2dd75777-3...3baee79.xlsx  
> import_ebitda_xlsx  
> 15b2b5fb-f...77044cd.xlsx  
> import_pl_form_xlsx  
> 83ef39ea-c...2d0c518.xlsx  
> import_planned_rates_xlsx  
> 985624f4-9...283f62d.xlsx  
> import_src_budgets_pl_xlsx  
> ccaff580-4...07f36f9.xlsx  
> import_src_dds_form_xlsx  
> 074e17cc-1...2337166.xlsx  
> + Создать подключение  
> Разделы  
> Страница  
> + Создать  
> Скрипт загрузки  
> Модель данных  
> Table "Costs"  
> Delete @@@  
> DROP TABLE IF EXISTS "Costs"  
> @@@  
> Create @@@  
> CREATE TABLE IF NOT EXISTS "Costs" (  
>   "Date" Nullable(String),  
>   "Sum" Nullable(String),  
>   "Product_name" Nullable(String),  
>   "Category" Nullable(String),  
>   "file_name" Nullable(String),  
>   "updated_date" Nullable(String),  
>   "fb_created_date" Nullable(String)  
> ) ENGINE = MergeTree()  
> 12:00:25 Получен скрипт  
> 2) Скриншот показывает интерфейс BI-платформы Fastboard с панелью подключений, списком разделов (включая активный «Страница») и генерируемым SQL-скриптом для создания таблицы «Costs» в ClickHouse.



## **Импорт файлов**[​](#импорт-файлов)


### **Переключатель "Исключить пустые столбцы при импорте"**[​](#переключатель-исключить-пустые-столбцы-при-импорте)

Теперь при импорте данных у вас появился новый удобный инструмент — переключатель для работы с пустыми столбцами. Он есть и в новом окне предпросмотра, и в классическом окне выбора столбцов.

![Чек бокс исключения пустых столбцов](data:image/jpeg;base64,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)

Система автоматически проверяет первые 1000 строк и определяет, есть ли в выбранных столбцах хоть какие-то данные. Если столбец полностью пустой, то при включённом переключателе он не будет мешаться в интерфейсе — исчезнет из предпросмотра и не попадёт в импорт или скрипт. А если переключатель выключен, все такие столбцы снова будут отображаться.

Изменения применяются только после обновления окна предпросмотра.


## **Модель данных**[​](#модель-данных)


### **Список связей**[​](#список-связей)

В раскрывающемся меню из правой панели показывает все связи в одной модели данных и позволяет управлять ими. В одном месте вы видите полный список: тип связи (Inner, Full, Left, Right), таблицы и поля-источники, а также таблицы и поля-цели.

![UkWimage.png](https://book.winsolutions.ru/uploads/images/gallery/2025-08/scaled-1680-/ukwimage.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2025-08/scaled-1680-/ukwimage.png)):
> 1)  
> Скрипт загрузки  
> Загрузить данные  
> Модели данных  
> Задания  
> Таблицы  
> Rate_detail  
> Shop  
> Rate_detail  
> Key  
> Тариф  
> Месяц  
> Год  
> Активные пользо...  
> Shop  
> Key  
> Key1  
> Детализация  
> Голос, мин  
> Интернет, мб  
> Список связей  
> Inner 'Rate_detail'[Key] - Shop'[key1]  
> Inner 'Тариф'[Тариф] - 'Sales'[Интернет, мб]  
> Rate_detail  
> Предварительный просмотр <
> 2) Скриншот показывает интерфейс настройки модели данных в BI-платформе Fastboard с визуализацией связей между таблицами Rate_detail и Shop через поля Key и Key1, а также список установленных связей.



### **Показывать направление связей**[​](#показывать-направление-связей)

Позволяет определить, из какой таблицы выходит связь и к какой таблице она направлена.

![Показывать направление связей ](https://help.fastboard.online/assets/images/kzfimage-c0468e269d287c1a03b5a9733ac78647.png)

> **Со скриншота** ([изображение](https://help.fastboard.online/assets/images/kzfimage-c0468e269d287c1a03b5a9733ac78647.png)):
> Rate_detail  
> Key  
> Тариф  
> Месяц  
> Год  
> Активные пользо...  
> Shop  
> Key  
> Key1  
> Детализация  
> Голос, мин  
> Интернет, мб  
> Скриншот показывает связь между таблицами Rate_detail и Shop через поля Key и Тариф.



### **Подсветка полей и связей при наведении и выделении**[​](#подсветка-полей-и-связей-при-наведении-и-выделении)

Акцентная подсветка в интерфейсе для упрощения работы с таблицами в модели данных.

![Подсветка полей и связей](https://help.fastboard.online/assets/images/d0dimage-afcbb78eb273ef418e65cb6c51164571.png)

> **Со скриншота** ([изображение](https://help.fastboard.online/assets/images/d0dimage-afcbb78eb273ef418e65cb6c51164571.png)):
> Rate_detail  
> Key  
> Тариф  
> Месяц  
> Год  
> Активные пользо...  
> Shop  
> Key  
> Key1  
> Детализация  
> Голос, мин  
> Интернет, мб  
> Скриншот показывает связь между двумя таблицами: Rate_detail и Shop, где поле Key из Rate_detail связано с полем Key1 в Shop.



### **Менять положение ключевых полей**[​](#менять-положение-ключевых-полей)

Настройка для размещения ключевых полей в топе таблицы. Позволяет организовать строки таким образом, чтобы пользователю было проще формировать и оценивать связи в таблицах.

![Ключевые поля](https://help.fastboard.online/assets/images/7mdimage-e5e839451f88190fbd4512b95a49ab92.png)

> **Со скриншота** ([изображение](https://help.fastboard.online/assets/images/7mdimage-e5e839451f88190fbd4512b95a49ab92.png)):
> Настройки  
> Закрепить ключевые поля сверху таблицы  
> Показывать ключевые поля, если таблица свёрнута  
> Отмена  
> Сохранить  
> Скриншот показывает окно настроек с двумя включёнными опциями для управления отображением ключевых полей в таблице и кнопками «Отмена» и «Сохранить».



### **Объединение таблиц в модели**[​](#объединение-таблиц-в-модели)

Новый функционал для взаимодействия со скриптом загрузки через модель данных. Позволяет собрать в одну несколько таблиц с помощью интерфейса.

**Кнопка «Объединить таблицы»** позволяет:

- задать название для новой объединённой таблицы
- выбирать, какие таблицы объединить
- решить, объединять ли поля с одинаковыми названиями.
В результате вы получаете удобный способ собрать нужные таблицы в единую, не отвлекаясь на ручное редактирование SQL (язык структурированных запросов).


### **Переработка UI (пользовательский интерфейс) в создании новой связи**[​](#переработка-ui-пользовательский-интерфейс-в-создании-новой-связи)

Мы переработали процесс создания связи. Логика осталась прежней, но интерфейс стал гораздо понятнее и удобнее. Теперь шаги выглядят последовательнее, а сама работа с настройкой связей стала интуитивной.

![Новый сценарий добавления связи.jpg](https://book.winsolutions.ru/uploads/images/gallery/2025-08/scaled-1680-/8sqnovyi-scenarii-dobavleniia-sviazi.jpg)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2025-08/scaled-1680-/8sqnovyi-scenarii-dobavleniia-sviazi.jpg)):
> 1)  
> Нажимаем кнопку «Создать связь».  
> Таблицу выделять не обязательно.  
> Если она была выбрана выбрана в момент нажатия, то автоматом подставится в поле «таблица 1» на следующем шаге  
> Выбираем две таблицы. Направление связи будет от первой ко второй. Выбираем вид JOIN и жмем кнопку дальше  
> + Новая связь  
> Таблица 1  
> Rate_detail  
> Таблица 2  
> Products_Ids  
> Отмена  
> Дальше  
> 2) Скриншот показывает интерфейс создания связи между двумя таблицами (Rate_detail и Products_Ids) в BI-платформе Fastboard, с пошаговой инструкцией и кнопками для продолжения или отмены.


![Новый сценарий добавления связи — копия.jpg](https://book.winsolutions.ru/uploads/images/gallery/2025-08/scaled-1680-/novyi-scenarii-dobavleniia-sviazi-kopiia.jpg)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2025-08/scaled-1680-/novyi-scenarii-dobavleniia-sviazi-kopiia.jpg)):
> 3 Выбираем поля для связи  
> Rate_detail Key Join Inner Operator = Products_Ids Id  
> Назад Создать  
> 4 Связь готова. Она будет высвечиваться при выделении любой из таблиц. Порядок полей таблиц согласно направлению связи  
> Rate_detail Key Join Inner Operator = Products_Ids Id  
> + Новая связь  
> Скриншот показывает интерфейс настройки связи между таблицами Rate_detail и Products_Ids в BI-платформе Fastboard, включая выбор полей, типа соединения (Inner) и оператора (=), а также кнопки управления связью.



## **Баги и мелкие фичи (доработки)**[​](#баги-и-мелкие-фичи-доработки)

- Добавлена поддержка тайм-зон при загрузке данных
- Исправлена ошибка, из-за которой разработчики могли назначать права на собственные потоки
- Реализована автоматическая очистка кэша при выпуске нового релиз
- Добавлено подтверждение от пользователя при повторной загрузке файла в источнике
- Удалены временные решения (костыли) из компонента превью источника