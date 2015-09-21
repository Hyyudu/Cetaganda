# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0007_auto_20150920_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='fleet',
            name='route',
            field=models.TextField(default='', verbose_name='\u0417\u0430\u043a\u0430\u0437\u0430\u043d\u043d\u044b\u0439 \u043c\u0430\u0440\u0448\u0440\u0443\u0442'),
        ),
    ]
