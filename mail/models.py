# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models

import reversion

from base.model_utils import TimeStampedModel


TEMPLATE_TYPE_DJANGO = 'django'
TEMPLATE_TYPE_MANDRILL = 'mandrill'


class MailError(Exception):

    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return repr('%s, %s' % (self.__class__.__name__, self.value))


class MailTemplate(TimeStampedModel):
    """email template.

    The 'description' should include details of the available context
    variables.

    If this is a Mandrill template, then we will ignore the description and
    use the slug to lookup the template name using the API.
    """

    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=100)
    help_text = models.TextField(blank=True)
    is_html = models.BooleanField(default=False)
    template_type = models.CharField(max_length=32, default=TEMPLATE_TYPE_DJANGO)
    subject = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Template'
        verbose_name_plural = 'Template'

    @property
    def is_mandrill(self):
        return self.template_type == TEMPLATE_TYPE_MANDRILL

    def __str__(self):
        return '{}'.format(self.title)

reversion.register(MailTemplate)


class Message(TimeStampedModel):
    """the actual mail message - one or more email addresses attached.

    If the template is blank, the subject and description will be sent as
    they are.

    If the template is not blank, the message will be rendered using the
    template.
    """

    subject = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_html = models.BooleanField(default=False)
    template = models.ForeignKey(MailTemplate, blank=True, null=True)
    # link to the object in the system which asked us to send the email.
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    class Meta:
        ordering = ['-created']
        verbose_name = 'Mail message'
        verbose_name_plural = 'Mail messages'

    def __str__(self):
        return '{}'.format(self.subject)

    @property
    def is_mandrill(self):
        return self.template and self.template.is_mandrill

reversion.register(Message)


class Mail(TimeStampedModel):
    """email messages to send."""

    message = models.ForeignKey(Message)
    email = models.EmailField(blank=True)
    retry_count = models.IntegerField(blank=True, null=True)
    sent = models.DateTimeField(blank=True, null=True)
    sent_response_code = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        ordering = ['created']
        verbose_name = 'Mail detail'
        verbose_name_plural = 'Mail detail'

    def __str__(self):
        return '{}: {}'.format(
            self.email,
            self.message.subject,
        )

reversion.register(Mail)


class MailField(models.Model):
    """key, value store for each email."""

    mail = models.ForeignKey(Mail)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=256)

    class Meta:
        verbose_name = 'Mail field'
        verbose_name_plural = 'Mail fields'

    def __str__(self):
        return '{}: {}'.format(
            self.mail.email,
            self.key
        )

reversion.register(MailField)


class Notify(TimeStampedModel):
    """List of people to notify on an event e.g. enquiry or payment."""

    email = models.EmailField()

    def __str__(self):
        return '{}'.format(self.email)

reversion.register(Notify)
