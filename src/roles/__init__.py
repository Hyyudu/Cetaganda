from __future__ import unicode_literals

from django.apps import AppConfig
from django.contrib.auth import get_user_model

from roles.models import UserInfo


class RolesConfig(AppConfig):
    name = 'roles'

    def ready(self):
        get_user_model().__unicode__ = lambda user: '%s %s' % (user.last_name, user.first_name)
        get_user_model().info = lambda user: UserInfo.objects.get(ulogin__user=user)

default_app_config = 'roles.RolesConfig'
