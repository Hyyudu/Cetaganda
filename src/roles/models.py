# coding: utf-8
from __future__ import unicode_literals

import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.core.urlresolvers import reverse

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


class Game(models.Model):
    owner = models.ForeignKey(AUTH_USER_MODEL, verbose_name='Мастер')
    title = models.CharField(verbose_name='Название', max_length=255)
    allrpg = models.CharField(verbose_name='Ссылка на allrpg.r', max_length=255, null=True, blank=True, default=None)
    start = models.DateField(verbose_name='Дата начала', null=True, blank=True, default=None,
                             help_text='В виде 2015-01-31')
    description = models.TextField(verbose_name='Описание', null=True, blank=True, default=None)
    paid = models.BooleanField(verbose_name='Оплачено', default=False)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('game', args=[self.pk])

    def is_master(self, user):
        if not user.is_authenticated():
            return False

        if user.is_superuser or user == self.owner or self.pk == 1:
            return True

        if self.master_set.filter(user=user).exists():
            return True

        return False

    def is_paid(self):
        return self.paid or self.pk == 1

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'


class Master(models.Model):
    game = models.ForeignKey(Game, verbose_name='Игра')
    user = models.ForeignKey(AUTH_USER_MODEL, verbose_name='Мастер')

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'


class GameField(models.Model):
    TYPES = (
        (1, 'Строка'),
        (2, 'Текст'),
        (3, 'Число'),
        (4, 'Варианты'),
    )
    game = models.ForeignKey(Game, verbose_name='Игра')
    name = models.CharField(verbose_name='Название', max_length=255)
    type = models.IntegerField(verbose_name='Тип поля', choices=TYPES)
    additional = models.CharField(verbose_name='Доп инфо', max_length=255, null=True, blank=True, default=None,
                                  help_text='Для поля вариантов - варианты через запятую')
    order = models.IntegerField(verbose_name='Порядок', default=0)
    visibility = models.CharField(
        verbose_name='Уровень видимости',
        max_length=100,
        choices=(('master', 'Мастер'), ('player', 'Игрок'), ('all', 'Все')),
        default='all',
    )

    class Meta:
        verbose_name = 'Поле игры'
        verbose_name_plural = 'Поля ролей'
        ordering = ('game', 'order')


class Group(models.Model):
    """Группировка ролей"""
    game = models.ForeignKey(Game, verbose_name='Игра')
    name = models.CharField(verbose_name='Название', max_length=255)
    description = models.TextField(verbose_name='Описание', null=True, blank=True, default=None)
    color = models.CharField(verbose_name='Цвет', default='000000', max_length=6, help_text='В hex формате')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Блок в игре'
        verbose_name_plural = 'Блоки'


class Topic(models.Model):
    """Сюжет для связей ролей"""
    game = models.ForeignKey(Game, verbose_name='Игра')
    name = models.CharField(verbose_name='Название', max_length=255)
    description = models.TextField(verbose_name='Описание', null=True, blank=True, default=None)
    color = models.CharField(verbose_name='Цвет', default='000000', max_length=6, help_text='В hex формате')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Блок в игре'
        verbose_name_plural = 'Блоки'


class Role(models.Model):
    game = models.ForeignKey(Game, verbose_name='Игра')
    group = models.ForeignKey(Group, verbose_name='Блок', null=True, blank=True, default=None)
    user = models.ForeignKey(AUTH_USER_MODEL, verbose_name='Пользователь', null=True, blank=True, default=None)
    name = models.CharField(verbose_name='Имя', max_length=255)
    is_locked = models.BooleanField(verbose_name='Заморожена', default=False,
                                    help_text='Можно ли человеку редактировать роль')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('role', args=[self.id])

    def username(self):
        if not self.user:
            return '-'
        userinfo = UserInfo.objects.get(ulogin__user=self.user)
        name = '%s %s' % (self.user.last_name, self.user.first_name)
        if userinfo.nick:
            name += ' (%s)' % userinfo.nick
        return name
    username.short_description = 'Игрок'

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'


class RoleField(models.Model):
    role = models.ForeignKey(Role, verbose_name='Роль')
    field = models.ForeignKey(GameField, verbose_name='Поле')
    value = models.TextField(verbose_name='Значение', null=True, blank=True, default=None)

    def get_value(self):
        if self.field.type == 4:
            try:
                return self.field.additional.split(',')[int(self.value)].strip()
            except IndexError:
                return '-'
        else:
            return self.value

    class Meta:
        verbose_name = 'Поле роли'
        verbose_name_plural = 'Поля ролей'


class RoleConnection(models.Model):
    role = models.ForeignKey(Role, verbose_name='Роль', related_name='roles')
    role_rel = models.ForeignKey(Role, verbose_name='Связанная роль',
                                 related_name='linked_roles', null=True, blank=True)
    comment = models.TextField(verbose_name='Описание', null=True, blank=True, default=None)
    topic = models.ForeignKey(Topic, verbose_name='Сюжет', null=True, blank=True, default=None)
    is_locked = models.BooleanField(verbose_name='Заморожено', default=False)

    class Meta:
        verbose_name = 'Связь ролей'
        verbose_name_plural = 'Связи ролей'
