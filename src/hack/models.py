# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random
import uuid

from django.core.urlresolvers import reverse
from django.db import models

from roles.models import Role
from market.models import Goods


class Duel(models.Model):
    owner = models.ForeignKey(Role, verbose_name='Запустивший')
    role_1 = models.CharField(verbose_name='Игрок 1', max_length=100)
    role_2 = models.CharField(verbose_name='Игрок 2', max_length=100)
    email_1 = models.CharField(verbose_name='Email 1', max_length=100)
    email_2 = models.CharField(verbose_name='Email 2', max_length=100)
    STATES = (
        ('not_started', 'Не началась'),
        ('in_progress', 'Идет'),
        ('finished', 'завершена'),
    )
    state = models.CharField(verbose_name='Состояние', max_length=20, default='not_started', choices=STATES)
    number_1 = models.CharField(
        verbose_name='Загаданное число 1', max_length=10,
        help_text='До 10 символов. Обычно - 4. Машинист должен будет ввести число такой же длины.',
    )
    number_2 = models.CharField(verbose_name='Загаданное число 2', max_length=10, null=True, blank=True, default=None)
    winner = models.CharField(verbose_name='Победитель', max_length=100, null=True, blank=True, default=None)
    result = models.CharField(verbose_name='Итог', max_length=20, null=True, blank=True, default=None)
    dt = models.DateTimeField(verbose_name='Начало дуэли', default=None)

    @classmethod
    def get_result(cls, number, move):
        res = []
        good = list(number)
        for i, l in enumerate(move):
            if l == good[i]:
                res.append('1')
            elif l in good:
                res.append('0')

        res.sort(reverse=True)
        return ''.join(res)

    @property
    def number_len(self):
        return len(str(self.number_1))

    class Meta:
        verbose_name = 'Дуэль'
        verbose_name_plural = 'Взломы: дуэли'


