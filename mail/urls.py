# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import (
    patterns,
    url,
)

from .views import MessageListView


urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=MessageListView.as_view(),
        name='mail.list'
        ),
)
