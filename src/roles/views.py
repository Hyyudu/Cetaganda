# coding: utf8
from __future__ import unicode_literals

from json import dumps

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http.response import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, FormView, UpdateView, CreateView, DetailView, DeleteView
from django.template.response import TemplateResponse

from roles import forms
from roles.decorators import class_view_decorator
from roles.models import Role, Game, RoleField, RoleConnection, Topic


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['all_roles'] = Game.objects.filter(paid=True)

        if self.request.user.is_authenticated():
            context['roles'] = Role.objects.filter(user=self.request.user)
            context['own_roles'] = Game.objects.filter(owner=self.request.user)
        return context


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


@class_view_decorator(login_required)
class CreateGameView(CreateView):
    """Создание роли"""
    template_name = 'roles/new_game.html'
    form_class = forms.GameForm

    def form_valid(self, form):
        game = form.save(commit=False)
        game.owner = self.request.user
        game.save()
        return super(CreateGameView, self).form_valid(form)


class GameView(DetailView):
    template_name = 'roles/game.html'
    queryset = Game.objects.all()

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.is_paid() or self.object.is_master(request.user):
            return super(GameView, self).dispatch(request, *args, **kwargs)

        raise Http404

    def get_context_data(self, **kwargs):
        context = super(GameView, self).get_context_data(**kwargs)
        context['roles'] = Role.objects.filter(game=self.object).order_by('name')

        if self.request.user.is_authenticated():
            if Role.objects.filter(game=self.object, user=self.request.user).count() == 0:
                context['free_user'] = True

            if self.object.is_master(self.request.user):
                context['can_edit'] = True
        return context


@class_view_decorator(login_required)
class EditGameView(UpdateView):
    template_name = 'roles/edit_game.html'
    form_class = forms.GameForm
    object = None
    queryset = Game.objects.all()

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.is_master(request.user):
            return super(EditGameView, self).dispatch(request, *args, **kwargs)

        raise Http404


