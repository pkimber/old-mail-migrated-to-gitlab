# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from mail.service import init_mail_template


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
