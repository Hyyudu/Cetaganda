# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from science import views

urlpatterns = [
    url('^$', views.IndexView.as_view(), name='index'),
    url('^new$', views.CreateInventionView.as_view(), name='create_invention'),
    url('^produce$', views.CreateProductionView.as_view(), name='produce'),
    url('^invention/(?P<slug>\w+)$', views.InventionView.as_view(), name='invention'),
]
