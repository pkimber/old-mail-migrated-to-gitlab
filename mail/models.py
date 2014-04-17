# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models

import reversion

from base.model_utils import TimeStampedModel


class MailError(Exception):

    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return repr('%s, %s' % (self.__class__.__name__, self.value))


class Message(TimeStampedModel):
    """email messages to send."""

    subject = models.CharField(max_length=200)
    description = models.TextField()
    # link to the object in the system which asked us to send the email.
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    class Meta:
        ordering = ['created']
        unique_together = ('object_id', 'content_type')
        verbose_name = 'Mail message'
        verbose_name_plural = 'Mail messages'

    def __str__(self):
        return '{}'.format(self.subject)

reversion.register(Message)


class Mail(TimeStampedModel):
    """email messages to send."""

    message = models.ForeignKey(Message)
    email = models.EmailField(blank=True)
    retry_count = models.IntegerField(blank=True, null=True)
    sent = models.DateTimeField(blank=True, null=True)

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
