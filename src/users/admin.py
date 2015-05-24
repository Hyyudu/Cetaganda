# coding: utf-8
from __future__ import unicode_literals

from django.contrib import admin

from django_ulogin import models as ulogin_models
from . import models


admin.site.register(models.UserInfo)
admin.site.register(ulogin_models.ULoginUser)
