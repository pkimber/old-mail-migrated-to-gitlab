# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.test import TestCase


class TestView(TestCase):

    def test_project_home(self):
        response = self.client.get(reverse('project.home'))
        self.assertEqual(response.status_code, 200)
