# -*- encoding: utf-8 -*-
from base.form_utils import RequiredFieldForm

from .models import MailTemplate


class MailTemplateCreateDjangoForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ('subject', 'description', 'title'):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )

    class Meta:
        model = MailTemplate
        fields = (
            'slug',
            'title',
            'subject',
            'description',
        )


class MailTemplateCreateMandrillForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ('title',):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )

    class Meta:
        model = MailTemplate
        fields = (
            'slug',
            'title',
        )


class MailTemplateUpdateDjangoForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ('subject', 'description', 'title'):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )

    class Meta:
        model = MailTemplate
        fields = (
            'slug',
            'title',
            'subject',
            'description',
        )


class MailTemplateUpdateMandrillForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ('title',):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )

    class Meta:
        model = MailTemplate
        fields = (
            'slug',
            'title',
        )
