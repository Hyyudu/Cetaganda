# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('science', '0002_auto_20150621_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='invention',
            name='base',
            field=models.CharField(default=None, max_length=255, verbose_name='\u041e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invention',
            name='change',
            field=models.CharField(default=None, max_length=255, verbose_name='\u0418\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0435'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invention',
            name='base_coded',
            field=models.CharField(max_length=255, verbose_name='\u041e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='invention',
            name='change_coded',
            field=models.CharField(max_length=255, verbose_name='\u0418\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0435'),
        ),
    ]
