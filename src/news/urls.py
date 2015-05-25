# -*- coding: utf-8 -*-

from django.conf.urls import *
from django.views.generic.list import ListView

from .models import News

urlpatterns = [
    url(r'^$', ListView.as_view(queryset=News.objects.all()), name='site_news'),
]
