from __future__ import unicode_literals

from django.contrib import admin
from hack import models


class DuelMoveInline(admin.TabularInline):
    model = models.DuelMove
    fk_name = 'duel'
    extra = 0


class DuelAdmin(admin.ModelAdmin):
    list_display = ('role_1', 'role_2', 'state', 'winner', 'result')
    inlines = (DuelMoveInline,)


class HackMoveInline(admin.TabularInline):
    model = models.HackMove
    fk_name = 'hack'
    extra = 0


class HackAdmin(admin.ModelAdmin):
    list_display = ('hacker', 'number', 'status', 'dt')
    inlines = (HackMoveInline,)
    ordering = ('-dt',)
    search_fields = ('hacker',)


class FloatAdmin(admin.ModelAdmin):
    list_display = ('owner', 'target', 'target_level', 'is_active')
    list_filter = ('is_active',)


class TargetAdmin(admin.ModelAdmin):
    list_display = ('role', 'target', 'get_levels')


admin.site.register(models.Duel, DuelAdmin)
admin.site.register(models.Hack, HackAdmin)
admin.site.register(models.Float, FloatAdmin)
admin.site.register(models.Target, TargetAdmin)
