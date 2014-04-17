# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from mail.service import send_mail


class Command(BaseCommand):

    help = "Send mail messages."

    def handle(self, *args, **options):
        send_mail()
