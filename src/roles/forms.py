# coding: utf8
from __future__ import unicode_literals

from django import forms

from roles import models


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
        fields = ('name', 'group', 'target')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(RoleForm, self).__init__(*args, **kwargs)

        self.fields['group'].widget.choices = [('', '---')] + [
            (group.pk, group.name)
            for group in models.Group.objects.all()
        ]

        fields = models.GameField.objects.all().order_by('order')
        if self.request.user.has_perm('roles.can_edit_role'):
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
        role.creator = self.request.user
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


class BaseConnectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.role = kwargs.pop('role')
        super(BaseConnectionForm, self).__init__(*args, **kwargs)

        self.fields['role_rel'].widget.choices = [('', '-----')] + [
            (str(role.pk), role.name)
            for role in models.Role.objects.exclude(pk=self.role.pk)
        ]
        self.fields['topic'].widget.choices = [('', '-----')] + [
            (str(topic.pk), topic.name)
            for topic in models.Topic.objects.all()
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
