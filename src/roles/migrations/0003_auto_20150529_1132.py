# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('roles', '0002_auto_20150525_0155'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='creator',
            field=models.ForeignKey(related_name='creator', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u0421\u043e\u0437\u0434\u0430\u0442\u0435\u043b\u044c'),
        ),
        migrations.AddField(
            model_name='role',
            name='target',
            field=models.CharField(default='free', max_length=20, verbose_name='\u0414\u043b\u044f \u043a\u043e\u0433\u043e', choices=[('free', '\u0421\u0432\u043e\u0431\u043e\u0434\u043d\u0430\u044f'), ('me', '\u0414\u043b\u044f \u0441\u0435\u0431\u044f'), ('other', '\u0414\u043b\u044f \u0434\u0440\u0443\u0433\u0430')]),
        ),
        migrations.AlterField(
            model_name='role',
            name='user',
            field=models.ForeignKey(related_name='gamer', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u0418\u0433\u0440\u043e\u043a'),
        ),
    ]
