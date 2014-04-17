# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from mail.service import init_app_mail


class Command(BaseCommand):

    help = "Initialise 'mail' application"

    def handle(self, *args, **options):
        init_app_mail()
        print("Initialised 'mail' app...")
