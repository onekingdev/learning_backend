"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from .env import SECRET_KEY, ENV_INSTALLED_APPS, SENDGRID_API_KEY, SENDGRID_DEFAULT_SENDER
from .env import CORS_ORIGIN_WHITELIST as ENV_CORS_ORIGIN_WHITELIST
from .env import ALLOWED_HOSTS as ENV_ALLOWED_HOSTS
# from .env import GOOGLE_AUTH_CLIENT_ID, GOOGLE_AUTH_CLIENT_SECRET, GOOGLE_AUTH_API_KEY

from pathlib import Path
from datetime import timedelta
from django.conf import settings
import mimetypes

# Enable mimetypes
mimetypes.add_type("text/javascript", ".js", True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/
CORS_ALLOW_ALL_ORIGINS = True

# Application definition

# CORS_ORIGIN_WHITELIST = ENV_CORS_ORIGIN_WHITELIST
# ALLOWED_HOSTS = ENV_ALLOWED_HOSTS

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',


    'django_extensions',
    'mptt',
    'polymorphic',
    'ckeditor',
    'parler',
    'import_export',
    'import_export_celery',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'graphene_django',
    'graphql_jwt.refresh_token.apps.RefreshTokenConfig',
    'mailer',
    'adminsortable2',
    'djmoney',
    'djstripe',

    'api',
    'avatars',
    'audiences',
    'accounting',
    'achievements',
    'bank',
    'block',
    'collectibles',
    'emails',
    'engine',
    'experiences',
    'guardians',
    'games',
    'kb',
    'organization',
    'plans',
    'students',
    'universals',
    'users',
    'wallets',
    'payments'
]


INSTALLED_APPS += [app for app in ENV_INSTALLED_APPS if app not in INSTALLED_APPS]


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'author.middlewares.AuthorDefaultBackendMiddleware',
]


# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'app.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = 'users.User'


LOGIN_REDIRECT_URL = '/my-account'

REST_USE_JWT = True
JWT_AUTH_COOKIE = 'my-app-auth'
JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token'


GRAPH_MODELS = {
    'all_applications': True,
    'group_models': True,
}

# Graphene
GRAPHENE = {
    "SCHEMA": "app.schema.schema",
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}

GRAPHQL_JWT = {
    'JWT_PAYLOAD_HANDLER': 'app.utils.jwt_payload',
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LONG_RUNNING_REFRESH_TOKEN': True,
    'JWT_EXPIRATION_DELTA': timedelta(days=2),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7),
    # TODO: Change to environment variable
    'JWT_SECRET_KEY': 'llave super secreta',
    'JWT_ALGORITHM': 'HS256',
}
AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
    # 'allauth.account.auth_backend.AuthenticationBackends',
]


ACCOUNT_UNIQUE_EMAIL = False
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_VERIFICATION = 'none'


EMAIL_BACKEND = "mailer.backend.DbBackend"
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'apikey'  # this is exactly the value 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
DEFAULT_FROM_EMAIL = SENDGRID_DEFAULT_SENDER

# Additional languages
settings.LANGUAGES.append(
    ('en-us', 'American English')
)


PARLER_ENABLE_CACHING = False


def topics_resource():
    from kb.resources import TopicAdminResource
    return TopicAdminResource


IMPORT_EXPORT_CELERY_MODELS = {
    "Topics": {
        'app_label': 'kb',
        'model_name': 'Topic',
        'resource': topics_resource,
    }
}

# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'APP': {
#             'client_id': GOOGLE_AUTH_CLIENT_ID,
#             'secret': GOOGLE_AUTH_CLIENT_SECRET,
#             'key': GOOGLE_AUTH_API_KEY,
#         }
#     }
# }
