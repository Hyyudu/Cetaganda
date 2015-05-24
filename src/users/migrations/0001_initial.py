# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('django_ulogin', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nick', models.CharField(default='', max_length=255, verbose_name='\u041d\u0438\u043a', blank=True)),
                ('age', models.IntegerField(default=None, null=True, verbose_name='\u0412\u043e\u0437\u0440\u0430\u0441\u0442', blank=True)),
                ('sex', models.IntegerField(blank=True, null=True, choices=[(2, 'male'), (1, 'female')])),
                ('phone', models.CharField(default='', max_length=255, blank=True)),
                ('city', models.CharField(default='', max_length=255, blank=True)),
                ('med', models.TextField(default='', verbose_name='\u041c\u0435\u0434\u0438\u0446\u0438\u043d\u0430')),
                ('ulogin', models.ForeignKey(default=None, blank=True, to='django_ulogin.ULoginUser', null=True)),
                ('user', models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
