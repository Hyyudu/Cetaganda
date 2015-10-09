# coding: utf-8
from __future__ import unicode_literals
import random

from space import models


def move_fleets():
    for fleet in models.Fleet.objects.all():
        if not fleet.route:
            continue

        distance = min(len(fleet.route_points()), fleet.get_distance())

        if distance:
            for i in xrange(distance):
                if fleet.route:
                    fleet.step()

                    alive = fight(fleet)
                    if not alive:
                        break

                    harvest(fleet)

                    unloading(fleet)


def fight(fleet):
    def _try_shoot(ship, target):
        if target.is_alive and not ship.friends.filter(id=target.id).exists():
            print "HIT from ", ship, " TO", target
            target.destroy()

            ship.owner.records.create(
                category='Космос',
                message='Ваш корабль "%s" попадает по кораблю "%s"' % (ship, target),
            )
            target.owner.records.create(
                category='Космос',
                message='Ваш корабль "%s" уничтожен залпом "%s"' % (target, ship),
            )
            return True

    while True:
        print "Turn"

        targets = False

        our_shots = []
        our_side = fleet.ship_set.all()
        our_side = sorted(our_side, key=lambda ship: models.SHIPS[ship.type]['hit_priority'])
        if not our_side:
            return False

        their_shots = []
        their_side = models.Ship.objects.exclude(fleet=fleet)
        their_side = sorted(their_side, key=lambda ship: models.SHIPS[ship.type]['hit_priority'])
        if not their_side:
            return True

        for ship in our_side:
            dice = str(random.randint(0, 9))
            print "DICE", dice
            if dice in models.SHIPS[ship.type]['hit']:
                print "SHOT", ship
                our_shots.append(ship)
            else:
                ship.owner.records.create(
                    category='Космос',
                    message='Ваш корабль "%s" промахивается' % ship
                )

        print "OUR", our_shots

        for ship in their_side:
            dice = str(random.randint(0, 9))
            print "DICE", dice
            if dice in models.SHIPS[ship.type]['hit']:
                print "SHOT", ship
                their_shots.append(ship)
            else:
                ship.owner.records.create(
                    category='Космос',
                    message='Ваш корабль "%s" промахивается' % ship
                )

        print "THEIR", their_shots

        for shooting_ship in our_shots:
            for target in their_side:
                hit = _try_shoot(shooting_ship, target)

                if hit:
                    targets = True
                    break

        for shooting_ship in their_shots:
            for target in our_side:
                hit = _try_shoot(shooting_ship, target)

                if hit:
                    targets = True
                    break

        if not targets:
            break

    return fleet.ship_set.all().exists()


def harvest(fleet):
    """Сбор ресурсов с планеты"""
    if not fleet.point.resources:
        return

    for transport in fleet.ship_set.filter(type='t').all():
        for resource in fleet.point.resources:
            transport.resources[resource] = transport.resources.get(resource, 0) + 1

        transport.save()


def unloading(fleet):
    """Выгрузка ресурсов в порту приписки"""
    for transport in fleet.ship_set.filter(type='t').all():
        if transport.home == transport.position:
            for res, amount in transport.resources.items():
                transport.alliance.resources[res] = transport.alliance.resources.get(res, 0) + amount
            transport.alliance.save()
            transport.resources = {}
            transport.save()
