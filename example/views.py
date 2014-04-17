# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import ListView

from mail.models import Message


class HomeView(ListView):

    model = Message
    template_name = 'example/home.html'
