"""
Django settings for MercadoOrganico project.
Generated by 'django-admin startproject' using Django 1.11.4.
For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Variable de entrono para CI
ON_CODESHIP = os.getenv('ON_CODESHIP', False)
ON_HEROKU_TEST = os.getenv('ON_HEROKU_TEST', False)
ON_HEROKU_PROD = os.getenv('ON_HEROKU_PRODheroku config', False)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ec*%#&9wh7^s%kv1(or3=zio8egzxi--v+)2^_9vn)7%*8f4x^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['amo-system-test.herokuapp.com','amo-system.herokuapp.com','localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'MercadoOrganico',
    'apps.administrador',
    'apps.apirest',
    'apps.comun',
    'apps.consumidor',
    'apps.distribuidor',
    'apps.productor',
]


MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',

]

ROOT_URLCONF = 'MercadoOrganico.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'MercadoOrganico.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
if ON_CODESHIP:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'test',
            'USER': os.environ.get('PGUSER'),
            'PASSWORD': os.environ.get('PGPASSWORD'),
            'HOST': '127.0.0.1',
        }
    }
elif ON_HEROKU_TEST:
    # Configuracion de base de datos para https://amo-system-test.herokuapp.com
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'd6b3o2o3b9013i',
            'USER': 'zjxwucjyszunpw',
            'PASSWORD': '30ccc70eceb57dea539050dff3ae8a9a11452124b37a0d60c5b2b3f6829c5f04',
            'HOST': 'ec2-184-72-230-93.compute-1.amazonaws.com',
            'PORT': '5432',
        }
    }

elif ON_HEROKU_PROD:
    # Configuracion de base de datos para https://amo-system.herokuapp.com/
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'd4n589lgspk1ar',
            'USER': 'kykrhryvappeeo',
            'PASSWORD': '43daabedf8d79c96e2cb686bbec2dd975ae28c208ccfcc093e4812385f176d2d',
            'HOST': 'ec2-204-236-236-188.compute-1.amazonaws.com',
            'PORT': '5432',
        }
    }
else:
    # Configuracion de base de datos local
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'MerkaOrganico',
            'USER': 'postgres',
            'PASSWORD': '1072661319',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

#STATIC_URL = '/static/'
STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'images'),
    os.path.join(BASE_DIR, 'static'),

)


# :::::::::::::::: ::::::::::::::::::::: ::::::::::
# :::::::::::::::: CONFIGURACION DE CORS::::::::::
# :::::::::::::::: ::::::::::::::::::::: ::::::::::

#Permitir peticiones de cualquier servidor
#DEV
CORS_ORIGIN_ALLOW_ALL = True

#Para permitir solo peticiones de los siguientes servidores
# Produccion

#CORS_ORIGIN_WHITELIST = (
#    'google.com',
#    'hostname.example.com',
#    'localhost:8000',
#    '127.0.0.1:9000'
#)