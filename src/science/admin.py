# coding: utf-8
from __future__ import unicode_literals

from django.contrib import admin

from science import models


class InventionAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'base', 'change', 'action')
    list_filter = ('author',)


class ProductionAdmin(admin.ModelAdmin):
    list_display = ('owner', 'invention')
    list_filter = ('owner',)


admin.site.register(models.Store)
admin.site.register(models.Invention, InventionAdmin)
admin.site.register(models.Production, ProductionAdmin)
