# -*- encoding: utf-8 -*-
from django.test import TestCase

from mail.models import (
    Mail,
    MailTemplate,
)
from mail.service import _mail_template_render


class TestMailTemplate(TestCase):

    def test_init_template(self):
        MailTemplate.objects.init_mail_template(
            'hello',
            'Welcome to our mailing list.',
            "You can add the '{{ name }}' variable to this template.",
            False,
            MailTemplate.DJANGO,
        )

    def test_init_template_update(self):
        MailTemplate.objects.init_mail_template(
                'hello',
                'Welcome to our mailing list.',
                '',
                False,
                MailTemplate.DJANGO
        )
        MailTemplate.objects.init_mail_template(
                'hello',
                'Welcome...',
                '', False,
                MailTemplate.DJANGO
        )
        template = MailTemplate.objects.get(slug='hello')
        self.assertEqual(template.title, 'Welcome...')

    def test_render(self):
        template = MailTemplate.objects.init_mail_template(
            'hello',
            'Welcome to our mailing list.',
            (
                "You can add the following variables to the template:\n"
                "'{{ name }}' name of the customer.\n"
                "'{{ title }}' name of the village."
            ),
            False,
            MailTemplate.DJANGO
        )
        template.subject = 'Hello {{ name }}'
        template.description = 'Welcome to {{ title }}'
        template.save()
        subject, description = _mail_template_render(
            'hello', dict(name='Patrick', title='Hatherleigh')
        )
        self.assertEqual('Hello Patrick', subject)
        self.assertEqual('Welcome to Hatherleigh', description)
