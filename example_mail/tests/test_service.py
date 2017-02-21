# -*- encoding: utf-8 -*-
import filecmp
import json
import os
import pytest

from django.contrib.contenttypes.models import ContentType
from django.core import mail
from unittest import mock

from example_mail.base import get_env_variable
from example_mail.tests.model_maker import make_enquiry
from mail.models import Mail, MailError, MailField, MailTemplate, Message
from mail.service import (
    _can_use_debug_console,
    _can_use_mailgun,
    _can_use_smtp,
    queue_mail_message,
    queue_mail_template,
    send_mail,
)


def _mail(enquiry):
    message = Message.objects.get(
        content_type=ContentType.objects.get_for_model(enquiry),
        object_id=enquiry.pk
    )
    return message.mail_set.all()[0]


def _queue_enquiry(attachments=None):
    if not attachments:
        attachments = []
    email_address = get_env_variable('TEST_EMAIL_ADDRESS_1')
    enquiry = make_enquiry(
        email_address,
        "Farming",
        'How many cows in the field?',
    )
    queue_mail_message(
        enquiry,
        [enquiry.email, ],
        enquiry.subject,
        enquiry.description,
        attachments=attachments,
    )
    return enquiry


def _create_welcome_template():
    welcome_template = MailTemplate.objects.init_mail_template(
        'welcome',
        'Welcome...',
        'Available variables {{name}} {{title}} and {{question}}',
        False,
        MailTemplate.DJANGO,
    )
    welcome_template.subject = "Welcome {{name}}"
    welcome_template.description = (
        "Hello {{name}}\n\n"
        "Welcome to the {{title}} group\n\n"
        "We acknowledge your question {{question}}\n\n"
        "We probably won't answer it because we've not written "
        "that bit of code yet\n\n"
        "The {{ title }} team\n"
    )
    welcome_template.save()
    return welcome_template


def _create_goodbye_mandrill_template():
    goodbye_template = MailTemplate.objects.init_mail_template(
        'goodbye',
        'Goodbye...',
        'Available variables *|name|* *|title|* and *|question|*',
        True,
        MailTemplate.MANDRILL,
    )
    goodbye_template.subject = "Goodbye *|name|*"
    goodbye_template.description = (
        "Goodbye *|name|*\n\n"
        "Sorry you are leaving the *|title|* group\n\n"
        "You had a question *|question|* sorry we've not answered it yet\n\n"
        "The *|title|* team\n"
    )
    goodbye_template.save()
    return goodbye_template


def _create_goodbye_sparkpost_template():
    goodbye_template = MailTemplate.objects.init_mail_template(
        'goodbye-sparkpost',
        'Goodbye...',
        'Available variables {{name}} {{title}} and {{question}}',
        True,
        MailTemplate.SPARKPOST,
    )
    goodbye_template.subject = "Goodbye {{name}}"
    goodbye_template.description = (
        "Goodbye {{name}}\n\n"
        "Sorry you are leaving the {{title}} group\n\n"
        "You had a question {{question}} sorry we've not answered it yet\n\n"
        "The {{title}} team\n"
    )
    goodbye_template.save()
    return goodbye_template


@pytest.mark.django_db
def test_can_use_debug_console(settings):
    settings.DEBUG = True
    settings.EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    assert _can_use_debug_console() is True


@pytest.mark.django_db
def test_can_use_debug_console_not(settings):
    settings.DEBUG = False
    assert _can_use_debug_console() is False


@pytest.mark.django_db
def test_can_use_mailgun(settings):
    settings.EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
    assert _can_use_mailgun() is True


@pytest.mark.django_db
def test_can_use_mailgun_not(settings):
    settings.EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    assert _can_use_mailgun() is False


@pytest.mark.django_db
def test_can_use_smtp(settings):
    settings.EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    assert _can_use_smtp() is True


@pytest.mark.django_db
def test_queue_mail():
    enquiry = _queue_enquiry()
    message = Message.objects.get(subject='Farming')
    email_address = get_env_variable('TEST_EMAIL_ADDRESS_1')
    mail = Mail.objects.get(email=email_address)
    assert message == mail.message
    assert enquiry == message.content_object