class DuelMove(models.Model):
    duel = models.ForeignKey(Duel, verbose_name='Дуэль')
    dt = models.DateTimeField(verbose_name='Начало хода', default=None)
    move_1 = models.CharField(verbose_name='Ход игрока 1', max_length=10, null=True, blank=True, default=None)
    result_1 = models.CharField(verbose_name='Результат игрока 1', max_length=10, null=True, blank=True, default=None)
    move_2 = models.CharField(verbose_name='Ход игрока 2', max_length=10, null=True, blank=True, default=None)
    result_2 = models.CharField(verbose_name='Результат игрока 2', max_length=10, null=True, blank=True, default=None)

    def save(self, *args, **kwargs):
        if self.move_1 and not self.result_1:
            self.result_1 = Duel.get_result(self.duel.number_2, self.move_1)

        if self.move_2 and not self.result_2:
            self.result_2 = Duel.get_result(self.duel.number_1, self.move_2)

        super(DuelMove, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Ход дуэли'
        verbose_name_plural = 'Ходы дуэлей'


class Target(models.Model):
    TARGETS = (
        ('role.credits', 'Персонаж: кража 10 кредитов'),
        ('role.official', 'Персонаж: официальное досье'),
        ('role.personal', 'Персонаж: профессиональные особенности'),
        ('role.messages', 'Персонаж: переписка'),
        ('role.info', 'Персонаж: Личное дело'),
        ('role.defence', 'Персонаж: Список защит'),
        # ('corporation.book', 'Корпорация: гостевая книга'),
        # ('corporation.money', 'Корпорация: сумма на счету'),
        # ('corporation.docslist', 'Корпорация: список документов'),
        # ('corporation.doc', 'Корпорация: кража/изменение документа'),
    )
    role = models.ForeignKey(Role, verbose_name='Роль', null=True, blank=True, default=None, related_name='targets')
    target = models.CharField(verbose_name='Цель', max_length=50, choices=TARGETS)

    def get_levels(self):
        floats = self.floats.filter(is_active=True)
        return sorted(list(set(float.target_level for float in floats)))
    get_levels.short_description = 'Уровни защиты'

    def __unicode__(self):
        return self.target

    @property
    def complexity(self):
        return {
            'role.credits': 4,
            'role.official': 4,
            'role.personal': 4,
            'role.messages': 5,
            'role.info': 6,
            'role.defence': 6,
        }[self.target]

    def prize(self):
        """
        :return: Взломанная информация
        """
        return self.target + uuid.uuid4().hex

    class Meta:
        verbose_name = 'Цель атаки'
        verbose_name_plural = 'Цели атак'


class Float(models.Model):
    owner = models.ForeignKey(Role, verbose_name='Роль', related_name='floats')
    hash = models.CharField(verbose_name='Хэш', max_length=32)
    target = models.ForeignKey(
        Target,
        verbose_name='Защищает',
        null=True, blank=True, default=None,
        related_name='floats'
    )
    target_level = models.PositiveIntegerField(verbose_name='Уровень защиты', null=True, blank=True, default=None)
    is_active = models.BooleanField(verbose_name='Активен', default=True)

    @classmethod
    def create(cls, owner):
        return cls.objects.create(
            owner=owner,
            hash=uuid.uuid4().hex[:8],
        )

    @staticmethod
    def market_name():
        return 'Поплавок'

    @staticmethod
    def market_description():
        return ''

    def change_owner(self, owner):
        self.owner = owner
        self.save()

    class Meta:
        verbose_name = 'Поплавок'
        verbose_name_plural = 'Поплавки'


Goods.register_infinite_product(Float, 100)


class Hack(models.Model):
    """Хак без защитника"""
    hacker = models.ForeignKey(Role, verbose_name='Хакер')
    hash = models.CharField(verbose_name='Хэш', max_length=32)
    target = models.ForeignKey(Target, verbose_name='Цель')
    dt = models.DateTimeField(auto_now_add=True, verbose_name='Начало атаки')
    number = models.CharField(max_length=10, verbose_name='Взламываемое число')
    STATUSES = (
        (None, 'Создано'),
        ('inprocess', 'Идет'),
        ('win', 'Взломано'),
        ('run', 'Сбежал'),
        ('failstatic', 'Не хватило поплавков'),
        ('fail', 'Не осилил'),
        ('late', 'Опоздал'),
    )
    status = models.CharField(
        verbose_name='Статус', choices=STATUSES,
        max_length=20, null=True, blank=True, default=None,
    )

    @classmethod
    def make_number(cls, length):
        seq = range(10)
        random.shuffle(seq)
        number = ''.join(str(i) for i in seq[:length])
        return number

    def get_absolute_url(self):
        return reverse('hack:hack', args=[self.hash])

    def set_status(self, status):
        self.status = status
        self.save()

        if status == 'inprocess':
            self.target.role.send_mail(
                'Цетаганда: вы начали взлом',
                'Вы начали взлом "%s - %s". Ссылка на взлом - %s.'
                % (self.target.role, self.target.get_target_display(), self.get_absolute_url()),
            )

        elif status == 'failstatic':
            self.target.role.send_mail(
                'Цетаганда: вас пытались взломать',
                'Хакер %s пытался взломать %s, но не смог преодолеть статическую защиту. Проверьте уровень защиты.'
                % (self.hacker, self.target.get_target_display()),
            )
            self.hacker.send_mail(
                'Цетаганда: вы облажались',
                'У вас не хватило поплавков, чтобы пройти уровни защиты. Бегите.',
            )

        elif status == 'fail':
            self.target.role.send_mail(
                'Цетаганда: вас пытались взломать',
                'Хакер %s пытался взломать %s, но не смог преодолеть динамическую защиту. Проверьте уровень защиты.'
                % (self.hacker, self.target.get_target_display()),
            )
            self.hacker.send_mail(
                'Цетаганда: вы не смогли взломать систему',
                'У вас не хватило умения и удачи, чтобы взломать базу. Бегите.',
            )

        elif status == 'win':
            self.target.role.send_mail(
                'Цетаганда: вас взломали',
                'Хакер %s успешно взломал %s. Примите наши соболезнования.'
                % (self.hacker, self.target.get_target_display()),
            )
            self.hacker.send_mail(
                'Цетаганда: вы успешно взломали',
                'Вы успешно взломали "%s - %s". Ваш результат: %s'
                % (self.target.role, self.target.get_target_display(), self.target.prize()),
            )

    class Meta:
        verbose_name = 'Взлом'
        verbose_name_plural = 'Взломы'


class HackMove(models.Model):
    hack = models.ForeignKey(Hack, verbose_name='Взлом')
    dt = models.DateTimeField(verbose_name='Начало хода', auto_now_add=True)
    move = models.CharField(verbose_name='Ход', max_length=10, null=True, blank=True, default=None)
    result = models.CharField(verbose_name='Результат', max_length=10, null=True, blank=True, default=None)

    def save(self, *args, **kwargs):
        if self.move and not self.result:
            self.result = Duel.get_result(self.hack.number, self.move)

        super(HackMove, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Ход взлома'
        verbose_name_plural = 'Ходы взломов'
