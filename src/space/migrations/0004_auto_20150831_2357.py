# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0003_auto_20150831_2319'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ship',
            old_name='is_space',
            new_name='in_space',
        ),
    ]
