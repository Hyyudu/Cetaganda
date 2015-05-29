# encoding: utf-8

from django import template
from django.conf import settings

from ..models import News

register = template.Library()


@register.inclusion_tag('news/last_news.html')
def last_news():
    return {'news': News.objects.all()[:getattr(settings, 'LAST_NEWS_AMOUNT', 10)]}
