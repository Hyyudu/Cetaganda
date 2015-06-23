# coding: utf8
from __future__ import unicode_literals

from uuid import uuid4

from django import forms

from science import models
from science.utils import translate


class StoreForm(forms.Form):
    resource = forms.CharField(label='', widget=forms.Select)
    amount = forms.IntegerField(label='')

    def __init__(self, *args, **kwargs):
        super(StoreForm, self).__init__(*args, **kwargs)

        self.fields['resource'].widget.choices = [
            (letter, letter)
            for letter in 'бЗзКкСсЖж'
        ]

    def save(self, store):
        store.goods[self.cleaned_data['resource']] = \
            store.goods.get(self.cleaned_data['resource'], 0) + int(self.cleaned_data['amount'])
        store.save()


class InventionForm(forms.Form):
    base_coded = forms.CharField(label='База', widget=forms.TextInput(attrs={'style': 'width: 800px;'}))
    change_coded = forms.CharField(label='Изменение', widget=forms.TextInput(attrs={'style': 'width: 800px;'}))
    name = forms.CharField(label='Название', required=False)

    def clean_base_coded(self):
        self.cleaned_data['base_coded'] = self.cleaned_data['base_coded'].strip()

        for c in self.cleaned_data['base_coded']:
            if c not in 'нНр':
                raise forms.ValidationError('База должна состоять из символов н, Н, р.')

        if self.cleaned_data['base_coded'].startswith('рр'):
            raise forms.ValidationError('База не может начинаться с "рр"')
        if self.cleaned_data['base_coded'].endswith('рр'):
            raise forms.ValidationError('База не может заканчиваться на "рр"')

        try:
            self.cleaned_data['base'] = translate(self.cleaned_data['base_coded']).capitalize()
            return self.cleaned_data['base_coded']
        except ValueError:
            raise forms.ValidationError('База не распознана')

    def clean_change_coded(self):
        self.cleaned_data['change_coded'] = self.cleaned_data['change_coded'].strip()

        for c in self.cleaned_data['change_coded']:
            if c not in 'бЗзКкСсЖж':
                raise forms.ValidationError('Изменение должно состоять из символов б, З, з, К, к, С, с, Ж, ж.')

        if self.cleaned_data['change_coded'].startswith('бб'):
            raise forms.ValidationError('Основание не может начинаться с "бб"')
        if self.cleaned_data['change_coded'].endswith('бб'):
            raise forms.ValidationError('Основание не может заканчиваться на "бб"')

        try:
            self.cleaned_data['change'] = translate(self.cleaned_data['change_coded']).capitalize()
            return self.cleaned_data['change_coded']
        except ValueError:
            raise forms.ValidationError('Изменение не распознано')

    def clean(self):
        if self.errors:
            return

        if abs(len(self.cleaned_data['change']) - len(self.cleaned_data['base'])) > 2:
            raise forms.ValidationError('Длина строк отличается больше чем на два символа.')

        return self.cleaned_data

    def save(self, role):
        invention = models.Invention.objects.create(
            author=role,
            name=self.cleaned_data['name'],
            hash=uuid4().hex,
            base_coded=self.cleaned_data['base_coded'],
            base=translate(self.cleaned_data['base_coded']).capitalize(),
            change_coded=self.cleaned_data['change_coded'],
            change=translate(self.cleaned_data['change_coded']).capitalize(),
        )

        return invention