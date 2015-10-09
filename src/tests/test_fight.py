# coding: utf-8
from __future__ import unicode_literals
import random

import pytest
from mock import patch

from space.models import Ship, Fleet
from space.tactics import move_fleets
from register.models import Record
from tests.utils import refresh
from tests.test_space import create_ship

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
    assert records[1].message == 'Ваш корабль "frodoship" попадает по кораблю "legoship"'

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
