# coding: utf8
from __future__ import unicode_literals

from django import forms

from users import models


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
