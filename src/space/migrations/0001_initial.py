# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0008_auto_20150825_1118'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alliance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('role_name', models.CharField(max_length=100, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0443 \u0440\u043e\u043b\u0438')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': '\u0410\u043b\u044c\u044f\u043d\u0441',
                'verbose_name_plural': '\u0410\u043b\u044c\u044f\u043d\u0441\u044b',
            },
        ),
        migrations.CreateModel(
            name='Fleet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('navigator', models.ForeignKey(verbose_name='\u041d\u0430\u0432\u0438\u0433\u0430\u0442\u043e\u0440', to='roles.Role')),
            ],
            options={
                'verbose_name': '\u0424\u043b\u043e\u0442',
                'verbose_name_plural': '\u0424\u043b\u043e\u0442\u0430',
            },
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=20, verbose_name='\u0422\u0438\u043f', choices=[('planet', '\u041f\u043b\u0430\u043d\u0435\u0442\u0430'), ('transit', 'PV-\u043f\u0435\u0440\u0435\u0445\u043e\u0434')])),
                ('name', models.CharField(max_length=100, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('resources', models.CharField(default='', max_length=10, verbose_name='\u0420\u0435\u0441\u0443\u0440\u0441\u044b', blank=True)),
                ('alliance', models.ForeignKey(verbose_name='\u0410\u043b\u044c\u044f\u043d\u0441', to='space.Alliance')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': '\u0422\u043e\u0447\u043a\u0430',
                'verbose_name_plural': '\u0422\u043e\u0447\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='Ship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_space', models.BooleanField(default=False, verbose_name='\u0412 \u043a\u043e\u0441\u043c\u043e\u0441\u0435')),
                ('type', models.CharField(max_length=1, verbose_name='\u0422\u0438\u043f', choices=[('s', '\u0421\u0442\u0430\u043d\u0446\u0438\u044f'), ('k', '\u041a\u0440\u0435\u0439\u0441\u0435\u0440'), ('r', '\u0420\u0430\u0437\u0432\u0435\u0434\u0447\u0438\u043a'), ('l', '\u041b\u0438\u043d\u043a\u043e\u0440'), ('t', '\u0422\u0440\u0430\u043d\u0441\u043f\u043e\u0440\u0442')])),
                ('name', models.CharField(max_length=100, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('resources', models.CharField(default='', max_length=10, verbose_name='\u0420\u0435\u0441\u0443\u0440\u0441\u044b', blank=True)),
                ('diplomats', models.ManyToManyField(related_name='responsible_for', verbose_name='\u0414\u0438\u043f\u043b\u043e\u043c\u0430\u0442\u044b', to='roles.Role')),
                ('fleet', models.ForeignKey(default=None, blank=True, to='space.Fleet', null=True, verbose_name='\u0424\u043b\u043e\u0442')),
                ('owner', models.ForeignKey(related_name='ships', verbose_name='\u0412\u043b\u0430\u0434\u0435\u043b\u0435\u0446', to='roles.Role')),
                ('position', models.ForeignKey(default=None, blank=True, to='space.Point', null=True, verbose_name='\u041f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u041a\u043e\u0440\u0430\u0431\u043b\u044c',
                'verbose_name_plural': '\u041a\u043e\u0440\u0430\u0431\u043b\u0438',
            },
        ),
        migrations.CreateModel(
            name='Transit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('point1', models.ForeignKey(related_name='point_from', verbose_name='\u043e\u0442\u043a\u0443\u0434\u0430', to='space.Point')),
                ('point2', models.ForeignKey(related_name='point_to', verbose_name='\u043a\u0443\u0434\u0430', to='space.Point')),
            ],
            options={
                'verbose_name': '\u041f\u0435\u0440\u0435\u0445\u043e\u0434',
                'verbose_name_plural': '\u041f\u0435\u0440\u0435\u0445\u043e\u0434\u044b',
            },
        ),
        migrations.AddField(
            model_name='fleet',
            name='point',
            field=models.ForeignKey(verbose_name='\u041f\u043e\u0437\u0438\u0446\u0438\u044f', to='space.Point'),
        ),
    ]
