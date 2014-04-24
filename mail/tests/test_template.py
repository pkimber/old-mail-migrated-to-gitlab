# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from mail.models import Template
from mail.service import init_template


class TestTemplate(TestCase):

    def test_init_template(self):
        init_template('hello', 'Welcome to our mailing list...')

    def test_init_template_update(self):
        init_template('hello', 'Welcome to our mailing list...')
        init_template('hello', 'Welcome...')
        template = Template.objects.get(slug='hello')
        self.assertEqual(template.title, 'Welcome...')
