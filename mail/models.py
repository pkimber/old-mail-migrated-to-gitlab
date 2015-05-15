# -*- encoding: utf-8 -*-
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


class MailTemplateManager(models.Manager):

    def create_mail_template(
            self, slug, title, help_text, is_html, template_type,
            subject=None, description=None, is_system=None):
        obj = self.model(
            title=title,
            slug=slug,
            help_text=help_text,
            is_html=is_html,
            is_system=is_system or False,
            template_type=template_type,
            subject=subject or '',
            description=description or '',
        )
        obj.save()
        return obj

    def init_mail_template(
            self, slug, title, help_text, is_html, template_type,
            subject=None, description=None, is_system=None):
        try:
            obj = self.model.objects.get(slug=slug)
            obj.title = title
            obj.help_text = help_text
            obj.is_html = is_html
            obj.is_system = is_system or False
            obj.template_type = template_type
            obj.subject = subject or ''
            obj.description = description or ''
            obj.save()
        except self.model.DoesNotExist:
            obj = self.create_mail_template(
                slug, title, help_text, is_html, template_type,
                subject, description, is_system
            )
        return obj


class MailTemplate(TimeStampedModel):
    """email template.

    The 'description' should include details of the available context
    variables.

    If this is a Mandrill template, then we will ignore the description and
    use the slug to lookup the template name using the API.

    If this is a system template, then the user should not be allowed to edit
    it.
    """

    DJANGO = 'django'
    MANDRILL = 'mandrill'

    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=100)
    help_text = models.TextField(blank=True)
    is_html = models.BooleanField(default=False)
    is_system = models.BooleanField(default=False)
    template_type = models.CharField(max_length=32, default=DJANGO)
    subject = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    objects = MailTemplateManager()

    class Meta:
        ordering = ('title',)
        verbose_name = 'Template'
        verbose_name_plural = 'Template'

    @property
    def is_mandrill(self):
        return self.template_type == self.MANDRILL

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
        ordering = ['mail', 'key']
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
