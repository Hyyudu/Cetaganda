# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from roles.models import Role


class Record(models.Model):
    role = models.ForeignKey(Role, verbose_name='Роль')
    category = models.CharField(verbose_name='Категория', max_length=255)
    message = models.TextField(verbose_name='Сообщение')
    dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Журнал'
        ordering = ('-dt',)
