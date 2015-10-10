# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='role',
            field=models.ForeignKey(related_name='records', verbose_name='\u0420\u043e\u043b\u044c', to='roles.Role'),
        ),
    ]
