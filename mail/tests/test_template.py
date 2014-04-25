# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from mail.models import Template
from mail.service import (
    init_template,
    mail_template_render,
)


class TestTemplate(TestCase):

    def test_init_template(self):
        init_template('hello', 'Welcome to our mailing list...')

    def test_init_template_update(self):
        init_template('hello', 'Welcome to our mailing list...')
        init_template('hello', 'Welcome...')
        template = Template.objects.get(slug='hello')
        self.assertEqual(template.title, 'Welcome...')

    def test_render(self):
        template = init_template('hello', 'Welcome to our mailing list...')
        template.subject = 'Hello {{ name }}'
        template.description = 'Welcome to {{ title }}'
        template.save()
        subject, description = mail_template_render(
            'hello', dict(name='Patrick', title='Hatherleigh')
        )
        self.assertEqual('Hello Patrick', subject)
        self.assertEqual('Welcome to Hatherleigh', description)
