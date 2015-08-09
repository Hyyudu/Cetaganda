# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from datetime import datetime
import uuid
import string

from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse

from hack import models


class DefenceForm(forms.Form):
    floats = forms.CharField(label='Поплавки', required=True, widget=forms.TextInput(attrs={'style': 'width: 600px;'}))
    target = forms.CharField(label='Защита', widget=forms.Select, required=True)

    def __init__(self, role, *args, **kwargs):
        self.role = role
        super(DefenceForm, self).__init__(*args, **kwargs)

        self.fields['target'].widget.choices = models.Target.TARGETS

    def clean_floats(self):
        hashes = map(string.strip, re.sub('[^\w]', ' ', self.cleaned_data['floats']).split())
        print hashes
        floats = []
        for hash in hashes:
            try:
                floats.append(models.Float.objects.get(owner=self.role, target__isnull=True, hash=hash, is_active=True))
            except (models.Float.DoesNotExist, models.Float.MultipleObjectsReturned):
                raise forms.ValidationError('Поплавок "%s" не найден' % hash)
        print floats
        return floats

    def clean_target(self):
        if self.cleaned_data['target'] in [target[0] for target in models.Target.TARGETS]:
            return self.cleaned_data['target']
        else:
            raise forms.ValidationError('Неизвестная цель защиты')

    def clean(self):
        if self.errors:
            return

        target, _ = models.Target.objects.get_or_create(role=self.role, target=self.cleaned_data['target'])
        levels = target.get_levels()
        required_level = self.get_level_hole(levels)
        print required_level
        print len(self.cleaned_data['floats'])

        if len(self.cleaned_data['floats']) < required_level:
            raise forms.ValidationError(
                'Недостаточно ПО для постановки защиты, требуется %s поплавков' % required_level
            )

        self.cleaned_data['floats'] = self.cleaned_data['floats'][:required_level]
        self.cleaned_data['target'] = target
        self.cleaned_data['level'] = required_level
        return self.cleaned_data

    def get_level_hole(self, levels):
        """
        Ищет дырку в ряду уровней - минимальное число, которого нет в списке
        :param levels: список натуральных чисел
        :return: уровень
        """
        levels = set(levels)
        for i in xrange(1, 100):
            if i not in levels:
                return i

        raise forms.ValidationError('Слишком много уровней защиты, хватит уже')

    def save(self):
        for float in self.cleaned_data['floats']:
            float.target = self.cleaned_data['target']
            float.target_level = self.cleaned_data['level']
            float.is_active = True
            float.save()


class NewDuelForm(forms.Form):
    number = forms.CharField(label='Загадайте число')
    email_1 = forms.EmailField(label='Ваш email')
    email_2 = forms.EmailField(label='Email оппонента')

    def clean_number(self):
        number = self.cleaned_data['number']

        if not number.isdigit():
            raise forms.ValidationError('Введите число')

        if len(set(number)) != len(number):
            raise forms.ValidationError('Все цифры числа должны быть разными')

        return self.cleaned_data['number']

    def save(self, role):
        duel = models.Duel.objects.create(
            owner=role,
            role_1=uuid.uuid4().hex,
            role_2=uuid.uuid4().hex,
            email_1=self.cleaned_data['email_1'],
            email_2=self.cleaned_data['email_2'],
            number_1=self.cleaned_data['number'],
            dt=datetime.now(),
        )

        send_mail(
            'Дуэль',
            'Вы отправили приглашение на дуэль. Ваша ссылка - %s%s' %
            (settings.DOMAIN, reverse('hack:duel', args=[duel.role_1])),
            None,
            [self.cleaned_data['email_1']],
        )

        send_mail(
            'Дуэль',
            'Вы вызваны на дуэль с %s. Ваша ссылка - %s%s' %
            (self.cleaned_data['email_1'], settings.DOMAIN, reverse('hack:duel', args=[duel.role_2])),
            None,
            [self.cleaned_data['email_2']],
        )

        return duel


class NewHackForm(forms.Form):
    email = forms.EmailField(label='Ваш email')
    length = forms.IntegerField(label='Количество цифр')

    def save(self):
        hack = models.Hack.objects.create(
            hacker=uuid.uuid4().hex,
            number=models.Hack.make_number(self.cleaned_data['length']),
        )

        send_mail(
            'Взлом',
            'Вы начали взлом. Ваша ссылка - %s%s' % (settings.DOMAIN, reverse('hack:hack', args=[hack.hacker])),
            None,
            [self.cleaned_data['email']],
        )

        return hack
