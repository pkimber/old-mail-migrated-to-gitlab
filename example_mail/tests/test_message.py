# -*- encoding: utf-8 -*-
from django.test import TestCase

from .factories import EnquiryFactory
from mail.models import MailTemplate
from mail.tests.factories import (
    MailTemplateFactory,
    MessageFactory,
)


class TestMessage(TestCase):

    def test_is_mandrill(self):
        mandrill_template = MailTemplateFactory(
            template_type=MailTemplate.MANDRILL
        )
        message = MessageFactory(
            content_object=EnquiryFactory(),
            template=mandrill_template,
        )
        self.assertTrue(message.is_mandrill)

    def test_is_not_mandrill(self):
        django_template = MailTemplateFactory(
            template_type=MailTemplate.DJANGO
        )
        message = MessageFactory(
            content_object=EnquiryFactory(),
            template=django_template,
        )
        self.assertFalse(message.is_mandrill)

    def test_is_sparkpost(self):
        mandrill_template = MailTemplateFactory(
            template_type=MailTemplate.SPARKPOST
        )
        message = MessageFactory(
            content_object=EnquiryFactory(),
            template=mandrill_template,
        )
        self.assertTrue(message.is_sparkpost)

    def test_is_not_sparkpost(self):
        django_template = MailTemplateFactory(
            template_type=MailTemplate.DJANGO
        )
        message = MessageFactory(
            content_object=EnquiryFactory(),
            template=django_template,
        )
        self.assertFalse(message.is_sparkpost)

    def test_is_not_template(self):
        message = MessageFactory(content_object=EnquiryFactory())
        self.assertFalse(message.is_mandrill)
        self.assertFalse(message.is_sparkpost)
