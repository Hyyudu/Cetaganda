# coding: utf8
from __future__ import unicode_literals

from django.views.generic import TemplateView

from roles.decorators import class_view_decorator, login_required, role_required
from register import models


@class_view_decorator(login_required)
@class_view_decorator(role_required)
class IndexView(TemplateView):
    template_name = 'register/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['records'] = models.Record.objects.filter(role=self.request.role)
        return context
