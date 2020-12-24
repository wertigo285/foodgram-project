
![Foodgram workflow](https://github.com/wertigo285/foodgram-project/workflows/Foodgram/badge.svg)
# Проект "Foodgram"


Учебный проект, по разработке онлайн-сервиса Foodgram — онлайн сервис для обмена рецептами, пользователи которого могут подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», формировать список покупок из отмеченных рецептов.

Проект развернут на виртуальном сервере Яндекс.Облако и доступен по адресу - http://foodgram-khsb.tk/



## Установка

### 1. Установить Docker

Процесс установки описан в [официальном руководстве](https://docs.docker.com/engine/install/).

### 2. Клонировать репозиторий

```
git clone git@github.com:wertigo285/foodgram-project.git
```


## Запук проекта

Для запуска проекта в папке клонированного репозитория необходимо выполнить команду.

```
docker-compose up
```

После построения образов приложение REST API для YamDb будет развернуто в виде двух docker контейнеров:
* db  - контейнер СУБД PostgreSQL разернутый из [официального образа](https://hub.docker.com/_/postgres)
* web - контейнер веб-приложения, загруженный из образа
* nginx - контейнер с веб-серером

Шаблон настроек находятся в файле **.env.template** . 

Для начального заполнения базы данных тэгами и ингредиентами в корневой папке проекта необходимо выполнить команды:
```
docker exec -it web python manage.py makemigrations
docker exec -it web python manage.py migrate
docker exec -it web python manage.py collectstatic
docker exec -it web python data_to_db.py
```


## Управление запущенным приложением

### Создать суперпользователя
```
docker exec -it web python manage.py createsuperuser
```

### Создать миграции
```
docker exec -it web python manage.py makemigrations
```

### Выполнить миграции
```
docker exec -it web python manage.py migrate
```

### Заполнить базу данных тестовыми данными
```
docker exec -it web python data_to_db.py
```

### Остановить проект
В командной строке, в папке репозитория выполнить:
```
docker-compose down
```
### использованные технологии

* [Python 3.8](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [Docker](https://www.docker.com/)
* [PostgreSQL](https://www.postgresql.org/)
* [NGINX](https://nginx.org/)
