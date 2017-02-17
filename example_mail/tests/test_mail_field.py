# -*- encoding: utf-8 -*-
import json
import pytest

from mail.models import MailField
from mail.tests.factories import MailFactory, MailFieldFactory, MessageFactory
from .factories import EnquiryFactory


@pytest.mark.django_db
def test_data():
    message = MessageFactory(content_object=EnquiryFactory())
    mail = MailFactory(message=message)
    obj = MailFieldFactory(mail=mail, value='xyz')
    assert isinstance(obj.data, str)
    assert 'xyz' == obj.data


@pytest.mark.django_db
def test_data_dict():
    message = MessageFactory(content_object=EnquiryFactory())
    mail = MailFactory(message=message)
    obj = MailFieldFactory(
        mail=mail,
        is_json=True,
        value=json.dumps({'age': 52})
    )
    assert isinstance(obj.data, dict)
    assert {'age': 52 == obj.data}


@pytest.mark.django_db
def test_factory():
    message = MessageFactory(content_object=EnquiryFactory())
    mail = MailFactory(message=message)
    obj = MailFieldFactory(mail=mail)
