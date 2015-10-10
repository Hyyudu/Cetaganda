# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0013_alliance_resources'),
    ]

    operations = [
        migrations.AlterField(
            model_name='point',
            name='resources',
            field=jsonfield.fields.JSONField(default='[]', verbose_name='\u0420\u0435\u0441\u0443\u0440\u0441\u044b'),
        ),
        migrations.AlterField(
            model_name='ship',
            name='fleet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_DEFAULT, default=None, blank=True, to='space.Fleet', null=True, verbose_name='\u0424\u043b\u043e\u0442'),
        ),
        migrations.AlterField(
            model_name='ship',
            name='home',
            field=models.ForeignKey(related_name='home', default=None, blank=True, to='space.Point', null=True, verbose_name='\u041f\u043e\u0440\u0442 \u043f\u0440\u0438\u043f\u0438\u0441\u043a\u0438'),
        ),
    ]
