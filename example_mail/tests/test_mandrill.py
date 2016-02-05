# -*- encoding: utf-8 -*-
import pytest

from unittest import mock

from mail.models import (
    MailError,
    MailTemplate,
)
from mail.service import (
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
def test_mail_process():
    pass


@pytest.mark.django_db
def test_mail_send():
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
def test_send_mail_mandrill_template():
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
