# coding: utf-8
from __future__ import unicode_literals

import pytest

from space.models import Ship, Alliance, Point, Transit, Fleet
from space.tactics import move_fleets
from tests.utils import refresh

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


def create_ship(type, owner, navigator, position, fleet=None):
    ship = Ship.objects.create(
        name='ship',
        owner=owner,
        alliance=Alliance.get_alliance(owner),
        in_space=True,
        position=position,
        type=type,
    )

    if not fleet:
        fleet = Fleet.objects.create(name='fleet', navigator=navigator, point=ship.position)
    ship.fleet = fleet
    ship.save()
    return ship, fleet


def test_move(users, roles, points, alliances):
    ship, fleet = create_ship('k', roles['frodo'], roles['legolas'], points[0])

    fleet.route = ' '.join(map(str, [points[3].id, points[4].id, points[1].id]))
    fleet.save()
    assert fleet.human_route() == 'Планета 1 (p) -> Переход 1 (t) -> Переход 2 (t) -> Планета 2 (p)'
    assert fleet.distance() == 2

    move_fleets()

    fleet = refresh(fleet)
    assert fleet.point == points[4]
    assert fleet.route == str(points[1].id)

    move_fleets()

    fleet = refresh(fleet)
    assert fleet.point == points[1]
    assert fleet.route == ''


def test_move_together(users, roles, points, alliances):
    ship, fleet = create_ship('l', roles['frodo'], roles['legolas'], points[0])
    ship, fleet = create_ship('k', roles['frodo'], roles['legolas'], points[0], fleet=fleet)

    fleet.route = ' '.join(map(str, [points[3].id, points[4].id, points[1].id]))
    fleet.save()
    assert fleet.human_route() == 'Планета 1 (p) -> Переход 1 (t) -> Переход 2 (t) -> Планета 2 (p)'
    assert fleet.distance() == 1

    move_fleets()

    fleet = refresh(fleet)
    assert fleet.point == points[3]
    assert fleet.route == ' '.join(map(str, [points[4].id, points[1].id]))

    move_fleets()

    fleet = refresh(fleet)
    assert fleet.point == points[4]
    assert fleet.route == ' '.join(map(str, [points[1].id]))

    move_fleets()

    fleet = refresh(fleet)
    assert fleet.point == points[1]
    assert fleet.route == ''
