# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import (
    ListView,
    UpdateView,
)

from braces.views import (
    LoginRequiredMixin,
    StaffuserRequiredMixin,
)

from base.view_utils import BaseMixin

from .forms import MailTemplateForm
from .models import (
    Message,
    MailTemplate,
)


class MailTemplateListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    model = MailTemplate


class MailTemplateUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = MailTemplateForm
    model = MailTemplate

    def get_success_url(self):
        return reverse('mail.template.list')


class MessageListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    model = Message
