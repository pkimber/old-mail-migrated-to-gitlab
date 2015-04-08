# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from .models import Enquiry


class EnquiryForm(forms.ModelForm):

    class Meta:
        model = Enquiry
        fields = (
            'email',
            'subject',
            'description',
        )
