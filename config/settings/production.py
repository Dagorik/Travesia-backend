from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7yy31*i9(-o$hth3nv8%-+a2)bp#*0kioi9vof4k%j_lkpa6t='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
