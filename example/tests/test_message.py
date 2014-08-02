# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from .factories import EnquiryFactory
from mail.models import (
    TEMPLATE_TYPE_DJANGO,
    TEMPLATE_TYPE_MANDRILL,
)
from mail.tests.factories import (
    MailTemplateFactory,
    MessageFactory,
)


class TestMessage(TestCase):

    def test_is_mandrill(self):
        mandrill_template = MailTemplateFactory(
            template_type=TEMPLATE_TYPE_MANDRILL
        )
        message = MessageFactory(
            content_object=EnquiryFactory(),
            template=mandrill_template,
        )
        self.assertTrue(message.is_mandrill)

    def test_is_not_mandrill(self):
        django_template = MailTemplateFactory(
            template_type=TEMPLATE_TYPE_DJANGO
        )
        message = MessageFactory(
            content_object=EnquiryFactory(),
            template=django_template,
        )
        self.assertFalse(message.is_mandrill)

    def test_is_not_template(self):
        message = MessageFactory(content_object=EnquiryFactory())
        self.assertFalse(message.is_mandrill)
