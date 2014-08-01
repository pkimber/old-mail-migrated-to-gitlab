# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import factory

from mail.models import (
    MailTemplate,
    Message,
)


class MailTemplateFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = MailTemplate


class MessageFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Message
