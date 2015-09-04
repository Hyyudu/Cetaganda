# coding: utf8
from __future__ import unicode_literals

from django import forms
from django.conf import settings

from space import models


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
            navigator=self.role,
        )

        for fleet in (self.cleaned_data['fleet1'], self.cleaned_data['fleet2']):
            for ship in fleet.ship_set.all():
                ship.fleet = merged_fleet
                ship.save()

            fleet.delete()
