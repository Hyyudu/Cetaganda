# coding: utf8
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import CreateView

from guestbook import models, forms


class IndexView(CreateView):
    template_name = 'guestbook/index.html'
    form_class = forms.PostForm

    def get_success_url(self):
        return reverse('guestbook:index')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['posts'] = models.Post.objects.order_by('-dt')[:50]
        return context

    def get_form_kwargs(self):
        kwargs = super(IndexView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
