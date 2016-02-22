# -*- encoding: utf-8 -*-
from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'temp.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'test_app_mail_patrick',
#         'USER': 'patrick',
#         'PASSWORD': '',
#         'HOST': '',
#         'PORT': '',
#     }
# }

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
