# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.conf import settings

from space import models
from roles.models import Role
from space.tactics import move_fleets


@admin.register(models.Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ('type', 'name', 'alliance', 'resources')
    ordering = ('name', 'type')
    list_filter = ('type', 'alliance')


@admin.register(models.Alliance)
class AllianceAdmin(admin.ModelAdmin):
    list_display = ('name', 'resources')
    actions = ['clean']

    def clean(self, request, queryset):
        models.Ship.objects.all().delete()
        models.Fleet.objects.all().delete()
        for role in Role.objects.all():
            role.set_field(settings.MONEY_FIELD, 150000)
            role.records.create(category='Космос', message='Регата началась')
        models.Alliance.objects.all().update(resources='{}')
        models.Point.objects.filter(type='transit').update(resources='{}')
        for planet in models.Point.objects.filter(type='planet'):
            planet.resources = [r for r in (planet.resources or []) if 'баран' not in r] + \
                               ['баран с планеты %s' % planet.name]
            planet.save()
    clean.short_description = 'Обнулить корабли'


@admin.register(models.Transit)
class TransitAdmin(admin.ModelAdmin):
    list_display = ('point1', 'point2')
    raw_id_fields = ('point1', 'point2')


@admin.register(models.Fleet)
class FleetAdmin(admin.ModelAdmin):
    list_display = ('name', 'point', 'navigator', 'ships_amount')
    actions = ['turn', 'clean']

    def turn(self, request, queryset):
        move_fleets()
    turn.short_description = 'Запустить фазу перемещений'

    def clean(self, request, queryset):
        for fleet in models.Fleet.objects.all():
            if not fleet.ship_set.exists():
                fleet.delete()
    clean.short_description = 'Удалить пустые флоты'


@admin.register(models.Ship)
class ShipAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'type', 'in_space', 'position', 'is_alive')
    raw_id_fields = ('diplomats',)

    def get_queryset(self, request):
        return models.Ship.all


@admin.register(models.Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('requester', 'point', 'direction', 'photo')
    raw_id_fields = ('requester', 'point')


@admin.register(models.Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('dt', 'is_done')
    list_filter = ('is_done',)
