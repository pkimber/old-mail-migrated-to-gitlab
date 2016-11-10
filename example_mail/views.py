# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import transaction
from django.views.generic import (
    CreateView,
    ListView,
    TemplateView,
)

from braces.views import (
    LoginRequiredMixin,
    StaffuserRequiredMixin,
)

from base.view_utils import BaseMixin

from mail.models import Message
from mail.service import queue_mail_template
from mail.tasks import process_mail

from .forms import EnquiryForm
from .models import Enquiry


class HomeView(ListView):

    model = Message
    template_name = 'example_mail/home.html'


class EnquiryCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    form_class = EnquiryForm
    model = Enquiry

    def form_valid(self, form):
        with transaction.atomic():
            result = super(EnquiryCreateView, self).form_valid(form)
            context = {
                self.object.email: {
                    "SUBJECT": "Re: " + self.object.subject,
                    "BODY": self.object.description,
                    "DATE": self.object.created.strftime("%d-%b-%Y %H:%M:%S"),
                },
            }
            queue_mail_template(
                self.object,
                'enquiry_acknowledgement',
                context,
            )
            process_mail.delay()
            return result

    def get_success_url(self):
        return reverse('example.enquiry.list')


class EnquiryListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    model = Enquiry


class SettingsView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, TemplateView):

    model = Message
    template_name = 'example_mail/settings.html'
