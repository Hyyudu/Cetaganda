from __future__ import unicode_literals

from django.http.response import HttpResponse, Http404
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator


def class_view_decorator(function_decorator):
    """Convert a function based decorator into a class based decorator usable
    on class based Views.

    Can't subclass the `View` as it breaks inheritance (super in particular),
    so we monkey-patch instead.
    """

    def simple_decorator(View):
        View.dispatch = method_decorator(function_decorator)(View.dispatch)
        return View

    return simple_decorator


def login_required(f):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponse(TemplateResponse(request, 'login_required.html').render())
        return f(request, *args, **kwargs)
    return wrapper


def role_required(f):
    def wrapper(request, *args, **kwargs):
        if not getattr(request, 'role', None) or not request.role:
            return HttpResponse(TemplateResponse(request, 'role_required.html').render())
        return f(request, *args, **kwargs)
    return wrapper


def no_role_required(f):
    def wrapper(request, *args, **kwargs):
        if getattr(request, 'role', None):
            return HttpResponse(TemplateResponse(request, 'no_role_required.html').render())
        return f(request, *args, **kwargs)
    return wrapper


def superuser_required(f):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404
        return f(request, *args, **kwargs)
    return wrapper
