# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Expense(models.Model):
    buyer = models.CharField(verbose_name='Кто покупал', max_length=255)
    product = models.CharField(verbose_name='Что куплено', max_length=255)
    cost = models.IntegerField(verbose_name='Стоимость')
    dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
