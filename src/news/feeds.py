# -*- coding:utf-8 -*-
from django.contrib.syndication.views import Feed
from django.conf import settings
from .models import News


class NewsFeed(Feed):
    """Новости"""
    title = u"Уралкон: новости"
    link = "http://%s" % settings.DOMAIN
    author_name = "Уралкон"

    def items(self, obj):
        return News.objects.all()[:20]

    def item_pubdate(self, item):
        return item.dt

    def item_title(self, item):
        return ""

    def item_link(self, item):
        return "http://%s/news/" % settings.DOMAIN
