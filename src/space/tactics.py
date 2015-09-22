# coding: utf-8
from __future__ import unicode_literals

from space import models


def move_fleets():
    for fleet in models.Fleet.objects.all():
        if not fleet.route:
            continue

        distance = fleet.distance()
        if distance:
            for i in xrange(distance):
                if fleet.route:
                    fleet.step()
