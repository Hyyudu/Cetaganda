# coding: utf-8
from __future__ import unicode_literals

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Manager, Q

from roles.models import Role


class GoodsManager(Manager):
    def get_goods(self, role):
        """
        Текущие товары на продажу плюс бесконечные товары
        :param role:
        :return:
        """
        current_goods = [
            {
                'id': product.id,
                'name': product.product.market_name(),
                'description': product.product.market_description(),
                'cost': product.cost,
                'dt': product.dt,
                'seller': product.seller,
            }
            for product in super(GoodsManager, self).filter(is_finished=False)
            .filter(Q(buyer__isnull=True) | Q(buyer=role)).order_by('-dt')
        ]
        for infinite_product_class in self.model.products_classes:
            for product in infinite_product_class.get_infinite_goods():
                current_goods.append({
                    'id': product['type'],
                    'name': product['name'],
                    'description': product['description'],
                    'cost': product['cost'],
                    'dt': None,
                    'seller': None,
                    'class': self.model,
                })
        return current_goods


class Goods(models.Model):
    products_classes = []

    seller = models.ForeignKey(Role, verbose_name='Продавец', related_name='seller')
    buyer = models.ForeignKey(Role, verbose_name='Покупатель', related_name='buyer', null=True, default=None)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    product = GenericForeignKey('content_type', 'object_id')
    dt = models.DateTimeField(auto_now_add=True)
    is_finished = models.BooleanField(verbose_name='Завершена', default=False)
    cost = models.PositiveIntegerField(verbose_name='Стоимость', default=0)

    objects = GoodsManager()

    @classmethod
    def register(cls, product_class):
        cls.products_classes.append(product_class)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class MarketInterface(object):
    @classmethod
    def get_infinite_goods(cls):
        """
        :return: список словарей с описаниями товаров, которые можно покупать неограниченно
        """
        raise NotImplementedError

    @classmethod
    def get_available_for_market(self, owner):
        """
        :param owner: роль
        :return: список объектов, моторые можно выставить на продажу
        """
        raise NotImplementedError

    def market_name(self):
        """
        :return: Название товара для маркета
        """
        raise NotImplementedError

    def market_description(self):
        """
        :return: описание товара для маркета
        """
        raise NotImplementedError

    @classmethod
    def create(cls, object_type, owner):
        """
        :return: вновь созданный объект из числа бесконечных товаров
        """
        raise NotImplementedError

    def change_owner(self, owner):
        """
        Смена владельца, при покупке или при снятии с продажи
        :param owner: role - новый владелец товара
        :return:
        """
        raise NotImplementedError
