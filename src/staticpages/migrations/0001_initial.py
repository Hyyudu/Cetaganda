# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a')),
                ('content', redactor.fields.RedactorField(verbose_name='\u0421\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435')),
                ('url', models.CharField(default=None, max_length=255, blank=True, help_text='\u0412\u043c\u0435\u0441\u0442\u043e \u043e\u0442\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u044f \u0442\u0435\u043a\u0441\u0442\u0430 \u0431\u0443\u0434\u0435\u0442 \u043f\u0435\u0440\u0435\u0445\u043e\u0434 \u043f\u043e \u0441\u0441\u044b\u043b\u043a\u0435', null=True, verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430')),
                ('order', models.PositiveSmallIntegerField(default=100, verbose_name='\u041f\u043e\u0440\u044f\u0434\u043e\u043a')),
                ('top_menu', models.BooleanField(default=False, verbose_name='\u0412 \u0432\u0435\u0440\u0445\u043d\u0435\u043c \u043c\u0435\u043d\u044e')),
                ('parent', models.ForeignKey(default=None, blank=True, to='staticpages.Article', null=True)),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': '\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u0430',
                'verbose_name_plural': '\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u044b',
            },
        ),
    ]
