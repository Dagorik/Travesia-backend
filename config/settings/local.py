from .base import *
import datetime


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7yy31*i9(-o$hth3nv8%-+a2)bp#*0kioi9vof4k%j_lkpa6t='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'teams',
        'USER': 'teams_admin',
        'PASSWORD': 'teams2018',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',

}


