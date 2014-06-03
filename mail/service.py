# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import logging

from datetime import datetime

from django.conf import settings
from django.core import mail
from django.db import transaction
from django.template import (
    Context,
    Template,
)
from django.utils.text import slugify

from django_mailgun import MailgunAPIError

from djrill import MandrillAPIError

from smtplib import SMTPException

from base.tests.model_maker import clean_and_save

from .models import (
    Mail,
    MailField,
    MailTemplate,
    Message,
    TEMPLATE_TYPE_DJANGO,
    TEMPLATE_TYPE_MANDRILL,
)


logger = logging.getLogger(__name__)


def _get_merge_vars(mail_item):
    return dict(
        [ (mf.key, mf.value) for mf in mail_item.mailfield_set.all()]
    )


def _process_mail(primary_keys):
    for pk in primary_keys:
        m = Mail.objects.get(pk=pk)
        try:
            _send_django_format_message(m)
            m.sent = datetime.now()
        except (SMTPException, MailgunAPIError) as e:
            logger.error(e.message)
            retry_count = m.retry_count or 0
            m.retry_count = retry_count + 1
        m.save()


def _render(text, context):
    t = Template(text)
    c = Context(context)
    return t.render(c)


def _send_django_format_mail():
    primary_keys = [
        e.pk for e in Mail.objects.filter(
            sent__isnull=True,
            message__template_type=TEMPLATE_TYPE_DJANGO,
        )
    ]

    print ("Message IDs:" + str(primary_keys))
    _process_mail(primary_keys)


def _send_mandrill_format_mail():
    primary_keys = []
    last_id = 0

    # get a list of message - Have to use this convoluted method because
    # sqlite does not support select distinct
    for mail_item in Mail.objects.filter(
            sent__isnull=True,
            message__template_type=TEMPLATE_TYPE_MANDRILL
        ).order_by('message'):
        if (last_id != mail_item.message.pk):
            primary_keys.append(mail_item.message.pk)
            last_id = mail_item.message.pk

    print ("Message IDs: " + str(primary_keys))
    for pk in primary_keys:
        m = Message.objects.get(pk=pk)
        _send_mandrill_format_message(m)

def _send_django_format_message(m):
    """Send message to a list of email addresses."""
    #print ("Doing send_django_format_mail :-" + 
    #        "\n    User: " + settings.MANDRILL_USER_NAME + 
    #        "\n    Email: " + m.email + 
    #        "\n    Subject: " + m.message.subject +
    #        "\n    Description: " + m.message.description)

    if (m.message.template_type == TEMPLATE_TYPE_DJANGO):
        merge_vars = _get_merge_vars(m)
        subject = _render(m.message.subject, merge_vars)
        body = _render(m.message.description, merge_vars)

    if (settings.MANDRILL_USER_NAME and settings.MANDRILL_API_KEY):
        mail.send_mail(
            subject,
            body,
            'notify@{}'.format(settings.MAILGUN_SERVER_NAME),
            [m.email,],
            fail_silently=False,
            auth_user=settings.MANDRILL_USER_NAME,
            auth_password=settings.MANDRILL_API_KEY,
        )
    else:
        mail.send_mail(
            subject,
            body,
            'notify@{}'.format(settings.MAILGUN_SERVER_NAME),
            [m.email,],
            fail_silently=False,
        )


def _send_mandrill_format_message(m):
    """ Send message to a list of email addresses."""

    if ((settings.MANDRILL_USER_NAME and settings.MANDRILL_API_KEY) == False):
        raise MandrillAPIError("Mandrill user name and password are not correctly configured")

    if (settings.MAILGUN_SERVER_NAME == None):
        raise MailgunAPIError("Mailgun server name is not correctly configured")

    try:
        mail_items = m.mail_set.all()

        email_addresses = [
            mail_item.email for mail_item in mail_items
        ]

        msg = mail.EmailMultiAlternatives(
            subject = m.subject,
            from_email = 'notify@{}'.format(settings.MAILGUN_SERVER_NAME),
            to = email_addresses,
        )

        msg.metadata = {'user_id': settings.MANDRILL_USER_NAME},

        if (m.is_html):
            msg.attach_alternative(m.description, "text/html")
            msg.auto_text = True
        else:
            msg.body = m.description

        merge_vars = dict()

        for mail_item in mail_items:
            user_vars = _get_merge_vars(mail_item)

            if (len(user_vars) > 0):
                merge_vars.update ({mail_item.email : user_vars})

        if (len(merge_vars) > 0):
            msg.merge_vars = merge_vars

        msg.send()

        for resp in msg.mandrill_response:
            mi = mail_items.filter(email=resp['email'])[0]

            if (resp['status'] == 'sent'):
                mi.sent = datetime.now()
                mi.sent_response_code = resp['_id']
            else:
                mi.retry_count = (mi.retry_count or 0) + 1
                logger.error("Failed to send message to " + resp.email +
                    ": " + resp.reject_reason)

            mi.save()
    except (SMTPException, MailgunAPIError, MandrillAPIError) as e:
        logger.error(e.message)
        for mi in mail_items:
            mi.retry_count = (mi.retry_count or 0) + 1
            mi.save()


def get_mail_template(slug):
    slug = slugify(slug)
    return MailTemplate.objects.get(slug=slug)


def init_app_mail():
    pass


def init_mail_template(slug, title, help_text, is_html, template_type):
    slug=slugify(slug)
    try:
        template = MailTemplate.objects.get(slug=slug)
        template.title = title
        template.help_text = help_text
        template.is_html = is_html
        template.template_type = template_type
        template.save()
    except MailTemplate.DoesNotExist:
        return clean_and_save(MailTemplate(**dict(
            title=title,
            slug=slug,
            help_text=help_text,
            is_html = is_html,
            template_type = template_type,
        )))
    return template


def mail_template_render(template_slug, context):
    description = None
    subject = None
    template = MailTemplate.objects.get(slug=template_slug)
    description = _render(template.description, context)
    subject = _render(template.subject, context)
    return subject, description


@transaction.atomic
def queue_mail(content_object, email_addresses, subject, description, template_type=TEMPLATE_TYPE_DJANGO, is_html=False, fields=None):
    """Add a mail message to the models."""
    message = Message(**dict(
        content_object=content_object,
        subject=subject,
        description=description,
        template_type=template_type,
        is_html=is_html,
    ))

    message.save()
    for email in email_addresses:
        mail = Mail(**dict(
            email=email,
            message=message,
        ))
        mail.save()

        if (fields):
            mail_fields = fields.get(email, None)
            if (mail_fields):
                for key in mail_fields.keys():
                    value = mail_fields.get(key, None)

                    if (value):
                        mf = MailField(**dict(
                            mail = mail,
                            key = key,
                            value = value
                        ))
                        mf.save()
    return message


@transaction.atomic
def queue_mail_message(content_object, template, content_data):
    """Add a mail message to the models."""

    # check if we've been passed the slug and if so get the template
    if (isinstance (template, str)):
        template = get_mail_template(template)

    message = Message(**dict(
        content_object=content_object,
        subject=template.subject,
        description=template.description,
        is_html=template.is_html,
        template_type=template.template_type,
    ))

    message.save()

    for email in content_data.keys():
        mail = Mail(**dict(
            email=email,
            message=message,
        ))
        mail.save()

        email_data = content_data[email]

        if (email_data):
            for key in email_data.keys():
                value = email_data.get(key, None)

                if (value):
                    mf = MailField(**dict(mail=mail, key=key, value=value))
                    mf.save()
    return message


def send_mail():
    _send_mandrill_format_mail()
    _send_django_format_mail()
