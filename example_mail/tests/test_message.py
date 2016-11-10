# -*- encoding: utf-8 -*-
import pytest

from mail.models import MailTemplate
from mail.tests.factories import MailTemplateFactory, MessageFactory
from .factories import EnquiryFactory


@pytest.mark.django_db
def test_is_mandrill():
    mandrill_template = MailTemplateFactory(
        template_type=MailTemplate.MANDRILL
    )
    message = MessageFactory(
        content_object=EnquiryFactory(),
        template=mandrill_template,
    )
    assert message.is_mandrill is True


@pytest.mark.django_db
def test_is_not_mandrill():
    django_template = MailTemplateFactory(
        template_type=MailTemplate.DJANGO
    )
    message = MessageFactory(
        content_object=EnquiryFactory(),
        template=django_template,
    )
    assert message.is_mandrill is False


@pytest.mark.django_db
def test_is_not_template():
    message = MessageFactory(content_object=EnquiryFactory())
    assert message.is_mandrill is False
