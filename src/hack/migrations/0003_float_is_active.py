# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack', '0002_auto_20150809_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='float',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='\u0410\u043a\u0442\u0438\u0432\u0435\u043d'),
        ),
    ]
