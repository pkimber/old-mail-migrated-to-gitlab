# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from mail.service import init_template


def default_scenario_mail():
    init_template('goodbye', 'Sorry to see you go...')
    init_template('hello', 'Welcome to our mailing list...')
