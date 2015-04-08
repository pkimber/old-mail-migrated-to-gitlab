# -*- encoding: utf-8 -*-
import factory

from example_mail.models import Enquiry


class EnquiryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Enquiry
