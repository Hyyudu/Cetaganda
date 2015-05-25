# coding: utf-8

from django.conf.urls import *

from users import views

urlpatterns = [
    url(r'^cabinet$', views.CabinetView.as_view(), name='cabinet'),
    url(r'^registration', views.RegistrationView.as_view(), name='registration'),
    url(r'^login$', views.LoginView.as_view(), name='login'),
]
