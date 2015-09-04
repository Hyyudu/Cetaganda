# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0005_point_is_major'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ship',
            options={'verbose_name': '\u041a\u043e\u0440\u0430\u0431\u043b\u044c', 'verbose_name_plural': '\u041a\u043e\u0440\u0430\u0431\u043b\u0438', 'permissions': (('can_edit_ship', '\u041c\u043e\u0436\u0435\u0442 \u0440\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u043a\u043e\u0440\u0430\u0431\u043b\u0438'),)},
        ),
        migrations.RemoveField(
            model_name='point',
            name='is_major',
        ),
        migrations.AddField(
            model_name='ship',
            name='home',
            field=models.ForeignKey(related_name='home', default=None, blank=True, to='space.Point', null=True, verbose_name='\u041f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='ship',
            name='position',
            field=models.ForeignKey(related_name='position', default=None, blank=True, to='space.Point', null=True, verbose_name='\u041f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='ship',
            name='resources',
            field=jsonfield.fields.JSONField(default='{}', verbose_name='\u0420\u0435\u0441\u0443\u0440\u0441\u044b'),
        ),
    ]
