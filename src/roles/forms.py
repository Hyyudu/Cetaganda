# coding: utf8
from __future__ import unicode_literals

import random
import re

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms.models import modelform_factory

from roles import models
from roles.utils import process_template, send_html_mail


class RegistrationForm(forms.Form):
    email = forms.EmailField(max_length=100, error_messages={'required': 'Укажите свой email'})
    next = forms.CharField(max_length=2000, required=False, widget=forms.HiddenInput)

    def free_credentials(self, s):
        """ Проверяет строку на емейл, логин или имя пользователя """
        return User.objects.filter(Q(username=s) | Q(email=s) | Q(first_name=s)).count() == 0

    def make_login(self, desired_login=None):
        """ Генерация логина на основе емейла """
        if desired_login:
            login = desired_login
        elif '@' in self.cleaned_data['email']:
            login = self.cleaned_data['email'][:self.cleaned_data['email'].find('@')]
        else:
            login = self.cleaned_data['email']

        while True:
            if self.free_credentials(login):
                return login

            login += str(random.randint(1, 9))

    def check_login(self, name):
        return re.match('^[\d\w-]+$', name)

    def clean_email(self):
        if self.free_credentials(self.cleaned_data['email']):
            return self.cleaned_data['email']
        else:
            raise forms.ValidationError('В базе уже есть пользователь с введенным email')

    def generate_password(self):
        vowels = 'euioa'
        consonants = 'qwrtypsdfghjklzxcvbnm'
        digits = '123456789'
        pattern = 'cvcvcdcvcvc'
        return ''.join(random.choice({'v': vowels, 'c': consonants, 'd': digits}[c]) for c in pattern)

    def save(self):
        self.password = self.generate_password()
        new_user = User.objects.create_user(self.cleaned_data['email'],
                                            self.cleaned_data['email'],
                                            self.password)
        new_user.is_active = True
        new_user.first_name = self.cleaned_data['email']
        new_user.save()

        self.user = authenticate(username=new_user.username, password=self.password)

        subject, content = process_template(
            'email/registration.html',
            {
                'user': new_user,
                'form': self
            }
        )
        send_html_mail(subject, content, [self.cleaned_data['email']])


class LoginForm(forms.Form):
    login = forms.CharField(label='Email', max_length=100)
    passwd = forms.CharField(label='Пароль', max_length=100, widget=forms.PasswordInput)
    next = forms.CharField(max_length=2000, required=False, widget=forms.HiddenInput)

    def get_user(self, s):
        """ Проверяет строку на емейл, логин или имя пользователя """
        return User.objects.get(Q(username=s) | Q(email=s) | Q(first_name=s))

    def clean(self):
        login = self.cleaned_data.get('login', '')
        passwd = self.cleaned_data.get('passwd', '')

        try:
            user = self.get_user(login)
        except User.DoesNotExist:
            raise forms.ValidationError('Логин или пароль не верен')

        auth_user = authenticate(username=user.username, password=passwd)
        if auth_user:
            self.user = auth_user
            return self.cleaned_data
        else:
            raise forms.ValidationError('Логин или пароль не верен')


class CabinetForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=50)
    family = forms.CharField(label='Фамилия', max_length=50)
    nick = forms.CharField(label='Ник', max_length=50)
    age = forms.IntegerField(label='Возраст')
    phone = forms.CharField(label='Телефон', max_length=50)
    email = forms.CharField(label='Email', max_length=50)
    city = forms.CharField(label='Город', max_length=50)
    med = forms.CharField(label='Медицина', widget=forms.Textarea,
                          help_text='ваши медицинские особенности, которые надо знать организаторам.')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        try:
            self.userinfo = models.UserInfo.objects.get(ulogin__user=user)
        except models.UserInfo.DoesNotExist:
            try:
                self.userinfo = models.UserInfo.objects.get(user=user)
            except models.UserInfo.DoesNotExist:
                self.userinfo = models.UserInfo.objects.create(user=user)
        super(CabinetForm, self).__init__(*args, **kwargs)

        self.initial['name'] = user.first_name
        self.initial['family'] = user.last_name
        self.initial['email'] = user.email
        self.initial['nick'] = self.userinfo.nick
        self.initial['age'] = self.userinfo.age
        self.initial['phone'] = self.userinfo.phone
        self.initial['city'] = self.userinfo.city
        self.initial['med'] = self.userinfo.med

    def save(self):
        self.user.first_name = self.cleaned_data['name']
        self.user.last_name = self.cleaned_data['family']
        self.user.email = self.cleaned_data['email']
        self.user.save()

        self.userinfo.nick = self.cleaned_data['nick']
        self.userinfo.age = self.cleaned_data['age']
        self.userinfo.phone = self.cleaned_data['phone']
        self.userinfo.city = self.cleaned_data['city']
        self.userinfo.med = self.cleaned_data['med']
        self.userinfo.save()


