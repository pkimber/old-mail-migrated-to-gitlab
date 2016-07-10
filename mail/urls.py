# -*- encoding: utf-8 -*-
from django.conf.urls import (
    patterns,
    url,
)

from .views import (
    MailTemplateCreateDjangoView,
    MailTemplateCreateMandrillView,
    MailTemplateListView,
    MailTemplateUpdateDjangoView,
    MailTemplateUpdateMandrillView,
    MessageListView,
)


urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=MessageListView.as_view(),
        name='mail.message.list'
        ),
    url(regex=r'^template/$',
        view=MailTemplateListView.as_view(),
        name='mail.template.list'
        ),
    url(regex=r'^template/create/django/$',
        view=MailTemplateCreateDjangoView.as_view(),
        name='mail.template.create.django'
        ),
    url(regex=r'^template/create/mandrill/$',
        view=MailTemplateCreateMandrillView.as_view(),
        name='mail.template.create.mandrill'
        ),
    url(regex=r'^template/(?P<pk>\d+)/update/django/$',
        view=MailTemplateUpdateDjangoView.as_view(),
        name='mail.template.update.django'
        ),
    url(regex=r'^template/(?P<pk>\d+)/update/mandrill/$',
        view=MailTemplateUpdateMandrillView.as_view(),
        name='mail.template.update.mandrill'
        ),
)
