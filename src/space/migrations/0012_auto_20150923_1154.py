# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0011_auto_20150923_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='point',
            name='resources',
            field=jsonfield.fields.JSONField(default='{}', verbose_name='\u0420\u0435\u0441\u0443\u0440\u0441\u044b'),
        ),
    ]
