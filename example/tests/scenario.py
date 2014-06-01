# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from mail.service import init_mail_template

from mail.service import queue_mail
from mail.models import MailTemplate
from example.models import Enquiry
from example.base import get_env_variable

def default_scenario_mail():
    init_mail_template(
        'goodbye',
        'Sorry to see you go...',
        (
            "You can add the following variables to the template:\n"
            "{{ name }} name of the user\n"
            "{{ age }} age of the customer."
        )
    )
    template = init_mail_template(
        'hello',
        'Welcome to our mailing list.',
        (
            "You can add the following variables to the template:\n"
            "{{ name }} name of the customer.\n"
            "{{ title }} name of the village."
        )
    )

    create_email_ack_template()
    queue_enquiry_acknowledgement()
    queue_enquiry_ack_with_copy()


def create_email_ack_template():
    template = init_mail_template(
        'enquiry_acknowledgement',
        'Enquiry acknowledgement',
        (
            'You can add the following variables to the template:\n'
            '*|BODY|* The body of the original enquiry\n'
            '*|SUBJECT|* The subject of the original enquiry\n'
        )
    )
    template.subject='Re: *|SUBJECT|*'
    template.description= (
        "<style>.body {padding: 10px; border: 1px solid grey;"
        "background-color: #F8ECE0;} </style>"
        "<h2>Re: *|SUBJECT|*</h2>"
        "<p>Thank you for writing to us on *|DATE|*.  We've noted your enquiry</p>"
        "<p><div class='body'><pre>*|BODY|*</pre></div></p>"
        "<p>We will reply to you as soon as possible</p>"
    )
    template.save()


def create_enquiry():
    email = get_env_variable('TEST_EMAIL_ADDRESS_1')

    e = Enquiry(**dict(
        email = email,
        subject = "Membership Options",
        description = (
            "Dear Sirs,\n\n"
            "I've just got a job as a legal secretary."
            "  Can you please outline details of membership options available to me\n\n"
            "Kind regards,\n\n"
            "G. Paltrow"
        )
    ))
    e.save()
    return e


def queue_enquiry_acknowledgement(enq=None):
    template = MailTemplate.objects.get(slug='enquiry_acknowledgement')

    if (enq == None):
        enq = create_enquiry()

    dFields = dict(
        {
            enq.email: {
                "SUBJECT": "Re: " + enq.subject,
                "BODY": enq.description,
                "DATE": enq.created.strftime("%d-%b-%Y %H:%M:%S")
            }
        }
    )

    queue_mail(
        enq,
        [enq.email],
        template.subject,
        template.description,
        is_html=True,
        fields=dFields
    )

def queue_enquiry_ack_with_copy(enq=None):
    template = MailTemplate.objects.get(slug='enquiry_acknowledgement')

    copy_email = get_env_variable('TEST_EMAIL_ADDRESS_2')

    if (enq == None):
        enq = create_enquiry()

    email_addresses = [
        enq.email,
        copy_email,
    ]

    dFields = dict(
        {
            enq.email: {
                "SUBJECT": "Re: " + enq.subject,
                "BODY": enq.description,
                "DATE": enq.created.strftime("%d-%b-%Y %H:%M:%S")
            },
            copy_email: {
                "SUBJECT": "Copy: " + enq.subject,
                "BODY": "<h1>Copy of Message sent to '" + 
                enq.email + "':</h1>" + enq.description,
                "DATE": enq.created.strftime("%d-%b-%Y %H:%M:%S")
            }
        }
    )

    queue_mail(
        enq,
        email_addresses,
        "Re: " + enq.subject,
        template.description,
        is_html=True,
        fields=dFields
    )


