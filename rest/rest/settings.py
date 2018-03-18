"""
Django settings for docker_django project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys
import os.path as op
import environ

root: environ.Path = environ.Path(__file__) - 2
env = environ.Env(DEBUG=(bool, False), )
# environ.Env.read_env()

BASE_DIR: str = root()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY: str = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG: bool = env('DEBUG', cast=bool)

ALLOWED_HOSTS: list = env('ALLOWED_HOSTS', cast=list, default=['*'])


# Claim definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'crispy_forms',
    'apps.common',
    'apps.credits',
    'apps.partners',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rest.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            root('rest', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rest.wsgi.application'


# Database
DATABASES = {
    'default': env.db('DATABASE_URL')
}

CACHES = {
    'default': env.cache('REDIS_URL'),
}
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# LOGIN_URL = '/api-auth/login/'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation'
             '.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation'
             '.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation'
             '.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation'
             '.NumericPasswordValidator', },
]


# Internationalization
LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = env('TIME_ZONE', default='UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATICFILES_DIRS = [
    root('rest', 'static'),
]
STATIC_ROOT = root('public', 'static')
if not op.exists(STATIC_ROOT):
    os.makedirs(STATIC_ROOT)
STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'custom': {
            'format': '[%(name)s %(levelname)s] %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'custom',
        },
    },
    'loggers': {
        'apps': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
