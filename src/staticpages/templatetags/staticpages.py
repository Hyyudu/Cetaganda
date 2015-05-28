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


@register.inclusion_tag('staticpages/top_menu.html')
def top_menu():
    return {'articles': Article.objects.filter(top_menu=True).order_by('order')}


@register.inclusion_tag('staticpages/chapter_menu.html', takes_context=True)
def chapter_menu(context, article):
    children = Article.objects.filter(parent=article).order_by('order')
    if not children.exists():
        return {'article': article, 'request': context['request']}

    return {'article': article, 'request': context['request'], 'children': children}
