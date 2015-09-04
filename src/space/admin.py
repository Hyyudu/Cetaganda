from __future__ import unicode_literals

from django.contrib import admin
from space import models


@admin.register(models.Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ('type', 'name', 'alliance', 'resources')
    ordering = ('name', 'type')
    list_filter = ('type', 'alliance')


@admin.register(models.Alliance)
class AllianceAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(models.Transit)
class TransitAdmin(admin.ModelAdmin):
    list_display = ('point1', 'point2')


@admin.register(models.Fleet)
class FleetAdmin(admin.ModelAdmin):
    list_display = ('name', 'point', 'navigator', 'ships_amount')


@admin.register(models.Ship)
class ShipAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'type', 'in_space', 'position', 'is_alive')
    raw_id_fields = ('diplomats',)

    def get_queryset(self, request):
        return models.Ship.all
