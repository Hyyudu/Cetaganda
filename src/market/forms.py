# coding: utf8
from __future__ import unicode_literals

from django import forms
from django.db.models import Q
from django.conf import settings

from roles.models import Role
from market import models


class BuyForm(forms.Form):
    product = forms.CharField(label='Товар')

    def __init__(self, *args, **kwargs):
        self.buyer = kwargs.pop('buyer')
        super(BuyForm, self).__init__(*args, **kwargs)

    def clean_product(self):
        product_id = self.cleaned_data['product']
        if product_id.isdigit():
            try:
                return models.Goods.objects\
                    .filter(Q(buyer__isnull=True) | Q(buyer=self.buyer))\
                    .get(pk=product_id, is_finished=False)
            except models.Goods.DoesNotExist:
                raise forms.ValidationError('Товар не найден')
        else:
            for infinite_product_class in models.Goods.products_classes:
                for product in infinite_product_class.get_infinite_goods():
                    if product_id == product['type']:
                        return product
            raise forms.ValidationError('Неизвестный товар')

    def clean(self):
        if self.errors:
            return

        product = self.cleaned_data['product']
        if isinstance(product, models.Goods):
            cost = product.cost
        else:
            cost = product['cost']

        if self.buyer.get_field(settings.MONEY_FIELD) < cost:
            raise forms.ValidationError('У вас недостаточно средств для покупки')

        return self.cleaned_data


class SellForm(forms.Form):
    product = forms.CharField(label='Товар', widget=forms.Select)
    cost = forms.IntegerField(label='Стоимость', min_value=1)

    def __init__(self, *args, **kwargs):
        self.seller = kwargs.pop('role')
        super(SellForm, self).__init__(*args, **kwargs)

        available_products = []
        for product_class in models.Goods.products_classes:
            for product in product_class.get_available_for_market(self.seller):
                available_products.append((
                    '%s:%s' % (product_class.__name__, product.id),
                    '%s: %s' % (product.market_name(), product.market_description())
                ))
        self.fields['product'].widget.choices = available_products

    def clean_product(self):
        for product_class in models.Goods.products_classes:
            for product in product_class.get_available_for_market(self.seller):
                if self.cleaned_data['product'] == '%s:%s' % (product_class.__name__, product.id):
                    return product
        raise forms.ValidationError('Неизвестный товар')

    def save(self):
        models.Goods.objects.create(
            seller=self.seller,
            product=self.cleaned_data['product'],
            cost=self.cleaned_data['cost'],
        )
        self.cleaned_data['product'].change_owner(Role.all.get(name='market'))
