# coding: utf-8
from __future__ import unicode_literals

import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from django_ulogin.models import ULoginUser
from django_ulogin.signals import assign

ALBUM = getattr(settings, 'YAFOTKI_ALBUM', 'default')

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class UserInfo(models.Model):
    SEX_FEMALE = 1
    SEX_MALE = 2

    ulogin = models.ForeignKey(ULoginUser, null=True, blank=True, default=None)
    user = models.ForeignKey(AUTH_USER_MODEL, null=True, blank=True, default=None)
    nick = models.CharField(verbose_name='Ник', blank=True, default='', max_length=255)
    age = models.IntegerField(verbose_name='Возраст', blank=True, null=True, default=None)
    sex = models.IntegerField(blank=True, null=True, choices=((SEX_MALE, 'male'), (SEX_FEMALE, 'female')))
    phone = models.CharField(blank=True, default='', max_length=255)
    city = models.CharField(blank=True, default='', max_length=255)
    med = models.TextField(verbose_name='Медицина', default='')


def catch_ulogin_signal(*args, **kwargs):
    user = kwargs['user']
    json = kwargs['ulogin_data']
    ulogin = kwargs['ulogin_user']

    if kwargs['registered']:
        user.first_name = json['first_name']
        user.last_name = json['last_name']
        user.save()

        data = {'ulogin': ulogin}

        for fld in ['sex', 'city']:
            if fld not in json:
                continue
            data[fld] = json[fld]

        UserInfo.objects.create(**data)

assign.connect(catch_ulogin_signal, sender=ULoginUser, dispatch_uid='customize.models')


def create_user(request, ulogin_response):
    User = get_user_model()
    return User.objects.create_user(
        username=uuid.uuid4().hex[:30],
        password=get_random_string(20, '0123456789abcdefghijklmnopqrstuvwxyz'),
        email='',
    )
