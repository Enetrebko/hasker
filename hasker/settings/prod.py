from .base import *

DEBUG = False

SECRET_KEY = os.getenv('SECRET_KEY')

ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.getenv('STATIC_ROOT')
MEDIA_ROOT = os.getenv('MEDIA_ROOT')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('HASKER_DATABASE_NAME'),
        'USER': os.getenv('HASKER_DATABASE_USER'),
        'PASSWORD': os.getenv('HASKER_DATABASE_PASSWORD'),
        'HOST': os.getenv('HASKER_DATABASE_HOST'),
        'PORT': os.getenv('HASKER_DATABASE_PORT')
    }
}

EMAIL_USE_SSL = True
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
