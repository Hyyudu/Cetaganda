# -*- coding: utf-8 -*-
from django.db import models

from redactor.fields import RedactorField


class News(models.Model):
    content = RedactorField(verbose_name=u"Содержание")
    dt = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата создания")

    def __unicode__(self):
        return self.content

    class Meta:
        verbose_name = u"Админская новость"
        verbose_name_plural = u"Админские новости"
        ordering = ('-dt',)
