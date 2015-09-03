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
