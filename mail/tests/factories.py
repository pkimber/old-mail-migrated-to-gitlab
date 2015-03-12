# -*- encoding: utf-8 -*-
import factory

from mail.models import (
    MailTemplate,
    Message,
    Notify,
)


class MailTemplateFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = MailTemplate

    @factory.sequence
    def slug(n):
        return 'template_{:02d}'.format(n)


class MessageFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Message


class NotifyFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Notify

    @factory.sequence
    def email(n):
        return 'test{}@email.com'.format(n)
