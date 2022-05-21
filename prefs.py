APACHE_USER = "www-data"                        # используется в init.py для создания Sqlite базы.
APACHE_GROUP = "www-data"                       # используется в init.py для создания Sqlite базы.
DATA_PATH = "/var/www/upload/pult"              # папка, где хранится Sqlite база и zip-файлы отчетов
SITE_DOMAIN = "http://your.domain"              # URL домена, где опубликован сервис
#SITE_URL = "/a/pult/s"                         # Версия с ограничением доступа к веб страницам сервиса. Часть URL публикации сервиса. Значение переменной должно заканчиваться на "pult" (требование 1С:Предприятие)
SITE_URL = "/a/pult"                            # Версия без ограничения доступа к веб страницам сервиса. Часть URL публикации сервиса. Значение переменной должно заканчиваться на "pult" (требование 1С:Предприятие)
SMTP_HOST = "localhost"                         # Если пустая строка, то отправок почты не будет
SMTP_PORT = "25"                                # Если почта отправляется, то указание значения обязательно
SMTP_FROM = "root@your.domain"                  # Если пустая строка, то отправок почты не будет
SMTP_LOGIN = ""
SMTP_PASSWORD =  ""

# Конфигурации и их версии, по которым принимаются отчеты об ошибках 
# В словаре (dict) ключ - имя конфигурации, значение - массив из 2-х списков.
# 1-й список - список допустимых версий. Если список пустой, то отчеты не принимаются.
# Пустая строка - принимаются любые версии. Неполное задание версии допускается.
# 2-й список - список email, которым будет отправлено сообщение о регистрации новой ошибки.
# Если список пустой, то почта для этой конфигурации не отправляется.

CONFIGS = {
    'МедицинаБольница':[
        ["2.0.6."],
        ["med@1c.ru","test@test.test"]
    ], 
    'МедицинаПоликлиника':[
        ["3.0.6."],
        ["med@1c.ru"]
    ], 
    'ДемонстрацияСвязиСТехподдержкой':[
        ["1.0.0.0"],
        ['test@test.test']
    ], 
    'БольничнаяАптека':[
        ["2.2.4"],
        ["med@1c.ru"]
    ]
}
