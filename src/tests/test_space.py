# coding: utf-8
from __future__ import unicode_literals

import pytest

from space.models import Ship, Alliance, Fleet
from space.tactics import move_fleets
from tests.utils import refresh

pytestmark = pytest.mark.django_db


def create_ship(type, owner, navigator, position, fleet=None, name='ship'):
    ship = Ship.objects.create(
        name=name,
        owner=owner,
        alliance=Alliance.get_alliance(owner),
        in_space=True,
        position=position,
        type=type,
        home=position,
    )

    if not fleet:
        fleet = Fleet.objects.create(name=name + '_fleet', navigator=navigator, point=ship.position)
    ship.fleet = fleet
    ship.save()
    return ship, fleet


def test_move(roles, points, alliances):
    ship, fleet = create_ship('k', roles['frodo'], roles['legolas'], points[0])

    fleet.route = ' '.join(map(str, [points[3].id, points[4].id, points[1].id]))
    fleet.save()
    assert fleet.human_route() == 'Планета 1 (p) -> Переход 1 (t) -> Переход 2 (t) -> Планета 2 (p)'
    assert fleet.get_distance() == 2

    move_fleets()

    fleet = refresh(fleet)
    assert fleet.point == points[4]
    assert fleet.route == str(points[1].id)

    move_fleets()

    fleet = refresh(fleet)
    assert fleet.point == points[1]
    assert fleet.route == ''
    assert fleet.ship_set.get().position == points[1]


def test_move_together(roles, points, alliances):
    """ Два корабля движутся со скоростью самого медленного """
    ship, fleet = create_ship('l', roles['frodo'], roles['legolas'], points[0])
    ship, fleet = create_ship('k', roles['frodo'], roles['legolas'], points[0], fleet=fleet)

    fleet.route = ' '.join(map(str, [points[3].id, points[4].id, points[1].id]))
    fleet.save()
    assert fleet.human_route() == 'Планета 1 (p) -> Переход 1 (t) -> Переход 2 (t) -> Планета 2 (p)'
    assert fleet.get_distance() == 1

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


def test_transport(roles, points, alliances):
    """ Транспорт может забирать ресурсы с планеты и выгружать в родном порту """
    ship, fleet = create_ship('t', roles['frodo'], roles['legolas'], points[0])
    alliance = refresh(alliances[0])
    assert alliance.resources == {}

    points[1].resources = ['sheep1']
    points[1].save()

    fleet.route = ' '.join(map(str, [points[3].id, points[4].id, points[1].id]))
    fleet.save()

    for i in xrange(4):
        move_fleets()

    ship = refresh(ship)
    assert ship.resources == {'sheep1': 1}

    fleet.route = ' '.join(map(str, [points[4].id, points[3].id, points[0].id]))
    fleet.save()

    for i in xrange(4):
        move_fleets()

    ship = refresh(ship)
    assert ship.resources == {}

    alliance = refresh(alliance)
    assert alliance.resources == {'sheep1': 1}


def test_transport_many_resources(roles, points, alliances):
    ship, fleet = create_ship('t', roles['frodo'], roles['legolas'], points[0])
    alliance = refresh(alliances[0])
    assert alliance.resources == {}

    points[1].resources = ['sheep1']
    points[1].save()
    points[2].resources = ['sheep2']
    points[2].save()

    fleet.route = ' '.join(map(str, [points[3].id, points[4].id, points[1].id, points[4].id, points[5].id,
                               points[2].id, points[5].id, points[3].id, points[0].id]))
    fleet.save()

    for i in xrange(9):
        move_fleets()

    alliance = refresh(alliance)
    assert alliance.resources == {'sheep1': 1, 'sheep2': 1}


def test_station_move(roles, points, alliances):
    """ Станция перемещается только с транспортом """
    ship, fleet = create_ship('s', roles['frodo'], roles['legolas'], points[0])
    assert fleet.get_distance() == 0

    ship, fleet = create_ship('l', roles['frodo'], roles['legolas'], points[0], fleet=fleet)
    assert fleet.get_distance() == 0

    ship, fleet = create_ship('t', roles['frodo'], roles['legolas'], points[0], fleet=fleet)
    assert fleet.get_distance() == 1
