# coding: utf8
from __future__ import unicode_literals

from django import forms
from django.conf import settings

from space import models


class DeployForm(forms.Form):
    home = forms.IntegerField(label='Порт приписки', widget=forms.Select)

    def __init__(self, role, *args, **kwargs):
        super(DeployForm, self).__init__(*args, **kwargs)

        self.role = role
        self.alliance = models.Alliance.get_alliance(self.role)
        self.fields['home'].widget.choices = [
            (planet.id, planet.name)
            for planet in self.alliance.point_set.all().order_by('name')
        ]

    def clean_home(self):
        try:
            return models.Point.objects.get(alliance=self.alliance, pk=self.cleaned_data['home'])
        except models.Point.DoesNotExist:
            raise forms.ValidationError('Неизвестная планета')

    def save(self, ship):
        ship.in_space = True
        ship.position = self.cleaned_data['home']
        ship.home = self.cleaned_data['home']
        ship.save()


class FleetForm(forms.Form):
    navigator = forms.IntegerField(label='', widget=forms.Select)

    def __init__(self, *args, **kwargs):
        super(FleetForm, self).__init__(*args, **kwargs)

        self.navigators = {
            role.id: role.name
            for role in models.Role.objects.all()
            if role.get_field(settings.TACTICS_FIELD[0]) == settings.TACTICS_FIELD[1]
        }
        self.fields['navigator'].widget.choices = self.navigators.items() + [(0, 'без навигатора')]

    def clean_navigator(self):
        if self.cleaned_data['navigator'] == 0:
            return None

        if int(self.cleaned_data['navigator']) not in self.navigators:
            raise forms.ValidationError('Неизвестный навигатор')

        return models.Role.objects.get(pk=self.cleaned_data['navigator'])

    def save(self, ship):
        if ship.fleet and ship.fleet.ship_set.count() == 1:
            ship.fleet.delete()
        ship.fleet = None
        ship.save()

        if self.cleaned_data['navigator']:
            fleet = models.Fleet.objects.create(
                name=ship.name,
                point=ship.position,
                navigator=self.cleaned_data['navigator'],
            )

            ship.fleet = fleet
            ship.save()


class TacticsMergeForm(forms.Form):
    fleet1 = forms.IntegerField(label='Флот 1', widget=forms.Select)
    fleet2 = forms.IntegerField(label='Флот 2', widget=forms.Select)
    name = forms.CharField(label='Новое название')

    def __init__(self, *args, **kwargs):
        self.role = kwargs.pop('role')
        super(TacticsMergeForm, self).__init__(*args, **kwargs)

        fleets = models.Fleet.objects.filter(navigator=self.role).order_by('point__name', 'name')
        self.fields['fleet1'].widget.choices = [(fleet.id, unicode(fleet)) for fleet in fleets]
        self.fields['fleet2'].widget.choices = [(fleet.id, unicode(fleet)) for fleet in fleets]

    def clean_fleet1(self):
        try:
            return models.Fleet.objects.get(navigator=self.role, pk=self.cleaned_data['fleet1'])
        except models.Fleet.DoesNotExist:
            raise forms.ValidationError('Неизвестный флот в поле 1')

    def clean_fleet2(self):
        try:
            return models.Fleet.objects.get(navigator=self.role, pk=self.cleaned_data['fleet2'])
        except models.Fleet.DoesNotExist:
            raise forms.ValidationError('Неизвестный флот в поле 2')

    def clean(self):
        if self.errors:
            return

        if self.cleaned_data['fleet1'] == self.cleaned_data['fleet2']:
            raise forms.ValidationError('Выберите разные флота')

        if self.cleaned_data['fleet1'].point != self.cleaned_data['fleet2'].point:
            raise forms.ValidationError('Флота должны находиться в одной точке')

        return self.cleaned_data

    def save(self):
        merged_fleet = models.Fleet.objects.create(
            name=self.cleaned_data['name'],
            point=self.cleaned_data['fleet1'].point,
            route=self.cleaned_data['fleet1'].route,
            navigator=self.role,
        )

        for fleet in (self.cleaned_data['fleet1'], self.cleaned_data['fleet2']):
            for ship in fleet.ship_set.all():
                ship.fleet = merged_fleet
                ship.save()

            fleet.delete()


class RouteForm(forms.Form):
    route = forms.CharField(label='Маршрут', required=False, widget=forms.TextInput(attrs={'style': 'width: 500px'}))

    def __init__(self, *args, **kwargs):
        self.fleet = kwargs.pop('fleet')
        super(RouteForm, self).__init__(*args, **kwargs)

    def clean_route(self):
        if not self.cleaned_data['route']:
            return ''

        try:
            points = map(int, self.cleaned_data['route'].strip().split())
        except TypeError:
            raise forms.ValidationError('Непонятный формат маршрута. Введите числа, разделенные пробелами.')

        all_points = {p.id: p for p in models.Point.objects.all()}
        for point in points:
            if point not in all_points:
                raise forms.ValidationError('Неизвестная точка %s' % point)

        prev_point = self.fleet.point_id
        for point in points:
            if not (models.Transit.objects.filter(point1=prev_point, point2=point).exists() or
                    models.Transit.objects.filter(point2=prev_point, point1=point).exists()):
                raise forms.ValidationError(
                    'Нет перехода между точками %s (%s) и %s (%s). Измените маршрут.' %
                    (prev_point, all_points[prev_point], point, all_points[point])
                )
            prev_point = point

        return ' '.join(map(unicode, points))

    def save(self):
        self.fleet.route = self.cleaned_data['route']
        self.fleet.save()
