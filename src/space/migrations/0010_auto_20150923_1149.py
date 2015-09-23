# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0009_auto_20150921_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='point',
            name='resources',
            field=models.CharField(default='', max_length=100, verbose_name='\u0420\u0435\u0441\u0443\u0440\u0441\u044b', blank=True),
        ),
    ]
