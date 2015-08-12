"""
Django settings for cetaganda project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(__file__)

SECRET_KEY = '$b*5p2p#up#)gc*(m##6y(5u&(x#gurcx6lb@hwkl+l(78-g8h'
ALLOWED_HOSTS = ['cetaganda.ru']
DOMAIN = 'https://cetaganda.ru'
INTERNAL_IPS = ('127.0.0.1',)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SERVER_EMAIL = DEFAULT_FROM_EMAIL = 'info@cetaganda.ru'
ADMINS = (('Glader', 'glader.ru@gmail.com'),)
MANAGERS = (('Lina', 'linashyti@gmail.com'),)

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')
STATIC_URL = '/static/'

LOGIN_URL = '/users/cabinet'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_ulogin',
    'gunicorn',
    'pytils',
    'redactor',
    'yafotki',

    'bookkeeping',
    'hack',
    'news',
    'post_logger',
    'roles',
    'science',
    'staticpages',
    'users',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'roles.middleware.GetUserRole',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'post_logger.middleware.LogPostData',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'

# Internationalization
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Redactor
REDACTOR_OPTIONS = {
    'lang': 'ru',
    'buttonSource': True,
}
REDACTOR_UPLOAD_HANDLER = 'yafotki.handlers.FotkiUploader'

# Yafotki
YAFOTKI_STORAGE_OPTIONS = {
    'username': 'user',
    'album': 'default',
}

# ULogin
ULOGIN_FIELDS = ['first_name', 'last_name']
ULOGIN_OPTIONAL = ['sex', 'phone', 'city']
ULOGIN_PROVIDERS = ['vkontakte', 'livejournal', 'yandex', 'mailru']
ULOGIN_HIDDEN = ['facebook', 'twitter', 'google', 'odnoklassniki', 'openid']
ULOGIN_CREATE_USER_CALLBACK = 'users.models.create_user'
ULOGIN_DISPLAY = 'panel'

# Logging
LOG_DIR = '/var/log/projects/cetaganda'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(name)-15s %(levelname)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'traceback.log'),
            'formatter': 'verbose',
        },
        'post_log': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'post.log'),
            'formatter': 'verbose',
        },
        'mail_admin': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admin', 'file'],
            'level': 'WARNING',
            'propagate': True,
        },
        'post': {
            'handlers': ['post_log'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}


try:
    from local_settings import *
except ImportError:
    pass
