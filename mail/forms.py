# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from base.form_utils import RequiredFieldForm

from .models import MailTemplate


class MailTemplateForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super(MailTemplateForm, self).__init__(*args, **kwargs)
        for name in ('subject', 'description'):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )

    class Meta:
        model = MailTemplate
        fields = (
            'subject',
            'description',
        )
