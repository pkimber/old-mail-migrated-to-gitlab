# -*- encoding: utf-8 -*-
from celery import shared_task

from .service import send_mail


@shared_task
def process_mail():
    send_mail()
