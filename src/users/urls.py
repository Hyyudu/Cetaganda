# coding: utf-8

from django.conf.urls import *

from users import views

urlpatterns = [
    url(r'^cabinet$', views.CabinetView.as_view(), name='cabinet'),
]
