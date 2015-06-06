from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin

from hack import views

admin.autodiscover()

urlpatterns = [
    url('^$', views.HackIndexView.as_view(), name='duels'),
    url('^/hack/(?P<key>\w+)$', views.HackView.as_view(), name='hack'),
    url('^/duel/(?P<key>\w+)$', views.DuelView.as_view(), name='duel'),
]
