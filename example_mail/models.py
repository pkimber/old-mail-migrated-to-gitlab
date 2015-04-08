# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from base.model_utils import TimeStampedModel


class Enquiry(TimeStampedModel):

    email = models.EmailField()
    subject = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        ordering = ['-created']
        verbose_name = 'Enquiry'
        verbose_name_plural = 'Enquiries'

    def __str__(self):
        return '{}: {}'.format(
            self.email,
            self.subject,
        )
