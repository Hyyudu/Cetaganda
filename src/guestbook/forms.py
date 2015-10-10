# coding: utf8
from __future__ import unicode_literals

from django import forms

from guestbook import models


class PostForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': 3, 'cols': 100}))

    class Meta:
        model = models.Post
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(PostForm, self).__init__(*args, **kwargs)

    def clean(self):
        if not self.request.role:
            raise forms.ValidationError('Вам нужна роль, от имени которой вы будете писать.')

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        post = super(PostForm, self).save(*args, **kwargs)
        post.author = self.request.role
        post.save()
