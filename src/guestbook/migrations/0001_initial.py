# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0009_auto_20150904_0025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(verbose_name='\u0421\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435')),
                ('dt', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('author', models.ForeignKey(to='roles.Role')),
            ],
            options={
                'ordering': ('-dt',),
                'verbose_name': '\u041f\u043e\u0441\u0442',
                'verbose_name_plural': '\u041f\u043e\u0441\u0442\u044b',
            },
        ),
    ]
