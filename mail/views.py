# -*- encoding: utf-8 -*-
from django.conf import settings
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
    MailTemplateCreateRemoteForm,
    MailTemplateUpdateDjangoForm,
    MailTemplateUpdateRemoteForm,
)
from .models import (
    Message,
    MailTemplate,
)


def _get_remote_template_type():
    if settings.MAIL_TEMPLATE_TYPE:
        template_type = settings.MAIL_TEMPLATE_TYPE
    elif settings.SPARKPOST_API_KEY:
        template_type = MailTemplate.SPARKPOST
    elif settings.MANDRILL_API_KEY:
        template_type = MailTemplate.MANDRILL
    else:
        template_type = MailTemplate.DJANGO
    return template_type


class MailTemplateCreateDjangoView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    form_class = MailTemplateCreateDjangoForm
    model = MailTemplate
    template_name = 'mail/mailtemplate_create_django_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.template_type = MailTemplate.DJANGO
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mail.template.list')


class MailTemplateCreateRemoteView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    form_class = MailTemplateCreateRemoteForm
    model = MailTemplate
    template_name = 'mail/mailtemplate_create_remote_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.template_type = _get_remote_template_type()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mail.template.list')


class MailTemplateListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    model = MailTemplate

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        template_type = _get_remote_template_type()

        context.update({'template_type': template_type})
        return context


class MailTemplateUpdateDjangoView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = MailTemplateUpdateDjangoForm
    model = MailTemplate
    template_name = 'mail/mailtemplate_update_django_form.html'

    def get_success_url(self):
        return reverse('mail.template.list')


class MailTemplateUpdateRemoteView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = MailTemplateUpdateRemoteForm
    model = MailTemplate
    template_name = 'mail/mailtemplate_update_remote_form.html'

    def get_success_url(self):
        return reverse('mail.template.list')


class MessageListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    model = Message
    paginate_by = 10
