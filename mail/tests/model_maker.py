# -*- encoding: utf-8 -*-
from base.tests.model_maker import clean_and_save

from mail.models import Notify


def make_notify(email, **kwargs):
    defaults = dict(
        email=email,
    )
    defaults.update(kwargs)
    return clean_and_save(Notify(**defaults))
