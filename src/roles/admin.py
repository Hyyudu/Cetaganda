# coding: utf-8
from __future__ import unicode_literals

from django.contrib import admin

from django_ulogin import models as ulogin_models
from . import models


class MasterInline(admin.TabularInline):
    model = models.Master
    extra = 0


class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'paid')
    inlines = (MasterInline,)


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


admin.site.register(models.Game, GameAdmin)
admin.site.register(models.Role, RoleAdmin)
admin.site.register(models.UserInfo)
admin.site.register(ulogin_models.ULoginUser)
