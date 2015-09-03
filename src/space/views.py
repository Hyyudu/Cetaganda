# coding: utf8
from __future__ import unicode_literals

from django.views.generic import TemplateView, DetailView, FormView
from django.http import HttpResponseRedirect, Http404
from django.conf import settings

from roles.decorators import class_view_decorator, login_required, role_required
from space import models, forms


@class_view_decorator(login_required)
@class_view_decorator(role_required)
class IndexView(TemplateView):
    template_name = 'space/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['active_ships'] = models.Ship.objects.filter(owner=self.request.role, in_space=True, is_alive=True)
        context['passive_ships'] = models.Ship.objects.filter(owner=self.request.role, in_space=False, is_alive=True)
        context['dead_ships'] = models.Ship.objects.filter(owner=self.request.role, is_alive=False)
        context['page'] = 'ships'
        return context


@class_view_decorator(login_required)
@class_view_decorator(role_required)
class ShipView(DetailView):
    model = models.Ship

    def get_template_names(self):
        return ['space/ship_%s.html' % self.object.state]

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.has_perm('space.can_edit_ship') or request.user == self.object.owner:
            return super(ShipView, self).dispatch(request, *args, **kwargs)

        raise Http404

    def get_context_data(self, **kwargs):
        context = super(ShipView, self).get_context_data(**kwargs)
        context['page'] = 'ships'
        try:
            context['alliance'] = models.Alliance.get_alliance(self.request.role)
            context['dockyard'] = context['alliance'].get_major_planet()
        except (models.Alliance.DoesNotExist, models.Point.DoesNotExist):
            pass

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(object=self.object)

        if request.POST.get('action') == 'deploy':
            if context['dockyard'] and self.object.state == 'dockyard':
                self.object.in_space = True
                self.object.position = context['dockyard']
                self.object.save()

                return HttpResponseRedirect(self.object.get_absolute_url())
            else:
                context['error'] = 'Что-то пошло не так'
        return self.render_to_response(context)


@class_view_decorator(login_required)
@class_view_decorator(role_required)
class ShipFleetView(FormView):
    template_name = 'space/ship_fleet.html'
    form_class = forms.FleetForm

    def dispatch(self, request, *args, **kwargs):
        self.object = models.Ship.objects.get(pk=kwargs['pk'])
        if request.user.has_perm('space.can_edit_ship') or request.user == self.object.owner:
            return super(ShipFleetView, self).dispatch(request, *args, **kwargs)

        raise Http404

    def get_context_data(self, **kwargs):
        context = super(ShipFleetView, self).get_context_data(**kwargs)
        context['page'] = 'ships'
        context['object'] = self.object
        return context

    def form_valid(self, form):
        if self.object.state == 'space':
            form.save(self.object)

        return HttpResponseRedirect(self.object.get_absolute_url())


@class_view_decorator(login_required)
@class_view_decorator(role_required)
class ShipDiplomatsView(TemplateView):
    pass


@class_view_decorator(login_required)
@class_view_decorator(role_required)
class TacticsView(TemplateView):
    template_name = 'space/tactics.html'

    def get_context_data(self, **kwargs):
        context = super(TacticsView, self).get_context_data(**kwargs)
        if self.request.role.get_field(settings.TACTICS_FIELD[0]) == settings.TACTICS_FIELD[1]:
            context['fleets'] = models.Fleet.objects.filter(navigator=self.request.role)
        else:
            context['error'] = 'Так получилось, что вы не космотактик. ' \
                               'Вашей квалификации недостаточно, чтобы управлять кораблями'

        context['page'] = 'tactics'
        return context


class DiplomacyView(TemplateView):
    pass
