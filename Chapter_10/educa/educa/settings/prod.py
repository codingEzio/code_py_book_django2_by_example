from .base import *
from .whoa import *

# Obviously, it's for prod-mode!
DEBUG = False

# All the errors that being raised
#   will be sent to the admin user's email ( all of them :D )
ADMINS = {
    (TEST_NAME, TEST_PSWD),
}

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE'  : 'django.db.backends.postgresql',
        'NAME'    : 'educa',
        'USER'    : 'educa',
        'PASSWORD': POSTGRESQL_PASSWORD,
    }
}