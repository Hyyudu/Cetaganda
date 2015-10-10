# -*- coding: utf-8 -*-

from django.conf.urls import *

from guestbook.views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
]