@class_view_decorator(login_required)
class GameDescendantsView(TemplateView):
    """Редактирование подчиненных объектов игры"""
    formset = None

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(Game, pk=kwargs['pk'])

        if self.object.is_master(request.user):
            return super(GameDescendantsView, self).dispatch(request, *args, **kwargs)

        raise Http404

    def get(self, request, *args, **kwargs):
        context = {
            'formset': self.formset(instance=self.object),
            'object': self.object,
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = {
            'formset': self.formset(request.POST, instance=self.object),
            'object': self.object,
        }

        if context['formset'].is_valid():
            context['formset'].save()
            return HttpResponseRedirect(reverse('game', args=[self.object.id]) + '?save=ok')
        else:
            return self.render_to_response(context)


class GameFieldsView(GameDescendantsView):
    """Редактирование полей игры"""
    template_name = 'roles/edit_game_fields.html'
    formset = forms.GameFieldsFormSet


class GameGroupsView(GameDescendantsView):
    """Редактирование блоков игры"""
    template_name = 'roles/edit_game_groups.html'
    formset = forms.GameGroupsFormSet


class GameTopicsView(GameDescendantsView):
    """Редактирование сюжетов игры"""
    template_name = 'roles/edit_game_topics.html'
    formset = forms.GameTopicsFormSet


@class_view_decorator(login_required)
class CreateFreeRoleView(CreateView):
    """Создание свободной роли роли"""
    template_name = 'roles/new_role.html'
    form_class = forms.RoleForm

    def dispatch(self, request, *args, **kwargs):
        self.game = get_object_or_404(Game, pk=kwargs['pk'])

        if not self.game.is_master(request.user):
            raise Http404

        if not self.game.is_paid():
            return HttpResponse(TemplateResponse(request, 'roles/payment_required.html').render())

        return super(CreateFreeRoleView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateFreeRoleView, self).get_form_kwargs()
        kwargs['game'] = self.game
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        role = form.save()
        role.game = self.game
        role.save()
        return super(CreateFreeRoleView, self).form_valid(form)


@class_view_decorator(login_required)
class CreateRoleView(CreateView):
    """Создание свободной роли роли"""
    template_name = 'roles/new_role.html'
    form_class = forms.RoleForm

    def dispatch(self, request, *args, **kwargs):
        self.game = get_object_or_404(Game, pk=kwargs['pk'])

        if Role.objects.filter(game=self.game, user=self.request.user).count() > 0:
            raise Http404

        if not self.game.is_paid():
            return HttpResponse(TemplateResponse(request, 'roles/payment_required.html').render())

        return super(CreateRoleView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateRoleView, self).get_form_kwargs()
        kwargs['game'] = self.game
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        role = form.save()
        role.game = self.game
        role.user = self.request.user
        role.save()
        return super(CreateRoleView, self).form_valid(form)


@class_view_decorator(login_required)
class RoleView(DetailView):
    template_name = 'roles/role.html'
    queryset = Role.objects.all()

    def get_context_data(self, **kwargs):
        context = super(RoleView, self).get_context_data(**kwargs)
        context['owner'] = self.object.game.is_master(self.request.user)
        context['player'] = self.request.user == self.object.user

        context['fields'] = RoleField.objects.filter(role=self.object)
        if not context['owner']:
            if context['player']:
                context['fields'] = context['fields'].filter(field__visibility__in=('player', 'all'))
            else:
                context['fields'] = context['fields'].filter(field__visibility='all')

        if context['owner'] or context['player']:
            context['connections'] = RoleConnection.objects.filter(role=self.object).order_by('role_rel__name')

        context['can_edit'] = context['owner'] or self.request.user == self.object.user
        context['can_occupy'] = self.object.user is None and \
            Role.objects.filter(game=self.object.game, user=self.request.user).count() == 0
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.GET.get('take') and \
                self.object.user is None and \
                Role.objects.filter(game=self.object.game, user=self.request.user).count() == 0:
            self.object.user = request.user
            self.object.save()
            return HttpResponseRedirect(self.object.get_absolute_url())

        if request.GET.get('free') and \
                self.object.user is not None and \
                self.object.game.is_master(request.user):
            self.object.user = None
            self.object.save()
            return HttpResponseRedirect(self.object.get_absolute_url())

        return super(RoleView, self).get(request, *args, **kwargs)


@class_view_decorator(login_required)
class EditRoleView(UpdateView):
    template_name = 'roles/edit_role.html'
    form_class = forms.RoleForm
    object = None
    queryset = Role.objects.all()

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.game.is_master(request.user) or request.user == self.object.user:
            return super(EditRoleView, self).dispatch(request, *args, **kwargs)

        raise Http404

    def get_form_kwargs(self):
        kwargs = super(EditRoleView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


@class_view_decorator(login_required)
class DeleteRoleView(DeleteView):
    model = Role

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.game.is_master(self.request.user):
            raise Http404

        return super(DeleteRoleView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('game', args=[self.object.game_id])


@class_view_decorator(login_required)
class EditConnectionsView(TemplateView):
    """Редактирование связей роли"""
    template_name = 'roles/edit_connections.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(Role, pk=kwargs['pk'])

        if self.object.game.is_master(request.user) or request.user == self.object.user:
            return super(EditConnectionsView, self).dispatch(request, *args, **kwargs)

        raise Http404

    def get(self, request, *args, **kwargs):
        context = {
            'formset': forms.ConnectionFormSet(instance=self.object),
            'object': self.object,
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = {
            'formset': forms.ConnectionFormSet(request.POST, instance=self.object),
            'object': self.object,
        }

        if context['formset'].is_valid():
            context['formset'].save()
            return HttpResponseRedirect(reverse('role', args=[self.object.id]) + '?save=ok')
        else:
            return self.render_to_response(context)


@class_view_decorator(login_required)
class AddConnectionView(FormView):
    """Добавление связи роли"""
    template_name = 'roles/new_connection.html'
    form_class = forms.DualConnectionForm

    def dispatch(self, request, *args, **kwargs):
        self.role = get_object_or_404(Role, pk=kwargs['pk'])
        self.connection = RoleConnection.objects.get(pk=self.request.GET['based_on'])

        if self.role.game.is_master(request.user):
            return super(AddConnectionView, self).dispatch(request, *args, **kwargs)

        raise Http404

    def get_context_data(self, **kwargs):
        context = super(AddConnectionView, self).get_context_data(**kwargs)
        context['connection'] = self.connection
        return context

    def form_valid(self, form):
        form.save(self.connection)
        return HttpResponseRedirect(reverse('report_dual_connections', args=[self.role.game_id]))


@class_view_decorator(login_required)
class ReportConnectionsDiagram(DetailView):
    template_name = 'reports/connections_diagram.html'
    queryset = Game.objects.all()

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.is_master(request.user):
            return super(ReportConnectionsDiagram, self).dispatch(request, *args, **kwargs)

        raise Http404

    def get_context_data(self, **kwargs):
        context = super(ReportConnectionsDiagram, self).get_context_data(**kwargs)
        topics = set()
        for connection in RoleConnection.objects.filter(role__game=self.object):
            if connection.topic and connection.topic.game == self.object:
                topics.add(connection.topic)

        context['topics'] = topics
        return context


translit = {u'а': u'a', u'б': u'b', u'в': u'v', u'г': u'g', u'д': u'd', u'е': u'e',
            u'ж': u'zh', u'з': u'z', u'и': u'i', u'й': u'j', u'к': u'k', u'л': u'l',
            u'м': u'm', u'н': u'n', u'о': u'o', u'п': u'p', u'р': u'r', u'с': u's',
            u'т': u't', u'у': u'u', u'ф': u'f', u'х': u'x', u'ц': u'cz', u'ч': u'ch',
            u'ш': u'sh', u'щ': u'shh', u'ъ': u'_d', u'ы': u'yi', u'ь': u'y', u'э': u'ye',
            u'ю': u'yu', u'я': u'ya', u'ё': u'yo',
            u'æ': u'e',
            u'á': u'a', u'é': u'e', u'ć': u'c',
            u'ä': u'a', u'ü': u'u', u'ö': u'o',
            u'å': u'a', u'ů': u'u',
            u'č': u'c', u'š': u's', u'ř': u'r', u'ž': u'z', u'ě': u'e',
            u'ø': u'o',
            }


def rus2translit(text):
    res = u''
    for c in text:
        if c in translit:
            res += translit[c]
        elif c.lower() in translit:
            res += translit[c.lower()].upper()
        else:
            res += c
    return res


def slug(title):
    import re
    return re.sub('\s+', '-', rus2translit(title.strip())).lower()


@class_view_decorator(login_required)
class ReportConnectionsData(DetailView):
    template_name = 'reports/connections_diagram.html'
    queryset = Game.objects.all()

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.is_master(request.user):
            return super(ReportConnectionsData, self).dispatch(request, *args, **kwargs)

        raise Http404

    def get(self, request, **kwargs):
        roles = Role.objects.filter(game=self.object).order_by('group__name', 'name')
        connection_queryset = RoleConnection.objects.filter(role_rel__isnull=False)
        try:
            topic = Topic.objects.get(pk=request.GET['topic'], game=self.object)
            connection_queryset = connection_queryset.filter(topic=topic)
        except Exception:
            pass
        result = []

        def role_key(role):
            return (role.group and slug(role.group.name) or '') + '.' + slug(role.name)

        for role in roles:
            result.append({
                'name': role_key(role),
                'full_name': role.name,
                'group_color': role.group and role.group.color or '000000',
                'link': role.get_absolute_url(),
                'imports': [
                    role_key(connection.role_rel)
                    for connection in connection_queryset.filter(role=role)
                ]
            })

        return HttpResponse(dumps(result, indent=2, ensure_ascii=False), content_type='application/json; charset=UTF-8')


@class_view_decorator(login_required)
class ReportConnectionsTable(DetailView):
    template_name = 'reports/connections_table.html'
    queryset = Game.objects.all()

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.is_master(request.user):
            return super(ReportConnectionsTable, self).dispatch(request, *args, **kwargs)

        raise Http404

    def get_context_data(self, **kwargs):
        context = super(ReportConnectionsTable, self).get_context_data(**kwargs)
        roles = dict((role.pk, role) for role in Role.objects.filter(game=self.object))
        connections_dict = {}
        for connection in RoleConnection.objects.filter(role__game=self.object):
            key = (
                min(connection.role_id, connection.role_rel_id),
                max(connection.role_id, connection.role_rel_id),
                connection.topic and connection.topic.name or '',
            )
            field = connection.role_id < connection.role_rel_id and 'first' or 'second'
            connections_dict.setdefault(key, {})[field] = connection

        context['paired_connections'] = [
            (roles[pair_key[0]], roles[pair_key[1]], pair_key[2], pair.get('first', None), pair.get('second', None))
            for pair_key, pair in connections_dict.items()
        ]

        context['paired_connections'].sort(key=lambda pair: (pair[0].name, pair[1].name))

        return context


@class_view_decorator(login_required)
class ReportFullRolesData(DetailView):
    template_name = 'reports/full.html'
    queryset = Game.objects.all()

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.is_master(request.user):
            return super(ReportFullRolesData, self).dispatch(request, *args, **kwargs)

        raise Http404

    def get_context_data(self, **kwargs):
        context = super(ReportFullRolesData, self).get_context_data(**kwargs)
        context['roles'] = Role.objects.filter(game=self.object)
        for role in context['roles']:
            role.connections = role.roles.all().order_by('role_rel__name')
        return context


@class_view_decorator(login_required)
class ReportDualConnections(DetailView):
    template_name = 'reports/dual_connections.html'
    queryset = Game.objects.all()

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.is_master(request.user):
            return super(ReportDualConnections, self).dispatch(request, *args, **kwargs)

        raise Http404

    def get_context_data(self, **kwargs):
        context = super(ReportDualConnections, self).get_context_data(**kwargs)
        connections = RoleConnection.objects.filter(role__game=self.object)
        pairs = list(
            (connection.role_id, connection.role_rel_id, connection.topic_id)
            for connection in connections
        )

        context['missing'] = []
        for connection in connections:
            if (connection.role_rel_id, connection.role_id, connection.topic_id) not in pairs:
                context['missing'].append(connection)

        return context


###############################################################################
# Авторизация


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
