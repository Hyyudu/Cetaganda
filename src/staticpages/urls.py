# -*- coding: utf-8 -*-

from django.conf.urls import *
from django.views.generic.detail import DetailView

from .models import Article

urlpatterns = [
    url(r'^(?P<pk>\d+)$', DetailView.as_view(queryset=Article.objects.all()), name='article'),
]
