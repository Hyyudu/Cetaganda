# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
import uuid

from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse

from models import *


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

    def save(self):
        duel = Duel.objects.create(
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
            (settings.DOMAIN, reverse('duel', args=[duel.role_1])),
            None,
            [self.cleaned_data['email_1']],
        )

        send_mail(
            'Дуэль',
            'Вы вызваны на дуэль с %s. Ваша ссылка - %s%s' %
            (self.cleaned_data['email_1'], settings.DOMAIN, reverse('duel', args=[duel.role_2])),
            None,
            [self.cleaned_data['email_2']],
        )

        return duel


class NewHackForm(forms.Form):
    email = forms.EmailField(label='Ваш email')
    length = forms.IntegerField(label='Количество цифр')

    def save(self):
        hack = Hack.objects.create(
            hacker=uuid.uuid4().hex,
            number=Hack.make_number(self.cleaned_data['length']),
        )

        send_mail(
            'Взлом',
            'Вы начали взлом. Ваша ссылка - %s%s' % (settings.DOMAIN, reverse('hack', args=[hack.hacker])),
            None,
            [self.cleaned_data['email']],
        )

        return hack
