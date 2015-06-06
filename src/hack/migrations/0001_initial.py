# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Duel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role_1', models.CharField(max_length=100, verbose_name='\u0418\u0433\u0440\u043e\u043a 1')),
                ('role_2', models.CharField(max_length=100, verbose_name='\u0418\u0433\u0440\u043e\u043a 2')),
                ('email_1', models.CharField(max_length=100, verbose_name='Email 1')),
                ('email_2', models.CharField(max_length=100, verbose_name='Email 2')),
                ('state', models.CharField(default='not_started', max_length=20, verbose_name='\u0421\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u0435', choices=[('not_started', '\u041d\u0435 \u043d\u0430\u0447\u0430\u043b\u0430\u0441\u044c'), ('in_progress', '\u0418\u0434\u0435\u0442'), ('finished', '\u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u0430')])),
                ('number_1', models.CharField(help_text='\u0414\u043e 10 \u0441\u0438\u043c\u0432\u043e\u043b\u043e\u0432. \u041e\u0431\u044b\u0447\u043d\u043e - 4. \u041c\u0430\u0448\u0438\u043d\u0438\u0441\u0442 \u0434\u043e\u043b\u0436\u0435\u043d \u0431\u0443\u0434\u0435\u0442 \u0432\u0432\u0435\u0441\u0442\u0438 \u0447\u0438\u0441\u043b\u043e \u0442\u0430\u043a\u043e\u0439 \u0436\u0435 \u0434\u043b\u0438\u043d\u044b.', max_length=10, verbose_name='\u0417\u0430\u0433\u0430\u0434\u0430\u043d\u043d\u043e\u0435 \u0447\u0438\u0441\u043b\u043e 1')),
                ('number_2', models.CharField(default=None, max_length=10, null=True, verbose_name='\u0417\u0430\u0433\u0430\u0434\u0430\u043d\u043d\u043e\u0435 \u0447\u0438\u0441\u043b\u043e 2', blank=True)),
                ('winner', models.CharField(default=None, max_length=100, null=True, verbose_name='\u041f\u043e\u0431\u0435\u0434\u0438\u0442\u0435\u043b\u044c', blank=True)),
                ('result', models.CharField(default=None, max_length=20, null=True, verbose_name='\u0418\u0442\u043e\u0433', blank=True)),
                ('dt', models.DateTimeField(default=None, verbose_name='\u041d\u0430\u0447\u0430\u043b\u043e \u0434\u0443\u044d\u043b\u0438')),
            ],
            options={
                'verbose_name': '\u0414\u0443\u044d\u043b\u044c',
                'verbose_name_plural': '\u0412\u0437\u043b\u043e\u043c\u044b: \u0434\u0443\u044d\u043b\u0438',
            },
        ),
        migrations.CreateModel(
            name='DuelMove',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dt', models.DateTimeField(default=None, verbose_name='\u041d\u0430\u0447\u0430\u043b\u043e \u0445\u043e\u0434\u0430')),
                ('move_1', models.CharField(default=None, max_length=10, null=True, verbose_name='\u0425\u043e\u0434 \u0438\u0433\u0440\u043e\u043a\u0430 1', blank=True)),
                ('result_1', models.CharField(default=None, max_length=10, null=True, verbose_name='\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442 \u0438\u0433\u0440\u043e\u043a\u0430 1', blank=True)),
                ('move_2', models.CharField(default=None, max_length=10, null=True, verbose_name='\u0425\u043e\u0434 \u0438\u0433\u0440\u043e\u043a\u0430 2', blank=True)),
                ('result_2', models.CharField(default=None, max_length=10, null=True, verbose_name='\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442 \u0438\u0433\u0440\u043e\u043a\u0430 2', blank=True)),
                ('duel', models.ForeignKey(verbose_name='\u0414\u0443\u044d\u043b\u044c', to='hack.Duel')),
            ],
            options={
                'verbose_name': '\u0425\u043e\u0434 \u0434\u0443\u044d\u043b\u0438',
                'verbose_name_plural': '\u0425\u043e\u0434\u044b \u0434\u0443\u044d\u043b\u0435\u0439',
            },
        ),
        migrations.CreateModel(
            name='Hack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hacker', models.CharField(max_length=100, verbose_name='\u0418\u0433\u0440\u043e\u043a 1')),
                ('dt', models.DateTimeField(auto_now_add=True, verbose_name='\u041d\u0430\u0447\u0430\u043b\u043e \u0430\u0442\u0430\u043a\u0438')),
                ('number', models.CharField(max_length=10, verbose_name='\u0412\u0437\u043b\u0430\u043c\u044b\u0432\u0430\u0435\u043c\u043e\u0435 \u0447\u0438\u0441\u043b\u043e')),
                ('result', models.CharField(default=None, choices=[(None, '\u0418\u0434\u0435\u0442'), ('win', '\u0412\u0437\u043b\u043e\u043c\u0430\u043d\u043e'), ('run', '\u0421\u0431\u0435\u0436\u0430\u043b'), ('fail', '\u041e\u0431\u043b\u043e\u043c'), ('late', '\u041e\u043f\u043e\u0437\u0434\u0430\u043b')], max_length=20, blank=True, null=True, verbose_name='\u0418\u0442\u043e\u0433')),
            ],
            options={
                'verbose_name': '\u0412\u0437\u043b\u043e\u043c',
                'verbose_name_plural': '\u0412\u0437\u043b\u043e\u043c\u044b',
            },
        ),
        migrations.CreateModel(
            name='HackMove',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dt', models.DateTimeField(auto_now_add=True, verbose_name='\u041d\u0430\u0447\u0430\u043b\u043e \u0445\u043e\u0434\u0430')),
                ('move', models.CharField(default=None, max_length=10, null=True, verbose_name='\u0425\u043e\u0434', blank=True)),
                ('result', models.CharField(default=None, max_length=10, null=True, verbose_name='\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442', blank=True)),
                ('hack', models.ForeignKey(verbose_name='\u0412\u0437\u043b\u043e\u043c', to='hack.Hack')),
            ],
            options={
                'verbose_name': '\u0425\u043e\u0434 \u0432\u0437\u043b\u043e\u043c\u0430',
                'verbose_name_plural': '\u0425\u043e\u0434\u044b \u0432\u0437\u043b\u043e\u043c\u043e\u0432',
            },
        ),
    ]
