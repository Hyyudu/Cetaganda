# coding: utf8
from __future__ import unicode_literals

from json import dumps

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http.response import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, FormView, UpdateView, CreateView, DetailView, DeleteView

from roles import forms
from roles.decorators import class_view_decorator
from roles.models import Role, RoleField, RoleConnection, Topic
# from users.decorators import profile_required


@class_view_decorator(login_required)
# @class_view_decorator(profile_required)
class ChooseRoleView(FormView):
    u"""Выбор роли"""
    template_name = 'roles/request.html'
    form_class = forms.RequestForm

    def form_valid(self, form):
        self.role = form.save(self.request.user)
        return super(ChooseRoleView, self).form_valid(form)

    def get_success_url(self):
        return self.role.get_absolute_url()


@class_view_decorator(login_required)
# @class_view_decorator(profile_required)
class CreateRoleView(CreateView):
    """Создание свободной роли роли"""
    template_name = 'roles/new_role.html'
    form_class = forms.RoleForm

    def get_form_kwargs(self):
        kwargs = super(CreateRoleView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


@class_view_decorator(login_required)
class RoleView(DetailView):
    template_name = 'roles/role.html'
    queryset = Role.objects.all()

    def get_context_data(self, **kwargs):
        context = super(RoleView, self).get_context_data(**kwargs)
        context['owner'] = self.request.user.has_perm('roles.can_edit_role')
        context['player'] = self.request.user == self.object.user
        context['can_edit'] = self.object.can_edit(self.request.user)

        context['fields'] = RoleField.objects.filter(role=self.object)
        if not context['owner']:
            if context['player']:
                context['fields'] = context['fields'].filter(field__visibility__in=('player', 'all'))
            else:
                context['fields'] = context['fields'].filter(field__visibility='all')

        if context['can_edit']:
            context['connections'] = RoleConnection.objects.filter(role=self.object).order_by('role_rel__name')

        context['can_occupy'] = self.object.user is None and \
            not Role.objects.filter(user=self.request.user).exists()
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.GET.get('take') and \
                self.object.user is None and not Role.objects.filter(user=self.request.user).exists():
            self.object.user = request.user
            self.object.save()
            return HttpResponseRedirect(self.object.get_absolute_url())

        if request.GET.get('free') and \
                self.object.user is not None and \
                self.object.can_edit(request.user):
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

        if self.object.can_edit(self.request.user):
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
        if not request.user.has_perm('roles.can_edit_role'):
            raise Http404

        return super(DeleteRoleView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return '/'


@class_view_decorator(login_required)
class EditConnectionsView(TemplateView):
    """Редактирование связей роли"""
    template_name = 'roles/edit_connections.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(Role, pk=kwargs['pk'])

        if self.object.can_edit(request.user):
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
class ReportConnectionsDiagram(TemplateView):
    template_name = 'reports/connections_diagram.html'

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
class ReportConnectionsData(TemplateView):
    template_name = 'reports/connections_diagram.html'

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
class ReportConnectionsTable(TemplateView):
    template_name = 'reports/connections_table.html'

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
class ReportFullRolesData(TemplateView):
    template_name = 'reports/full.html'

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
class ReportDualConnections(TemplateView):
    template_name = 'reports/dual_connections.html'

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
