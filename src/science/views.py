# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, Http404
from django.views.generic import TemplateView, FormView, DetailView

from roles.decorators import class_view_decorator, login_required, role_required

from science import models, forms


@class_view_decorator(login_required)
@class_view_decorator(role_required)
class IndexView(TemplateView):
    template_name = 'science/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['inventions'] = self.request.role.invention_set.all().order_by('pk')
        context['productions'] = self.request.role.production_set.all().order_by('pk')
        context['store_form'] = forms.StoreForm()
        context['transfer_form'] = forms.TransferForm(self.request.role)
        context['store'] = models.Store.get_or_create(self.request.role)

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        if request.POST.get('action') == 'store':
            context['store_form'] = forms.StoreForm(request.POST)
            if context['store_form'].is_valid():
                context['store_form'].save(context['store'])
                return HttpResponseRedirect(reverse('science_index'))

        if request.POST.get('action') == 'transfer':
            context['transfer_form'] = forms.TransferForm(self.request.role, request.POST)
            if context['transfer_form'].is_valid():
                context['transfer_form'].save()
                return HttpResponseRedirect(reverse('science_index'))

        return self.render_to_response(context)


@class_view_decorator(login_required)
@class_view_decorator(role_required)
class CreateInventionView(FormView):
    template_name = 'science/create_invention.html'
    form_class = forms.InventionForm

    def form_valid(self, form):
        if self.request.POST.get('action') == 'Запомнить':
            form.save(self.request.role)
            return HttpResponseRedirect(reverse('science_index'))

        return self.render_to_response(self.get_context_data(form=form))


@class_view_decorator(login_required)
@class_view_decorator(role_required)
class CreateProductionView(TemplateView):
    template_name = 'science/index.html'


@class_view_decorator(login_required)
@class_view_decorator(role_required)
class InventionView(DetailView):
    queryset = models.Invention.objects.all()
    slug_field = 'hash'

    def dispatch(self, request, *args, **kwargs):
        invention = self.get_object()
        if invention.author == request.user or request.user.has_perm('science.change_invention'):
            return super(InventionView, self).dispatch(request, *args, **kwargs)

        raise Http404

    def post(self, request, *args, **kwargs):
        invention = self.get_object()
        if invention.enough_store():
            invention.produce()
            return HttpResponseRedirect(reverse('science_index'))

        return self.get(request, *args, **kwargs)
