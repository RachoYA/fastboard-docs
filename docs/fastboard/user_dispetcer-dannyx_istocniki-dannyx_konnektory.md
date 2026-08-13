# Коннекторы источников данных | Документация Fastboard

Source: https://help.fastboard.online/user/dispetcer-dannyx/istocniki-dannyx/konnektory/

Источники, из которых можно загружать данные в FastBoard, делятся на 3 типа:

- Файловые источники
- СУБД
- Rest-API
![Rest-API](https://lh7-rt.googleusercontent.com/docsz/AD_4nXePI-VGm9FyMQOtplBPECXki2a1yBlA2YQaq-V5Y-cpVfbi-vKEtbYXDExyYEV4ac38_ZNwzje4ybbRA7aAfsLzMksURjogJQ5taIZKkxnWqmy-bVoPi6mDrt1nmAIetWdtdIigYcNJZABNQ3vZ2gk?key=qrG8cwHTnh3h37EXtdw7pg)

> **Со скриншота** ([изображение](https://lh7-rt.googleusercontent.com/docsz/AD_4nXePI-VGm9FyMQOtplBPECXki2a1yBlA2YQaq-V5Y-cpVfbi-vKEtbYXDExyYEV4ac38_ZNwzje4ybbRA7aAfsLzMksURjogJQ5taIZKkxnWqmy-bVoPi6mDrt1nmAIetWdtdIigYcNJZABNQ3vZ2gk?key=qrG8cwHTnh3h37EXtdw7pg)):
> Новое подключение  
> Выберите тип источника  
> Файл  
> База данных  
> REST API  
> Отмена  
> Скриншот показывает окно выбора типа источника данных при создании нового подключения в BI-платформе Fastboard.



## **Файловые источники**[​](#файловые-источники)

Поддерживаются следующие форматы:

![Поддерживаются следующие форматы:](https://lh7-rt.googleusercontent.com/docsz/AD_4nXddp-v4DUz6IGNJQu7VwYGClJUH5m2SRHSSGEO5sYSgULxNpt70xng4ZRK6G0mMMvQ9C1l21wQq1rTAJq1KcRiU6KZUbX081RPnuKAVoxO1Mc5_NjIWSd_2NcVt06hi2U2YgyFyVNa4YZuIGVYA_v0?key=qrG8cwHTnh3h37EXtdw7pg)

> **Со скриншота** ([изображение](https://lh7-rt.googleusercontent.com/docsz/AD_4nXddp-v4DUz6IGNJQu7VwYGClJUH5m2SRHSSGEO5sYSgULxNpt70xng4ZRK6G0mMMvQ9C1l21wQq1rTAJq1KcRiU6KZUbX081RPnuKAVoxO1Mc5_NjIWSd_2NcVt06hi2U2YgyFyVNa4YZuIGVYA_v0?key=qrG8cwHTnh3h37EXtdw7pg)):
> Формат файла  
> Авто  
> Авто  
> XLSX/XLS  
> CSV  
> TXT  
> JSON  
> XML  
> Скриншот показывает выпадающий список выбора формата файла в интерфейсе BI-платформы Fastboard.


**СУБД**

Поддерживаются следующие СУБД:

![Поддерживаются следующие СУБД:](https://lh7-rt.googleusercontent.com/docsz/AD_4nXcAhiTSHeoLQ0H9Is_lm62bQCJ7pcoL5bxe0N0wEU615CZsrR_so5_PGbTDQj4YOTI_tjhsLZDjwqRZuE5wtT0K8VVFiarFFQikSqLNuy4siekdlkceKoBiG27P2WYgtTncPxZ3XCVvNJuKpVcunsI?key=qrG8cwHTnh3h37EXtdw7pg)

> **Со скриншота** ([изображение](https://lh7-rt.googleusercontent.com/docsz/AD_4nXcAhiTSHeoLQ0H9Is_lm62bQCJ7pcoL5bxe0N0wEU615CZsrR_so5_PGbTDQj4YOTI_tjhsLZDjwqRZuE5wtT0K8VVFiarFFQikSqLNuy4siekdlkceKoBiG27P2WYgtTncPxZ3XCVvNJuKpVcunsI?key=qrG8cwHTnh3h37EXtdw7pg)):
> СУБД  
> PostgreSQL  
> ClickHouse  
> PostgreSQL  
> MSSQL  
> MYSQL  
> ORACLE  
> HIVE  
> Скриншот показывает выпадающий список выбора СУБД (системы управления базами данных) в интерфейсе BI-платформы Fastboard.


Также через PostreSQL поддерживается подключение к GreenPlum.


### **REST-API**[​](#rest-api)

Коннектор к Rest-API позволяет загружать данные из API сторонних систем в тех случаях, когда это можно сделать одним запросом.

При обращении к внешнему API задаются такие параметры как:

- URL, само собой
- Метод (get/post)
- Тело запроса, если это post
- Limit и offset
- Timeout
- Формат получаемого ответа: json / csv / xml
- Параметры авторизации basic auth (login/pass), если требуется
На практике, кроме подключения к самим API, часто производится подключение напрямую к источникам csv, которые публикуют на веб-ресурсы.
