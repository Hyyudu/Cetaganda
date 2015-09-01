# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0002_auto_20150831_0102'),
    ]

    operations = [
        migrations.AddField(
            model_name='ship',
            name='alliance',
            field=models.ForeignKey(related_name='alliance_ships', default=None, verbose_name='\u0410\u043b\u044c\u044f\u043d\u0441', to='space.Alliance'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ship',
            name='is_alive',
            field=models.BooleanField(default=True, verbose_name='\u0416\u0438\u0432\u043e\u0439'),
        ),
    ]
