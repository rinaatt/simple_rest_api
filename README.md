# Пример простого REST API
Технологии: Python 3 / Django, REST framework

Для запуска необходимо наличие docker и docker-compose

Клонируем репозитарий, переходим в корень проекта и выполняем команду, для запуска проекта:

    docker-compose up

Консоль будет выводить лог и станут доступны два урла:

* http://localhost:8001/ - сам API созданный на REST framework
* http://localhost:8002/ - "админка" проекта

Для создания суперюзера, даём комманду:

    docker-compose exec rest ./create_su.sh

Нужно будет ввести два разад желаемый пароль и будет создан "Django superuser" с логином 'admin'.
Либо можно через команду:

    ./run_django_admin.sh createsuperuser

создать этого пользователя со своими данными.

Для заполнения БД фиктивными данными можно использовать команду:

    ./run_django_admin.sh fake_data

Будет созданы такие фейковые данные:

* 10 - партнёрских организаций с привязанными пользователями
* 50 - кредитных организаций с привязанными пользователями
* 400 - предложений (Offer)
* 1000 - анкет клиентов

в папке `./rest/fake_users.txt` будут сохранены логины и пароли свежесозданных пользователей.

Чтобы "остановить" проект нажимайте в консоли с логом `Ctrl+C` и далее с помощью комманды:

    docker-compose down --rmi all -v

можно будет удалить созданные докером образы, контейнеры и тома.
