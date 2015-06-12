# -*- encoding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase

from login.tests.factories import TEST_PASSWORD
from login.tests.scenario import (
    default_scenario_login,
    get_user_staff,
)

from mail.models import MailTemplate


class TestView(TestCase):

    def setUp(self):
        default_scenario_login()
        staff = get_user_staff()
        self.assertTrue(
            self.client.login(username=staff.username, password=TEST_PASSWORD)
        )

    def test_template_update_django(self):
        t = MailTemplate.objects.init_mail_template(
            'hello',
            'Welcome...',
            '',
            False,
            MailTemplate.DJANGO
        )
        url = reverse('mail.template.update.django', kwargs=dict(pk=t.pk))
        response = self.client.post(
            url,
            dict(
                slug='goodbye',
                subject='123',
                description='ABC',
                title='Testing',
            )
        )
        self.assertEqual(response.status_code, 302)
        template = MailTemplate.objects.get(slug='goodbye')
        self.assertEqual('ABC', template.description)
