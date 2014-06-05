# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core import mail
from django.test import TestCase

from example.tests.model_maker import make_enquiry
from example.base import get_env_variable
from mail.models import (
    Mail,
    Message,
)
from mail.service import (
    init_mail_template,
    queue_mail_message,
    queue_mail_template,
    send_mail,
    TEMPLATE_TYPE_DJANGO,
    TEMPLATE_TYPE_MANDRILL,
)


class TestService(TestCase):

    def _mail(self, enquiry):
        message = Message.objects.get(
            content_type=ContentType.objects.get_for_model(enquiry),
            object_id=enquiry.pk
        )
        return message.mail_set.all()[0]

    def _queue_enquiry(self):
        email_address = get_env_variable('TEST_EMAIL_ADDRESS_1')
        enquiry = make_enquiry(
            email_address,
            "Farming",
            'How many cows in the field?',
        )
        queue_mail_message(
            enquiry,
            [enquiry.email,],
            enquiry.subject,
            enquiry.description,
        )
        return enquiry

    def _create_welcome_template(self):
        welcome_template = init_mail_template(
            'welcome',
            'Welcome...',
            'Available variables {{name}} {{title}} and {{question}}',
            False,
            TEMPLATE_TYPE_DJANGO,
        )
        welcome_template.subject = "Welcome {{name}}"
        welcome_template.description = (
            "Hello {{name}}\n\n"
            "Welcome to the {{title}} group\n\n"
            "We acknowledge your question {{question}}\n\n"
            "We probably won't answer it because we've not written "
            "that bit of code yet\n\n"
            "The {{ title }} team\n"
        )
        welcome_template.save()
        return welcome_template

    def _create_goodbye_template(self):
        goodbye_template = init_mail_template(
            'goodbye',
            'Goodbye...',
            'Available variables *|name|* *|title|* and *|question|*',
            True,
            TEMPLATE_TYPE_MANDRILL,
        )
        goodbye_template.subject = "Goodbye *|name|*"
        goodbye_template.description = (
            "Goodbye *|name|*\n\n"
            "Sorry you are leaving the *|title|* group\n\n"
            "You had a question *|question|* sorry we've not answered it yet\n\n"
            "The *|title|* team\n"
        )
        goodbye_template.save()
        return goodbye_template

    def test_queue_mail(self):
        enquiry = self._queue_enquiry()
        message = Message.objects.get(subject='Farming')
        email_address = get_env_variable('TEST_EMAIL_ADDRESS_1')
        mail = Mail.objects.get(email=email_address)
        self.assertEqual(message, mail.message)
        self.assertEqual(enquiry, message.content_object)

    def test_queue_mail_message(self):
        email_address = get_env_variable('TEST_EMAIL_ADDRESS_2')
        enquiry = make_enquiry(
            email_address,
            "Welcome",
            'Can I join your club?',
        )
        template = self._create_welcome_template()
        content_data = {
            email_address: {
                "name": "Fred",
                "title": "SpaceX",
                "question": enquiry.description
            }
        }
        queue_mail_template(enquiry, template.slug, content_data)
        message = Message.objects.get(subject='Welcome {{name}}')
        mail_item = Mail.objects.get(email=email_address)
        self.assertEqual(message, mail_item.message)
        self.assertEqual(enquiry, mail_item.message.content_object)

    def test_queue_mail_message_and_send_via_mandrill(self):
        email_address = get_env_variable('TEST_EMAIL_ADDRESS_2')
        enquiry = make_enquiry(
            email_address,
            "Welcome",
            'Can I join your club?',
        )
        template = self._create_goodbye_template()
        content_data = {
            email_address: {
                "name": "Fred",
                "title": "SpaceX",
                "question": enquiry.description
            }
        }
        queue_mail_template(enquiry, template.slug, content_data)
        m = self._mail(enquiry)
        self.assertIsNone(m.sent)
        self.assertIsNone(m.sent_response_code)
        self.assertEqual(m.message.subject,'Goodbye *|name|*')
        # test the send facility using djrill mail backend
        temp_email_backend = settings.EMAIL_BACKEND
        settings.EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
        settings.MANDRILL_API_KEY = get_env_variable('TEST_MANDRILL_API_KEY')
        send_mail()
        # self.assertEqual(len(mail.outbox), 1)
        m = self._mail(enquiry)
        self.assertIsNotNone(m.sent)
        self.assertIsNotNone(m.sent_response_code)
        # tidy up!!
        settings.EMAIL_BACKEND = temp_email_backend

    def test_send_mail(self):
        enquiry = self._queue_enquiry()
        m = self._mail(enquiry)
        self.assertIsNone(m.sent)
        send_mail()
        self.assertEqual(len(mail.outbox), 1)
        m = self._mail(enquiry)
        self.assertIsNotNone(m.sent)
