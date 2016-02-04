# -*- encoding: utf-8 -*-
import pytest

from unittest import mock

from mail.models import MailError
from mail.service import _send_mail_mandrill_template
from mail.tests.factories import (
    MailFactory,
    MessageFactory,
)
from .factories import EnquiryFactory


@pytest.mark.django_db
def test_send_mail_mandrill_template(client, mocker):
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
        assert 'Failed to send message' in str(e.value)
