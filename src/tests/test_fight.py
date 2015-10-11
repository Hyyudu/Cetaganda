# coding: utf-8
from __future__ import unicode_literals
import random

import pytest
from mock import patch

from register.models import Record
from space import tactics
from space.models import Ship, Fleet, Report
from space.tactics import move_fleets
from tests.test_space import create_ship
from tests.utils import refresh

pytestmark = pytest.mark.django_db


def test_fight(roles, points, alliances):
    ship1, fleet1 = create_ship('k', roles['frodo'], roles['boromir'], points[3], name='frodoship')
    ship2, fleet2 = create_ship('k', roles['legolas'], roles['aragorn'], points[4], name='legoship')

    fleet1.route = str(points[4].id)
    fleet1.save()

    def dice(*args, **kwargs):
        yield 1
        yield 5

    with patch.object(random, 'randint') as randint:
        randint.side_effect = dice()

        move_fleets()

    fleet1 = refresh(fleet1)
    assert fleet1.point == points[4]

    records = Record.objects.filter(role=roles['frodo']).order_by('id')
    assert records[0].category == 'Космос'
    assert records[0].message == 'Ваш корабль "frodoship" перемещается в точку "Переход 2 (t)"'
    assert records[1].category == 'Космос'
    assert records[1].message == 'Ваш корабль "frodoship" уничтожает корабль "legoship"'

    ship1 = refresh(ship1)
    assert ship1.is_alive

    records = Record.objects.filter(role=roles['legolas']).order_by('id')
    assert records[0].category == 'Космос'
    assert records[0].message == 'Ваш корабль "legoship" промахивается'
    assert records[1].category == 'Космос'
    assert records[1].message == 'Ваш корабль "legoship" уничтожен залпом "frodoship"'

    ship2 = Ship.all.get(pk=ship2.id)
    assert not ship2.is_alive

    assert not Fleet.objects.filter(id=fleet2.id).exists()

    assert Report.objects.get().content == \
        '''Корабль "frodoship" (Переход 1 (t)) переместился в "Переход 2 (t)"
Корабль "legoship" (Переход 2 (t)) уничтожен
'''


def test_enemy_scout(roles, points, alliances):
    ship1, fleet1 = create_ship('k', roles['frodo'], roles['boromir'], points[3], name='frodoship')
    ship2, fleet2 = create_ship('r', roles['legolas'], roles['aragorn'], points[4], name='legoship')

    fleet1.route = str(points[4].id)
    fleet1.save()

    with patch.object(tactics, '_is_shoot') as shoot:
        shoot.return_value = 1

        move_fleets()

    ship1 = refresh(ship1)
    assert ship1.is_alive

    ship2 = Ship.all.get(pk=ship2.id)
    assert ship2.is_alive


def test_scout(roles, points, alliances):
    ship1, fleet1 = create_ship('r', roles['frodo'], roles['boromir'], points[3], name='frodoship')
    ship2, fleet2 = create_ship('k', roles['legolas'], roles['aragorn'], points[4], name='legoship')

    fleet1.route = str(points[4].id)
    fleet1.save()

    with patch.object(tactics, '_is_shoot') as shoot:
        shoot.return_value = 1

        move_fleets()

    ship1 = refresh(ship1)
    assert ship1.is_alive

    ship2 = Ship.all.get(pk=ship2.id)
    assert ship2.is_alive


def test_one_navigator(roles, points, alliances):
    ship1, fleet1 = create_ship('k', roles['frodo'], roles['boromir'], points[3], name='frodoship')
    ship2, fleet2 = create_ship('k', roles['legolas'], roles['boromir'], points[4], name='legoship')

    fleet1.route = str(points[4].id)
    fleet1.save()

    with patch.object(tactics, '_is_shoot') as shoot:
        shoot.return_value = 1

        move_fleets()

    ship1 = refresh(ship1)
    assert ship1.is_alive

    ship2 = refresh(ship1)
    assert ship2.is_alive


def test_one_alliance(roles, points, alliances):
    ship1, fleet1 = create_ship('k', roles['frodo'], roles['frodo'], points[3], name='frodoship')
    ship2, fleet2 = create_ship('k', roles['aragorn'], roles['legolas'], points[4], name='aragornship')

    fleet1.route = str(points[4].id)
    fleet1.save()

    with patch.object(tactics, '_is_shoot') as shoot:
        shoot.return_value = 1

        move_fleets()

    ship1 = refresh(ship1)
    assert ship1.is_alive

    ship2 = Ship.all.get(pk=ship2.id)
    assert ship2.is_alive


def test_catch_transport(roles, points, alliances):
    ship1, fleet1 = create_ship('k', roles['frodo'], roles['frodo'], points[3], name='frodoship')
    ship2, fleet1 = create_ship('t', roles['frodo'], roles['frodo'], points[3], name='frodotransport', fleet=fleet1)
    ship3, fleet2 = create_ship('k', roles['legolas'], roles['legolas'], points[4], name='legolasship')

    fleet1.route = str(points[4].id)
    fleet1.save()

    def dice():
        yield 5  # our cruiser miss
        yield 1  # their cruiser hit

    with patch.object(random, 'randint') as randint:
        randint.side_effect = dice()

        move_fleets()

    ship1 = Ship.all.get(pk=ship1.id)
    assert not ship1.is_alive
    assert ship1.owner == roles['frodo']

    ship2 = refresh(ship2)
    assert ship2.is_alive
    assert ship2.owner == roles['legolas']

    ship3 = refresh(ship3)
    assert ship3.is_alive

    assert roles['frodo'].records.order_by('-dt')[0].message == 'Вы утратили корабль "%s"' % ship2
    assert roles['legolas'].records.order_by('-dt')[0].message == 'Вы захватили корабль "%s"' % ship2
