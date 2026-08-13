# RLS | Документация Fastboard

Source: https://help.fastboard.online/user/sls-ols-pls/rls/

**RLS (Row Level Security)** - самый детальный уровень доступа. Он позволяет пользователям видеть разные данные в одних и тех же графиках, в зависимости от их учётной записи.

![RLS](https://help.fastboard.online/assets/images/photo_2025-08-11_16-53-12-81d0cdfaf00d83448c07d787cb176d5d.jpg)

> **Со скриншота** ([изображение](https://help.fastboard.online/assets/images/photo_2025-08-11_16-53-12-81d0cdfaf00d83448c07d787cb176d5d.jpg)):
> RLS  
> IDENT  
> Скриншот иллюстрирует принцип работы Row-Level Security (RLS) в BI-платформе Fastboard: разные пользователи получают доступ к разным строкам данных в таблице, где поле IDENT определяет уровень доступа.


Политика настройки доступа: ограничивающая. Вы указываете пользователей / ГП, которым нужно ограничить доступ.

Например, есть такой простой отчёт по продажам:

![Отчет по продажам](https://help.fastboard.online/assets/images/unnamed-7baa694d36b7382e797430168991db4f.png)

> **Со скриншота** ([изображение](https://help.fastboard.online/assets/images/unnamed-7baa694d36b7382e797430168991db4f.png)):
> Продажи +  
> Период Краснодар Москва Ростов Сочи Магазин ∨  
> Выручка, млн. ₽ 48,4  
> Ср.чек, тыс. ₽ 29,7  
> Кол-во ТТ 20  
> Рейтинг Регион > ТТ  
> Москва  
> Ростов  
> Краснодар  
> Сочи  
> Выручка млн.руб  
> 2.5  
> 2  
> 1.5  
> 1  
> 0.5  
> 0  
> 01.01.24 04.01.24 07.01.24 10.01.24 13.01.24 16.01.24 19.01.24 22.01.24 25.01.24 28.01.24 31.01.24  
> Скриншот показывает дашборд продаж с метриками выручки, среднего чека и количества торговых точек по регионам (Москва, Ростов, Краснодар, Сочи) за январь 2024 года, включая линейный график динамики выручки и горизонтальную диаграмму рейтинга регионов.


И вам нужно сделать, чтобы региональные менеджеры видели только свои продажи, а остальных пользователей не ограничивать.

Для этого мы переходим в менеджер данных и настраиваем нашу модель. При наведении на модель данных в панели нажимаем на иконку настройки доступа:

![Модель](data:image/png;base64,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)

**В первую очередь будет рассмотрен один из вариантов реализации данного функционала. После этого будут разъяснены принципы его работы, а также представлены доступные возможности.**

В качестве примера будет использоваться поле **«Регион»** из справочника **«Магазины»**.

**Пример реализации:**

![Пример реализации ](https://help.fastboard.online/assets/images/unnamed-2--c17dc88943e57b761646f2b81f5f2fb7.png)

> **Со скриншота** ([изображение](https://help.fastboard.online/assets/images/unnamed-2--c17dc88943e57b761646f2b81f5f2fb7.png)):
> shops > region  
> shop  
> region  
> shop_id  
> ИНТЕРНЕТ-МАГАЗИН  
> 7c896cd7-37e9-11e7-9d70-002...  
> МАГАЗИН М10  
> Москва  
> baab8f77-37e4-11e7-9d70-0025...  
> МАГАЗИН М14  
> Москва  
> 15542db7-37e5-11e7-9d70-002...  
> МАГАЗИН М15  
> Москва  
> c7cf66d7-37e5-11e7-9d70-0025...  
> МАГАЗИН М16  
> Москва  
> 96557277-37e5-11e7-9d70-002...  
> МАГАЗИН М17  
> Москва  
> e44a7a77-37e5-11e7-9d70-002...  
> МАГАЗИН М18  
> Москва  
> 67570d37-37e5-11e7-9d70-002...  
> МАГАЗИН М19  
> Москва  
> 8915cb97-37e6-11e7-9d70-002...  
> МАГАЗИН М20  
> Ростов  
> d1bba277-37e6-11e7-9d70-002...  
> МАГАЗИН М22  
> Ростов  
> 8b7eb037-37e7-11e7-9d70-002...  
> МАГАЗИН М23  
> Ростов  
> d7e16fd7-37e7-11e7-9d70-0025...  
> МАГАЗИН М25  
> Ростов  
> 2403ea57-37e8-11e7-9d70-002...  
> МАГАЗИН М26  
> Ростов  
> 5f37bcf7-37e8-11e7-9d70-0025...  
> Связи  
> Метаданные  
> Скриншот показывает таблицу с данными о магазинах (shop), их регионах (region) и уникальных идентификаторах (shop_id), включая интернет-магазин и физические точки в Москве и Ростове.


Создаём правило и называем его:

![Наименование правила ](https://help.fastboard.online/assets/images/unnamed-3--96e5d0124b6d3e197d221a03eb9b7067.png)

> **Со скриншота** ([изображение](https://help.fastboard.online/assets/images/unnamed-3--96e5d0124b6d3e197d221a03eb9b7067.png)):
> Создать правило  
> Название  
> Региональные менеджеры видят свои ТТ  
> Прикрепить файл  
> Скачать образец файла  
> Отмена  
> Создать  
> Скриншот показывает форму создания правила в BI-платформе Fastboard с полем ввода названия, кнопками прикрепления файла и скачивания образца, а также кнопками «Отмена» и «Создать».


После чего открывается окно настройки правила RLS

![Окно РЛС](https://help.fastboard.online/assets/images/unnamed-4--e88d9dcb636b3bda51f6ed25650b9e4a.png)

> **Со скриншота** ([изображение](https://help.fastboard.online/assets/images/unnamed-4--e88d9dcb636b3bda51f6ed25650b9e4a.png)):
> 1) Изменение правила  
> Региональные менеджеры видят свои ТТ  
> Активно  
> Экспорт Импорт  
> Пользователи  
> Фильтр  
> WHERE  
> + Добавить пользователя  
> Группы  
> Переменные  
> Введите значение переменной  
> + Добавить группу  
> + Создать переменную  
> Закрыть Сохранить  
> 2) Скриншот показывает интерфейс настройки правила фильтрации данных в BI-платформе Fastboard, где можно добавить пользователей и группы, задать SQL-фильтр (WHERE) и переменные для динамического ограничения видимости данных по региональным менеджерам.


**Блоки Пользователи и Группы** отвечают за тех, на кого мы накладываем ограничение на данных.

**Блок Переменные** позволяет привязать пользователям / ГП их значения для дальнейшего использования в условии отображения отдельных строк данных.

**Блок Фильтр** – непосредственно описывает правило.

Первым шагом добавляем пользователей, которых мы хотим ограничить в данных: например, региональные менеджеры.

![Региональные менеджеры](data:image/png;base64,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)

Все прочие пользователи никак не будут ограничены.

Затем создаём переменную `manager_regions`. Значение по умолчанию – пустая строка .

![Создание переменной](https://help.fastboard.online/assets/images/unnamed-6--a1b1963ea4340d62c6a2fba8c4677769.png)

> **Со скриншота** ([изображение](https://help.fastboard.online/assets/images/unnamed-6--a1b1963ea4340d62c6a2fba8c4677769.png)):
> Создание переменной  
> Название  
> manager_regions  
> Значение по умолчанию  
> «  
> Отмена  
> Создать  
> Скриншот показывает окно создания переменной в BI-платформе Fastboard с полями для ввода названия и значения по умолчанию, а также кнопками «Отмена» и «Создать».


После чего задаём пользователям их значения. Выбираем moscow_manager и прописываем его регион Москва.

Значения должны с точностью совпадать с теми, что лежат в данных.

![Пользователи](https://help.fastboard.online/assets/images/unnamed-7--42deac0c765031fcda3c3e001fe9ae30.png)

> **Со скриншота** ([изображение](https://help.fastboard.online/assets/images/unnamed-7--42deac0c765031fcda3c3e001fe9ae30.png)):
> 1) Пользователи  
> Поиск  
> moscow_manager  
> rostov_manager  
> + Добавить пользователя  
> Группы  
> Фильтр  
> WHERE  
> Переменные  
> manager_regions  
> 'Москва'
> 2) Скриншот показывает интерфейс настройки прав доступа или фильтрации данных в BI-платформе Fastboard, где можно выбрать пользователей, задать SQL-условие (WHERE), привязать переменную и указать значение для фильтрации.


Для rostov_manager значение, соответственно, Ростов.

И, наконец, само правило: `WHERE shops.region in ( {{manager_regions}} )`

Проверим, как работает правило.

Так это выглядит у обычного пользователя, для которого нет правила:

![Пример графика](https://help.fastboard.online/assets/images/unnamed-8--ef4e5626784a125b6d300ca6e7ada98c.png)

> **Со скриншота** ([изображение](https://help.fastboard.online/assets/images/unnamed-8--ef4e5626784a125b6d300ca6e7ada98c.png)):
> 1)  
> Продажи +  
> Период Краснодар Москва Ростов Сочи Магазин ∨  
> Выручка, млн. ₽ 48,4  
> Ср.чек, тыс. ₽ 29,7  
> Кол-во ТТ 20  
> Рейтинг Регион > ТТ  
> Москва  
> Ростов  
> Краснодар  
> Сочи  
> Выручка млн.руб  
> 2.5  
> 2  
> 1.5  
> 1  
> 0.5  
> 0  
> 01.01.24 04.01.24 07.01.24 10.01.24 13.01.24 16.01.24 19.01.24 22.01.24 25.01.24 28.01.24 31.01.24  
> 2) Скриншот показывает дашборд BI-платформы Fastboard с метриками продаж (выручка, средний чек, количество торговых точек), графиком выручки по дням января 2024 и рейтингом регионов по объёму продаж в виде горизонтальной гистограммы.


Так это выглядит под пользователем moscow_region:

![Пример 2](https://help.fastboard.online/assets/images/unnamed-9--0d36abce1f736cc5d8ecf23b67a1f37f.png)

> **Со скриншота** ([изображение](https://help.fastboard.online/assets/images/unnamed-9--0d36abce1f736cc5d8ecf23b67a1f37f.png)):
> 1)  
> Продажи +  
> Период Москва Магазин ∨  
> Выручка, млн. ₽ 19,2  
> Ср.чек, тыс. ₽ 30,5  
> Кол-во ТТ 10  
> Рейтинг Регион > ТТ  
> МАГАЗИН М7  
> МАГАЗИН М5  
> МАГАЗИН М4  
> МАГАЗИН M18  
> МАГАЗИН М9  
> МАГАЗИН M16  
> МАГАЗИН M19  
> МАГАЗИН M17  
> МАГАЗИН M10  
> МАГАЗИН M15  
> Выручка млн.руб  
> 1  
> 0,8  
> 0,6  
> 0,4  
> 0,2  
> 0  
> 01.01.24 04.01.24 07.01.24 10.01.24 13.01.24 16.01.24 19.01.24 22.01.24 25.01.24 28.01.24 31.01.24  
> 2) Скриншот показывает дашборд продаж в Москве за январь 2024 года с ключевыми метриками (выручка, средний чек, количество торговых точек), графиком динамики выручки по дням и рейтингом магазинов по региону ТТ.


Видим, что значения всех графиков изменились, в фильтре остался только регион Москва, а рейтинг, помимо фильтрации по Москве, автоматически перешёл на следующий уровень drill_down – сразу до магазинов.

По rostov_manager аналогично:

![пример 3 ](https://help.fastboard.online/assets/images/unnamed-10--8fae73c3b95c29b39e3d81088404b370.png)

> **Со скриншота** ([изображение](https://help.fastboard.online/assets/images/unnamed-10--8fae73c3b95c29b39e3d81088404b370.png)):
> Продажи  
> Период  
> Ростов  
> Магазин ∨  
> Выручка, млн. ₽  
> 15,1  
> Ср.чек, тыс. ₽  
> 31,2  
> Кол-во ТТ  
> 5  
> Рейтинг  
> Регион > ТТ  
> МАГАЗИН М26  
> МАГАЗИН М22  
> МАГАЗИН М29  
> МАГАЗИН М20  
> МАГАЗИН М25  
> Выручка  
> млн.руб  
> 1  
> 0.8  
> 0.6  
> 0.4  
> 0.2  
> 0  
> 01.01.24  04.01.24  07.01.24  10.01.24  13.01.24  16.01.24  19.01.24  22.01.24  25.01.24  28.01.24  31.01.24  
> Скриншот показывает дашборд BI-платформы Fastboard с метриками продаж за январь 2024 года в Ростове: общая выручка 15,1 млн ₽, средний чек 31,2 тыс. ₽, количество торговых точек — 5, а также график динамики выручки по дням и рейтинг магазинов (М26 лидирует).


**Как это работает?**

На каждый запрос от визуальных компонентов накладывается условие, описанное в правиле


```
WHERE shops.region in ( {{manager_regions}} )
```

На основании текущей учётной записи вместо всех переменных подставляются их значения. На примере менеджера Московских магазинов это


```
WHERE shops.region in ( ‘Москва’ )
```

Таким образом каждый из перечисленных пользователей будут видеть только свои данные. Все прочие по умолчанию видят все данные.

Какие ещё есть возможности RLS?

В форме настройки правила вы пишете произвольный SQL (язык структурированных запросов), ограничиваясь лишь его синтаксисом и своим воображением. Важно лишь помнить о том, что переменные – это простая подстановка значений, а также о кавычках, когда работаете с текстовыми значениями.

В нашем случае мы сразу заложили логику, когда под управлением одного менеджера может быть несколько регионов, поэтому используется оператор IN. В простом случае можно использовать `WHERE shops.region = {{manager_region}}`

Разберём несколько вариаций нашей задачи:

- Если в справочнике магазинов уже прописан их менеджер, правило можно описать следующим образом `WHERE shops.manager = {{manager}}`, задав предварительно значения переменной для каждого менеджера
- Если у вас более сложная иерархия, например менеджеры магазинов и региональные менеджеры
![Иерархия ](https://help.fastboard.online/assets/images/unnamed-11--e3df5645dc1ab50440a6113c8cf0f570.png)

> **Со скриншота** ([изображение](https://help.fastboard.online/assets/images/unnamed-11--e3df5645dc1ab50440a6113c8cf0f570.png)):
> 1)  
> shop > shop  
> T shop  
> T manager  
> T region_manager  
> T shop_id  
> МАГАЗИН М10 Смирнов Иванова baab8f77-37e4-11e7-9d70-0025...  
> МАГАЗИН М14 Кузнецов Иванова 15542db7-37e5-11e7-9d70-002...  
> МАГАЗИН М15 Попов Иванова c7cf66d7-37e5-11e7-9d70-0025...  
> МАГАЗИН М16 Васильев Иванова 96557277-37e5-11e7-9d70-002...  
> МАГАЗИН М17 Петров Иванова e44a7a77-37e5-11e7-9d70-002...  
> МАГАЗИН М18 Соколов Иванова 67570d37-37e5-11e7-9d70-002...  
> МАГАЗИН М19 Михайлов Иванова 8915cb97-37e6-11e7-9d70-002...  
> МАГАЗИН М20 Новиков Кравченко d1bba277-37e6-11e7-9d70-002...  
> МАГАЗИН М22 Федоров Кравченко 8b7eb037-37e7-11e7-9d70-002...  
> МАГАЗИН М23 Морозов Кравченко d7e16fd7-37e7-11e7-9d70-0025...  
> МАГАЗИН М25 Волков Кравченко 2403ea57-37e8-11e7-9d70-002...  
> МАГАЗИН М26 Алексеев Кравченко 5f37bcf7-37e8-11e7-9d70-0025...  
> МАГАЗИН М28 Лебедев Кравченко a0d865b7-37e8-11e7-9d70-002...  
> Связи  
> негатанные  
> 2) Скриншот показывает таблицу данных из BI-платформы Fastboard с информацией о магазинах, их менеджерах, региональных менеджерах и уникальных идентификаторах магазинов.


Хорошим вариантом будет создать 2 правила: для обычных менеджеров и для региональных. Их логика схожа с п.1. В этом случае для каждого из них будет работать своё правило.

Также можно описать всё в одном:

- описываем 2 переменные: manager и `region_manager`. У обычных менеджеров будет заполнена только первая, у региональных – вторая. *Например,* у Смирнова (магазин М10)
![2](https://help.fastboard.online/assets/images/unnamed-12--4fdfbb093abb8d0dca952c2da389a0e5.png)

> **Со скриншота** ([изображение](https://help.fastboard.online/assets/images/unnamed-12--4fdfbb093abb8d0dca952c2da389a0e5.png)):
> smirnov  
> ivanova  
> petrov  
> + Добавить пользователя  
> Группы ⓘ  
> Переменные ⓘ  
> region_manager  
> manager  
> Введите значение переменной  
> Скриншот показывает интерфейс управления пользователями и переменными в BI-платформе Fastboard, включая список пользователей, кнопку добавления пользователя, разделы «Группы» и «Переменные» с примерами значений.


![3](https://help.fastboard.online/assets/images/unnamed-13--7e7b4b4581bd935173c8967009668b57.png)

> **Со скриншота** ([изображение](https://help.fastboard.online/assets/images/unnamed-13--7e7b4b4581bd935173c8967009668b57.png)):
> smirnov  
> ivanova  
> petrov  
> + Добавить пользователя  
> Группы ⓘ  
> Переменные ⓘ  
> region_manager  
> manager  
> Смирнов  
> Скриншот показывает интерфейс управления пользователями и переменными в BI-платформе Fastboard, включая список пользователей, кнопку добавления пользователя, разделы «Группы» и «Переменные», а также отображение имени пользователя «Смирнов».


- фильтр задаём выражением `WHERE manager = '{{manager}}' or region_manager = '{{region_manager}}'`
Таким образом, у Смирнова фильтр примет вид: `WHERE manager = 'Смирнов' or region_manager = ''` А т.к. пустых региональных менеджеров в данных нет, он увидит данные только по своему магазину.

Мы разобрали несколько бизнес-кейсов, теперь **рассмотрим технические возможности:**

- Можно задавать несколько правил на одну и ту же модель данных. Если один пользователь фигурирует в несольких правилах, для него будут применены все ограничения
- Правила можно экспортировать/импортировать в csv/xlsx. Помогает переносить логику между проектами
![Экспорт ](https://help.fastboard.online/assets/images/unnamed-14--152dde0618ce3a621fc3106798e20181.png)

> **Со скриншота** ([изображение](https://help.fastboard.online/assets/images/unnamed-14--152dde0618ce3a621fc3106798e20181.png)):
> 1) Изменение правила  
> Менеджеры видят только свои ТТ  
> Активно  
> Пользователи  
> + Добавить пользователя  
> Группы  
> + Добавить группу  
> Фильтр  
> WHERE  
> Переменные  
> Введите значение переменной  
> + Создать переменную  
> Экспорт  
> Импорт  
> Закрыть  
> Сохранить  
> 2) Скриншот показывает интерфейс настройки правила видимости данных в BI-платформе Fastboard, где можно управлять доступом пользователей и групп к данным через фильтры и переменные.


**У разработчиков проекта есть возможность тестировать работу RLS, не запрашивая доступы пользователей и не создавая тестовые УЗ. Для этого предусмотрен предпросмотр RLS – просто включите его в настройках проекта и выберите пользователя, под которым хотите проверить работу правил.**

![У разработчиков проекта есть возможность тестировать работу RLS, не запрашивая доступы пользоват](https://help.fastboard.online/assets/images/unnamed-15--ea88538d19e2d183832f267e83b369de.png)

> **Со скриншота** ([изображение](https://help.fastboard.online/assets/images/unnamed-15--ea88538d19e2d183832f267e83b369de.png)):
> Режим просмотра  
> Модель данных по умолчанию  
> Реальные данные  
> Локальный шрифт  
> Шаг сетки  
> Масштабирование страницы  
> Предпросмотр RLS  
> moscow_manager  
> Скриншот показывает настройки предпросмотра RLS (Row-Level Security) в BI-платформе Fastboard, включая активацию функции и выбор роли «moscow_manager».


**Это сильно сократит время отладки. В целях безопасности предпросмотр RLS работает только для администраторов, а также разработчиков, не ограниченных настроенными правилами.**
