# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0018_report_is_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='ship',
            name='drive',
            field=models.BooleanField(default=False, verbose_name='\u0413\u0438\u043f\u0435\u0440\u0434\u0440\u0430\u0439\u0432'),
        ),
        migrations.AddField(
            model_name='ship',
            name='shield',
            field=models.BooleanField(default=False, verbose_name='\u0411\u0440\u043e\u043d\u044f'),
        ),
        migrations.AlterField(
            model_name='fleet',
            name='route',
            field=models.TextField(default='', verbose_name='\u0417\u0430\u043a\u0430\u0437\u0430\u043d\u043d\u044b\u0439 \u043c\u0430\u0440\u0448\u0440\u0443\u0442', blank=True),
        ),
    ]
