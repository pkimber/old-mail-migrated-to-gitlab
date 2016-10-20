# -*- encoding: utf-8 -*-
import factory

from mail.models import (
    Attachment,
    Mail,
    MailTemplate,
    Message,
    Notify,
)


class MailFactory(factory.django.DjangoModelFactory):
    """

    message = MessageFactory(content_object=EnquiryFactory())
    obj = MailFactory(message=message)

    """

    class Meta:
        model = Mail

    @factory.sequence
    def email(n):
        return 'mail_{:02d}@test.com'.format(n)


class MailTemplateFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = MailTemplate

    @factory.sequence
    def slug(n):
        return 'template_{:02d}'.format(n)


class MessageFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Message

    template = factory.SubFactory(MailTemplateFactory)


class AttachmentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Attachment

    message = factory.SubFactory(MessageFactory)
    document = factory.django.FileField()


class NotifyFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Notify

    @factory.sequence
    def email(n):
        return 'test{}@email.com'.format(n)
