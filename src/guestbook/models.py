# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from roles.models import Role


class Post(models.Model):
    author = models.ForeignKey(Role)
    content = models.TextField(verbose_name='Содержание')
    dt = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __unicode__(self):
        return self.content

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-dt',)
