# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from guestbook.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'dt')
