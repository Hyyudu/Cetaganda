# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0015_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='dt',
            field=models.DateTimeField(default=None, verbose_name='\u0412\u0440\u0435\u043c\u044f', auto_now=True),
            preserve_default=False,
        ),
    ]
