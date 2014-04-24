# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import (
    patterns,
    url,
)

from .views import (
    MessageListView,
    TemplateListView,
    TemplateUpdateView,
)


urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=MessageListView.as_view(),
        name='mail.message.list'
        ),
    url(regex=r'^template/$',
        view=TemplateListView.as_view(),
        name='mail.template.list'
        ),
    url(regex=r'^template/(?P<slug>[-\w\d]+)/update/$',
        view=TemplateUpdateView.as_view(),
        name='mail.template.update'
        ),
)
