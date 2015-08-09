from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin

from hack import views

admin.autodiscover()

urlpatterns = [
    url('^$', views.DefenceIndexView.as_view(), name='defence'),
    url('^duels$', views.DuelsIndexView.as_view(), name='duels'),
    url('^duel/(?P<key>\w+)$', views.DuelView.as_view(), name='duel'),
    url('^hacks$', views.HacksIndexView.as_view(), name='hacks'),
    url('^hack/(?P<key>\w+)$', views.HackView.as_view(), name='hack'),
]
