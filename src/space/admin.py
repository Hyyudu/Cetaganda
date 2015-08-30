from __future__ import unicode_literals

from django.contrib import admin
from space import models


@admin.register(models.Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ('type', 'name', 'alliance', 'resources')
    ordering = ('name', 'type')


@admin.register(models.Alliance)
class AllianceAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(models.Transit)
class TransitAdmin(admin.ModelAdmin):
    list_display = ('point1', 'point2')
