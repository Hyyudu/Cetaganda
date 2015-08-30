# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from roles.models import Role


class Alliance(models.Model):
    name = models.CharField(verbose_name='Название', max_length=100)
    role_name = models.CharField(verbose_name='Название у роли', max_length=100)

    class Meta:
        verbose_name = 'Альянс'
        verbose_name_plural = 'Альянсы'
        ordering = ('name',)


class Point(models.Model):
    """Планеты"""
    TYPES = (
        ('planet', 'Планета'),
        ('transit', 'PV-переход'),
    )
    type = models.CharField(verbose_name='Тип', max_length=20, choices=TYPES)
    alliance = models.ForeignKey(Alliance, verbose_name='Альянс')
    name = models.CharField(verbose_name='Название', max_length=100)
    resources = models.CharField(verbose_name='Ресурсы', max_length=10, blank=True, default='')

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.type)

    class Meta:
        verbose_name = 'Точка'
        verbose_name_plural = 'Точки'
        ordering = ('name',)


class Transit(models.Model):
    point1 = models.ForeignKey(Point, verbose_name='откуда', related_name='point_from')
    point2 = models.ForeignKey(Point, verbose_name='куда', related_name='point_to')

    class Meta:
        verbose_name = 'Переход'
        verbose_name_plural = 'Переходы'


class Fleet(models.Model):
    name = models.CharField(verbose_name='Название', max_length=100)
    point = models.ForeignKey(Point, verbose_name='Позиция')
    navigator = models.ForeignKey(Role, verbose_name='Навигатор')

    class Meta:
        verbose_name = 'Флот'
        verbose_name_plural = 'Флота'


SHIPS = {
    'l': {
        'name': 'Линкор',
        'distance': 1,
        'hit': '56789',
        'cost': 1000,
    },
    'k': {
        'name': 'Крейсер',
        'distance': 2,
        'hit': '1234',
        'cost': 2000,
    },
    's': {
        'name': 'Станция',
        'distance': 0,
        'hit': '2468',
        'cost': 1500,
    },
    'r': {
        'name': 'Разведчик',
        'distance': 2,
        'hit': '150',
        'cost': 300,
    },
    't': {
        'name': 'Транспорт',
        'distance': 1,
        'hit': '37',
        'cost': 2000,
    },
}

SHIP_TYPES = ((k, v['name']) for k, v in SHIPS.items())


class Ship(models.Model):
    owner = models.ForeignKey(Role, verbose_name='Владелец', related_name='ships')
    is_space = models.BooleanField(verbose_name='В космосе', default=False)
    fleet = models.ForeignKey(Fleet, verbose_name='Флот', null=True, blank=True, default=None)
    position = models.ForeignKey(Point, verbose_name='Положение', null=True, blank=True, default=None)
    type = models.CharField(verbose_name='Тип', max_length=1, choices=SHIP_TYPES)
    name = models.CharField(verbose_name='Название', max_length=100)
    resources = models.CharField(verbose_name='Ресурсы', max_length=10, blank=True, default='')  # для транспорта
    diplomats = models.ManyToManyField(Role, verbose_name='Дипломаты', related_name='responsible_for')

    class Meta:
        verbose_name = 'Корабль'
        verbose_name_plural = 'Корабли'
