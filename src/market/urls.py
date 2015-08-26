from __future__ import unicode_literals

from django.conf.urls import url

from market import views

urlpatterns = [
    url(r'^$', views.MarketView.as_view(), name='index'),
    url(r'^buy$', views.BuyView.as_view(), name='buy'),
]
