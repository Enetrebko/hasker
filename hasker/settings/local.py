from .base import *

DEBUG = True

SECRET_KEY = '7#_o8oc2od1un53#se+y0n-qj-@^7kzbx7$wm^lyob(v%z=7x*'

STATIC_ROOT = os.path.join(BASE_DIR, 'hasker_app/static_loc')
MEDIA_ROOT = os.path.join(BASE_DIR, 'hasker_app/media_loc')

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hasker_db',
        'USER': 'postgres',
        'PASSWORD': '1134',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'hasker.app@mail.ru'
EMAIL_HOST_PASSWORD = 'otus1134'
