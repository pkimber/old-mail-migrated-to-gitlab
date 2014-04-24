# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import logging

from datetime import datetime

from django.conf import settings
from django.core import mail
from django.utils.text import slugify

from django_mailgun import MailgunAPIError

from smtplib import SMTPException

from base.tests.model_maker import clean_and_save

from .models import (
    Mail,
    Message,
    Template,
)


logger = logging.getLogger(__name__)


def _process_mail(primary_keys):
    for pk in primary_keys:
        m = Mail.objects.get(pk=pk)
        try:
            _send_mail(m)
            m.sent = datetime.now()
        except (SMTPException, MailgunAPIError) as e:
            logger.error(e.message)
            retry_count = m.retry_count or 0
            m.retry_count = retry_count + 1
        m.save()


def _send_mail(m):
    """Send message to a list of email addresses."""
    mail.send_mail(
        m.message.subject,
        m.message.description,
        'notify@{}'.format(settings.MAILGUN_SERVER_NAME),
        [m.email,],
        fail_silently=False
    )


def init_app_mail():
    pass


def init_template(slug, title):
    slug=slugify(slug)
    try:
        template = Template.objects.get(slug=slug)
        template.title = title
        template.save()
    except Template.DoesNotExist:
        return clean_and_save(Template(**dict(
            title=title,
            slug=slug,
        )))


def queue_mail(content_object, email_addresses, subject, description):
    """Add a mail message to the models."""
    message = Message(**dict(
        content_object=content_object,
        subject=subject,
        description=description
    ))
    message.save()
    for email in email_addresses:
        mail = Mail(**dict(email=email, message=message))
        mail.save()
    return message


def send_mail():
    primary_keys = [
        e.pk for e in Mail.objects.filter(sent__isnull=True)
    ]
    _process_mail(primary_keys)
