# -*- encoding: utf-8 -*-
import pytest

from unittest import mock

from mail.models import (
    MailError,
    MailTemplate,
)
from mail.service import (
    _mail_process,
    _mail_send,
    _send_mail_mandrill_template,
)
from mail.tests.factories import (
    MailFactory,
    MailTemplateFactory,
    MessageFactory,
)
from .factories import EnquiryFactory


@pytest.mark.django_db
def test_mail_process(settings):
    settings.EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
    with mock.patch('django.core.mail.EmailMultiAlternatives') as mock_mail:
        mock_mail.return_value.mandrill_response = [{
            "email": "abc@test.com",
            "status": "sent",
            "_id": "123",
            "reject_reason": None,
        }]
        template = MailTemplateFactory(template_type=MailTemplate.MANDRILL)
        message = MessageFactory(
            template=template,
            content_object=EnquiryFactory(),
        )
        m1 = MailFactory(message=message)
        m2 = MailFactory(message=message, retry_count=9)
        m3 = MailFactory(message=message, retry_count=11)
        m4 = MailFactory(message=message)
        m5 = MailFactory(message=message, retry_count=0)
        m6 = MailFactory(message=message, retry_count=1)
        m7 = MailFactory(message=message, retry_count=99)
        sent = _mail_process()
        assert [m1.pk, m2.pk, m4.pk, m5.pk, m6.pk] == sent


@pytest.mark.django_db
def test_mail_send_rejected():
    with mock.patch('django.core.mail.EmailMultiAlternatives') as mock_mail:
        mock_mail.return_value.mandrill_response = [{
            "email": "abc@test.com",
            "status": "rejected",
            "_id": "123",
            "reject_reason": "hard-bounce"
        }]
        template = MailTemplateFactory(template_type=MailTemplate.MANDRILL)
        message = MessageFactory(
            template=template,
            content_object=EnquiryFactory(),
        )
        obj = MailFactory(message=message)
        _mail_send([obj.pk])
        obj.refresh_from_db()
        assert 1 == obj.retry_count


@pytest.mark.django_db
def test_send_mail_mandrill_template_rejected():
    with mock.patch('django.core.mail.EmailMultiAlternatives') as mock_mail:
        mock_mail.return_value.mandrill_response = [{
            "email": "abc@test.com",
            "status": "rejected",
            "_id": "123",
            "reject_reason": "hard-bounce"
        }]
        message = MessageFactory(content_object=EnquiryFactory())
        obj = MailFactory(message=message)
        with pytest.raises(MailError) as e:
            _send_mail_mandrill_template(obj)
        msg = str(e.value)
        assert 'Failed to send mail' in msg
        assert '[abc@test.com]' in msg
        assert '[hard-bounce]' in msg
