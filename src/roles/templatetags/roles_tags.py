# encoding: utf-8
from __future__ import unicode_literals

from django import template
from django.db.models import Q

from roles import models

register = template.Library()


@register.filter
def nick(user):
    try:
        return models.UserInfo.objects.get(Q(ulogin__user=user) | Q(user=user)).nick or u'??'
    except models.UserInfo.DoesNotExist:
        return '??'
