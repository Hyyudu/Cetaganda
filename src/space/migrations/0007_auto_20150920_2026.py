# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0006_auto_20150905_0012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ship',
            name='type',
            field=models.CharField(max_length=10, verbose_name='\u0422\u0438\u043f', choices=[('s', '\u0421\u0442\u0430\u043d\u0446\u0438\u044f'), ('k', '\u041a\u0440\u0435\u0439\u0441\u0435\u0440'), ('r', '\u0420\u0430\u0437\u0432\u0435\u0434\u0447\u0438\u043a'), ('l', '\u041b\u0438\u043d\u043a\u043e\u0440'), ('t', '\u0422\u0440\u0430\u043d\u0441\u043f\u043e\u0440\u0442')]),
        ),
    ]
