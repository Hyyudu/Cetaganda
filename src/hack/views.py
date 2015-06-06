# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from hack.forms import NewDuelForm, NewHackForm
from hack.models import Duel, DuelMove, Hack, HackMove


class HackIndexView(TemplateView):
    template_name = 'hack/index.html'

    def get_context_data(self, **kwargs):
        context = super(HackIndexView, self).get_context_data(**kwargs)
        context['duel_form'] = NewDuelForm()
        context['hack_form'] = NewHackForm()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        if request.POST.get('action') == 'duel':
            context['duel_form'] = NewDuelForm(request.POST)
            if context['duel_form'].is_valid():
                duel = context['duel_form'].save()
                return HttpResponseRedirect(reverse('duel', args=[duel.role_1]))
        else:
            context['hack_form'] = NewHackForm(request.POST)
            if context['hack_form'].is_valid():
                duel = context['hack_form'].save()
                return HttpResponseRedirect(reverse('hack', args=[duel.hacker]))

        return self.render_to_response(context)


def check_number(string, length):
    if not string.isdigit():
        raise ValueError('Введите число')

    if len(string) != length:
        raise ValueError('Число должно состоять из %s цифр' % length)

    if len(set(string)) != len(string):
        raise ValueError('Все цифры числа должны быть разными')


class DuelView(TemplateView):
    template_name = 'hack/duel.html'

    def get_context_data(self, **kwargs):
        context = super(DuelView, self).get_context_data(**kwargs)
        self.duel = get_object_or_404(Duel, Q(role_1=kwargs['key']) | Q(role_2=kwargs['key']))

        context.update({
            'mode': kwargs['key'] == self.duel.role_1 and 'hacker' or 'security',
            'moves': list(self.duel.duelmove_set.all().order_by('dt')),
            'last_move': None,
            'duel': self.duel,
            'number_len': self.duel.number_len,
        })
        context['can_move'] = context['mode'] == 'security' and self.duel.state == 'not_started'

        if len(context['moves']):
            context['last_move'] = context['moves'][-1]

        if self.duel.state == 'in_progress':
            if context['last_move']:
                # предыдущий ход сделан обоими сторонами
                if context['last_move'].move_1 and context['last_move'].move_2:
                    context['can_move'] = True

                elif context['mode'] == 'hacker':
                    # Ломщик
                    if not context['last_move'].move_1:
                        context['can_move'] = True

                else:
                    # Машинист
                    if not context['last_move'].move_2:
                        context['can_move'] = True

            else:  # Еще не сделано ни одного хода
                context['can_move'] = True

        return context

    def post(self, request, *agrs, **kwargs):
        context = self.get_context_data(**kwargs)

        if self.duel.state == 'finished':
            return self.render_to_response(context)

        if context['mode'] == 'security' and self.duel.state == 'not_started':
            try:
                n = request.POST.get('number')
                check_number(n, len(self.duel.number_1))

                self.duel.number_2 = n
                self.duel.state = 'in_progress'
                self.duel.save()

                return HttpResponseRedirect(reverse('duel', args=[kwargs['key']]))

            except ValueError, e:
                context['error'] = unicode(e)

        # Ходы
        if self.duel.state == 'in_progress':
            if request.POST.get('action') == 'Сдаться':
                self.duel.state = 'finished'
                self.duel.winner = self.duel.role_2
                self.duel.result = 'Ломщик сбежал'
                self.duel.save()
                return HttpResponseRedirect(reverse('duels'))

            try:
                number = request.POST.get('number')
                check_number(number, len(self.duel.number_1))

                if not context['last_move'] or (context['last_move'].move_1 and context['last_move'].move_2):
                    context['last_move'] = DuelMove.objects.create(
                        duel=self.duel,
                        dt=datetime.now()
                    )
                    setattr(context['last_move'], 'move_%s' % (context['mode'] == 'hacker' and '1' or '2'), number)
                    context['last_move'].save()

                elif context['mode'] == 'hacker' and not context['last_move'].move_1:
                    context['last_move'].move_1 = number
                    context['last_move'].save()

                elif context['mode'] == 'security' and not context['last_move'].move_2:
                    context['last_move'].move_2 = number
                    context['last_move'].save()

                if context['last_move'].result_1 == '1' * self.duel.number_len:
                    self.duel.state = 'finished'
                    self.duel.winner = self.duel.role_1
                    self.duel.result = 'Хакер выиграл'
                    self.duel.save()
                    return HttpResponseRedirect(reverse('duel', args=[kwargs['key']]))

                if context['last_move'].result_2 == '1' * self.duel.number_len:
                    self.duel.state = 'finished'
                    self.duel.winner = self.duel.role_2
                    self.duel.result = 'Защитник выиграл'
                    self.duel.save()
                    return HttpResponseRedirect(reverse('duel', args=[kwargs['key']]))

                return HttpResponseRedirect(reverse('duel', args=[kwargs['key']]))

            except ValueError, e:
                context['error'] = unicode(e)

        return self.render_to_response(context)


class HackView(TemplateView):
    template_name = 'hack/hack.html'

    def get_context_data(self, **kwargs):
        context = super(HackView, self).get_context_data(**kwargs)
        self.hack = get_object_or_404(Hack, hacker=kwargs['key'])
        context['hack'] = self.hack
        context['moves'] = self.hack.hackmove_set.all().order_by('id')
        return context

    def post(self, request, *agrs, **kwargs):
        context = self.get_context_data(**kwargs)

        if self.hack.result:
            return self.render_to_response(context)

        if request.POST.get('action') == 'Сбежать':
            self.hack.result = 'run'
            self.hack.save()
            return HttpResponseRedirect(reverse('hack', args=[self.hack.hacker]))

        else:
            try:
                number = request.POST.get('number')
                check_number(number, len(self.hack.number))

                result = Duel.get_result(self.hack.number, number)
                context['last_move'] = HackMove.objects.create(
                    hack=self.hack,
                    move=number,
                    result=result,
                )

                if result == '1' * len(self.hack.number):
                    # Сохраняем результат
                    self.hack.result = 'win'
                    self.hack.save()

                    return HttpResponseRedirect(reverse('hack', args=[self.hack.hacker]))

                if HackMove.objects.filter(hack=self.hack).count() >= 6:
                    self.hack.result = 'fail'
                    self.hack.save()

                    return HttpResponseRedirect(reverse('hack', args=[self.hack.hacker]))

            except ValueError, e:
                context['error'] = e

        return self.render_to_response(context)
