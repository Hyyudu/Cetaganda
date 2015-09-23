# coding: utf-8
from __future__ import unicode_literals

from space import models


def move_fleets():
    for fleet in models.Fleet.objects.all():
        if not fleet.route:
            continue

        distance = fleet.get_distance()
        if distance:
            for i in xrange(distance):
                if fleet.route:
                    fleet.step()

                    fight(fleet)

                    harvest(fleet)

                    unloading(fleet)


def fight(fleet):
    pass


def harvest(fleet):
    if not fleet.point.resources:
        return

    for transport in fleet.ship_set.filter(type='t').all():
        for resource in fleet.point.resources:
            transport.resources[resource] = transport.resources.get(resource, 0) + 1

        transport.save()


def unloading(fleet):
    for transport in fleet.ship_set.filter(type='t').all():
        if transport.home == transport.position:
            for res, amount in transport.resources.items():
                transport.alliance.resources[res] = transport.alliance.resources.get(res, 0) + amount

            transport.alliance.save()
            transport.resources = {}
            transport.save()
