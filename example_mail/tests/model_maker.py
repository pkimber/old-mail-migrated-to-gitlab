# -*- encoding: utf-8 -*-
from base.tests.model_maker import clean_and_save

from example_mail.models import Enquiry


def make_enquiry(email, subject, description, **kwargs):
    defaults = dict(
        email=email,
        subject=subject,
        description=description,
    )
    defaults.update(kwargs)
    return clean_and_save(Enquiry(**defaults))
