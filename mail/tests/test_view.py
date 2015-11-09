# -*- encoding: utf-8 -*-
import pytest

from django.core.urlresolvers import reverse
from django.test import TestCase

from login.tests.factories import (
    TEST_PASSWORD,
    UserFactory,
)
from login.tests.scenario import (
    default_scenario_login,
    get_user_staff,
)

from mail.models import MailTemplate


@pytest.mark.django_db
def test_template_create_django(client):
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD)
    url = reverse('mail.template.create.django')
    response = client.post(
        url,
        dict(
            slug='orange',
            subject='123',
            description='ABC',
            title='Testing',
        )
    )
    assert 302 == response.status_code
    template = MailTemplate.objects.get(slug='orange')
    assert 'ABC' == template.description


@pytest.mark.django_db
def test_template_create_mandrill(client):
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD)
    url = reverse('mail.template.create.mandrill')
    response = client.post(
        url,
        dict(
            slug='apple',
            title='Testing',
        )
    )
    assert 302 == response.status_code
    template = MailTemplate.objects.get(slug='apple')
    assert 'Testing' == template.title


@pytest.mark.django_db
def test_template_update_django(client):
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD)
    t = MailTemplate.objects.init_mail_template(
        'hello',
        'Welcome...',
        '',
        False,
        MailTemplate.DJANGO
    )
    url = reverse('mail.template.update.django', kwargs=dict(pk=t.pk))
    response = client.post(
        url,
        dict(
            slug='goodbye',
            subject='123',
            description='ABC',
            title='Testing',
        )
    )
    assert 302 == response.status_code
    with pytest.raises(MailTemplate.DoesNotExist):
        MailTemplate.objects.get(slug='hello')
    template = MailTemplate.objects.get(slug='goodbye')
    assert 'ABC' == template.description


@pytest.mark.django_db
def test_template_update_mandrill(client):
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD)
    t = MailTemplate.objects.init_mail_template(
        'pear',
        'Sorry...',
        '',
        False,
        MailTemplate.MANDRILL
    )
    url = reverse('mail.template.update.django', kwargs=dict(pk=t.pk))
    response = client.post(
        url,
        dict(
            slug='foot',
            title='Duck',
        )
    )
    assert 302 == response.status_code
    with pytest.raises(MailTemplate.DoesNotExist):
        MailTemplate.objects.get(slug='pear')
    template = MailTemplate.objects.get(slug='foot')
    assert 'Duck' == template.title
