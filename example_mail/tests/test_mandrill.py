# -*- encoding: utf-8 -*-
import pytest

from unittest import mock

# from django.core.mail import EmailMultiAlternatives

from mail.service import _send_mail_mandrill_template
from mail.tests.factories import (
    MailFactory,
    MessageFactory,
)
from .factories import EnquiryFactory


# @mock.patch('django.core.mail.EmailMultiAlternatives')
@pytest.mark.django_db
def test_send_mail_mandrill_template(client, mocker):
    # mock.patch.object('django.core.mail.EmailMultiAlternatives', 'mandrill_response', new_callable=Patrick, create=True)
    # with mock.patch('django.core.mail.message.EmailMultiAlternatives') as mock_mail:
    with mock.patch('django.core.mail.EmailMultiAlternatives') as mock_mail:
        # mock_mail.mandrill_response.return_value = 'abc'
        # mock_mail.return_value.mandrill_response = 'abc'
        mock_mail.return_value.mandrill_response = [{
            "email": "abc@test.com",
            "status": "rejected",
            "_id": "123",
            "reject_reason": "hard-bounce"
        }]
        # mock_mail.mandrill_response.side_effect = 'abc'
        #    #mock_mail.mandrill_response = 'abc'
        #    mock_mail.mandrill_response = [{
        #        "email": "abc@test.com",
        #        "status": "rejected",
        #        "_id": "123",
        #        "reject_reason": "hard-bounce"
        #    }]
        # with mock.patch('django.core.mail.EmailMultiAlternatives') as mock_mail:
        #     #mock_mail.EmailMultiAlternatives.return_value = 'abc'
        #     mock_mail.mandrill_response = 'abc'
        #     #mock_mail.mandrill_response.return_value = [{
        #     #    "email": "abc@test.com",
        #     #    "status": "rejected",
        #     #    "_id": "123",
        #     #    "reject_reason": "hard-bounce"
        #     #}]
        # mock_mail = mock.patch('django.core.mail.EmailMultiAlternatives')
        # mock_mail.mandrill_response = 'abc'
        # mock_mail.mandrill_response.return_value = [{
        #     "email": "abc@test.com",
        #     "status": "rejected",
        #     "_id": "123",
        #     "reject_reason": "hard-bounce"
        # }]
        # mock.patch('django.core.mail.EmailMultiAlternatives')
        #with mock.patch('django.core.mail.EmailMultiAlternatives') as mock_mail:
        #    mock_mail.mandrill_response.return_value = [{
        #        "email": "abc@test.com",
        #        "status": "rejected",
        #        "_id": "123",
        #        "reject_reason": "hard-bounce"
        #    }]
        # temp = mocker.patch('django.core.mail.EmailMultiAlternatives')
        # temp.mandrill_response = 'abx'
        # mocker.patch('stripe.Customer.create')
        # patcher.mandrill_response.return_value = [{
        #     "email": "abc@test.com",
        #     "status": "rejected",
        #     "_id": "123",
        #     "reject_reason": "hard-bounce"
        # }]
        message = MessageFactory(content_object=EnquiryFactory())
        obj = MailFactory(message=message)
        obj = _send_mail_mandrill_template(obj)
