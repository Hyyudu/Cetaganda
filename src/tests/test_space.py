# coding: utf-8
from __future__ import unicode_literals

import pytest

from space.models import Ship, Alliance, Point, Transit, Fleet
from space.tactics import move_fleets

pytestmark = pytest.mark.django_db


@pytest.fixture()
def alliances():
    return [
        Alliance.objects.create(name='Барраяр', role_name='Барраяр'),
        Alliance.objects.create(name='Цетаганда', role_name='Цетаганда'),
    ]


@pytest.fixture()
def points():
    p1 = Point.objects.create(name='Планета 1', type='planet')
    p2 = Point.objects.create(name='Планета 2', type='planet')
    p3 = Point.objects.create(name='Планета 3', type='planet')
    tr1 = Point.objects.create(name='Переход 1', type='transit')
    tr2 = Point.objects.create(name='Переход 2', type='transit')
    tr3 = Point.objects.create(name='Переход 3', type='transit')
    Transit.objects.create(point1=p1, point2=tr1)
    Transit.objects.create(point1=p2, point2=tr2)
    Transit.objects.create(point1=p3, point2=tr3)
    Transit.objects.create(point1=tr1, point2=tr2)
    Transit.objects.create(point1=tr2, point2=tr3)
    Transit.objects.create(point1=tr3, point2=tr1)
    return [p1, p2, p3, tr1, tr2, tr3]


def test_space(users, roles, points, alliances):
    ship = Ship.objects.create(
        name='11',
        owner=roles['frodo'],
        alliance=alliances[0],
        in_space=True,
        position=points[0],
        type='t',
    )

    fleet = Fleet.objects.create(name='fl1', navigator=roles['legolas'], point=ship.position)
    ship.fleet = fleet
    ship.save()

    fleet.route = ' '.join(map(str, [points[0].id, points[3].id, points[4].id, points[1].id]))
    assert fleet.human_route() == 'Планета 1 (p) -> Переход 1 (t) -> Переход 2 (t) -> Планета 2 (p)'

    move_fleets()

    assert fleet.point == points[1]
