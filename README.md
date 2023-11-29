![](yatube/static/img/logo.png)

### Описание проекта:

В репозитории - финальный проект социальной сети. Позволяет вести блог/создавать заметки авторам с добавлением картинок. Зарегистрированные пользователи могут осуществить подписку на авторов и оставлять свои комментарии.

### Технологии

Python 3.7, Django, Bootstrap

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py makemigrations
```

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```
