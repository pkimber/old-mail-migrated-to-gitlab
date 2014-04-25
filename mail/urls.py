# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import (
    patterns,
    url,
)

from .views import (
    MailTemplateListView,
    MailTemplateUpdateView,
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
    url(regex=r'^template/(?P<slug>[-\w\d]+)/update/$',
        view=MailTemplateUpdateView.as_view(),
        name='mail.template.update'
        ),
)
