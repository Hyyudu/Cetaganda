# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack', '0005_auto_20150811_2338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hack',
            name='result',
        ),
        migrations.AddField(
            model_name='hack',
            name='status',
            field=models.CharField(default=None, choices=[(None, '\u0421\u043e\u0437\u0434\u0430\u043d\u043e'), ('inprocess', '\u0418\u0434\u0435\u0442'), ('win', '\u0412\u0437\u043b\u043e\u043c\u0430\u043d\u043e'), ('run', '\u0421\u0431\u0435\u0436\u0430\u043b'), ('failstatic', '\u041d\u0435 \u0445\u0432\u0430\u0442\u0438\u043b\u043e \u043f\u043e\u043f\u043b\u0430\u0432\u043a\u043e\u0432'), ('fail', '\u041d\u0435 \u043e\u0441\u0438\u043b\u0438\u043b'), ('late', '\u041e\u043f\u043e\u0437\u0434\u0430\u043b')], max_length=20, blank=True, null=True, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441'),
        ),
    ]
