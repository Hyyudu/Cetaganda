# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

urlpatterns = [
    url('^$', 'science.views.index', name="science_index"),
]
