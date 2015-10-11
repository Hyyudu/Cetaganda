# coding: utf8
from __future__ import unicode_literals

from django.views.generic import TemplateView, FormView
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from roles.decorators import class_view_decorator, login_required, role_required
from market import models, forms


@class_view_decorator(login_required)
@class_view_decorator(role_required)
class MarketView(TemplateView):
    template_name = 'market/index.html'

    def get_context_data(self, **kwargs):
        context = super(MarketView, self).get_context_data(**kwargs)
        context['goods'] = models.Goods.objects.get_goods(self.request.role)
        context['money'] = self.request.role.get_field(settings.MONEY_FIELD) or 0
        return context

    # def post(self, request, *args, **kwargs):
    #     if request.POST.get('amount').isdigit():
    #         money = request.role.get_field(settings.MONEY_FIELD) or 0
    #         request.role.set_field(settings.MONEY_FIELD, money + int(request.POST.get('amount')))
    #     return HttpResponseRedirect(reverse('market:index'))


@class_view_decorator(login_required)
@class_view_decorator(role_required)
class BuyView(FormView):
    template_name = 'market/buy.html'
    form_class = forms.BuyForm

    def get_form_kwargs(self):
        kwargs = super(BuyView, self).get_form_kwargs()
        kwargs['buyer'] = self.request.role
        return kwargs

    def form_valid(self, form):
        product = form.cleaned_data['product']

        if isinstance(product, models.Goods):
            product.buyer = self.request.role
            product.is_finished = True
            product.save()

            stuff = product.product
            stuff.change_owner(self.request.role)
            cost = product.cost

            money = product.seller.get_field(settings.MONEY_FIELD) or 0
            product.seller.set_field(settings.MONEY_FIELD, money + cost)

            product.seller.records.create(
                category='Маркет',
                message='Вы продали %s за %s' % (stuff.market_name(), cost)
            )
        else:
            # Бесконечный товар
            try:
                stuff = product['class'].create(product['type'], self.request.role)
                cost = product['cost']
            except Exception as e:
                return self.render_to_response({'error': e})

        money = self.request.role.get_field(settings.MONEY_FIELD) or 0
        self.request.role.set_field(settings.MONEY_FIELD, money - cost)

        self.request.role.records.create(
            category='Маркет',
            message='Вы приобрели %s за %s' % (stuff.market_name(), cost)
        )

        return HttpResponseRedirect(reverse('market:index'))


@class_view_decorator(login_required)
@class_view_decorator(role_required)
class SellView(FormView):
    template_name = 'market/sell.html'
    form_class = forms.SellForm

    def get_form_kwargs(self):
        kwargs = super(SellView, self).get_form_kwargs()
        kwargs['role'] = self.request.role
        return kwargs

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('market:index'))
