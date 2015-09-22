# coding: utf-8
from __future__ import unicode_literals


def refresh(obj):
    """Перезапрашивает объект из базы и возвращает новый инстанс."""
    return obj.__class__.objects.get(pk=obj.pk)
