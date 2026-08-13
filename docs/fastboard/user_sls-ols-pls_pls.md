# PLS | Документация Fastboard

Source: https://help.fastboard.online/user/sls-ols-pls/pls/

**PLS (Pages Level Security)** позволяет ограничивать доступ к отдельным страницам внутри проектов.

Политика настройки доступа: исключающая. Доступ к странице исключается для перечисленных пользователей / ГП.

Например, есть большой финансовый отчёт со следующими страницами:

- Монитор, на котором видно общую картину
- Поступления
- Расходы
- ФОТ, на котором представлены зарплатные показатели
Зарплаты считаются чувствительными данными, потому приняли решение оставить доступ только Бухгалтерии и Генеральному директору, Финансистам следует исключить из доступа.

Для этого в доп. действиях со страницей выберем **Ограничить доступ**:

![Для этого в доп. действиях со страницей выберем Ограничить доступ :](https://lh7-rt.googleusercontent.com/docsz/AD_4nXedhhPB4tpxdxO3LWxxoCvgr3ltSZeJC-5vsEvE7ZukkppZak5LuPPcvNtHSALyCLePdM45zQ2TcLdQrlM7PPBroJ4YxKOXVTyGdXSc1XprsaPjrDTtWn1xrjtGwclfW4GWOqPIdXBgCc1fOrurN2o?key=96b5rTBx3_R9fIz0iBmuzQ)

> **Со скриншота** ([изображение](https://lh7-rt.googleusercontent.com/docsz/AD_4nXedhhPB4tpxdxO3LWxxoCvgr3ltSZeJC-5vsEvE7ZukkppZak5LuPPcvNtHSALyCLePdM45zQ2TcLdQrlM7PPBroJ4YxKOXVTyGdXSc1XprsaPjrDTtWn1xrjtGwclfW4GWOqPIdXBgCc1fOrurN2o?key=96b5rTBx3_R9fIz0iBmuzQ)):
> + Создать страницу  
> Монитор  
> Поступления  
> Расходы  
> ФОТ  
> Скрыть из навигации  
> Дублировать  
> Ограничить доступ  
> Удалить  
> Скриншот показывает контекстное меню с опциями управления элементом «ФОТ» в интерфейсе BI-платформы Fastboard.


И выберем ГП Финансисты. Обратите внимание, в этом списке выводятся только те пользователи и ГП, у которых уже есть доступ к проекту в соответствии с настройками доступа потока.

![И выберем ГП Финансисты. Обратите внимание, в этом списке выводятся только те пользователи и ГП,](https://lh7-rt.googleusercontent.com/docsz/AD_4nXcaLMBovR9htlkHLpMNkXa2u3oU8kBNM88YVJC8ILUvvtBa4hUMMPZCUXweH-yYj1OaH90t7XGxrEV0OSRF9q2hHgE1CzZA4ePQX7lbDicpnvR9qtsyyWOFSCks6aPOYP9ayOHeGAnho5u4C0O6LVg?key=96b5rTBx3_R9fIz0iBmuzQ)

> **Со скриншота** ([изображение](https://lh7-rt.googleusercontent.com/docsz/AD_4nXcaLMBovR9htlkHLpMNkXa2u3oU8kBNM88YVJC8ILUvvtBa4hUMMPZCUXweH-yYj1OaH90t7XGxrEV0OSRF9q2hHgE1CzZA4ePQX7lbDicpnvR9qtsyyWOFSCks6aPOYP9ayOHeGAnho5u4C0O6LVg?key=96b5rTBx3_R9fIz0iBmuzQ)):
> Исключить пользователей  
> Пользователи и группы пользователей  
> Финансисты ×  
> Выбрать все  
> Бухгалтеры  
> Финансисты  
> gen_dir  
> Скриншот показывает окно исключения пользователей из доступа в BI-платформе Fastboard, где группа «Финансисты» уже исключена (отмечена галочкой), а остальные пользователи и группы не исключены.


Применяем изменения и видим, что рядом со страницей появилась иконка ограничения доступа:

![Применяем изменения и видим, что рядом со страницей появилась иконка ограничения доступа:](https://lh7-rt.googleusercontent.com/docsz/AD_4nXecsGSopy1yB2dUWQnW_6zI9dBqg1YaNJHh9DFMxDPafOS6kqXMAMx0IIT8b3XTyx0Gn9ikeBojh0Vrkz67RBWpaEj4y2dCG62KMx1-Ia0dgwlgAP1zKUfTeJ7ssLcin1YWvhi_nVoZvjWB9MMIr90?key=96b5rTBx3_R9fIz0iBmuzQ)

> **Со скриншота** ([изображение](https://lh7-rt.googleusercontent.com/docsz/AD_4nXecsGSopy1yB2dUWQnW_6zI9dBqg1YaNJHh9DFMxDPafOS6kqXMAMx0IIT8b3XTyx0Gn9ikeBojh0Vrkz67RBWpaEj4y2dCG62KMx1-Ia0dgwlgAP1zKUfTeJ7ssLcin1YWvhi_nVoZvjWB9MMIr90?key=96b5rTBx3_R9fIz0iBmuzQ)):
> + Создать страницу  
> Монитор  
> Поступления  
> Расходы  
> ФОТ  
> Финансисты  
> Скриншот показывает интерфейс управления страницами в BI-платформе Fastboard с возможностью создания, перемещения и удаления страниц, а также отображает список существующих страниц и всплывающую подсказку «Финансисты» при наведении на значок пользователя.


Таким образом, ГП Бухгалтеры и Генеральный директор увидят полный набор страниц:

![Таким образом, ГП Бухгалтеры и Генеральный директор увидят полный набор страниц:](https://lh7-rt.googleusercontent.com/docsz/AD_4nXfMXS_sXtIzUek1c1Q2xuNc6OAwmV6F3PGIjH8G2cyoxLjEyqwv-XxccP_v6U7Tgf-yc8taZejBsltlOtxNurKiXaSjkM7E5-16kxuxwKoLpjWHQ7PyRfQTg0-qZpKPvGQJTNltojmIGdMLrueDMg?key=96b5rTBx3_R9fIz0iBmuzQ)

> **Со скриншота** ([изображение](https://lh7-rt.googleusercontent.com/docsz/AD_4nXfMXS_sXtIzUek1c1Q2xuNc6OAwmV6F3PGIjH8G2cyoxLjEyqwv-XxccP_v6U7Tgf-yc8taZejBsltlOtxNurKiXaSjkM7E5-16kxuxwKoLpjWHQ7PyRfQTg0-qZpKPvGQJTNltojmIGdMLrueDMg?key=96b5rTBx3_R9fIz0iBmuzQ)):
> Монитор Поступления Расходы ФОТ +  
> Скриншот показывает панель навигации с вкладками: «Монитор», «Поступления», «Расходы», «ФОТ» (выделена), и кнопкой добавления («+»).


А ГП Финансисты смогут работать на всех страницах, кроме ФОТ:

![А ГП Финансисты смогут работать на всех страницах, кроме ФОТ:](https://lh7-rt.googleusercontent.com/docsz/AD_4nXf7NQ-dFiN8XVqdjexqsvfaMQNCjQro4UGaeI68RHsboXC2Rq4qTVeqbfLUZU3XQG_J6tn-0My2gkSbJwgnE4NeVUGAxCfJT8CVbI9ehGXVGdQyDTflFpsR59UWXa2Pci8N99JnfiJH2oopCyUJwA?key=96b5rTBx3_R9fIz0iBmuzQ)

> **Со скриншота** ([изображение](https://lh7-rt.googleusercontent.com/docsz/AD_4nXf7NQ-dFiN8XVqdjexqsvfaMQNCjQro4UGaeI68RHsboXC2Rq4qTVeqbfLUZU3XQG_J6tn-0My2gkSbJwgnE4NeVUGAxCfJT8CVbI9ehGXVGdQyDTflFpsR59UWXa2Pci8N99JnfiJH2oopCyUJwA?key=96b5rTBx3_R9fIz0iBmuzQ)):
> Монитор Поступления Расходы  
> Скриншот показывает вкладку "Монитор" в интерфейсе BI-платформы Fastboard, рядом с ней расположены вкладки "Поступления" и "Расходы".


Даже если их коллега-друг бухгалтер пришлёт прямую ссылку на страницу, при попытке её открыть его встретит следующая ошибка.

![Даже если их коллега-друг бухгалтер пришлёт прямую ссылку на страницу, при попытке её открыть ег](https://lh7-rt.googleusercontent.com/docsz/AD_4nXdbX9CiJN13x0U-rgHYCvkgcxuPrBvrU4c22lfw6thEQuiXlQXYa_axuFIlXWJNMRol6dcjuGYhvLiEsmqeZWwAlwrR3ALb-74oTVxevCLAM0EITKVeCy-rM4cU7LXvOy_rk-RGNP6HJX5svvzpIYU?key=96b5rTBx3_R9fIz0iBmuzQ)

> **Со скриншота** ([изображение](https://lh7-rt.googleusercontent.com/docsz/AD_4nXdbX9CiJN13x0U-rgHYCvkgcxuPrBvrU4c22lfw6thEQuiXlQXYa_axuFIlXWJNMRol6dcjuGYhvLiEsmqeZWwAlwrR3ALb-74oTVxevCLAM0EITKVeCy-rM4cU7LXvOy_rk-RGNP6HJX5svvzpIYU?key=96b5rTBx3_R9fIz0iBmuzQ)):
> Запрашиваемая страница вам недоступна. Произведен переход на доступную вам страницу  
> Скриншот показывает сообщение об ошибке доступа к странице с автоматическим перенаправлением на доступную страницу.

