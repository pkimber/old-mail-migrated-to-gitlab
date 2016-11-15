# -*- encoding: utf-8 -*-
from django.conf.urls import url

from .views import (
    MailTemplateCreateDjangoView,
    MailTemplateCreateRemoteView,
    MailTemplateListView,
    MailTemplateUpdateDjangoView,
    MailTemplateUpdateRemoteView,
    MessageListView,
)


urlpatterns = [
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
        view=MailTemplateCreateRemoteView.as_view(),
        name='mail.template.create.mandrill'
        ),
    url(regex=r'^template/create/sparkpost/$',
        view=MailTemplateCreateRemoteView.as_view(),
        name='mail.template.create.sparkpost'
        ),
    url(regex=r'^template/(?P<pk>\d+)/update/django/$',
        view=MailTemplateUpdateDjangoView.as_view(),
        name='mail.template.update.django'
        ),
    url(regex=r'^template/(?P<pk>\d+)/update/mandrill/$',
        view=MailTemplateUpdateRemoteView.as_view(),
        name='mail.template.update.mandrill'
        ),
    url(regex=r'^template/(?P<pk>\d+)/update/sparkpost/$',
        view=MailTemplateUpdateRemoteView.as_view(),
        name='mail.template.update.sparkpost'
        ),
]
