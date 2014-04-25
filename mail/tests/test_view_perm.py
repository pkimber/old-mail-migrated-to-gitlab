# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse

from base.tests.test_utils import PermTestCase
from login.tests.scenario import default_scenario_login

from mail.service import init_mail_template


class TestViewPerm(PermTestCase):

    def setUp(self):
        default_scenario_login()

    def test_message_list(self):
        url = reverse('mail.message.list')
        self.assert_staff_only(url)

    def test_template_list(self):
        url = reverse('mail.template.list')
        self.assert_staff_only(url)

    def test_template_update(self):
        init_mail_template('hello', 'Welcome...', '')
        url = reverse('mail.template.update', kwargs=dict(slug='hello'))
        self.assert_staff_only(url)
