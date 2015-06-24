# coding: utf8
from __future__ import unicode_literals

from uuid import uuid4

from django import forms

from roles.models import Role

from science import models
from science.utils import translate


class StoreForm(forms.Form):
    resource = forms.CharField(label='', widget=forms.Select, required=True)
    amount = forms.IntegerField(label='', required=True)

    def __init__(self, *args, **kwargs):
        super(StoreForm, self).__init__(*args, **kwargs)

        self.fields['resource'].widget.choices = [
            (letter, letter)
            for letter in 'бЗзКкСсЖж'
        ]

    def save(self, store):
        store.goods[self.cleaned_data['resource']] = \
            store.goods.get(self.cleaned_data['resource'], 0) + self.cleaned_data['amount']
        store.save()


class TransferForm(forms.Form):
    role = forms.IntegerField(label='Кому', widget=forms.Select, required=True)
    resource = forms.CharField(label='', widget=forms.Select, required=True)
    amount = forms.IntegerField(label='', required=True)

    def __init__(self, sender, *args, **kwargs):
        self.sender = sender
        super(TransferForm, self).__init__(*args, **kwargs)

        self.fields['resource'].widget.choices = [
            (letter, letter)
            for letter in 'бЗзКкСсЖж'
        ]

        self.fields['role'].widget.choices = [
            (role.id, role.name)
            for role in Role.objects.exclude(pk=sender.pk)
        ]

    def clean_role(self):
        try:
            return Role.objects.get(pk=self.cleaned_data['role'])
        except Role.DoesNotExist:
            raise forms.ValidationError('Неизвестная роль')

    def clean_amount(self):
        if self.cleaned_data['amount'] <= 0:
            raise forms.ValidationError('Количество ресурса должно быть положительным')
        return self.cleaned_data['amount']

    def clean(self):
        if self.errors:
            return

        sender_store = models.Store.get_or_create(self.sender)
        if sender_store.goods.get(self.cleaned_data['resource']) < self.cleaned_data['amount']:
            raise forms.ValidationError('У вас недостаточно ресурсов этого типа для передачи')
        return self.cleaned_data

    def save(self):
        sender_store = models.Store.get_or_create(self.sender)
        sender_store.goods[self.cleaned_data['resource']] = \
            sender_store.goods.get(self.cleaned_data['resource'], 0) - self.cleaned_data['amount']
        sender_store.save()

        recipient_store = models.Store.get_or_create(self.cleaned_data['role'])
        recipient_store.goods[self.cleaned_data['resource']] = \
            recipient_store.goods.get(self.cleaned_data['resource'], 0) + self.cleaned_data['amount']
        recipient_store.save()


class InventionForm(forms.Form):
    base_coded = forms.CharField(
        label='Основа', widget=forms.TextInput(attrs={'style': 'width: 800px;'}), required=True
    )
    change_coded = forms.CharField(
        label='Изменение', widget=forms.TextInput(attrs={'style': 'width: 800px;'}), required=True
    )
    name = forms.CharField(label='Название', required=False)

    def clean_base_coded(self):
        self.cleaned_data['base_coded'] = self.cleaned_data['base_coded'].strip()

        for c in self.cleaned_data['base_coded']:
            if c not in 'нНб':
                raise forms.ValidationError('Основа должна состоять из символов н, Н, б.')

        if self.cleaned_data['base_coded'].startswith('бб'):
            raise forms.ValidationError('Основа не может начинаться с "бб"')
        if self.cleaned_data['base_coded'].endswith('бб'):
            raise forms.ValidationError('Основа не может заканчиваться на "бб"')

        try:
            self.cleaned_data['base'] = translate(self.cleaned_data['base_coded']).capitalize()
            return self.cleaned_data['base_coded']
        except ValueError:
            raise forms.ValidationError('Основа не распознана')

    def clean_change_coded(self):
        self.cleaned_data['change_coded'] = self.cleaned_data['change_coded'].strip()

        for c in self.cleaned_data['change_coded']:
            if c not in 'бЗзКкСсЖж':
                raise forms.ValidationError('Изменение должно состоять из символов б, З, з, К, к, С, с, Ж, ж.')

        if self.cleaned_data['change_coded'].startswith('бб'):
            raise forms.ValidationError('Изменение не может начинаться с "бб"')
        if self.cleaned_data['change_coded'].endswith('бб'):
            raise forms.ValidationError('Изменение не может заканчиваться на "бб"')

        try:
            self.cleaned_data['change'] = translate(self.cleaned_data['change_coded']).capitalize()
            return self.cleaned_data['change_coded']
        except ValueError:
            raise forms.ValidationError('Изменение не распознано')

    def clean(self):
        if self.errors:
            return

        if abs(len(self.cleaned_data['change_coded']) - len(self.cleaned_data['base_coded'])) > 2:
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
