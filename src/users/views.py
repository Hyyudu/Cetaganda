# coding: utf8
from __future__ import unicode_literals

from django.views.generic import FormView

from users import forms


class CabinetView(FormView):
    """Редактирование профиля"""
    template_name = 'users/profile_edit.html'
    form_class = forms.CabinetForm
    success_url = '/'

    def get_form_kwargs(self):
        kwargs = super(CabinetView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(CabinetView, self).form_valid(form)
