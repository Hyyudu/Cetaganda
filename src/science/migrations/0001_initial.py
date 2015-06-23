# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import science.models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0004_auto_20150621_1703'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invention',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('hash', models.CharField(max_length=255, verbose_name='\u0425\u044d\u0448')),
                ('action', models.CharField(default=None, max_length=255, null=True, verbose_name='\u0414\u0435\u0439\u0441\u0442\u0432\u0438\u0435', blank=True)),
                ('base_coded', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('change_coded', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('author', models.ForeignKey(verbose_name='\u0410\u0432\u0442\u043e\u0440', to='roles.Role')),
            ],
            options={
                'verbose_name': '\u0418\u0437\u043e\u0431\u0440\u0435\u0442\u0435\u043d\u0438\u0435',
                'verbose_name_plural': '\u0418\u0437\u043e\u0431\u0440\u0435\u0442\u0435\u043d\u0438\u044f',
            },
        ),
        migrations.CreateModel(
            name='Production',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hash', models.CharField(max_length=255, verbose_name='\u0425\u044d\u0448')),
                ('invention', models.ForeignKey(verbose_name='\u0418\u0437\u043e\u0431\u0440\u0435\u0442\u0435\u043d\u0438\u0435', to='science.Invention')),
                ('owner', models.ForeignKey(verbose_name='\u0412\u043b\u0430\u0434\u0435\u043b\u0435\u0446', to='roles.Role')),
            ],
            options={
                'verbose_name': '\u0418\u0437\u043e\u0431\u0440\u0435\u0442\u0435\u043d\u0438\u0435',
                'verbose_name_plural': '\u0418\u0437\u043e\u0431\u0440\u0435\u0442\u0435\u043d\u0438\u044f',
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('goods', science.models.JSONField(default='{}', verbose_name='\u0425\u0430\u0431\u0430\u0440')),
                ('author', models.OneToOneField(verbose_name='\u0412\u043b\u0430\u0434\u0435\u043b\u0435\u0446', to='roles.Role')),
            ],
            options={
                'verbose_name': '\u0421\u043a\u043b\u0430\u0434',
                'verbose_name_plural': '\u0421\u043a\u043b\u0430\u0434',
            },
        ),
    ]
