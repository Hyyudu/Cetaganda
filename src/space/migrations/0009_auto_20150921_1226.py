# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0008_fleet_route'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='point',
            options={'ordering': ('name', 'type'), 'verbose_name': '\u0422\u043e\u0447\u043a\u0430', 'verbose_name_plural': '\u0422\u043e\u0447\u043a\u0438'},
        ),
        migrations.AddField(
            model_name='ship',
            name='friends',
            field=models.ManyToManyField(related_name='friends_rel_+', verbose_name='\u0414\u0440\u0443\u0436\u0431\u0430', to='space.Ship'),
        ),
    ]
