# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from register import views

urlpatterns = [
    url('^$', views.IndexView.as_view(), name='index'),
]
