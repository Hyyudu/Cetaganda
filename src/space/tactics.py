# coding: utf-8
from __future__ import unicode_literals
import random
import logging

from space import models

log = logging.getLogger('space')


def move_fleets():
    log.info('')
    log.info('START TACTICS PHASE')
    ships = list(models.Ship.objects.all().order_by('position', 'name'))

    for fleet in models.Fleet.objects.all():
        if not fleet.route:
            continue

        distance = min(len(fleet.route_points()), fleet.get_distance())
        log.info('Fleet "%s", route "%s", distance "%s"', fleet.name, fleet.human_route(), distance)

        if distance:
            for i in xrange(distance):
                if fleet.route:
                    fleet.step()
                    log.info('Fleet "%s" now at "%s"', fleet.name, fleet.point)

                    alive = fight(fleet)
                    if not alive:
                        break

                    harvest(fleet)

                    unloading(fleet)

    new_ships = {ship.id: ship for ship in models.Ship.objects.all()}
    report = ''
    for ship in ships:
        new_ship = new_ships.get(ship.id)
        if not new_ship:
            report += 'Корабль "%s" (%s) уничтожен\n' % (ship.name, ship.position)
            continue

        if ship.owner != new_ship.owner:
            report += 'Корабль "%s" (%s) сменил владельца на "%s"\n' % (ship.name, ship.position, new_ship.owner)

        if ship.position != new_ship.position:
            report += 'Корабль "%s" (%s) переместился в "%s"\n' % (ship.name, ship.position, new_ship.position)

    models.Report.objects.create(content=report)
    log.info('FINISH TACTICS PHASE')


def fight(fleet):
    if fleet.is_silent():
        log.info('Fleet "%s" is silent' % fleet.name)
        return True

    for enemy_fleet in models.Fleet.objects.filter(point=fleet.point).exclude(navigator=fleet.navigator):
        if enemy_fleet.is_silent():
            log.info('Enemy fleet "%s" is silent' % fleet.name)
            continue

        alive = fight_with_enemy(fleet, enemy_fleet)
        if not alive:
            return False

    return True


def fight_with_enemy(fleet, enemy_fleet):
    log.info('Fight "%s" with "%s"' % (fleet.name, enemy_fleet.name))

    def _try_shoot(ship, target):
        if not target.is_alive:
            return

        if ship.friends.filter(id=target.id).exists() and target.friends.filter(id=ship.id).exists():
            return

        log.info("HIT from %s TO %s", ship, target)
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
        log.info('Turn')

        targets = False

        our_shots = []
        our_side = fleet.ship_set.all()
        our_side = sorted(our_side, key=lambda ship: models.SHIPS[ship.type]['hit_priority'])
        if not our_side:
            return False

        their_shots = []
        their_side = enemy_fleet.ship_set.all()
        their_side = sorted(their_side, key=lambda ship: models.SHIPS[ship.type]['hit_priority'])
        if not their_side:
            return True

        for ship in our_side:
            dice = str(random.randint(0, 9))
            log.info('DICE %s', dice)
            if dice in models.SHIPS[ship.type]['hit']:
                log.info('SHOT %s', ship)
                our_shots.append(ship)
            else:
                ship.owner.records.create(
                    category='Космос',
                    message='Ваш корабль "%s" промахивается' % ship
                )

        log.info('OUR_SHOTS %s', our_shots)

        for ship in their_side:
            dice = str(random.randint(0, 9))
            log.info('DICE %s', dice)
            if dice in models.SHIPS[ship.type]['hit']:
                log.info('ENEMY SHOT %s', ship)
                their_shots.append(ship)
            else:
                ship.owner.records.create(
                    category='Космос',
                    message='Ваш корабль "%s" промахивается' % ship
                )

        log.info('THEIR_SHOTS %s', their_shots)

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
