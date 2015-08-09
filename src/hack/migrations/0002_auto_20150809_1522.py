# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0006_auto_20150809_1522'),
        ('hack', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Float',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hash', models.CharField(max_length=32, verbose_name='\u0425\u044d\u0448')),
                ('target_level', models.PositiveIntegerField(default=None, null=True, verbose_name='\u0423\u0440\u043e\u0432\u0435\u043d\u044c \u0437\u0430\u0449\u0438\u0442\u044b', blank=True)),
                ('owner', models.ForeignKey(related_name='floats', verbose_name='\u0420\u043e\u043b\u044c', to='roles.Role')),
            ],
            options={
                'verbose_name': '\u041f\u043e\u043f\u043b\u0430\u0432\u043e\u043a',
                'verbose_name_plural': '\u041f\u043e\u043f\u043b\u0430\u0432\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('target', models.CharField(max_length=50, verbose_name='\u0426\u0435\u043b\u044c')),
                ('role', models.ForeignKey(related_name='targets', default=None, blank=True, to='roles.Role', null=True, verbose_name='\u0420\u043e\u043b\u044c')),
            ],
            options={
                'verbose_name': '\u0426\u0435\u043b\u044c \u0430\u0442\u0430\u043a\u0438',
                'verbose_name_plural': '\u0426\u0435\u043b\u0438 \u0430\u0442\u0430\u043a',
            },
        ),
        migrations.AddField(
            model_name='float',
            name='target',
            field=models.ForeignKey(related_name='floats', default=None, blank=True, to='hack.Target', null=True, verbose_name='\u0417\u0430\u0449\u0438\u0449\u0430\u0435\u0442'),
        ),
    ]
