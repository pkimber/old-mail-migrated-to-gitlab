# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from example.management.commands import demo_data_mail

from mail.management.commands import init_app_mail


class TestCommand(TestCase):

    def test_demo_data(self):
        """ Test the management command """
        pre_command = init_app_mail.Command()
        pre_command.handle()
        command = demo_data_mail.Command()
        command.handle()
