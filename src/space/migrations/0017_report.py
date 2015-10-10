# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0016_picture_dt'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(verbose_name='\u041e\u0442\u0447\u0435\u0442')),
                ('dt', models.DateTimeField(auto_now_add=True, verbose_name='\u0412\u0440\u0435\u043c\u044f')),
            ],
            options={
                'ordering': ('-dt',),
                'verbose_name': '\u041e\u0442\u0447\u0435\u0442',
                'verbose_name_plural': '\u041e\u0442\u0447\u0435\u0442\u044b',
            },
        ),
    ]
