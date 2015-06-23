# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, Http404
from django.views.generic import TemplateView, FormView, DetailView

from roles.decorators import class_view_decorator, role_required

from science import models, forms


@class_view_decorator(role_required)
class IndexView(TemplateView):
    template_name = 'science/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['inventions'] = self.request.role.invention_set.all().order_by('pk')
        context['productions'] = self.request.role.production_set.all().order_by('pk')
        context['store_form'] = forms.StoreForm()

        try:
            store = self.request.role.store
        except models.Store.DoesNotExist:
            store = models.Store.objects.create(owner=self.request.role, goods={})
        context['store'] = store

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        if request.POST.get('action') == 'store':
            form = forms.StoreForm(request.POST)
            if form.is_valid():
                form.save(context['store'])

        return HttpResponseRedirect(reverse('science_index'))


@class_view_decorator(role_required)
class CreateInventionView(FormView):
    template_name = 'science/create_invention.html'
    form_class = forms.InventionForm

    def form_valid(self, form):
        if self.request.POST.get('action') == 'Запомнить':
            form.save(self.request.role)
            return HttpResponseRedirect(reverse('science_index'))

        return self.render_to_response(self.get_context_data(form=form))


@class_view_decorator(role_required)
class CreateProductionView(TemplateView):
    template_name = 'science/index.html'


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
