# -*- encoding: utf-8 -*-
from django import forms

from base.form_utils import FileDropInput
from .models import Enquiry


class EnquiryForm(forms.ModelForm):

    CHOICES = (
        ('template', 'Mail template'),
        ('simple', 'Simple email (no template)'),
    )

    send_email = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields:
            if name != 'send_email':
                self.fields[name].widget.attrs.update(
                    {'class': 'pure-input-2-3'}
                )

    class Meta:
        model = Enquiry
        fields = (
            'send_email',
            'email',
            'subject',
            'description',
            'document',
        )
        widgets= {'document': FileDropInput}
