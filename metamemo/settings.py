"""
Django settings for metamemo project.

Generated by 'django-admin startproject' using Django 3.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import base64
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

import dj_database_url
import sentry_sdk
from decouple import Csv, config
from django.utils.log import DEFAULT_LOGGING
from sentry_sdk.integrations.django import DjangoIntegration


def base64_decode_to_file(value):
    """Decode base64 value, write to a temp file and return filename"""
    if not value:
        return ""
    credentials = base64.b64decode(value)
    temp = NamedTemporaryFile(delete=False)
    with open(temp.name, mode="wb") as fobj:
        fobj.write(credentials)
    return temp.name

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool, default=False)

# Hostname
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", cast=Csv())

# Application definition
INSTALLED_APPS = [
    "metamemoapp",
    "timeline",
    "import_export",
    "blog",
    "django_summernote",
    "django_celery_results",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
if DEBUG:

    def show_toolbar(request):
        return request.user.is_authenticated

    position = INSTALLED_APPS.index("blog")
    INSTALLED_APPS.insert(position, "debug_toolbar")

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": "metamemo.settings.show_toolbar",
    }

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
if DEBUG:
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

ROOT_URLCONF = "metamemo.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates/"),
        ],
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
WSGI_APPLICATION = "metamemo.wsgi.application"

# Error reporting
SENTRY_DSN = config("SENTRY_DSN", default=None)
if SENTRY_DSN:
    sentry_sdk.init(
        SENTRY_DSN,
        integrations=[DjangoIntegration()],
        send_default_pii=True,
    )
LOGGING = DEFAULT_LOGGING.copy()
LOGGING["handlers"]["null"] = {"class": "logging.NullHandler"}
LOGGING["loggers"]["django.security.DisallowedHost"] = {"handlers": ["null"], "propagate": False}

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    "default": dj_database_url.config(),
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = str(BASE_DIR) + "/static"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Storage
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_S3_ENDPOINT_URL = config("AWS_S3_ENDPOINT_URL", default="")
AWS_S3_ACCESS_KEY_ID = config("AWS_S3_ACCESS_KEY_ID", default="")
AWS_S3_SECRET_ACCESS_KEY = config("AWS_S3_SECRET_ACCESS_KEY", default="")
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME", default="")

# Celery
CELERY_RESULT_BACKEND = "django-db"
CELERY_BROKER_URL = config("REDIS_URL")

# Custom settings
METAMEMO_LANGUAGE = "pt-BR"

TWITTER_BEARER_TOKEN = config("TWITTER_BEARER_TOKEN", default="")

FACEBOOK_COOKIES = base64_decode_to_file(config("FACEBOOK_COOKIES_BASE64", default=""))
FACEBOOK_PAGES = config("FACEBOOK_PAGES", default=4, cast=int)
FACEBOOK_PPP = config("FACEBOOK_PPP", default=10, cast=int)

TELEGRAM_API_ID = config("TELEGRAM_API_ID", default="")
TELEGRAM_API_HASH = config("TELEGRAM_API_HASH", default="")

CROWDTANGLE_FACEBOOK_API_KEY = config("CROWDTANGLE_FACEBOOK_API_KEY", default="")
CROWDTANGLE_INSTAGRAM_API_KEY = config("CROWDTANGLE_INSTAGRAM_API_KEY", default="")
CROWDTANGLE_POSTS_COUNT = config("CROWDTANGLE_POSTS_COUNT", default=100, cast=int)
CROWDTANGLE_POSTS_INTERVAL = config("CROWDTANGLE_POSTS_INTERVAL", default="5 DAY")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = base64_decode_to_file(config("GOOGLE_APPLICATION_CREDENTIALS_BASE64", default=""))
GOOGLE_BLOGGER_CREDENTIALS = config("GOOGLE_BLOGGER_CREDENTIALS", default="")
GOOGLE_YOUTUBE_CREDENTIALS = config("GOOGLE_YOUTUBE_CREDENTIALS", default="")
