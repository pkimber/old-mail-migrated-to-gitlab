# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from celery import task

from .service import send_mail


@task()
def process_mail():
    send_mail()
