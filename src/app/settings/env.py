import os
import json
import configparser

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'este es el super'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['api.withsocrates.com', '143.244.183.24', 'localhost']

CORS_ORIGIN_WHITELIST = (
    'https://learningwithsocrates-frontend.web.app',
    'https://api.withsocrates.com',
    'http://localhost:3000',
    'http://localhost:8000',
)

SITE_ID = 1

ENV_INSTALLED_APPS = []


# DEFAULT_DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'socrates',
        'USER': 'postgres',
        'PASSWORD': '123456789',
        'HOST': 'localhost',
        'PORT': '',
    }
}

PARLER_ENABLE_CACHING = False

PARLER_LANGUAGES = {
    1: (
        {'code': 'en-us', },
        {'code': 'es-mx', },
        {'code': 'th', },
    ),
    # Mexico site
    2: (
        {'code': 'es-mx', },
        {'code': 'en-mx', },
    ),
    'default': {
        'fallbacks': ['en-us', 'en-mx'],             # defaults to PARLER_DEFAULT_LANGUAGE_CODE
        'hide_untranslated': False,
    }
}


SENDGRID_API_KEY = ''
SENDGRID_DEFAULT_SENDER = 

# Stripe settings

STRIPE_LIVE_SECRET_KEY = "sk_live_"
STRIPE_TEST_SECRET_KEY = "sk_test_"
STRIPE_LIVE_MODE = False  # Change to True in production
# Get it from the section in the Stripe dashboard where you added the
# webhook endpoint
DJSTRIPE_WEBHOOK_SECRET = "whsec"
# We recommend setting to True for new installations
DJSTRIPE_USE_NATIVE_JSONFIELD = True
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"

# Google OAuth
GOOGLE_AUTH_CLIENT_ID = '-7njjtk3jrcp74i9okjnisf.apps.googleusercontent.com'
GOOGLE_AUTH_CLIENT_SECRET = 'GOCSPX-BkwO77s6gD9x1sv-R6'
GOOGLE_AUTH_API_KEY = 'AIzaSyAqT6_TWFA3RDmvLSFGfc'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
