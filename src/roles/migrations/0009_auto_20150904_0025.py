# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

from django.db import models, migrations


def fix_fields(apps, schema_editor, with_create_permissions=True):
     RoleField = apps.get_model('roles', 'RoleField')
     for field in RoleField.objects.all():
         if field.field.type == 4 and field.value is not None:
             field.value = re.split('\s*,\s*', field.field.additional)[int(field.value)].strip()
             field.save()


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0008_auto_20150825_1118'),
    ]

    operations = [
        migrations.RunPython(fix_fields),
    ]
