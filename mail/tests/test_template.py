# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from mail.models import MailTemplate
from mail.service import (
    init_mail_template,
    mail_template_render,
)


class TestMailTemplate(TestCase):

    def test_init_template(self):
        init_mail_template(
            'hello',
            'Welcome to our mailing list.',
            "You can add the '{{ name }}' variable to this template."
        )

    def test_init_template_update(self):
        init_mail_template('hello', 'Welcome to our mailing list.', '')
        init_mail_template('hello', 'Welcome...', '')
        template = MailTemplate.objects.get(slug='hello')
        self.assertEqual(template.title, 'Welcome...')

    def test_render(self):
        template = init_mail_template(
            'hello',
            'Welcome to our mailing list.',
            (
                "You can add the following variables to the template:\n"
                "'{{ name }}' name of the customer.\n"
                "'{{ title }}' name of the village."
            )
        )
        template.subject = 'Hello {{ name }}'
        template.description = 'Welcome to {{ title }}'
        template.save()
        subject, description = mail_template_render(
            'hello', dict(name='Patrick', title='Hatherleigh')
        )
        self.assertEqual('Hello Patrick', subject)
        self.assertEqual('Welcome to Hatherleigh', description)