class RequestForm(forms.Form):
    role = forms.IntegerField(label='Роль', widget=forms.Select)

    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)

        self.fields['role'].widget.choices = [
            (role.id, role.name)
            for role in models.Role.objects.filter(user__isnull=True)
        ]

    def clean_role(self):
        try:
            return models.Role.objects.get(pk=self.cleaned_data['role'], user__isnull=True)
        except models.Role.DoesNotExist:
            raise forms.ValidationError('Неизвестная роль')

    def save(self, user):
        self.cleaned_data['role'].user = user
        self.cleaned_data['role'].save()

        user.role = self.cleaned_data['role']
        user.save()


class RoleForm(forms.ModelForm):
    class Meta:
        model = models.Role
        fields = ('name', 'group')

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            self.game = kwargs['instance'].game
        else:
            self.game = kwargs.pop('game')
        self.request = kwargs.pop('request')
        super(RoleForm, self).__init__(*args, **kwargs)

        self.fields['group'].widget.choices = [('', '---')] + [
            (group.pk, group.name)
            for group in models.Group.objects.filter(game=self.game)
        ]

        fields = models.GameField.objects.filter(game=self.game).order_by('order')
        if self.game.is_master(self.request.user):
            visibility = ('master', 'player', 'all')
        elif kwargs.get('instance') and kwargs.get('instance').user != self.request.user:
            visibility = ('all',)
        else:
            visibility = ('player', 'all')

        fields = fields.filter(visibility__in=visibility)

        for field in fields:
            if field.type == 1:
                formfield = forms.CharField(label=field.name, max_length=255, required=False)
            elif field.type == 2:
                formfield = forms.CharField(label=field.name, widget=forms.Textarea, required=False)
            elif field.type == 3:
                formfield = forms.IntegerField(label=field.name, required=False)
            elif field.type == 4:
                formfield = forms.IntegerField(label=field.name, widget=forms.Select, required=False)
            else:
                raise ValueError('Unknown field type %s' % field.type)

            self.fields['rolefield_%s' % field.pk] = formfield
            if field.type == 4:
                self.fields['rolefield_%s' % field.pk].widget.choices = list(enumerate(field.additional.split(',')))

        if kwargs.get('instance'):
            for field in models.RoleField.objects.filter(role=kwargs.get('instance')):
                self.initial['rolefield_%s' % field.field.pk] = field.value

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        role = super(RoleForm, self).save(*args, **kwargs)
        role.game = self.game
        role.save()

        for field_id, field in self.fields.items():
            if not field_id.startswith('rolefield'):
                continue

            pk = int(field_id[10:])
            rolefield, _ = models.RoleField.objects.get_or_create(
                role=role,
                field=models.GameField.objects.get(pk=pk),
            )
            rolefield.value = self.cleaned_data[field_id]
            rolefield.save()

        return role


class DualConnectionForm(forms.Form):
    comment = forms.CharField(label='Описание', widget=forms.Textarea)

    def save(self, base_connection):
        return models.RoleConnection.objects.create(
            role=base_connection.role_rel,
            role_rel=base_connection.role,
            comment=self.cleaned_data['comment'],
            topic=base_connection.topic,
        )


GameForm = modelform_factory(models.Game, exclude=('owner', 'paid'))
GameFieldsFormSet = forms.inlineformset_factory(models.Game, models.GameField, fk_name='game', extra=3, exclude=[])
GameGroupsFormSet = forms.inlineformset_factory(models.Game, models.Group, fk_name='game', extra=3, exclude=[])
GameTopicsFormSet = forms.inlineformset_factory(models.Game, models.Topic, fk_name='game', extra=3, exclude=[])


class BaseConnectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.role = kwargs.pop('role')
        super(BaseConnectionForm, self).__init__(*args, **kwargs)

        self.fields['role_rel'].widget.choices = [('', '-----')] + [
            (str(role.pk), role.name)
            for role in models.Role.objects.filter(game=self.role.game).exclude(pk=self.role.pk)
        ]
        self.fields['topic'].widget.choices = [('', '-----')] + [
            (str(topic.pk), topic.name)
            for topic in models.Topic.objects.filter(game=self.role.game)
        ]


class BaseConnectionFormSet(forms.BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        kwargs['role'] = self.instance
        return super(BaseConnectionFormSet, self)._construct_form(i, **kwargs)


ConnectionFormSet = forms.inlineformset_factory(
    models.Role,
    models.RoleConnection,
    form=BaseConnectionForm,
    formset=BaseConnectionFormSet,
    fk_name='role',
    exclude=('is_locked',),
    extra=1,
)
