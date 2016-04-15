#
# settings.py
#

import os
from os.path import join
import raven
import local_settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = local_settings.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = local_settings.DEBUG

DEFAULT_CHARSET = 'utf-8'

ALLOWED_HOSTS = [ local_settings.PUBLIC_HOST ]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'raven.contrib.django.raven_compat',
    'survey',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
)

ROOT_URLCONF = 'crawls.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'crawls.wsgi.application'

DATABASES = {
    'default': local_settings.DATABASE,
}

LANGUAGE_CODE = 'sv-se'

TIME_ZONE = 'CET'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'

MEDIA_ROOT = join(BASE_DIR, 'media/')

LOGIN_URL = '/admin/login'

CONTACT_EMAIL = local_settings.CONTACT_EMAIL

GOOGLE_ANALYTICS_KEY = local_settings.GOOGLE_ANALYTICS_KEY

RAVEN_DSN = local_settings.RAVEN_DSN

RAVEN_CONFIG = {
    'dsn': local_settings.RAVEN_DSN_WITH_PASSWORD,
}

