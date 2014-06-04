# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.conf import settings
from django.core import mail
from django.db import transaction
from django.template import (
    Context,
    Template,
)
from django.utils import timezone
from django.utils.text import slugify

from django_mailgun import MailgunAPIError

from djrill import MandrillAPIError

from smtplib import SMTPException

from base.tests.model_maker import clean_and_save

from .models import (
    Mail,
    MailError,
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


def _render(text, context):
    t = Template(text)
    c = Context(context)
    return t.render(c)


def _simple_mail_process():
    primary_keys = [
        e.pk for e in Mail.objects.filter(
            sent__isnull=True,
            message__template__isnull=True,
        )
    ]
    _simple_mail_send(primary_keys)


def _simple_mail_send(primary_keys):
    for pk in primary_keys:
        m = Mail.objects.get(pk=pk)
        try:
            _simple_mail_send_message(m)
            m.sent = timezone.now()
        except (SMTPException, MailgunAPIError) as e:
            logger.error(e.message)
            retry_count = m.retry_count or 0
            m.retry_count = retry_count + 1
        m.save()


def _simple_mail_send_message(m):
    """Send message to a list of email addresses."""
    if settings.MANDRILL_USER_NAME and settings.MANDRILL_API_KEY:
        mail.send_mail(
            m.message.subject,
            m.message.description,
            'notify@{}'.format(settings.MAILGUN_SERVER_NAME),
            [m.email,],
            fail_silently=False,
            auth_user=settings.MANDRILL_USER_NAME,
            auth_password=settings.MANDRILL_API_KEY,
        )
    else:
        mail.send_mail(
            m.message.subject,
            m.message.description,
            'notify@{}'.format(settings.MAILGUN_SERVER_NAME),
            [m.email,],
            fail_silently=False,
        )


def _template_mail_process():
    template_types = (
        TEMPLATE_TYPE_DJANGO,
        TEMPLATE_TYPE_MANDRILL,
    )
    qs = Mail.objects.filter(
        sent__isnull=True,
        message__template__template_type__in=template_types,
    ).order_by(
        'message'
    )
    message_keys = set()
    for item in qs:
        message_keys.add(item.message.pk)
    _template_mail_send(message_keys)


def _template_mail_send(message_keys):
    for pk in message_keys:
        message = Message.objects.get(pk=pk)
        if message.template.template_type == TEMPLATE_TYPE_DJANGO:
            _template_mail_send_django(message)
        elif message.template.template_type == TEMPLATE_TYPE_MANDRILL:
            _template_mail_send_mandrill(message)
        else:
            raise MailError(
                "Unknown mail template type: '{}'".format(
                    message.template.template_type
                )
            )


def _template_mail_send_django(message):
    if not settings.MAILGUN_SERVER_NAME:
        raise MailError("Mailgun server name is not correctly configured")
    for m in message.mail_set.all():
        try:
            merge_vars = _get_merge_vars(m)
            subject, description = _mail_template_render(
                message.template_slug,
                merge_vars,
            )
            msg = mail.EmailMultiAlternatives(
                subject=subject,
                from_email='notify@{}'.format(settings.MAILGUN_SERVER_NAME),
                to=mail.email,
            )
            if message.template.is_html:
                msg.attach_alternative(description, "text/html")
                msg.auto_text = True
            else:
                msg.body = description
            msg.send()
            m.save()
        except (SMTPException, MailgunAPIError) as e:
            logger.error(e.message)
            m.retry_count = (m.retry_count or 0) + 1
            m.save()


def _template_mail_send_mandrill(m):
    """ Send message to a list of email addresses."""
    if not settings.MANDRILL_USER_NAME and settings.MANDRILL_API_KEY:
        raise MailError(
            "Mandrill user name and password are not correctly configured"
        )
    mail_items = m.mail_set.all()
    try:
        email_addresses = [
            mail_item.email for mail_item in mail_items
        ]
        msg = mail.EmailMultiAlternatives(
            subject=m.subject,
            from_email='notify@{}'.format(settings.MAILGUN_SERVER_NAME),
            to=email_addresses,
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
            if len(user_vars):
                merge_vars.update ({mail_item.email : user_vars})
        if len(merge_vars):
            msg.merge_vars = merge_vars
        msg.template_name = m.template.slug
        msg.send()
        for resp in msg.mandrill_response:
            mi = mail_items.filter(email=resp['email'])[0]
            if (resp['status'] == 'sent'):
                mi.sent = timezone.now()
                mi.sent_response_code = resp['_id']
            else:
                mi.retry_count = (mi.retry_count or 0) + 1
                logger.error("Failed to send message to " + resp.email +
                    ": " + resp.reject_reason)
            mi.save()
    except (SMTPException, MandrillAPIError) as e:
        import ipdb
        ipdb.set_trace()
        logger.error(e)
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


def _mail_template_render(template_slug, context):
    description = None
    subject = None
    template = MailTemplate.objects.get(slug=template_slug)
    description = _render(template.description, context)
    subject = _render(template.subject, context)
    return subject, description


@transaction.atomic
def queue_mail_message(content_object, email_addresses, subject, description, is_html=False):
    """queue a mail message for one or more email addresses.

    The subject and description are fully formed i.e. this function does not
    do any templating.

    """

    message = Message(**dict(
        content_object=content_object,
        subject=subject,
        description=description,
        is_html=is_html,
    ))
    message.save()
    for email in email_addresses:
        mail = Mail(**dict(
            email=email,
            message=message,
        ))
        mail.save()
    return message


@transaction.atomic
def queue_mail_template(content_object, template_slug, content_data):
    """Queue a mail message.  The message will be rendered using the template.

    When the mail is sent, the template will be found and rendered using
    with Django or Mandrill.

    The content data is a dict containing email addresses and optionally a
    key, value dict for field values.
    """

    template = get_mail_template(template_slug)
    message = Message(**dict(
        content_object=content_object,
        subject=template.subject,
        template=template,
    ))
    message.save()
    for email in content_data.keys():
        mail = Mail(**dict(
            email=email,
            message=message,
        ))
        mail.save()
        email_data = content_data[email]
        if email_data:
            for key in email_data.keys():
                value = email_data.get(key, None)
                if value:
                    mf = MailField(**dict(mail=mail, key=key, value=value))
                    mf.save()
    return message


def send_mail():
    _simple_mail_process()
    _template_mail_process()
