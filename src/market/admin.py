from __future__ import unicode_literals

from django.contrib import admin
from market import models


class GoodsAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'buyer', 'cost', 'dt', 'is_finished')


admin.site.register(models.Goods, GoodsAdmin)