@pytest.mark.django_db
def test_queue_mail_with_attachment():
    file_name = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'data',
        'sample.odt',
    )
    enquiry = _queue_enquiry([file_name])
    message = Message.objects.get(subject='Farming')
    email_address = get_env_variable('TEST_EMAIL_ADDRESS_1')
    mail = Mail.objects.get(email=email_address)
    assert message == mail.message
    assert enquiry == message.content_object
    assert 1 == message.attachments().count()
    assert filecmp.cmp(
        file_name,
        message.attachments().first().document.file.name,
        shallow=False
    ) is True


@pytest.mark.django_db
def test_queue_mail_message():
    email_address = get_env_variable('TEST_EMAIL_ADDRESS_2')
    if not email_address:
        raise MailError("Cannot test without a 'TEST_EMAIL_ADDRESS_2'")
    enquiry = make_enquiry(
        email_address,
        "Welcome",
        'Can I join your club?',
    )
    template = _create_welcome_template()
    content_data = {
        email_address: {
            "name": "Fred",
            "title": "SpaceX",
            "question": enquiry.description,
            "dict": {'age': 52, 'colour': 'blue'},
            "list": [1, 3, 9],
        }
    }
    queue_mail_template(enquiry, template.slug, content_data)
    message = Message.objects.get(subject='Welcome {{name}}')
    mail_item = Mail.objects.get(email=email_address)
    assert message == mail_item.message
    assert enquiry == mail_item.message.content_object
    # name
    obj = MailField.objects.get(key='name')
    assert 'Fred' == obj.value
    assert obj.is_json is False
    # dict
    obj = MailField.objects.get(key='dict')
    assert obj.is_json is True
    assert {'age': 52, 'colour': 'blue'} == json.loads(obj.value)
    # list
    obj = MailField.objects.get(key='list')
    assert obj.is_json is True
    assert [1, 3, 9] == json.loads(obj.value)


@pytest.mark.django_db
def test_queue_mail_message_and_send_via_mandrill(settings):
    settings.EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
    with mock.patch('django.core.mail.EmailMultiAlternatives') as mock_mail:
        mock_mail.return_value.mandrill_response = [{
            "email": "abc@test.com",
            "status": "sent",
            "_id": "123",
            "reject_reason": None,
        }]
        email_address = get_env_variable('TEST_EMAIL_ADDRESS_2')
        enquiry = make_enquiry(
            email_address,
            "Welcome",
            'Can I join your club?',
        )
        template = _create_goodbye_mandrill_template()
        content_data = {
            email_address: {
                "name": "Fred",
                "title": "SpaceX",
                "question": enquiry.description
            }
        }
        queue_mail_template(enquiry, template.slug, content_data)
        m = _mail(enquiry)
        assert m.sent is None
        assert m.sent_response_code is None
        assert m.message.subject == 'Goodbye *|name|*'
        # test the send facility using djrill mail backend
        # temp_email_backend = settings.EMAIL_BACKEND
        send_mail()
        m = _mail(enquiry)
        assert m.sent is not None
        assert m.sent_response_code is not None


@pytest.mark.django_db
def test_queue_no_email():
    email_address = get_env_variable('TEST_EMAIL_ADDRESS_1')
    enquiry = make_enquiry(
        email_address,
        "Farming",
        'How many cows in the field?',
    )
    with pytest.raises(MailError) as e:
        queue_mail_message(
            enquiry,
            [],
            enquiry.subject,
            enquiry.description,
        )
    expect = "Cannot 'queue_mail_message' without 'email_addresses'"
    assert expect in str(e.value)


@pytest.mark.django_db
def test_send_mail():
    enquiry = _queue_enquiry()
    m = _mail(enquiry)
    assert m.sent is None
    send_mail()
    assert 1 == len(mail.outbox)
    m = _mail(enquiry)
    assert m.sent is not None
