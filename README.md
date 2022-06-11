# pult - реализация на Python сервиса регистрации ошибок для 1С:Предприятие 8

Сервис осуществляет регистрацию отчетов об ошибках, отправляемых 1С:Предприятие. См. https://its.1c.ru/db/instrpoly3#content:1190:hdoc, https://its.1c.ru/db/v8320doc#bookmark:dev:TI000002262,  https://wonderland.v8.1c.ru/blog/razvitie-mekhanizma-otobrazheniya-oshibok/.
Сервис реализован как Python скрипт для mod_wsgi. Скрипт использует SQLite3 для хранения информации об ошибках. Полученные отчеты хранятся в zip файлах без изменений.
При регистрации отчетов об ошибках в автоматическим режиме ведется учет уникальных ошибок. Поступивший отчет считается новой ошибкой, если образуется уникальная комбинация из следующих данных из отчета:
-	текст ошибки;
-	хеша стека ошибки конфигурации.

При регистрации новой ошибки есть возможность отправить email списку получателей. Через веб интерфейс можно просмотреть зарегистрированные ошибки и соответствующие им отчеты. Для ошибок можно устанавливать метки. Пример использования меток - если метка выставлена, значит ошибка обработана/зарегистрирована.

Если по ранее зарегистрированной пользователем ошибке будет повторно отправлен отчет с этого же компьютера, то изменится значение в поле "Число отчетов" в форме ошибки, пользовательское описание ошибки будет добавлено к предыдущему описанию. Сам отчет будет хранится в единственном экземпляре. Если в отчете не передана информации о компьютере или же в отчет был приложен файл, то отчет будет зарегистрирован и сохранен. 

## Описание структуры проекта
### init.py - создание SQLite базы

База создается в папке, заданной в переменной DATA_PATH файла prefs.py. Для получения доступа из веб сервера к базе необходимо задать переменные APACHE_USER и APACHE_GROUP в файле prefs.py значениями, которые использует веб сервер. Папке, указанной в DATA_PATH необходимо установить владельца и группу теми же значениями, которые использует веб сервер.

### prefs.py - настройки сервиса 
В переменной  CONFIGS задаются имена конфигурации и их версий, по которым принимаются отчеты об ошибках. Переменная имеет тип словарь (dict). Ключ - имя конфигурации, значение - список, состящий из 2-х списков.
-	1-й список - список допустимых версий. Если список пустой, то отчеты не принимаются. Пустая строка - принимаются любые версии. Неполное задание версии допускается.
-	2-й список - список email, которым будет отправлено сообщение о регистрации новой ошибки. Если список пустой, то почта для этой конфигурации не отправляется.
После внесения изменений в файл может потребоваться перезапуск веб сервера, чтобы настройки применились.

### pult.wsgi - основной скрипт
В скрипте реализованы следующие страницы веб интерфейса
#### s/errorsList - просмотр списка зарегистрированных ошибок
Для того чтобы просмотреть список ошибок, по которым был отправлен отчет, необходимо перейти по ссылке http://your.domain/pult/s/errorsList (в соответствии с указанной ниже настройке сервиса). Список ошибок имеет вид таблицы, в которой:
- N ошибки – порядковый номер ошибки. 
- Ошибки, errors – содержание ошибки.
- Конфигурация – конфигурация, в которой возникла ошибка.
- Расширения, extentions – установленные расширения.
- Метка – текстовая информация об ошибке с дополнительной информацией о пользователе и времени последнего изменения метки.

Доступен фильтр на конфигурации.

При нажатии на номер ошибки в табличной части открывается страница reports/N со списком отчетов, на ошибку с номером N.

#### errorsList - просмотр списка зарегистрированных ошибок
Страница идентична предыдущей, но поле Метка доступно только для просмотра и отсутствует фильтр на конфигурацию.

#### s/reports/N - просмотр 
Страница содержит информацию об ошибке и список отчетов по ошибке. Информация об ошибке отображается в таком же объеме как на странице s/errorsList.

Список отчетов содержит следующие колонки: дата, пользователь, IP адрес, с которого пришла ошибка, версия платформы и т.д. В поле "Число отчетов" показывается только отчетов было отправлено по ошибке с номером N с одного компьютера (дублирующиеся отчеты). Если в отчете есть вложенный файл, то в колонке с числом отчетов будет слово – Файл(ы) (отчеты с файлами не группируются).

При нажатии на гиперссылку в столбце «Число отчетов» откроется zip архив, в котором будет отчет об ошибке, полученный из 1С:Предприятие.
#### reports/N - просмотр 
Страница идентична предыдущей, но поле Метка у ошибки доступно только для просмотра.


#### s/settings - текущие настройки сервиса
В настройках указаны содержимое переменной CONFIGS файла с настройками сервиса prefs.py, в которой задаются имена конфигурации и их версий, по которым принимаются отчеты об ошибках. 

#### s/clear - удаление отчетов неподдерживаемых версий и конфигураций
Производится удаление ошибок и отчетов, которые не соответствуют критериям регистрации отчетов, приведенных в переменной CONFIGS файла prefs.py. Данная страница может быть использована для очистки базы при снятии конфигурации платформы 1С:Предприятия или версии конфигурации с поддержки.

## Установка
1) Подключить модуль mod_wsgi из пакета libapache2-mod-wsgi-py3
2) Скопировать файлы pult.wsgi, prefs.py, init.py в папку /var/www/wsgi/pult.
3) Внести настройки экземпляра сервиса в prefs.py
4) Запустить init.py
5) Зарегистрировать приложение WSGI
```
	WSGIScriptAlias /wsgi/pult /var/www/wsgi/pult/pult.wsgi
```

### Ограничение доступа
Для некотрых разделов сервиса предусмотрена возможность ограничить доступ. Такие разделы начинаются с префикса ``s/``. Чтобы ограничения доступа заработали нужно скопировать файл auth.wsgi в папку /var/www/wsgi/, перечислить в нём пользователей и их пароли, а в настройки apache добавить следующий раздел.
```
<Location "/wsgi/pult/s/">
    AuthType Basic
    AuthName "Restricted area"
    AuthBasicProvider wsgi
    WSGIAuthUserScript /var/www/wsgi/auth.wsgi
    Require valid-user
</Location>
```

Пример содержимого файла auth.wsgi
```
USERS = {
    "test" : "test"
}

def check_password(environ, user, password):
    if user in USERS:
        if password == USERS[user]:
            return True
        return False
    return None
```

