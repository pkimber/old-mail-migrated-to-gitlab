# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.test import TestCase

from example.tests.model_maker import make_enquiry
from mail.models import (
    Mail,
    Message,
)
from mail.service import queue_mail


class TestService(TestCase):

    def test_queue_mail(self):
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
        message = Message.objects.get(subject='Farming')
        mail = Mail.objects.get(email='test@pkimber.net')
        self.assertEqual(message, mail.message)
        self.assertEqual(enquiry, message.content_object)
