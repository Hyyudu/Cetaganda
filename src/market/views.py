# coding: utf8
from __future__ import unicode_literals

from django.views.generic import TemplateView

from roles.decorators import class_view_decorator, login_required, role_required
from market.models import Goods


@class_view_decorator(login_required)
@class_view_decorator(role_required)
class MarketView(TemplateView):
    template_name = 'market/index.html'

    def get_context_data(self, **kwargs):
        context = super(MarketView, self).get_context_data(**kwargs)
        context['goods'] = Goods.objects.get_goods(self.request.role)
        return context
