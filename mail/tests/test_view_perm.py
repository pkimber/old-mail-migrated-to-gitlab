# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse

from base.tests.test_utils import PermTestCase
from login.tests.scenario import default_scenario_login

from mail.service import init_mail_template
from mail.models import (
    TEMPLATE_TYPE_DJANGO,
    TEMPLATE_TYPE_MANDRILL,
)


class TestViewPerm(PermTestCase):

    def setUp(self):
        default_scenario_login()

    def test_message_list(self):
        url = reverse('mail.message.list')
        self.assert_staff_only(url)

    def test_template_list(self):
        url = reverse('mail.template.list')
        self.assert_staff_only(url)

    def test_template_create_django(self):
        self.assert_staff_only(reverse('mail.template.create.django'))

    def test_template_create_mandrill(self):
        self.assert_staff_only(reverse('mail.template.create.mandrill'))

    def test_template_update_django(self):
        t = init_mail_template(
            'hello', 'Welcome...', '', False, TEMPLATE_TYPE_DJANGO
        )
        url = reverse('mail.template.update.django', kwargs=dict(pk=t.pk))
        self.assert_staff_only(url)

    def test_template_update_mandrill(self):
        t = init_mail_template(
            'hello', 'Welcome...', '', False, TEMPLATE_TYPE_MANDRILL
        )
        url = reverse('mail.template.update.mandrill', kwargs=dict(pk=t.pk))
        self.assert_staff_only(url)
