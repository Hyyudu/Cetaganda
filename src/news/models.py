# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from redactor.fields import RedactorField


class News(models.Model):
    content = RedactorField(verbose_name='Содержание')
    dt = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __unicode__(self):
        return self.content

    class Meta:
        verbose_name = 'Админская новость'
        verbose_name_plural = 'Админские новости'
        ordering = ('-dt',)
