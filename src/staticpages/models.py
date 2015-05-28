# coding: utf-8

from django.core.urlresolvers import reverse
from django.db import models

from redactor.fields import RedactorField


class Article(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, default=None)
    title = models.CharField(verbose_name=u"Заголовок", max_length=100)
    content = RedactorField(verbose_name=u"Содержание")
    url = models.CharField(verbose_name=u"Ссылка", max_length=255, null=True, blank=True, default=None,
                           help_text=u"Вместо отображения текста будет переход по ссылке")
    order = models.PositiveSmallIntegerField(verbose_name=u"Порядок", default=100)
    top_menu = models.BooleanField(verbose_name=u"В верхнем меню", default=False)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        if self.url:
            return self.url
        else:
            return reverse('article', args=[self.id])

    def get_head(self):
        if self.parent:
            return self.parent.get_head()
        else:
            return self

    class Meta:
        verbose_name = u"Страница"
        verbose_name_plural = u"Страницы"
        ordering = ('order',)
