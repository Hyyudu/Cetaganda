# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('buyer', models.CharField(max_length=255, verbose_name='\u041a\u0442\u043e \u043f\u043e\u043a\u0443\u043f\u0430\u043b')),
                ('product', models.CharField(max_length=255, verbose_name='\u0427\u0442\u043e \u043a\u0443\u043f\u043b\u0435\u043d\u043e')),
                ('cost', models.IntegerField(verbose_name='\u0421\u0442\u043e\u0438\u043c\u043e\u0441\u0442\u044c')),
                ('dt', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '\u041f\u043e\u043a\u0443\u043f\u043a\u0430',
                'verbose_name_plural': '\u041f\u043e\u043a\u0443\u043f\u043a\u0438',
            },
        ),
    ]
