# coding: utf-8

from django import template
from ..models import Article

register = template.Library()


@register.simple_tag()
def content(article_id):
    try:
        if isinstance(article_id, int) or article_id.isdigit():
            return Article.objects.get(pk=article_id).content
        else:
            return Article.objects.get(title=article_id).content

    except Article.DoesNotExist:
        return ""


@register.inclusion_tag('top_menu.html')
def top_menu():
    return {'articles': Article.objects.filter(top_menu=True).order_by('order')}
