"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

from .envtools import getenv
from django.utils.timezone import timedelta
from celery.schedules import crontab
import django_crontab

# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = getenv("SECRET_KEY", default="###SECRET_KEY###")

DEBUG = getenv("DEBUG", default=True, coalesce=bool)

ALLOWED_HOSTS = ["*"]

USE_X_FORWARDED_HOST = False
SESSION_COOKIE_HTTPONLY = True

SERVER_URL = os.getenv("SERVER_URL", default="*")


APPEND_SLASH = False

AUTH_USER_MODEL = 'bonapetit.User'

# Application definition
#CELERY_BROKER_URL = "redis://localhost:6379"
#CELERY_RESULT_BACKEND = "redis://localhost:6379"
#CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_extensions",
    "backend_test.utils",
    "bonapetit.apps.BonapetitConfig",
    "celery",
    "django_celery_beat",
    'django_crontab',
    "slack"
]

MIDDLEWARE = [
    "backend_test.middleware.HealthCheckAwareSessionMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "backend_test.middleware.HeaderNoCacheMiddleware",
]

ROOT_URLCONF = "backend_test.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend_test.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": getenv("POSTGRES_DEFAULT_DB", default="cornershop"), #cornershop
        "USER": getenv("POSTGRES_DEFAULT_USER", default="cornershop"), #cornershop
        "PASSWORD": getenv("POSTGRES_DEFAULT_PASSWORD", default="mypass"), #mypass
        "HOST": getenv("POSTGRES_DEFAULT_HOSTNAME", default="localhost"), #localhost
        "PORT": 5432,
        "CONN_MAX_AGE": 600,
        "DISABLE_SERVER_SIDE_CURSORS": True,
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{}:6379/0".format(
            getenv("REDIS_CACHE_HOSTNAME", default="redis")
        ),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "../collected_static")
STATIC_URL = "/static/"

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        "rest_framework.authentication.SessionAuthentication",
        'rest_framework.authentication.BasicAuthentication'
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('JWT',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

if getenv("BROWSABLE_API_RENDERER", default=False, coalesce=bool):
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = REST_FRAMEWORK[
        "DEFAULT_RENDERER_CLASSES"
    ] + ["rest_framework.renderers.BrowsableAPIRenderer"]

# APP SPECIFIC SETTINGS

# if getenv("SENTRY_DSN", default=None):
#    sentry_sdk.init(dsn=getenv("SENTRY_DSN"), integrations=[DjangoIntegration()])

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "fluent_formatter": {
            "()": "backend_test.logging_formatter.VerboseFluentRecordFormatter",
            "format": {
                "level": "%(levelname)s",
                "pathname": "%(pathname)s",
                "hostname": "%(hostname)s",
                "logger": "%(name)s",
                "module": "%(module)s",
                "funcname": "%(funcName)s",
                "namespace": os.getenv("KUBERNETES_NAMESPACE", "localhost"),
                "release": os.getenv("GIT_HASH", "local"),
            },
            "encoder_class": "django.core.serializers.json.DjangoJSONEncoder",
            "raise_on_format_error": DEBUG,
        },
        "simple": {
            "format": "[{asctime}] {levelname} {message}",
            "style": "{",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        },
    },
    "filters": {"require_debug_true": {"()": "django.utils.log.RequireDebugTrue"}},
    "handlers": {
        "sentry": {
            "level": "WARNING",
            "class": "sentry_sdk.integrations.logging.EventHandler",
        },
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "filters": ["require_debug_true"],
        },
        "fluent": {
            "class": "fluent.handler.FluentHandler",
            "host": os.getenv("FLUENT_HOST", "fluentbit"),
            "port": int(os.getenv("FLUENT_PORT", 24224)),
            "tag": os.getenv("FLUENT_TAG", "catalog"),
            "formatter": "fluent_formatter",
            "level": "INFO",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
    },
    "root": {"level": "WARNING", "handlers": ["sentry"]},
    "loggers": {
        "django": {"handlers": ["console"], "propagate": True},
        "django.db": {
            "handlers": ["console"],
            "propagate": False,
            "level": os.getenv("DB_LOGGING_LEVEL", "INFO"),
        },
        "django.server": {"handlers": ["django.server"], "propagate": False},
        "backend_test": {
            "handlers": ["fluent", "console"],
            "level": os.getenv("APP_LOGGING_LEVEL", "INFO"),
            "propagate": True,
        },
    },
}

CELERY_BEAT_SCHEDULE = {
    "sample_task": {
        "task": "bonapetit.tasks.sample_task",
        "schedule": "10.0"#crontab(minute="*/1"),
    },
}

CRONJOBS = [
    ('1 9 * * *', 'bonapetit.cron.my_cron_job', )
]

VERIFICATION_TOKEN = "PdEpTMQEW3ycU1qHwbHUq5CN"
OAUTH_ACCESS_TOKEN = "xoxp-2014251975012-1993316122583-2005236709637-d136ee6652078d34eeaae6635aecbd80"
BOT_USER_ACCESS_TOKEN = "xoxb-2014251975012-1993396992055-x4VgFLcosZF0GV7dii2neb3u"
CLIENT_ID = "2014251975012.2014258538724"
CLIENT_SECRET = "d7e867f74ec48c3782a2d73130242684"