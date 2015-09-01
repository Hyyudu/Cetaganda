# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0004_auto_20150831_2357'),
    ]

    operations = [
        migrations.AddField(
            model_name='point',
            name='is_major',
            field=models.BooleanField(default=False, verbose_name='\u041e\u0441\u043d\u043e\u0432\u043d\u0430\u044f \u043f\u043b\u0430\u043d\u0435\u0442\u0430 \u0430\u043b\u044c\u044f\u043d\u0441\u0430'),
        ),
    ]
