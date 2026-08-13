# Работа с триггерами | Документация Fastboard

Source: https://help.fastboard.online/user/konstruktor-dasbordov/rabota-s-triggerami/


## **Создание триггеров**[​](#создание-триггеров)

**Триггер в Fastboard** – управляющий элемент, позволяющий настроить видимость объектов (визуализаций и фильтров) на дашборде.

Все триггеры создаются в **настройках страницы** – это отправной пункт при начале работы с интерактивной видимостью объектов.

Откроем общие настройки проекта (не должна быть выбрана ни одна визуализация), и перейдём на вкладку "Настройки страницы".

![image.png](https://help.fastboard.online/assets/images/frame-151-2-c99ffb9d52c551f10612dc6ba1db9e55.png)

> **Со скриншота** ([изображение](https://help.fastboard.online/assets/images/frame-151-2-c99ffb9d52c551f10612dc6ba1db9e55.png)):
> 1)  
> Настройки страницы  
> Размеры страницы  
> Ш 1600 пикс В 1200 пикс  
> Показать границы страницы  
> Изменить цвет страницы  
> Цвет  
> Изображение  
> Ссылка:  
> Пропорции  
> По размеру Заполнить Вписать Растянуть  
> Триггеры страницы  
> + Создать триггер  
> 2) Скриншот показывает панель настроек страницы в BI-платформе Fastboard, включая параметры размеров, отображения границ и цвета фона, настройки изображения (ссылка, пропорции) и раздел для создания триггеров страницы.


Раскроем секцию "Триггеры страницы", нажмём на кнопку "Создать триггер". В списке триггеров появится новый объект. Триггеру можно установить название – отнеситесь к этому ответственно, потому что в рамках одного проекта могут существовать десятки различных триггеров, которые могут применять разные пользователи.

![image.png](https://help.fastboard.online/assets/images/frame-152-3-82dd0de41cf359f32c3eccbb717326b6.png)

> **Со скриншота** ([изображение](https://help.fastboard.online/assets/images/frame-152-3-82dd0de41cf359f32c3eccbb717326b6.png)):
> 1)  
> Настроить  
> Текущее значение  
> true  
> Размеры страницы  
> Ш 1600 пикс В 1200 пикс  
> Показать границы страницы  
> Изменить цвет страницы  
> Цвет  
> Изображение  
> Ссылка:  
> Пропорции  
> По размеру Заполнить Вписать Растянуть  
> Триггеры страницы  
> Новый Триггер  
> + Создать триггер  
> 2) Скриншот показывает панель настроек страницы в BI-платформе Fastboard с параметрами размеров, отображения границ и цвета, настройки изображения и управления триггерами.


Название триггера должно отражать либо название визуализации, на которую он влияет, либо (если таких визуализаций несколько) – общее правило, по которому этот триггер вызывается.

Примеры "хороших" названий для триггеров: "Доход – вкл", "Детализация по расходам", "Карта (ур. 2)".

После выбора названия можно установить **текущее** значение триггера – true или false. По сути, каждый триггер представляет собой переменную логического типа: при значении true видимость включается, при значении false – выключается.

Планировать создание триггеров в отдельности от визуализаций – плохая идея! Рекомендуется сначала спланировать последовательность действий, а потом приступать к созданию и назначению триггеров.


## **Базовые триггеры**[​](#базовые-триггеры)

Самый простой функционал триггеров – скрывать/показывать визуализации при нажатии на кнопку. Для того, чтобы корректно настроить работу триггеров, нужно учитывать несколько правил:

- За видимость объекта может отвечать **ровно один** триггер.
- Один объект может управлять сразу несколькими триггерами.
- Один и тот же триггер можно назначить на несколько разных объектов.
Работа с триггерами в рамках объектов дашборда выполняется в настройках объекта на вкладке "События".

![image.png](https://help.fastboard.online/assets/images/frame-153-1-08c40c9101b86202947b4a06af974e73.png)

> **Со скриншота** ([изображение](https://help.fastboard.online/assets/images/frame-153-1-08c40c9101b86202947b4a06af974e73.png)):
> Страница 1 +  
> События  
> Управление триггерами  
> + Добавить триггер  
> Управление видимостью  
> Переход к объекту  
> Переход по гиперссылке  
> Активация объекта  
> Реагировать на фильтры  
> Работать как фильтр  
> Активировать фильтры  
> Круг /10  
> 1 6 18 18 5 8 12 2 20 10  
> Группа 1  
> Группа 2  
> Группа 3  
> Группа 4  
> Группа 5  
> Группа 6  
> Группа 7  
> Группа 8  
> Группа 9  
> Группа 10  
> Скриншот показывает интерфейс настройки событий и триггеров для круговой диаграммы в BI-платформе Fastboard, включая панель управления триггерами, переключатели видимости и действий, а также легенду с группами данных.


Здесь есть две секции:

Управление триггерами – список триггеров, значение которых изменяет нажатие на визуальный компонент. В данный список можно добавлять только триггеры, которые ранее были созданы в настройках страницы. Для каждого триггера в списке можно выбрать значение, которое будет установлено для него при нажатии на визуализацию:

- true
- false
- invert – меняет текущее значение на противоположное (true на false, false на true)
![image.png](https://book.winsolutions.ru/uploads/images/gallery/2025-10/scaled-1680-/BDBimage.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2025-10/scaled-1680-/BDBimage.png)):
> Управление триггерами  
> Доход  
> false  
> true  
> false  
> invert  
> + Добавить триггер  
> Управление видимостью  
> Скриншот показывает интерфейс настройки триггеров и управления видимостью в BI-платформе Fastboard, включая выпадающий список с логическими значениями (true/false/invert) для условия «Доход».


Управление видимостью – секция для определения, какой триггер определяет видимость объекта:

Если у триггера установлено значение true, то объект отображается на дашборде

Если у триггера установлено значение false, то объект скрыт

![Если у триггера установлено значение false, то объект скрыт](data:image/png;base64,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)

Не забудьте активировать секцию переключателем (иначе триггеры не будут действовать)


## **Продвинутые триггеры**[​](#продвинутые-триггеры)


### **Управление своей видимостью**[​](#управление-своей-видимостью)

Объекты могут управлять собственной видимостью с помощью триггеров. Особенно актуально это для "режимов" кнопок – используется несколько медиаблоков, наложенных друг на друга, которые при нажатии скрывают себя и показывают следующий объект в очереди.

В данном случае следует помнить, что если объект при нажатии выключает сам себя, то для его включения понадобится другой объект, связанный с ним. Иначе бизнес-пользователь проекта при нажатии может полностью потерять визуализацию.

Чтобы объект управлял собственной видимостью необходимо установить один и тот же триггер и в секции управления триггерами, и в секции управления видимостью.


## **Связанные кнопки**[​](#связанные-кнопки)

В случае, когда требуется задать несколько вариантов визуализации с помощью кнопок, необходимо уметь корректно создавать цепочки связанных условий с помощью триггеров. Существуют различные кейсы, при которых может возникнуть несколько связанных друг с другом кнопок (управляющих не только чужой, но и своей видимостью). Начнём, разумеется, с простого кейса.

Кейс – "включенная" кнопка может полностью закрыть собой "выключенную" кнопку

Суть кейса – кнопками выбирается одна из нескольких визуализаций, при этом саму кнопку при нажатии нужно как-то выделять.

Основная идея в этом кейсе – создать столько триггеров, сколько имеется визуализаций, и назначить их на "свои" кнопки включения и визуальные компоненты. При этом:

У нижних кнопок (при нажатии на которые появляется визуальный компонент) установлено управление триггерами:

- "Свой" (активирующий указанную визуализацию) триггер – True
- "Чужие" (активирующие другие визуализации) триггеры – False
У верхних кнопок установлено только управление видимостью – там стоит "свой" триггер (такие кнопки являются некликабельными заглушками)

У каждой визуализации установлено только управление видимостью – там стоит "свой" триггер


## **Назначение на области SVG**[​](#назначение-на-области-svg)

Уникальной визуализацией, способной взаимодействовать с триггерами особым образом, является SVG-объект. У данного визуального компонента доступно управление триггерами как с помощью контейнера объекта, так и через **каждую размеченную область** SVG-файла внутри. Для этого на вкладке "События" в секции "Управление триггерами" у SVG есть второй режим – "Раздельный".

![image.png](https://book.winsolutions.ru/uploads/images/gallery/2025-10/scaled-1680-/hUhimage.png)

> **Со скриншота** ([изображение](https://book.winsolutions.ru/uploads/images/gallery/2025-10/scaled-1680-/hUhimage.png)):
> 1)  
> Управление триггертами  
> Общий Раздельный  
> Боль... Бублик tr...  
> Средн... Столб... tr...  
> Мале... Водоп... tr...  
> + Добавить триггер  
> 2) Скриншот показывает интерфейс управления триггерами в BI-платформе Fastboard с вкладками «Общий» и «Раздельный», тремя строками настроек триггеров (с выпадающими списками и кнопками удаления) и кнопкой добавления нового триггера.


При переключении в раздельный режим появляется возможность не только выбрать триггер, но и назначить его на конкретную область (представьте, что области SVG являются отдельными визуализациями, с помощью которых можно управлять видимостью объектов дашборда). При этом действуют следующие правила:

- На каждую область можно назначить сколько угодно триггеров.
- Каждый триггер можно назначить на сколько угодно областей.
- Один и тот же триггер может быть назначен на одну и ту же область несколько раз. При этом применяться будет то значение, которое указано выше остальных в списке.
По умолчанию нажатие на область SVG фильтрует дашборд (отчёт) по этой области. Необходимо учитывать это при разработке логики переключения триггерами, поскольку такие фильтры могут ограничивать результат переключения.


## **Экспертные триггеры**[​](#экспертные-триггеры)


### **Связанные кнопки 2**[​](#связанные-кнопки-2)

Кейс – кнопка во втором режиме не перекрывает кнопку в первом

Суть кейса – нельзя разместить "включенную" кнопку поверх "выключенной" таким образом, чтобы она полностью её перекрывала (например, если кнопка задана какой-то фигурой)

Основная идея в этом кейсе – создать по два триггера на каждую логику: **триггер включения** и **триггер выключения**. Каждая пара таких триггеров будет привязана к своим кнопке и визуализации (желательно, одноименным)

Число триггеров будет равно числу кнопок или удвоенному числу вариантов визуализации (6 триггеров на 3 визуального компонента и т.д.). При этом самым удобным будет следующий алгоритм:

Парам триггеров даём одинаковые названия, отличающиеся указанием на действие включения/выключения (например, +/- или on/off)

В управлении видимостью "выключенных" кнопок (при нажатии на которые визуальный компонент должен появляться) устанавливаем **триггер выключения** (например, "Круговая_off")

В управлении видимостью "включенных" кнопок (после нажатия на выключенную) устанавливаем **триггер включения** (например, "Круговая_on")

В управлении видимостью визуализаций устанавливаем **триггер включения** (например, "Круговая_on")

Управление триггерами назначаем только на "выключенные" кнопки, при этом каждая такая кнопка будет влиять на ВСЕ используемые в логике триггеры. Каждая "выключенная" кнопка:

- Устанавливает True для своего триггера включения и чужих триггеров выключения
- Устанавливает False для своего триггера выключения и чужих триггеров включения
**Пример реализации**:

![image.png](https://help.fastboard.online/assets/images/frame-156-1-1e426eaa98e74050e78c63a88e03ef55.png)

> **Со скриншота** ([изображение](https://help.fastboard.online/assets/images/frame-156-1-1e426eaa98e74050e78c63a88e03ef55.png)):
> 1) Страница 1  
> Группа 3 × Ноябрь × Октябрь × Февраль ×  
> Заголовок  
> Подзаголовок  
> Водопад  
> Пузырьки  
> 3,500  
> 3,000  
> 2,500  
> 2,000  
> 1,500  
> 1,000  
> 500  
> 0  
> План Март Июнь Сентябрь Декабрь  
> План Позитив Негатив Факт  
> Управление триггерами  
> Водопад_on false  
> Водопад_off true  
> Пузырьки_on false  
> Пузырьки_off true  
> + Добавить триггер  
> Управление видимостью  
> Водопад_off  
> Переход к объекту  
> Переход по гиперссылке  
> Реагировать на фильтры  
> Активировать фильтры  
> 2) Скриншот показывает интерфейс BI-платформы Fastboard с панелью управления триггерами и видимостью элементов, а также графиком «Водопад» и кнопками для переключения визуализаций.


![image.png](https://help.fastboard.online/assets/images/frame-157-1-d04a845533701461ae81feffa393e95c.png)

> **Со скриншота** ([изображение](https://help.fastboard.online/assets/images/frame-157-1-d04a845533701461ae81feffa393e95c.png)):
> 1)  
> Страница 1 +  
> Группа 3 × Ноябрь × Октябрь × Февраль × Апрель ×  
> Заголовок  
> Подзаголовок  
> Водопад  
> Пузырьки  
> Управление триггерами  
> Водопад_off true  
> Пузырьки_on false  
> Водопад_on false  
> Пузырьки_off true  
> + Добавить триггер  
> Управление видимостью  
> Пузырьки_on  
> Переход к объекту  
> Переход по гиперссылке  
> Реагировать на фильтры  
> Активировать фильтры  
> 2) Скриншот показывает интерфейс настройки триггеров и видимости элементов (кнопок «Водопад» и «Пузырьки») в BI-платформе Fastboard, включая панель управления с переключателями и выпадающими списками для логики отображения.

