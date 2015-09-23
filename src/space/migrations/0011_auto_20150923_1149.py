# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from simplejson import dumps


def convert_planets(apps, schema_editor, with_create_permissions=True):
    Point = apps.get_model('space', 'Point')
    for point in Point.objects.all():
        if not point.resources:
            continue

        resources = list(point.resources)
        point.resources = dumps(resources)
        point.save()


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0010_auto_20150923_1149'),
    ]

    operations = [
        migrations.RunPython(convert_planets),
    ]
