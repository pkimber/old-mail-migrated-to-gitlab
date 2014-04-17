# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import logging
from datetime import datetime

from smtplib import SMTPException

from django.conf import settings
from django.core import mail
from django.core.management.base import BaseCommand

from django_mailgun import MailgunAPIError

from mail.models import Mail

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = "Send mail messages."

    def _process(self, primary_keys, emails):
        for pk in primary_keys:
            enquiry = Enquiry.objects.get(pk=pk)
            try:
                self._send_email(enquiry, emails)
                enquiry.email_sent = datetime.now()
            except (SMTPException, MailgunAPIError) as e:
                logger.error(e.message)
                retry_count = enquiry.retry_count or 0
                enquiry.retry_count = retry_count + 1
            enquiry.save()

    def _send_email(self, enquiry, emails):
        """Send enquiry notification to a list of email addresses."""
        mail.send_mail(
            'Enquiry from {}'.format(enquiry.name),
            enquiry.description,
            'notify@{}'.format(settings.MAILGUN_SERVER_NAME),
            emails,
            fail_silently=False
        )

    def handle(self, *args, **options):
        pks = [e.pk for e in Enquiry.objects.filter(email_sent__isnull=True)]
        self._process(pks, emails)
