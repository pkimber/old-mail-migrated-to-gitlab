# -*- encoding: utf-8 -*-
from django.core.management.base import BaseCommand

from example_mail.tests.scenario import default_scenario_mail


class Command(BaseCommand):

    help = "Create demo data for 'mail'"

    def handle(self, *args, **options):
        default_scenario_mail()
        print("Created 'mail' demo data...")
