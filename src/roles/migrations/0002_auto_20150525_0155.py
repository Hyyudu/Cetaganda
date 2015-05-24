# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def make_permissions(apps, schema_editor, with_create_permissions=True):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    try:
        perm = Permission.objects.get(codename='can_edit_role', content_type__app_label='roles')
    except Permission.DoesNotExist:
        if with_create_permissions:
            # Manually run create_permissions
            from django.contrib.auth.management import create_permissions
            assert not getattr(apps, 'models_module', None)
            apps.models_module = True
            create_permissions(apps, verbosity=0)
            apps.models_module = None
            return make_permissions(
                apps, schema_editor, with_create_permissions=False)
        else:
            raise
    my_new_group = Group.objects.create(name='Мастера')
    my_new_group.permissions.add(perm)


class Migration(migrations.Migration):
    dependencies = [
        ('roles', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(make_permissions),
    ]
