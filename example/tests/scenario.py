# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from mail.models import (
    TEMPLATE_TYPE_DJANGO,
    TEMPLATE_TYPE_MANDRILL,
)

from mail.service import (
    init_mail_template,
    queue_mail_template,
)

from example.models import Enquiry
from example.base import get_env_variable


def default_scenario_mail():
    create_hello_template()
    create_goodbye_template()
    create_email_ack_template()
    queue_enquiry_acknowledgement()
    queue_enquiry_ack_with_copy()
    queue_enquiry_hello()


def create_hello_template():
    hello_template = init_mail_template(
        'hello',
        'Welcome to our mailing list.',
        (
            "You can add the following variables to the template:\n"
            "{{ name }} name of the customer.\n"
            "{{ title }} name of the village."
        ),
        is_html=False,
        template_type=TEMPLATE_TYPE_DJANGO,
    )
    hello_template.subject = "hello {{ name }}"
    hello_template.description = (
        "Dear {{ name }},\n"
        "Thank you for subscribing to the {{ title }} news letter\n"
        "Best wishes\n\n"
        "The {{ title }} team"
    )
    hello_template.save()


def create_goodbye_template():
    goodbye_template = init_mail_template(
        'goodbye',
        'Sorry to see you go...',
        (
            "You can add the following variables to the template:\n"
            "{{ name }} name of the user\n"
            "{{ age }} age of the customer."
        ),
        is_html=False,
        template_type=TEMPLATE_TYPE_DJANGO,
    )

    goodbye_template.subject = "goodbye {{ name }}"
    goodbye_template.description = (
        "Dear {{name}},\n"
        "Sorry you no longer wish to receive the {{title}} news letter\n"
        "Goodbye and best wishes"
    )
    goodbye_template.save()


def create_email_ack_template():
    template = init_mail_template(
        'enquiry_acknowledgement',
        'Enquiry acknowledgement',
        (
            'You can add the following variables to the template:\n'
            '*|BODY|* The body of the original enquiry\n'
            '*|SUBJECT|* The subject of the original enquiry\n'
            '*|DATE|* The date of the original enquiry\n'
        ),
        is_html=True,
        template_type=TEMPLATE_TYPE_MANDRILL,
    )
    template.subject='Re: *|SUBJECT|*'
    template.description= (
        "<style>.body {padding: 10px; border: 1px solid grey;"
        "background-color: #F8ECE0;} </style>"
        "<h2>*|SUBJECT|*</h2>"
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
            "I've just got a job as a legal secretary.  "
            "Can you please outline details of membership "
            "options available to me\n\n"
            "Kind regards,\n\n"
            "G. Paltrow"
        )
    ))
    e.save()
    return e


def queue_enquiry_hello(enq=None):
    if not enq:
        enq = create_enquiry()
    content_data = dict({enq.email: {'name': 'Fred Bloggs', 'title': 'Okehampton'}})
    queue_mail_template(
        enq,
        'hello',
        content_data,
    )


def queue_enquiry_goodbye(enq=None):
    if not enq:
        enq = create_enquiry()
    context = dict({enq.email: {'name': 'Fred Bloggs', 'title': 'Okehampton'}})
    queue_mail_template(
        enq,
        'goodbye',
        context,
    )


def queue_enquiry_acknowledgement(enq=None):
    if not enq:
        enq = create_enquiry()
    content_data = dict(
        {
            enq.email: {
                "SUBJECT": "Re: " + enq.subject,
                "BODY": enq.description,
                "DATE": enq.created.strftime("%d-%b-%Y %H:%M:%S")
            }
        }
    )
    queue_mail_template(
        enq,
        'enquiry_acknowledgement',
        content_data=content_data,
    )


def queue_enquiry_ack_with_copy(enq=None):
    copy_email = get_env_variable('TEST_EMAIL_ADDRESS_2')
    if not enq:
        enq = create_enquiry()
    content_data = dict(
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
    queue_mail_template(
        enq,
        'enquiry_acknowledgement',
        content_data,
    )
