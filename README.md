# get-med
Сервис заказа медицинских услуг

###### Создание виртуального окружения:
```shell
python3 -m venv venv
```

###### Активация виртуального окружения на Mac:
```shell
source venv/bin/activate
```

###### Активация виртуального окружения на Windows:
```shell
venv\Scripts\activate
```

###### Обновление пакетов виртуального окружения:
```shell
pip install --upgrade pip
```

###### Установка зависимостей:
```shell
pip install -r requirements.txt
```

###### Создание миграции для БД:
```shell
python manage.py makemigrations
```

###### Миграция данных для таблиц:
```shell
python manage.py migrate
```

###### Создать суперпользователя:
```shell
python manage.py createsuperuser
```

###### Запуск локального сервера:
```shell
python manage.py runserver
```