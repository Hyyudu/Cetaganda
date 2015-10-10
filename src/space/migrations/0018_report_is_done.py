# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0017_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='is_done',
            field=models.BooleanField(default=False, verbose_name='\u0412\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u043e'),
        ),
    ]
