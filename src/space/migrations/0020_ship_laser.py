# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0019_auto_20151011_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='ship',
            name='laser',
            field=models.BooleanField(default=False, verbose_name='\u041b\u0430\u0437\u0435\u0440'),
        ),
    ]
