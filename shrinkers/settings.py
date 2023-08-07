"""
Django settings for shrinkers project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import json
import os
from pathlib import Path
from google.oauth2 import service_account

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-c$=1x@lyzvli3fb9x*8v+bgbz0&wq@%!5%6$ge69m=6(67=qy('

# SECURITY WARNING: don't run with debug turned on in production!
ENV = os.environ.get("DJANGO_ENV", "dev")

if ENV == "dev":
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = ["*"]


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shortener',
    'django_user_agents',
    'rest_framework',
    'drf_yasg',
    'corsheaders',
]

# if DEBUG:
#     INSTALLED_APPS += [
#         "debug_toolbar",
#         "django_seed",
#     ]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
}

INTERNAL_IPS = [
    '127.0.0.1',
]  # Django Debug Toolbar

LOGIN_URL = '/login'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'shortener.middleware.ShrinkersMiddleware',
]

# if DEBUG:
#     MIDDLEWARE += [
#         "debug_toolbar.middleware.DebugToolbarMiddleware",  # Django Debug Toolbar
#     ]

CORS_ORIGIN_ALLOW_ALL = True

GEOIP_PATH = os.path.join(BASE_DIR, "geolite2")

ROOT_URLCONF = 'shrinkers.urls'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'shrinkers.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "app_db",
        "USER": "root",
        "PASSWORD": "admin1234",
        "HOST": "34.64.232.58",
        "PORT": 3306,
        "OPTIONS": {
            "autocommit": True,
            "charset": "utf8mb4"
        }
    }
}

try:
    EMAIL_ID = json.load(
        open(os.path.join(BASE_DIR, "keys.json"))).get("email")
    EMAIL_PW = json.load(
        open(os.path.join(BASE_DIR, "keys.json"))).get("email_pw")

except Exception:
    EMAIL_ID = None
    EMAIL_PW = None

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

if DEBUG:
    STATIC_URL = "/static/"
else:
    SERVICE_KEY = json.load(
        open(os.path.join(BASE_DIR, "keys.json"))).get("service_key")
    GS_CREDENTIALS = service_account.Credentials.from_service_account_info(
        SERVICE_KEY
    )
    DEFAULT_FILE_STORAGE = "config.storage_backends.GoogleCloudMediaStorage"
    STATICFILES_STORAGE = "config.storage_backends.GoogleCloudStaticStorage"
    GS_STATIC_BUCKET_NAME = "shrinkers-project"
    STATIC_URL = "https://storage.googleapis.com/{}/statics/".format(
        GS_STATIC_BUCKET_NAME)

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CACHE = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": os.path.join(BASE_DIR, "cache_file"),
    }
}
