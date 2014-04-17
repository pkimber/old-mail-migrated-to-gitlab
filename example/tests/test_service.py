# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

from example.tests.model_maker import make_enquiry
from mail.models import (
    Mail,
    Message,
)
from mail.service import (
    queue_mail,
    send_mail,
)


class TestService(TestCase):

    def _mail(self, enquiry):
        message = Message.objects.get(
            content_type=ContentType.objects.get_for_model(enquiry),
            object_id=enquiry.pk
        )
        return message.mail_set.all()[0]

    def _queue_enquiry(self):
        enquiry = make_enquiry(
            'test@pkimber.net',
            'Farming',
            'How many cows in the field?',
        )
        queue_mail(
            enquiry,
            [enquiry.email,],
            enquiry.subject,
            enquiry.description,
        )
        return enquiry

    def test_queue_mail(self):
        enquiry = self._queue_enquiry()
        message = Message.objects.get(subject='Farming')
        mail = Mail.objects.get(email='test@pkimber.net')
        self.assertEqual(message, mail.message)
        self.assertEqual(enquiry, message.content_object)

    def test_send_mail(self):
        enquiry = self._queue_enquiry()
        m = self._mail(enquiry)
        self.assertIsNone(m.sent)
        send_mail()
        self.assertEqual(len(mail.outbox), 1)
        m = self._mail(enquiry)
        self.assertIsNotNone(m.sent)
