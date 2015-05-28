# coding: utf-8
from __future__ import unicode_literals

from django.contrib import admin

from . import models


class GameFieldAdmin(admin.ModelAdmin):
    list_filter = ('name', 'type', 'visibility')
    ordering = ('order',)


class RoleConnectionInline(admin.TabularInline):
    model = models.RoleConnection
    fk_name = 'role'
    extra = 0


class RoleFieldInline(admin.TabularInline):
    model = models.RoleField
    fk_name = 'role'
    extra = 0


class RoleAdmin(admin.ModelAdmin):
    list_display = ('username',)
    inlines = (RoleFieldInline, RoleConnectionInline,)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'created', 'is_readed')
    raw_id_fields = ('sender', 'recipient')


admin.site.register(models.GameField, GameFieldAdmin)
admin.site.register(models.Group)
admin.site.register(models.Topic)
admin.site.register(models.Role, RoleAdmin)
