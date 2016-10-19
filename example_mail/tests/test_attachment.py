# -*- encoding: utf-8 -*-
import pytest

from .factories import EnquiryFactory
from mail.tests.factories import AttachmentFactory, MessageFactory


@pytest.mark.django_db
def test_str():
    message = MessageFactory(subject='abc', content_object=EnquiryFactory())
    obj = AttachmentFactory(message=message)
    assert 'abc' == str(obj)
