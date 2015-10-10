# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import yafotki.fields


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0009_auto_20150904_0025'),
        ('space', '0014_auto_20151010_1332'),
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('direction', models.CharField(max_length=255, verbose_name='\u041d\u0430\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435')),
                ('photo', yafotki.fields.YFField(default=None, max_length=255, null=True, upload_to='cetaganda')),
                ('point', models.ForeignKey(verbose_name='\u041e\u0442\u043a\u0443\u0434\u0430', to='space.Point')),
                ('requester', models.ForeignKey(verbose_name='\u0417\u0430\u043a\u0430\u0437\u0447\u0438\u043a', to='roles.Role')),
            ],
            options={
                'verbose_name': '\u0421\u043d\u0438\u043c\u043e\u043a',
                'verbose_name_plural': '\u0421\u043d\u0438\u043c\u043a\u0438',
            },
        ),
    ]
