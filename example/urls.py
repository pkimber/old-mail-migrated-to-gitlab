# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import (
    include,
    patterns,
    url,
)
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from .views import (
    HomeView,
    EnquiryListView,
)

# Admin interface for djrill
from djrill import DjrillAdminSite

admin.site = DjrillAdminSite()
#end Admin interface for djrill

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=HomeView.as_view(),
        name='project.home'
        ),
    url(regex=r'^',
        view=include('login.urls')
        ),
    url(regex=r'^admin/',
        view=include(admin.site.urls)
        ),
    url(regex=r'^mail/',
        view=include('mail.urls')
        ),
    url(regex=r'^enquiry/',
        view=EnquiryListView.as_view(),
        name='example.enquiry.list'
        ),
    url(r'^home/user/$',
        view=RedirectView.as_view(url=reverse_lazy('project.home')),
        name='project.home.user'
        ),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#   ^ helper function to return a URL pattern for serving files in debug mode.
# https://docs.djangoproject.com/en/1.5/howto/static-files/#serving-files-uploaded-by-a-user

urlpatterns += staticfiles_urlpatterns()
