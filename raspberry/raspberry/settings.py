"""
Django settings for raspberry project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

CUR_DIR = os.path.dirname(__file__)
MONITEUR_TEMPLATE = os.path.join(CUR_DIR, os.pardir, 'visualisation/templates/')
REGISTRATION_TEMPLATE = os.path.join(CUR_DIR, os.pardir, 'visualisation/registration/templates')
ADMIN_TEMPLATE = os.path.join(CUR_DIR, os.pardir, 'visualisation/grappelli/templates/')


STATIC_DIR = os.path.join(CUR_DIR, os.pardir, 'visualisation/static')

LOGIN_REDIRECT_URL = 'localisation' 


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@62=*3zn@m8z1rpk(0u6(lm_63odg3&o!))++24()005jflv!*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True 

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['192.168.1.19', 'ademovic.isa-geek.com']


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'moniteur',
    'visualisation',
    'bootstrap_toolkit',
    'widget_tweaks',
    'bootstrap3',
    'debug_toolbar',
    'registration',
    'grappelli',
    'django.contrib.admin',
#    'registration_defaults',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'raspberry.urls'

WSGI_APPLICATION = 'raspberry.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'mesure_db', # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'pi',
        'PASSWORD': 'toto1',
        'HOST': 'localhost', # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '', # Set to empty string for default.
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = False 


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATICFILES_DIRS = (
        STATIC_DIR,
)

TEMPLATE_DIRS = (MONITEUR_TEMPLATE, REGISTRATION_TEMPLATE, ADMIN_TEMPLATE)

STATIC_URL = '/static/'
