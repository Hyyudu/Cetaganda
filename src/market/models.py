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
            }
            for product in super(GoodsManager, self).filter(is_finished=False)
            .filter(Q(buyer__isnull=True) | Q(buyer=self.request.role)).order_by('-dt')
        ]
        for number, infinite_product in enumerate(self.model.infinite_products):
            current_goods.append({
                'id': -number,
                'name': infinite_product[0].market_name(),
                'description': infinite_product[0].market_description(),
                'cost': infinite_product[1],
                'dt': None,
            })
        return current_goods


class Goods(models.Model):
    infinite_products = []

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
    def register_infinite_product(cls, product_class, cost):
        cls.infinite_products.append((product_class, cost))

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
