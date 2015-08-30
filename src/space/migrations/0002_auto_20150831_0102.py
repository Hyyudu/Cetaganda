# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='point',
            name='alliance',
            field=models.ForeignKey(default=None, blank=True, to='space.Alliance', null=True, verbose_name='\u0410\u043b\u044c\u044f\u043d\u0441'),
        ),
    ]
