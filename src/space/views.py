# coding: utf8
from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView, FormView

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

        try:
            alliance = models.Alliance.get_alliance(self.request.role)
            if alliance:
                context['resources'] = alliance.resources.items()
        except Exception:
            pass
        return context


@class_view_decorator(login_required)
@class_view_decorator(role_required)
class ShipsView(TemplateView):
    template_name = 'space/ships.html'

    def get_context_data(self, **kwargs):
        context = super(ShipsView, self).get_context_data(**kwargs)
        context['ships'] = models.Ship.objects.filter(in_space=True).order_by('name')
        context['page'] = 'all'
        return context


@class_view_decorator(login_required)
@class_view_decorator(role_required)
class ShipView(DetailView):
    model = models.Ship

    def get_template_names(self):
        return ['space/ship_%s.html' % self.object.state]

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.has_perm('space.can_edit_ship') or request.role == self.object.owner:
            return super(ShipView, self).dispatch(request, *args, **kwargs)

        raise Http404

    def get_context_data(self, **kwargs):
        context = super(ShipView, self).get_context_data(**kwargs)
        context['page'] = 'ships'
        try:
            context['alliance'] = models.Alliance.get_alliance(self.request.role)
            context['dockyards'] = context['alliance'].point_set.all()
            context['deploy_form'] = forms.DeployForm(self.request.role)
        except (models.Alliance.DoesNotExist, models.Point.DoesNotExist):
            pass

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(object=self.object)

        if request.POST.get('action') == 'deploy' and self.object.state == 'dockyard':
            context['deploy_form'] = forms.DeployForm(self.request.role, request.POST)
            if context['deploy_form'].is_valid():
                context['deploy_form'].save(self.object)
                return HttpResponseRedirect(self.object.get_absolute_url())
        return self.render_to_response(context)


@class_view_decorator(login_required)
@class_view_decorator(role_required)
class ShipFleetView(FormView):
    template_name = 'space/ship_fleet.html'
    form_class = forms.FleetForm

    def dispatch(self, request, *args, **kwargs):
        self.object = models.Ship.objects.get(pk=kwargs['pk'])
        if request.user.has_perm('space.can_edit_ship') or request.role == self.object.owner:
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
    """Дипломаты корабля"""
    template_name = 'space/ship_diplomacy.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(models.Ship, pk=kwargs['pk'])

        if request.role != self.object.owner:
            raise Http404

        return super(ShipDiplomatsView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            'formset': forms.DiplomatsFormSet(instance=self.object),
            'object': self.object,
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = {
            'formset': forms.DiplomatsFormSet(request.POST, instance=self.object),
            'object': self.object,
        }

        if context['formset'].is_valid():
            context['formset'].save()
            return HttpResponseRedirect(reverse('space:ship', args=[self.object.id]) + '?save=ok')
        else:
            return self.render_to_response(context)


def _is_tactic(role):
    return role.get_field(settings.TACTICS_FIELD[0]) == settings.TACTICS_FIELD[1]


def _is_diplomat(role):
    return role.get_field(settings.DIPLOMACY_FIELD[0]) == settings.DIPLOMACY_FIELD[1]


@class_view_decorator(login_required)
@class_view_decorator(role_required)
class TacticsView(TemplateView):
    template_name = 'space/tactics.html'

    def get_context_data(self, **kwargs):
        context = super(TacticsView, self).get_context_data(**kwargs)
        if _is_tactic(self.request.role):
            context['fleets'] = models.Fleet.objects.filter(navigator=self.request.role).order_by('point__name', 'name')
        else:
            context['error'] = 'Так получилось, что вы не космотактик. ' \
                               'Вашей квалификации недостаточно, чтобы управлять кораблями.'

        context['page'] = 'tactics'
        return context


@class_view_decorator(login_required)
@class_view_decorator(role_required)
class TacticsMergeView(FormView):
    template_name = 'space/tactics_merge.html'
    form_class = forms.TacticsMergeForm

    def dispatch(self, request, *args, **kwargs):
        if not _is_tactic(self.request.role):
            raise Http404
        return super(TacticsMergeView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(TacticsMergeView, self).get_form_kwargs()
        kwargs['role'] = self.request.role
        return kwargs

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('space:tactics'))


@class_view_decorator(login_required)
@class_view_decorator(role_required)
class FleetSplitView(TemplateView):
    template_name = 'space/tactics_split.html'

    def dispatch(self, request, *args, **kwargs):
        if not _is_tactic(self.request.role):
            raise Http404

        self.object = models.Fleet.objects.get(pk=kwargs['pk'])
        if self.object.navigator != request.role:
            raise Http404

        return super(FleetSplitView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FleetSplitView, self).get_context_data(**kwargs)
        context['page'] = 'tactics'
        context['object'] = self.object
        return context

    def post(self, request, *args, **kwargs):
        for ship in self.object.ship_set.all():
            fleet = models.Fleet.objects.create(
                name=ship.name,
                point=self.object.point,
                navigator=self.object.navigator,
            )

            ship.fleet = fleet
            ship.in_space = True
            ship.save()

        self.object.delete()
        return HttpResponseRedirect(reverse('space:tactics'))


@class_view_decorator(login_required)
@class_view_decorator(role_required)
class FleetRouteView(FormView):
    template_name = 'space/tactics_route.html'
    form_class = forms.RouteForm

    def dispatch(self, request, *args, **kwargs):
        if not _is_tactic(self.request.role):
            raise Http404

        self.object = models.Fleet.objects.get(pk=kwargs['pk'])
        if self.object.navigator != request.role:
            raise Http404

        return super(FleetRouteView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FleetRouteView, self).get_context_data(**kwargs)
        context['points'] = models.Point.objects.all()
        context['object'] = self.object
        return context

    def get_form_kwargs(self):
        kwargs = super(FleetRouteView, self).get_form_kwargs()
        kwargs['fleet'] = self.object
        return kwargs

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('space:tactics'))


