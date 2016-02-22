#!/bin/bash
# treat unset variables as an error when substituting.
set -u
# exit immediately if a command exits with a nonzero exit status.
set -e

py.test -x
touch temp.db && rm temp.db
django-admin.py migrate --noinput
django-admin.py demo_data_login
django-admin.py init_app_mail
django-admin.py demo_data_mail
django-admin.py runserver
