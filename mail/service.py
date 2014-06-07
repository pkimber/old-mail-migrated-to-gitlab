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


def _can_use_mandrill():
    api_key = None
    result = False
    user_name = None
    if 'DjrillBackend' in settings.EMAIL_BACKEND:
        try:
            api_key = settings.MANDRILL_API_KEY
            user_name = settings.MANDRILL_USER_NAME
            result = True
        except AttributeError:
            pass
    return result


def _check_backends(template_types):
    """Check the backend settings... so we can abort early."""
    for t in template_types:
        if t == TEMPLATE_TYPE_DJANGO:
            _using_mailgun()
        elif t == TEMPLATE_TYPE_MANDRILL:
            _using_mandrill()
            _using_mailgun()


def _get_merge_vars(mail_item):
    result = [ (mf.key, mf.value) for mf in mail_item.mailfield_set.all()]
    return dict(result)


def _mail_process():
    primary_keys = []
    template_types = []
    for m in Mail.objects.filter(sent__isnull=True):
        primary_keys.append(m.pk)
        if m.message.template:
            template_types.append(m.message.template.template_type)
    _check_backends(set(template_types))
    _mail_send(primary_keys)


def _render(text, context):
    t = Template(text)
    c = Context(context)
    return t.render(c)


#def _simple_mail_process():
#    primary_keys = [
#        e.pk for e in Mail.objects.filter(
#            sent__isnull=True,
#            message__template__isnull=True,
#        )
#    ]
#    _simple_mail_send(primary_keys)



def _mail_send(primary_keys):
    for pk in primary_keys:
        m = Mail.objects.get(pk=pk)
        try:
            if m.message.template:
                template_type = m.message.template.template_type
            else:
                template_type = None
            if template_type == TEMPLATE_TYPE_DJANGO:
                result = _send_mail_django_template(m)
            elif template_type == TEMPLATE_TYPE_MANDRILL:
                result = _send_mail_mandrill_template(m)
            else:
                result = _send_mail_simple(m)
            m.sent = timezone.now()
            if result:
                m.sent_response_code = result
        except (SMTPException, MailError, MailgunAPIError, MandrillAPIError) as e:
            logger.error(e.message)
            retry_count = m.retry_count or 0
            m.retry_count = retry_count + 1
        m.save()


def _send_mail_simple(m):
    """Send message to a single email address using the Django API."""
    if _can_use_mandrill():
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


#def _template_mail_process():
#    template_types = (
#        TEMPLATE_TYPE_DJANGO,
#        TEMPLATE_TYPE_MANDRILL,
#    )
#    qs = Mail.objects.filter(
#        sent__isnull=True,
#        message__template__template_type__in=template_types,
#    ).order_by(
#        'message'
#    )
#    message_keys = set()
#    for item in qs:
#        message_keys.add(item.message.pk)
#    _template_mail_send(message_keys)


#def _template_mail_send(message_keys):
#    for pk in message_keys:
#        message = Message.objects.get(pk=pk)
#        if message.template.template_type == TEMPLATE_TYPE_DJANGO:
#            _send_mail_django_template(message)
#        elif message.template.template_type == TEMPLATE_TYPE_MANDRILL:
#            _send_mail_mandrill_template(message)
#        else:
#            raise MailError(
#                "Unknown mail template type: '{}'".format(
#                    message.template.template_type
#                )
#            )


def _send_mail_django_template(m):
    merge_vars = _get_merge_vars(m)
    subject, description = _mail_template_render(
        m.message.template_slug,
        merge_vars,
    )
    msg = mail.EmailMultiAlternatives(
        subject=subject,
        from_email='notify@{}'.format(settings.MAILGUN_SERVER_NAME),
        to=mail.email,
    )
    if m.message.template.is_html:
        msg.attach_alternative(description, "text/html")
        msg.auto_text = True
    else:
        msg.body = description
    msg.send()


def _send_mail_mandrill_template(m):
    """Send message to a single email address."""
    result = None
    email_addresses = [m.email,]
    msg = mail.EmailMultiAlternatives(
        subject=m.message.subject,
        from_email='notify@{}'.format(settings.MAILGUN_SERVER_NAME),
        to=email_addresses,
    )
    msg.metadata = {
        'user_id': settings.MANDRILL_USER_NAME,
    }
    if m.message.template.is_html:
        msg.attach_alternative(m.message.description, "text/html")
        msg.auto_text = True
    else:
        msg.body = m.message.description
    merge_vars = dict()
    user_vars = _get_merge_vars(m)
    if len(user_vars):
        merge_vars.update ({m.email: user_vars})
    if len(merge_vars):
        msg.merge_vars = merge_vars
    msg.template_name = m.message.template.slug
    msg.send()
    # sending one email, so expecting a single element in this list e.g:
    # [
    #   {
    #     'email': 'testing@pkimber.net',
    #     'status': 'sent',
    #     '_id': '1dffa1548a884dcdb6942f758abff168',
    #     'reject_reason': None
    #   }
    # ]
    for resp in msg.mandrill_response:
        if resp['status'] == 'sent':
            result = resp['_id']
        else:
            raise MailError(
                "Failed to send message to {}: {}".format(
                    resp.email, resp.reject_reason
                )
            )
    return result


def _using_mailgun():
    """We are using mailgun (or the server name)... check settings."""
    if not settings.MAILGUN_SERVER_NAME:
        raise MailError("Mailgun server name is not correctly configured")


def _using_mandrill():
    """We are using mandrill... so check settings."""
    if not 'DjrillBackend' in settings.EMAIL_BACKEND:
        raise MailError(
            "The email backend is not 'DjrillBackend'.  You cannot send "
            "messages using Mandrill (or send Mandrill templates)."
        )
    if not _can_use_mandrill():
        raise MailError(
            "The Mandrill user name and/or API key are not configured"
        )


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
def queue_mail_template(content_object, template_slug, context):
    """Queue a mail message.  The message will be rendered using the template.

    When the mail is sent, the template will be found and rendered using
    with Django or Mandrill.

    The context is a dict containing email addresses and optionally a
    key, value dict for each email address.
    """

    template = get_mail_template(template_slug)
    message = Message(**dict(
        content_object=content_object,
        subject=template.subject,
        template=template,
    ))
    message.save()
    for email in context.keys():
        mail = Mail(**dict(
            email=email,
            message=message,
        ))
        mail.save()
        email_data = context[email]
        if email_data:
            for key in email_data.keys():
                value = email_data.get(key, None)
                if value:
                    mf = MailField(**dict(mail=mail, key=key, value=value))
                    mf.save()
    return message


def send_mail():
    _mail_process()
    #_simple_mail_process()
    #_template_mail_process()
