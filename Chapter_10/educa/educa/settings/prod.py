from .base import *

# Obviously, it's for prod-mode!
DEBUG = False

# All the errors that being raised
#   will be sent to the admin user's email ( all of them :D )
ADMINS = {
    ('alex', '383138191@qq.com'),
}

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        # pass
    }
}