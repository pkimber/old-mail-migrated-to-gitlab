# -*- encoding: utf-8 -*-
from django import forms

from .models import Enquiry


class EnquiryForm(forms.ModelForm):

    CHOICES = (
        ('template', 'Mail template'),
        ('simple', 'Simple email (no template)'),
    )

    send_email = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    class Meta:
        model = Enquiry
        fields = (
            'send_email',
            'email',
            'subject',
            'description',
            'document',
        )
