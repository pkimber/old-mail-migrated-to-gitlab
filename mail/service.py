# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from .models import (
    Mail,
    Message,
)


def init_app_mail():
    pass


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
