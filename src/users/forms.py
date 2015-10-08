# coding: utf8
from __future__ import unicode_literals
import uuid

from django import forms
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from users import models


class CabinetForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=50)
    family = forms.CharField(label='Фамилия', max_length=50)
    nick = forms.CharField(label='Ник', max_length=50)
    age = forms.IntegerField(label='Возраст')
    phone = forms.CharField(label='Телефон', max_length=50)
    email = forms.CharField(label='Email', max_length=50)
    city = forms.CharField(label='Город', max_length=50)
    med = forms.CharField(
        label='Медицина', widget=forms.Textarea, required=False,
        help_text='ваши медицинские особенности, которые надо знать организаторам.',
    )

    def __init__(self, user, *args, **kwargs):
        if not user.is_authenticated():
            return

        self.user = user
        try:
            self.userinfo = models.UserInfo.objects.filter(user=self.user)[0]
        except (models.UserInfo.DoesNotExist, IndexError):
            try:
                self.userinfo = models.UserInfo.objects.get(user=self.user)
            except models.UserInfo.DoesNotExist:
                self.userinfo = models.UserInfo.objects.create(user=self.user)
        super(CabinetForm, self).__init__(*args, **kwargs)

        self.initial['name'] = self.user.first_name
        self.initial['family'] = self.user.last_name
        self.initial['email'] = self.user.email
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


class RegistrationForm(forms.Form):
    email = forms.EmailField(max_length=100)

    def clean_email(self):
        if get_user_model().objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError('Такой email на сайте уже есть. Может, вы регистрировались у нас?')
        return self.cleaned_data['email']

    def save(self):
        password = get_random_string(20, '0123456789abcdefghijklmnopqrstuvwxyz')
        email = self.cleaned_data['email']

        user = get_user_model().objects.create_user(
            username=uuid.uuid4().hex[:30],
            password=password,
            email=email,
        )
        user.is_active = True
        user.save()

        models.UserInfo.objects.create(user=user)

        auth_user = authenticate(username=user.username, password=password)

        return auth_user, password


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())

    def clean(self):
        if self.errors:
            return

        User = get_user_model()
        try:
            user = User.objects.get(email=self.cleaned_data['email'])
        except User.DoesNotExist:
            raise forms.ValidationError('Логин или пароль не верен')

        auth_user = authenticate(username=user.username, password=self.cleaned_data['password'])
        if auth_user:
            self.cleaned_data['user'] = auth_user
            return self.cleaned_data
        else:
            raise forms.ValidationError('Логин или пароль не верен')
