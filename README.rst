mail
****

Django application for sending mail:
https://www.kbsoftware.co.uk/docs/app-mail.html

Development
===========

Prerequisites
-------------

Redis (for the celery queue)

Virtual Environment
-------------------

::

  virtualenv --python=python3 venv-mail
  source venv-mail/bin/activate

  pip install -r requirements/local.txt

Usage
-----

.. note:: Replace ``patrick`` with your user name in the examples below.

Create a ``settings/dev_patrick.py`` file (use ``settings/dev_patrick.py`` as a
template).

Create a ``.private`` file in the root of the project.

.. warning:: The ``.private`` file is for adding account keys etc to your
             environment.  Do NOT add it to the version control system.

Add the following to the ``.private`` file::

  export MAILGUN_SERVER_NAME="<your domain name used for the notify email address>"
  export MANDRILL_API_KEY="<your api key>"
  export MANDRILL_USER_NAME="<Your MANDRILL email address used to create your account>"
  export TEST_EMAIL_ADDRESS_1="<an email address to use for running the test scenarios>"
  export TEST_EMAIL_ADDRESS_2="<another different email address to use for running the test scenarios>"

Testing
=======

::

  find . -name '*.pyc' -delete
  py.test -x

Usage
=====

Create a test database::

  # this command will drop the database if it already exists.
  psql -X -U postgres -c "DROP DATABASE test_mail_patrick"
  psql -X -U postgres -c "CREATE DATABASE test_mail_patrick TEMPLATE=template0 ENCODING='utf-8';"

.. note:: We use PostgreSQL rather than SQLite because Celery has some issues
          with SQLite

Initialise the test database::

  ./init_dev.sh

You will need to open three terminal windows::

  # 1) Celery worker
  celery -A project worker --loglevel=info

  # 2) Celery beat
  celery -A project beat --loglevel=info

  # 3) Django development server
  django-admin.py runserver

Browse to http://localhost:8000/::

  user          staff
  password      letmein

To send email, use the ``mail_send`` management command::

  django-admin.py mail_send

Release
=======

https://www.kbsoftware.co.uk/docs/
