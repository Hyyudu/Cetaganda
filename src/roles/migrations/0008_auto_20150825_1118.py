# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def market_role(apps, schema_editor, with_create_permissions=True):
     Role = apps.get_model('roles', 'Role')
     Role.objects.create(
         name='market',
         is_hidden=True,
     )


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0007_role_is_hidden'),
    ]

    operations = [
        migrations.RunPython(market_role),
    ]