@class_view_decorator(login_required)
@class_view_decorator(role_required)
class DiplomacyView(TemplateView):
    template_name = 'space/diplomacy.html'

    def get_context_data(self, **kwargs):
        context = super(DiplomacyView, self).get_context_data(**kwargs)
        if _is_diplomat(self.request.role):
            context['ships'] = self.request.role.responsible_for.filter(is_alive=True).order_by('name')
        else:
            context['error'] = 'Так получилось, что вы не дипломат. ' \
                               'Вашей квалификации недостаточно, чтобы заключать соглашения.'

        context['page'] = 'diplomacy'
        return context


@class_view_decorator(login_required)
@class_view_decorator(role_required)
class FriendshipView(TemplateView):
    """Корабли, на которые не нападает текущий корабль"""
    template_name = 'space/ship_friends.html'

    def dispatch(self, request, *args, **kwargs):
        if not _is_diplomat(self.request.role):
            raise Http404

        self.object = get_object_or_404(self.request.role.responsible_for.filter(is_alive=True), pk=kwargs['pk'])

        return super(FriendshipView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            'formset': forms.FriendshipFormSet(instance=self.object),
            'object': self.object,
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = {
            'formset': forms.FriendshipFormSet(request.POST, instance=self.object),
            'object': self.object,
        }

        if context['formset'].is_valid():
            context['formset'].save()
            return HttpResponseRedirect(reverse('space:diplomacy') + '?save=ok')
        else:
            return self.render_to_response(context)


@class_view_decorator(login_required)
@class_view_decorator(role_required)
class PicturesView(TemplateView):
    template_name = 'space/pictures.html'

    def get_context_data(self, **kwargs):
        context = super(PicturesView, self).get_context_data(**kwargs)
        context['pictures'] = models.Picture.objects.filter(requester=self.request.role).order_by('-dt')
        context['page'] = 'pictures'
        return context


@class_view_decorator(login_required)
@class_view_decorator(role_required)
class RequestPictureView(FormView):
    template_name = 'space/pictures_request.html'
    form_class = forms.RequestPictureForm

    def get_context_data(self, **kwargs):
        context = super(RequestPictureView, self).get_context_data(**kwargs)
        context['page'] = 'pictures'
        return context

    def get_form_kwargs(self):
        kwargs = super(RequestPictureView, self).get_form_kwargs()
        kwargs['requester'] = self.request.role
        return kwargs

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('space:pictures'))
