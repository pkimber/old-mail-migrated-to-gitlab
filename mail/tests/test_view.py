# -*- encoding: utf-8 -*-
import pytest
from unittest import mock

from django.core.urlresolvers import reverse
from django.conf import settings
from login.tests.factories import (
    TEST_PASSWORD,
    UserFactory,
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
    with mock.patch.multiple(
            settings, MAIL_TEMPLATE_TYPE=MailTemplate.MANDRILL):
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
        assert MailTemplate.MANDRILL == template.template_type


@pytest.mark.django_db
def test_template_create_sparkpost(client):
    with mock.patch.multiple(
            settings, MAIL_TEMPLATE_TYPE=MailTemplate.SPARKPOST):
        user = UserFactory(is_staff=True)
        assert client.login(username=user.username, password=TEST_PASSWORD)
        url = reverse('mail.template.create.sparkpost')
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
        assert MailTemplate.SPARKPOST == template.template_type


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
    url = reverse('mail.template.update.mandrill', kwargs=dict(pk=t.pk))
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


@pytest.mark.django_db
def test_template_update_sparkpost(client):
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD)
    t = MailTemplate.objects.init_mail_template(
        'pear',
        'Sorry...',
        '',
        False,
        MailTemplate.SPARKPOST
    )
    url = reverse('mail.template.update.sparkpost', kwargs=dict(pk=t.pk))
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
