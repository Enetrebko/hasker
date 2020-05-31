# Hasker: Poor Man's Stackoverflow

## How to use

Provide .env file in the root folder

Example:
```
SECRET_KEY=secret

STATIC_ROOT=/static
MEDIA_ROOT=/media

HASKER_DATABASE_NAME=hasker_db
HASKER_DATABASE_USER=hasker
HASKER_DATABASE_PASSWORD=password
HASKER_DATABASE_HOST=db
HASKER_DATABASE_PORT=5432

EMAIL_HOST=smtp.mail.ru
EMAIL_PORT=465
EMAIL_HOST_USER=hasker.app@mail.ru
EMAIL_HOST_PASSWORD=password

DJANGO_SETTINGS_MODULE=hasker.settings.prod
```

To deploy app use

```shell
docker-compose up --build
```

app will be available on localhost:8000/hasker_app/
