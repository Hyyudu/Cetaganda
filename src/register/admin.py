from __future__ import unicode_literals

from django.contrib import admin
from register import models


@admin.register(models.Record)
class PointAdmin(admin.ModelAdmin):
    list_display = ('role', 'category', 'message')
    ordering = ('-dt',)
    list_filter = ('role', 'category')
