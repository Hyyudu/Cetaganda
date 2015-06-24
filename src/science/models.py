# coding: utf-8
from __future__ import unicode_literals

from collections import Counter
from uuid import uuid4
import simplejson

from django.db import models

from roles.models import Role


class JSONField(models.TextField):
    """ Поле для хранения данных, сериализованных в JSON. """
    __metaclass__ = models.SubfieldBase

    editable = False
    serialize = False

    class JSONDict(dict):
        def __str__(self):
            return simplejson.dumps(self, sort_keys=True)

    class JSONList(list):
        def __str__(self):
            return simplejson.dumps(self, sort_keys=True)

    def get_prep_value(self, value):
        if value is not None:
            return simplejson.dumps(value, sort_keys=True)

    def to_python(self, value):
        if value is None:
            return value
        elif not isinstance(value, basestring):
            return value
        if value:
            try:
                value = simplejson.loads(value)
                if isinstance(value, list):
                    value = self.JSONList(value)
                elif isinstance(value, dict):
                    value = self.JSONDict(value)
                return value
            except ValueError:
                # If value can't be decoded, output it as string
                return value
        return None


class Store(models.Model):
    owner = models.OneToOneField(Role, verbose_name='Владелец')
    goods = JSONField(verbose_name='Хабар', default='{}')

    def items(self):
        for letter in 'бЗзКкСсЖж':
            yield letter, self.goods.get(letter, 0)

    def __unicode__(self):
        return unicode(self.owner)

    @classmethod
    def get_or_create(cls, role):
        try:
            return role.store
        except cls.DoesNotExist:
            return cls.objects.create(owner=role, goods={})

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склад'


class Invention(models.Model):
    author = models.ForeignKey(Role, verbose_name='Автор')
    name = models.CharField(verbose_name='Название', max_length=255)
    hash = models.CharField(verbose_name='Хэш', max_length=255)
    action = models.CharField(verbose_name='Действие', max_length=255, null=True, blank=True, default=None)
    base_coded = models.CharField(verbose_name='Основание', max_length=255)
    base = models.CharField(verbose_name='Основание', max_length=255)
    change_coded = models.CharField(verbose_name='Изменение', max_length=255)
    change = models.CharField(verbose_name='Изменение', max_length=255)

    def __unicode__(self):
        return self.name

    @property
    def cost(self):
        counter = Counter(self.change_coded)
        return ', '.join('%s %s' % (v, k) for k, v in counter.items())

    def enough_store(self):
        store = self.author.store
        for color, amount in Counter(self.change_coded).items():
            if store.goods.get(color, 0) < amount:
                return False
        return True

    def produce(self):
        Production.objects.create(
            owner=self.author,
            invention=self,
            hash=uuid4().hex,
        )

        store = self.author.store
        for color, amount in Counter(self.change_coded).items():
            store.goods[color] = store.goods.get(color, 0) - amount
        store.save()

    class Meta:
        verbose_name = 'Изобретение'
        verbose_name_plural = 'Изобретения'


class Production(models.Model):
    owner = models.ForeignKey(Role, verbose_name='Владелец')
    invention = models.ForeignKey(Invention, verbose_name='Изобретение')
    hash = models.CharField(verbose_name='Хэш', max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Изделие'
        verbose_name_plural = 'Изделия'
