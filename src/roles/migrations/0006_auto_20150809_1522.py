# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0005_auto_20150625_0011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='target',
            field=models.CharField(default='free', max_length=20, verbose_name='\u0414\u043b\u044f \u043a\u043e\u0433\u043e \u0437\u0430\u043f\u043e\u043b\u043d\u044f\u0435\u0442\u0435 \u0437\u0430\u044f\u0432\u043a\u0443', choices=[('free', '\u0421\u0432\u043e\u0431\u043e\u0434\u043d\u0430\u044f'), ('me', '\u0414\u043b\u044f \u0441\u0435\u0431\u044f'), ('other', '\u0414\u043b\u044f \u0434\u0440\u0443\u0433\u0430'), ('fake', '\u0412\u0440\u0435\u043c\u0435\u043d\u043d\u0430\u044f')]),
        ),
    ]
