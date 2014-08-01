# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import factory

from example.models import Enquiry


class EnquiryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Enquiry
