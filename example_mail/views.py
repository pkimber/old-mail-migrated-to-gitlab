# -*- encoding: utf-8 -*-
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from django.core.urlresolvers import reverse
from django.db import transaction
from django.views.generic import CreateView, ListView, TemplateView

from base.view_utils import BaseMixin
from mail.models import Message
from mail.service import queue_mail_message, queue_mail_template
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
    template_name = 'example_mail/enquiry_form.html'

    def form_valid(self, form):
        selection = form.cleaned_data['send_email']
        use_template = selection == 'template'
        with transaction.atomic():
            result = super().form_valid(form)
            if use_template:
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
            else:
                attachments = []
                if self.object.document:
                    attachments.append(self.object.document.file.name)
                queue_mail_message(
                    self.object,
                    [self.object.email],
                    self.object.subject,
                    self.object.description,
                    attachments=attachments,
                )
            transaction.on_commit(lambda: process_mail.delay())
            return result

    def get_success_url(self):
        return reverse('example.enquiry.list')


class EnquiryListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    model = Enquiry
    template_name = 'example_mail/enquiry_list.html'


class SettingsView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, TemplateView):

    model = Message
    template_name = 'example_mail/settings.html'
