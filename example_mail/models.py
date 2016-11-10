# -*- encoding: utf-8 -*-
from django.db import models

from base.model_utils import TimeStampedModel


class Enquiry(TimeStampedModel):

    email = models.EmailField()
    subject = models.CharField(max_length=100)
    description = models.TextField()
    document = models.FileField(blank=True, null=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Enquiry'
        verbose_name_plural = 'Enquiries'

    def __str__(self):
        return '{}: {}'.format(
            self.email,
            self.subject,
        )
