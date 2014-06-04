mail
****

Django application for an sending email.

For notes:
https://django-dev-and-deploy-using-salt.readthedocs.org/en/latest/app-mail.html
or
https://github.com/pkimber/docs/blob/master/source/app-mail.rst

Install
=======

Virtual Environment
-------------------

::

  pyvenv-3.4 --without-pip venv-mail
  source venv-mail/bin/activate
  wget https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py
  python get-pip.py

  pip install -r requirements/local.txt

To run the tests, you will need to create a file called ``.private`` in the
top level directory of the app.  This should contain the following::

  export MAILGUN_SERVER_NAME="<your domain name used for the notify email address>"
  export MANDRILL_API_KEY="<your api key>"
  export MANDRILL_USER_NAME="<Your MANDRILL email address used to create your account>"
  export TEST_EMAIL_ADDRESS_1="<an email address to use for running the test scenarios>"
  export TEST_EMAIL_ADDRESS_2="<another different email address to use for running the test scenarios>"

.. warning:: The ``.private`` file should not be added to a public repository,
             as it contains *secret* information.  So please do not add it to
             ``git``.

To send email, use the ``mail_send`` management command::

  django-admin.py mail_send

Testing
=======

::

  find . -name '*.pyc' -delete
  py.test -x

Usage
=====

::

  py.test -x && \
      touch temp.db && rm temp.db && \
      django-admin.py syncdb --noinput && \
      django-admin.py migrate --all --noinput && \
      django-admin.py demo_data_login && \
      django-admin.py init_app_mail && \
      django-admin.py demo_data_mail && \
      django-admin.py runserver

Release
=======

https://django-dev-and-deploy-using-salt.readthedocs.org/
