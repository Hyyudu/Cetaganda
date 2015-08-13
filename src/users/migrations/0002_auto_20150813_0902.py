# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL("UPDATE users_userinfo i JOIN django_ulogin_uloginuser u ON i.ulogin_id=u.id SET i.user_id=u.user_id")
    ]
