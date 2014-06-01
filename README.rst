mail
****

Django application for an sending email.



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

  You'll also need to create a file called .private in the top level directory of the app
  This should contain the following:
    export MANDRILL_USER_NAME="<Your MANDRILL email address used to create your account>"
    export MANDRILL_USER_NAME="<Your MANDRILL email address used to create your account>"
    export MAILGUN_SERVER_NAME="<your domain name used for the notify email address>"
    export TEST_EMAIL_ADDRESS_1="<an email address to use for running the test scenarios>"
    export TEST_EMAIL_ADDRESS_2="<another different email address to use for running the test scenarios>"

  You'll also need a way to run the app mail sending service. One way to do this is to create a python run script called run_mail_service.py. This can then be run from a bash script.  This should contain:
    from mail.service import (send_mail, send_messages_via_mandrill) 
    
    # uncomment the next line if you are using mandrill
    # send_message_via_mandrill() 
    
    # uncomment the next line if you are using the default django mail backend
    # send_mail()
  
  You'll also need to create a shell script to run from cron Here's an example
  	#!/bin/bash
  	cd <directory where you installed the application that contains you app>
  	
  	source .env
  	
  	python <full path to run_mail_service.py script>
  	

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

::

  This app provides several API functions, these are accessed as follows:

  from mail.service import (
      queue_mail,
      send_mail,
      sned_mail_via_mandrill,
      render_mail_template
  )

::

  

Release
=======

https://django-dev-and-deploy-using-salt.readthedocs.org/
