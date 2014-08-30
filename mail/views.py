# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
)

from braces.views import (
    LoginRequiredMixin,
    StaffuserRequiredMixin,
)

from base.view_utils import BaseMixin

from .forms import (
    MailTemplateCreateDjangoForm,
    MailTemplateCreateMandrillForm,
    MailTemplateUpdateDjangoForm,
    MailTemplateUpdateMandrillForm,
)
from .models import (
    Message,
    MailTemplate,
    TEMPLATE_TYPE_DJANGO,
    TEMPLATE_TYPE_MANDRILL,
)


class MailTemplateCreateDjangoView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    form_class = MailTemplateCreateDjangoForm
    model = MailTemplate
    template_name = 'mail/mailtemplate_create_django_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.template_type = TEMPLATE_TYPE_DJANGO
        return super(MailTemplateCreateDjangoView, self).form_valid(form)

    def get_success_url(self):
        return reverse('mail.template.list')


class MailTemplateCreateMandrillView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    form_class = MailTemplateCreateMandrillForm
    model = MailTemplate
    template_name = 'mail/mailtemplate_create_mandrill_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.template_type = TEMPLATE_TYPE_MANDRILL
        return super(MailTemplateCreateMandrillView, self).form_valid(form)

    def get_success_url(self):
        return reverse('mail.template.list')



class MailTemplateListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    model = MailTemplate


class MailTemplateUpdateDjangoView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = MailTemplateUpdateDjangoForm
    model = MailTemplate
    template_name = 'mail/mailtemplate_update_django_form.html'

    def get_success_url(self):
        return reverse('mail.template.list')


class MailTemplateUpdateMandrillView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = MailTemplateUpdateMandrillForm
    model = MailTemplate
    template_name = 'mail/mailtemplate_update_mandrill_form.html'

    def get_success_url(self):
        return reverse('mail.template.list')


class MessageListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    model = Message
    paginate_by = 10
