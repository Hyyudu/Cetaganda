# coding: utf8
from __future__ import unicode_literals

from django import forms
from django.db.models import Q
from django.conf import settings

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
                    .filter(Q(buyer__isnull=True) | Q(buyer=self.role))\
                    .get(pk=product_id, is_finised=False)
            except models.Goods.DoesNotExist:
                raise forms.ValidationError('Товар не найден')
        else:
            for infinite_product_class in models.Goods.infinite_products:
                for product in infinite_product_class.get_infinite_goods():
                    print product
                    print product_id
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
