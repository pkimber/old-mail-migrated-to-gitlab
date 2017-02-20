# -*- encoding: utf-8 -*-
import pytest

from django.test import TestCase

from mail.models import MailTemplate
from mail.service import _mail_template_render


@pytest.mark.django_db
def test_init_template():
    MailTemplate.objects.init_mail_template(
        'hello',
        'Welcome to our mailing list.',
        "You can add the {{ name }} variable to this template.",
        False,
        MailTemplate.MANDRILL,
    )


@pytest.mark.django_db
def test_init_template_update():
    MailTemplate.objects.init_mail_template(
        'hello',
        'Welcome to our mailing list.',
        '',
        False,
        MailTemplate.DJANGO,
        subject='a',
        description='b',
    )
    template = MailTemplate.objects.get(slug='hello')
    assert 'a' == template.subject
    assert 'b' == template.description
    MailTemplate.objects.init_mail_template(
        'hello',
        'Welcome...',
        '',
        False,
        MailTemplate.DJANGO,
        subject='c',
        description='d',
    )
    template = MailTemplate.objects.get(slug='hello')
    assert 'Welcome...' == template.title
    assert 'a' == template.subject
    assert 'b' == template.description


@pytest.mark.django_db
def test_render():
    template = MailTemplate.objects.init_mail_template(
        'hello',
        'Welcome to our mailing list.',
        (
            "You can add the following variables to the template:\n"
            "{{ name }} name of the customer.\n"
            "{{ title }} name of the village.",
        ),
        False,
        MailTemplate.DJANGO,
    )
    template.subject = 'Hello {{ name }}'
    template.description = 'Welcome to {{ title }}'
    template.save()
    subject, description = _mail_template_render(
        'hello', dict(name='Patrick', title='Hatherleigh')
    )
    assert 'Hello Patrick' == subject
    assert 'Welcome to Hatherleigh' == description
