# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from celery import shared_task

from .service import send_mail


@shared_task
def process_mail():
    send_mail()


@shared_task
def process_periodic_task():
    send_mail()
