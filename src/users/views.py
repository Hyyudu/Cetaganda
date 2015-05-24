# coding: utf8
from __future__ import unicode_literals

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http.response import Http404, HttpResponseRedirect
from django.views.generic import TemplateView, FormView

from users import forms
from roles.decorators import class_view_decorator


@class_view_decorator(login_required)
class CabinetView(FormView):
    """Редактирование профиля"""
    template_name = 'roles/profile_edit.html'
    form_class = forms.CabinetForm
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise Http404
        return super(CabinetView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CabinetView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(CabinetView, self).form_valid(form)


class RegistrationView(TemplateView):
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'registration_form': forms.RegistrationForm(initial={'next': request.GET.get('next')}),
            'login_form': forms.LoginForm(),
        })

    def post(self, request, *args, **kwargs):
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            auth.login(request, form.user)
            next = request.POST.get('next') or form.user.get_absolute_url()
            return HttpResponseRedirect(next)

        return self.render_to_response({
            'registration_form': form,
            'login_form': forms.LoginForm(),
        })


class LoginView(TemplateView):
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'registration_form': forms.RegistrationForm(initial=request.GET),
            'login_form': forms.LoginForm(initial={'next': request.GET.get('next')}),
        })

    def post(self, request, *args, **kwargs):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = form.user
            auth.login(request, user)
            next = request.POST.get('next') or '/'
            return HttpResponseRedirect(next)

        registration_form = forms.RegistrationForm(initial=request.GET)
        return self.render_to_response({
            'registration_form': registration_form,
            'login_form': form,
        })
