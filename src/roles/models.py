# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.mail import send_mail

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class GenericManager(models.Manager):
    """
    Filters query set with given selectors
    """
    def __init__(self, **kwargs):
        super(GenericManager, self).__init__()
        self.selectors = kwargs

    def get_queryset(self):
        return super(GenericManager, self).get_queryset().filter(**self.selectors)


class GameField(models.Model):
    TYPES = (
        (1, 'Строка'),
        (2, 'Текст'),
        (3, 'Число'),
        (4, 'Варианты'),
    )
    name = models.CharField(verbose_name='Название', max_length=255)
    type = models.IntegerField(verbose_name='Тип поля', choices=TYPES)
    additional = models.CharField(
        verbose_name='Доп инфо', max_length=255, null=True, blank=True, default=None,
        help_text='Для поля вариантов - варианты через запятую',
    )
    order = models.IntegerField(verbose_name='Порядок', default=0)
    visibility = models.CharField(
        verbose_name='Уровень видимости',
        max_length=100,
        choices=(('master', 'Мастер'), ('player', 'Игрок'), ('all', 'Все')),
        default='all',
    )
    required = models.BooleanField(verbose_name='Обязательное', default=False)
    show_in_list = models.BooleanField(verbose_name='Отображать в списке ролей', default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Поле игры'
        verbose_name_plural = 'Поля ролей'
        ordering = ('order',)


class Group(models.Model):
    """Группировка ролей"""
    name = models.CharField(verbose_name='Название', max_length=255)
    description = models.TextField(verbose_name='Описание', null=True, blank=True, default=None)
    color = models.CharField(verbose_name='Цвет', default='000000', max_length=6, help_text='В hex формате')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Блок в игре'
        verbose_name_plural = 'Блоки'


class Topic(models.Model):
    """Сюжет для связей ролей"""
    name = models.CharField(verbose_name='Название', max_length=255)
    description = models.TextField(verbose_name='Описание', null=True, blank=True, default=None)
    color = models.CharField(verbose_name='Цвет', default='000000', max_length=6, help_text='В hex формате')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Сюжет'
        verbose_name_plural = 'Сюжеты'


class Role(models.Model):
    group = models.ForeignKey(Group, verbose_name='Блок', null=True, blank=True, default=None)
    creator = models.ForeignKey(
        AUTH_USER_MODEL, verbose_name='Создатель',
        null=True, blank=True, default=None,
        related_name='creator',
    )
    target = models.CharField(
        verbose_name='Для кого заполняете заявку',
        choices=(
            ('free', 'Свободная'),
            ('me', 'Для себя'),
            ('other', 'Для друга'),
            ('fake', 'Временная'),
        ),
        default='free',
        max_length=20,
    )
    user = models.ForeignKey(
        AUTH_USER_MODEL, verbose_name='Игрок',
        null=True, blank=True, default=None,
        related_name='gamer',
    )
    name = models.CharField(verbose_name='Имя', max_length=255)
    is_locked = models.BooleanField(
        verbose_name='Заморожена', default=False,
        help_text='Можно ли игроку редактировать роль',
    )
    is_hidden = models.BooleanField(verbose_name='Скрыта', default=False)

    objects = GenericManager(is_hidden=False)
    all = GenericManager()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('roles:view', args=[self.id])

    def can_edit(self, user):
        if user.has_perm('roles.can_edit_role'):
            return True

        if self.is_locked:
            return False

        if self.user == user:
            return True

        if not self.user and self.creator == user:
            return True

        return False

    def view_level(self, user):
        if user.has_perm('roles.can_edit_role'):
            return 'master'

        if self.user == user and self.is_locked:
            return 'player'

        if self.creator == user and not self.is_locked:
            return 'player'

        return 'all'

    def get_player(self):
        if self.target == 'me' and self.creator:
            return self.creator
        return self.user

    def username(self):
        user = self.get_player()
        if not user:
            return '-'
        from users.models import UserInfo
        userinfo = UserInfo.objects.filter(user=user)[0]
        name = '%s %s' % (user.last_name, user.first_name)
        if userinfo.nick:
            name += ' (%s)' % userinfo.nick
        return name
    username.short_description = 'Игрок'

    def userlink(self):
        user = self.get_player()
        if not user:
            return
        try:
            return user.ulogin_users.all()[0].identity
        except IndexError:
            return

    def send_mail(self, subject, message):
        if self.user and self.user.email:
            send_mail(subject, message, None, [self.user.email])
        else:
            send_mail('Для %s' % self.name + subject, message, None, [settings.ADMINS[0][1]])

    def set_field(self, field_name, value):
        try:
            gamefield = GameField.objects.get(name=field_name)
        except GameField.DoesNotExist:
            raise ValueError('Неизвестное поле %s' % field_name)

        field, _ = RoleField.objects.get_or_create(
            role=self, field=gamefield
        )
        field.value = value
        field.save()

    def get_field(self, field_name):
        try:
            gamefield = GameField.objects.get(name=field_name)
        except GameField.DoesNotExist:
            raise ValueError('Неизвестное поле %s' % field_name)

        field, _ = RoleField.objects.get_or_create(
            role=self, field=gamefield
        )
        if gamefield.type == 3:
            return int(field.value or 0)

        return field.value

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'
        permissions = (
            ('can_edit_role', 'Может редактировать роли'),
        )


class RoleField(models.Model):
    role = models.ForeignKey(Role, verbose_name='Роль')
    field = models.ForeignKey(GameField, verbose_name='Поле')
    value = models.TextField(verbose_name='Значение', null=True, blank=True, default=None)

    class Meta:
        verbose_name = 'Поле роли'
        verbose_name_plural = 'Поля ролей'


class RoleConnection(models.Model):
    role = models.ForeignKey(Role, verbose_name='Роль', related_name='roles')
    role_rel = models.ForeignKey(Role, verbose_name='Связанная роль',
                                 related_name='linked_roles', null=True, blank=True)
    comment = models.TextField(verbose_name='Описание', null=True, blank=True, default=None)
    topic = models.ForeignKey(Topic, verbose_name='Сюжет', null=True, blank=True, default=None)
    is_locked = models.BooleanField(verbose_name='Заморожено', default=False)

    class Meta:
        verbose_name = 'Связь ролей'
        verbose_name_plural = 'Связи ролей'
