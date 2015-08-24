# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0006_auto_20150809_1522'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('dt', models.DateTimeField(auto_now_add=True)),
                ('is_finished', models.BooleanField(default=False, verbose_name='\u0417\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u0430')),
                ('cost', models.PositiveIntegerField(default=0, verbose_name='\u0421\u0442\u043e\u0438\u043c\u043e\u0441\u0442\u044c')),
                ('buyer', models.ForeignKey(related_name='buyer', default=None, verbose_name='\u041f\u043e\u043a\u0443\u043f\u0430\u0442\u0435\u043b\u044c', to='roles.Role', null=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('seller', models.ForeignKey(related_name='seller', verbose_name='\u041f\u0440\u043e\u0434\u0430\u0432\u0435\u0446', to='roles.Role')),
            ],
            options={
                'verbose_name': '\u0422\u043e\u0432\u0430\u0440',
                'verbose_name_plural': '\u0422\u043e\u0432\u0430\u0440\u044b',
            },
        ),
    ]
