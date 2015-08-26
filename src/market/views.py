# coding: utf8
from __future__ import unicode_literals

from django.views.generic import TemplateView, FormView
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from roles.decorators import class_view_decorator, login_required, role_required
from market.models import Goods
from market.forms import BuyForm


@class_view_decorator(login_required)
@class_view_decorator(role_required)
class MarketView(TemplateView):
    template_name = 'market/index.html'

    def get_context_data(self, **kwargs):
        context = super(MarketView, self).get_context_data(**kwargs)
        context['goods'] = Goods.objects.get_goods(self.request.role)
        context['money'] = self.request.role.get_field(settings.MONEY_FIELD) or 0
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('amount').isdigit():
            money = request.role.get_field(settings.MONEY_FIELD) or 0
            request.role.set_field(settings.MONEY_FIELD, money + int(request.POST.get('amount')))
        return HttpResponseRedirect(reverse('market:index'))


@class_view_decorator(login_required)
@class_view_decorator(role_required)
class BuyView(FormView):
    template_name = 'market/buy.html'
    form_class = BuyForm

    def get_form_kwargs(self):
        kwargs = super(BuyView, self).get_form_kwargs()
        kwargs['buyer'] = self.request.role
        return kwargs

    def form_valid(self, form):
        product = form.cleaned_data['product']
        money = self.request.role.get_field(settings.MONEY_FIELD) or 0

        if isinstance(product, Goods):
            product.buyer = self.request.role
            product.is_finished = True
            product.save()

            product.product.change_owner(self.request.role)
            cost = product.cost

        else:
            # Бесконечный товар
            product['class'].create(product['type'], self.request.role)
            cost = product['cost']

        self.request.role.set_field(settings.MONEY_FIELD, money - cost)
        return HttpResponseRedirect(reverse('market:index'))
