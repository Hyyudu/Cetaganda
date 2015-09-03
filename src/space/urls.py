# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from space import views

urlpatterns = [
    url('^$', views.IndexView.as_view(), name='index'),
    url('^tactics$', views.TacticsView.as_view(), name='tactics'),
    url('^diplomacy$', views.DiplomacyView.as_view(), name='diplomacy'),
    url('^ship/(?P<pk>\d+)$', views.ShipView.as_view(), name='ship'),
    url('^ship/(?P<pk>\d+)/fleet$', views.ShipFleetView.as_view(), name='ship_fleet'),
    url('^ship/(?P<pk>\d+)/diplomats$', views.ShipDiplomatsView.as_view(), name='ship_diplomats'),
]