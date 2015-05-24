# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GameField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('type', models.IntegerField(verbose_name='\u0422\u0438\u043f \u043f\u043e\u043b\u044f', choices=[(1, '\u0421\u0442\u0440\u043e\u043a\u0430'), (2, '\u0422\u0435\u043a\u0441\u0442'), (3, '\u0427\u0438\u0441\u043b\u043e'), (4, '\u0412\u0430\u0440\u0438\u0430\u043d\u0442\u044b')])),
                ('additional', models.CharField(default=None, max_length=255, blank=True, help_text='\u0414\u043b\u044f \u043f\u043e\u043b\u044f \u0432\u0430\u0440\u0438\u0430\u043d\u0442\u043e\u0432 - \u0432\u0430\u0440\u0438\u0430\u043d\u0442\u044b \u0447\u0435\u0440\u0435\u0437 \u0437\u0430\u043f\u044f\u0442\u0443\u044e', null=True, verbose_name='\u0414\u043e\u043f \u0438\u043d\u0444\u043e')),
                ('order', models.IntegerField(default=0, verbose_name='\u041f\u043e\u0440\u044f\u0434\u043e\u043a')),
                ('visibility', models.CharField(default='all', max_length=100, verbose_name='\u0423\u0440\u043e\u0432\u0435\u043d\u044c \u0432\u0438\u0434\u0438\u043c\u043e\u0441\u0442\u0438', choices=[('master', '\u041c\u0430\u0441\u0442\u0435\u0440'), ('player', '\u0418\u0433\u0440\u043e\u043a'), ('all', '\u0412\u0441\u0435')])),
                ('required', models.BooleanField(default=False, verbose_name='\u041e\u0431\u044f\u0437\u0430\u0442\u0435\u043b\u044c\u043d\u043e\u0435')),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': '\u041f\u043e\u043b\u0435 \u0438\u0433\u0440\u044b',
                'verbose_name_plural': '\u041f\u043e\u043b\u044f \u0440\u043e\u043b\u0435\u0439',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('description', models.TextField(default=None, null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('color', models.CharField(default='000000', help_text='\u0412 hex \u0444\u043e\u0440\u043c\u0430\u0442\u0435', max_length=6, verbose_name='\u0426\u0432\u0435\u0442')),
            ],
            options={
                'verbose_name': '\u0411\u043b\u043e\u043a \u0432 \u0438\u0433\u0440\u0435',
                'verbose_name_plural': '\u0411\u043b\u043e\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u0418\u043c\u044f')),
                ('is_locked', models.BooleanField(default=False, help_text='\u041c\u043e\u0436\u043d\u043e \u043b\u0438 \u0438\u0433\u0440\u043e\u043a\u0443 \u0440\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0440\u043e\u043b\u044c', verbose_name='\u0417\u0430\u043c\u043e\u0440\u043e\u0436\u0435\u043d\u0430')),
                ('group', models.ForeignKey(default=None, blank=True, to='roles.Group', null=True, verbose_name='\u0411\u043b\u043e\u043a')),
                ('user', models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c')),
            ],
            options={
                'verbose_name': '\u0420\u043e\u043b\u044c',
                'verbose_name_plural': '\u0420\u043e\u043b\u0438',
                'permissions': (('can_edit_role', '\u041c\u043e\u0436\u0435\u0442 \u0440\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0440\u043e\u043b\u0438'),),
            },
        ),
        migrations.CreateModel(
            name='RoleConnection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField(default=None, null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('is_locked', models.BooleanField(default=False, verbose_name='\u0417\u0430\u043c\u043e\u0440\u043e\u0436\u0435\u043d\u043e')),
                ('role', models.ForeignKey(related_name='roles', verbose_name='\u0420\u043e\u043b\u044c', to='roles.Role')),
                ('role_rel', models.ForeignKey(related_name='linked_roles', verbose_name='\u0421\u0432\u044f\u0437\u0430\u043d\u043d\u0430\u044f \u0440\u043e\u043b\u044c', blank=True, to='roles.Role', null=True)),
            ],
            options={
                'verbose_name': '\u0421\u0432\u044f\u0437\u044c \u0440\u043e\u043b\u0435\u0439',
                'verbose_name_plural': '\u0421\u0432\u044f\u0437\u0438 \u0440\u043e\u043b\u0435\u0439',
            },
        ),
        migrations.CreateModel(
            name='RoleField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.TextField(default=None, null=True, verbose_name='\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435', blank=True)),
                ('field', models.ForeignKey(verbose_name='\u041f\u043e\u043b\u0435', to='roles.GameField')),
                ('role', models.ForeignKey(verbose_name='\u0420\u043e\u043b\u044c', to='roles.Role')),
            ],
            options={
                'verbose_name': '\u041f\u043e\u043b\u0435 \u0440\u043e\u043b\u0438',
                'verbose_name_plural': '\u041f\u043e\u043b\u044f \u0440\u043e\u043b\u0435\u0439',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('description', models.TextField(default=None, null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('color', models.CharField(default='000000', help_text='\u0412 hex \u0444\u043e\u0440\u043c\u0430\u0442\u0435', max_length=6, verbose_name='\u0426\u0432\u0435\u0442')),
            ],
            options={
                'verbose_name': '\u0411\u043b\u043e\u043a \u0432 \u0438\u0433\u0440\u0435',
                'verbose_name_plural': '\u0411\u043b\u043e\u043a\u0438',
            },
        ),
        migrations.AddField(
            model_name='roleconnection',
            name='topic',
            field=models.ForeignKey(default=None, blank=True, to='roles.Topic', null=True, verbose_name='\u0421\u044e\u0436\u0435\u0442'),
        ),
    ]
