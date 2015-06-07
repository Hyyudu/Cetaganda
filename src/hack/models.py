# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random

from django.db import models


class Duel(models.Model):
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


class Hack(models.Model):
    """Хак без защитника"""
    hacker = models.CharField(verbose_name='Игрок 1', max_length=100)
    dt = models.DateTimeField(auto_now_add=True, verbose_name='Начало атаки')
    number = models.CharField(max_length=10, verbose_name='Взламываемое число')
    RESULTS = (
        (None, 'Идет'),
        ('win', 'Взломано'),
        ('run', 'Сбежал'),
        ('fail', 'Облом'),
        ('late', 'Опоздал'),
    )
    result = models.CharField(verbose_name='Итог', choices=RESULTS, max_length=20, null=True, blank=True, default=None)

    @classmethod
    def make_number(cls, length):
        seq = range(10)
        random.shuffle(seq)
        number = ''.join(str(i) for i in seq[:length])
        return number

    def save(self, *args, **kwargs):
        super(Hack, self).save(*args, **kwargs)

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