# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0006_auto_20150809_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='is_hidden',
            field=models.BooleanField(default=False, verbose_name='\u0421\u043a\u0440\u044b\u0442\u0430'),
        ),
    ]
