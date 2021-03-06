from __future__ import unicode_literals

from django.apps import AppConfig
from django.contrib.auth import get_user_model

from users.models import UserInfo


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        get_user_model().__unicode__ = lambda user: '%s %s' % (user.last_name, user.first_name)
        get_user_model().info = lambda user: UserInfo.objects.get(user=user)

default_app_config = 'users.UsersConfig'
