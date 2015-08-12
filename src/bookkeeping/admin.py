from __future__ import unicode_literals

from django.contrib import admin
from bookkeeping import models


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'product', 'cost', 'dt')
    ordering = ('-dt',)

admin.site.register(models.Expense, ExpenseAdmin)
