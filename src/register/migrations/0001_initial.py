# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0009_auto_20150904_0025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=255, verbose_name='\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f')),
                ('message', models.TextField(verbose_name='\u0421\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435')),
                ('dt', models.DateTimeField(auto_now_add=True)),
                ('role', models.ForeignKey(verbose_name='\u0420\u043e\u043b\u044c', to='roles.Role')),
            ],
            options={
                'ordering': ('-dt',),
                'verbose_name': '\u0417\u0430\u043f\u0438\u0441\u044c',
                'verbose_name_plural': '\u0416\u0443\u0440\u043d\u0430\u043b',
            },
        ),
    ]
