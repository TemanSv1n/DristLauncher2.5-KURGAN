# DristLauncher2.5 KURGAN
 **Forked from Gungneer** and completely remade

Bla bla bla... Text here...


# ИНСТРУКЦИЯ ПО ПОЛЬЗОВАНИЮ ДЛЯ МАЛЫШЕЙ (пользователей) \#RU

Лаунчер запускается из файла **main.py** или же его "скомпилированного" аналога

Скрипты и папки нельзя никуда перемещать, все должно располагаться неизменно относительно друг друга

В меню пользователю будет предложено **ПОКА ЧТО** _3 основных опции_:
 
- Полная установка Майнкрафта, от JDK до модов
- Конфигурация никнейма и выделенной оперативной памяти
- Запуск майнкрафта с обновлением модов при необходимости

Помимо этого для списка модов существуе возможность небольшой конфигурации по желанию:
Чтобы мод не палился на радарах при обновлении манифеста, добавьте к нему приписку '**IGNORE.**'

Пример: *'uwu_mod_1.14.88.jar'* -> *'IGNORE.uwu_mod_1.14.88.jar'*

Если же вы наоборот хотите удалить какой то мод, но чтобы система думала, что он в наличии, добавьте в его конец приписку '**.disabled**'

Пример: *'dristant_horizons_1.19.84.jar'* -> *'dristant_horizons_1.19.84.jar.disabled'*

Если вы дристояр и не хотите, чтобы обновлялся манифест файлов, то поставьте в его json файле огромное число в поле версии. Тогда проверка не будет проходить. Не советуем так делать...

# ИНСТРУКЦИЯ ПО ПОЛЬЗОВАНИЮ ДЛЯ АДМИНОВ \#RU

Сервер поднимается из файла **s_main.py** или же его "скомпилированного" аналога.

Порт можно настроить в port.json. Для открытия сервера мы советуем использовать либо переадресаторы, такие как *ngrok* или *playit*, а также сети по типу *radmin vpn* и *zerotier*, а еще вы можете просто открыть порты на сервере, но это сложнее.
Размещать эти адреса необходимо в https://github.com/TemanSv1n/Slons/blob/77c0e19013ffbd5943390bef40c7c07649d4fe3a/launcher_ip.json . Если же вы как то нашли
наш лаунчер и не имеете к нам никакого отношения, то можете пересобрать лаунчер и просто добавить свою ссылку в **serverConnector#getIpManifest**.

Кстати о playit. Так как они говноеды последние, то у них в айпи адресах нет порта через двоеточие. Поэтому такие адреса можно писать только в поле playit в json файле.


Версию майнкрафта и загрузчика модов следует указывать в *manifests/minecraft_manifest.json*

Файлы размещаются в соответствующие папки: моды в *mods*, прочие папки в *files*, аналог папки .minecraft.

Для обновления манифеста на сервере, после того как вы изменили содержимое папок используйте **unabomber.py**

Для обновления манифеста модов просто запустите скрипт из унабомбера.

Для обновления манифеста файлов сделайте то же самое, но придется подумать... Вам будет предложено вручную отмечать, обновили ли вы папку. А еще можете удалить ее. **УДАЛЯЙТЕ ТОЛЬКО ЧЕРЕЗ ЭТОТ СКРИПТ**
