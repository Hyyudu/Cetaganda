# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20150813_0902'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='ulogin',
        ),
    ]
