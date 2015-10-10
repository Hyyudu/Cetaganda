# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from yafotki.fields import YFField

from jsonfield.fields import JSONField
from market.models import Goods
from roles.models import Role, GenericManager


class Alliance(models.Model):
    name = models.CharField(verbose_name='Название', max_length=100)
    role_name = models.CharField(verbose_name='Название у роли', max_length=100)
    resources = JSONField(verbose_name='Ресурсы', default='{}')

    def __unicode__(self):
        return self.name

    @classmethod
    def get_alliance(cls, role):
        role_alliance = role.get_field(settings.ALLIANCE_FIELD)
        return cls.objects.get(role_name=role_alliance)

    class Meta:
        verbose_name = 'Альянс'
        verbose_name_plural = 'Альянсы'
        ordering = ('name',)


class Point(models.Model):
    """Планеты"""
    TYPES = (
        ('planet', 'Планета'),
        ('transit', 'PV-переход'),
    )
    type = models.CharField(verbose_name='Тип', max_length=20, choices=TYPES)
    alliance = models.ForeignKey(Alliance, verbose_name='Альянс', null=True, blank=True, default=None)
    name = models.CharField(verbose_name='Название', max_length=100)
    resources = JSONField(verbose_name='Ресурсы', default='[]')

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.type[0])

    class Meta:
        verbose_name = 'Точка'
        verbose_name_plural = 'Точки'
        ordering = ('name', 'type')


class Transit(models.Model):
    point1 = models.ForeignKey(Point, verbose_name='откуда', related_name='point_from')
    point2 = models.ForeignKey(Point, verbose_name='куда', related_name='point_to')

    class Meta:
        verbose_name = 'Переход'
        verbose_name_plural = 'Переходы'


class Fleet(models.Model):
    name = models.CharField(verbose_name='Название', max_length=100)
    point = models.ForeignKey(Point, verbose_name='Позиция')
    navigator = models.ForeignKey(Role, verbose_name='Навигатор')
    route = models.TextField(verbose_name='Заказанный маршрут', default='')

    class Meta:
        verbose_name = 'Флот'
        verbose_name_plural = 'Флота'

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.point)

    def ships_amount(self):
        return self.ship_set.count()
    ships_amount.short_description = 'Кораблей'

    def get_distance(self):
        ships = list(self.ship_set.all())
        if any(ship.type == 't' for ship in ships):
            return 1
        return min(SHIPS[ship.type]['distance'] for ship in ships)

    def route_points(self):
        if not self.route:
            return []

        points = map(int, self.route.split())
        all_points = {p.id: p for p in Point.objects.all()}
        return [all_points[point] for point in points]

    def human_route(self):
        if not self.route:
            return 'нет команд'

        points = self.route_points()
        return ' -> '.join(unicode(point) for point in [self.point] + points)

    def step(self):
        if not self.route:
            return

        points = self.route_points()
        self.point = points[0]
        self.route = ' '.join(str(p.id) for p in points[1:])
        self.save()
        self.navigator.records.create(
            category='Космос',
            message='Ваш флот "%s" перемещается в точку "%s"' % (self.name, self.point),
        )

        self.ship_set.all().update(position=self.point)
        for ship in self.ship_set.all():
            ship.owner.records.create(
                category='Космос',
                message='Ваш корабль "%s" перемещается в точку "%s"' % (ship.name, self.point),
            )


SHIPS = {
    'l': {
        'name': 'Линкор',
        'distance': 1,
        'hit': '56789',
        'cost': 1000,
        'hit_priority': 3,
    },
    'k': {
        'name': 'Крейсер',
        'distance': 2,
        'hit': '1234',
        'cost': 2000,
        'hit_priority': 1,
    },
    's': {
        'name': 'Станция',
        'distance': 0,
        'hit': '2468',
        'cost': 1500,
        'hit_priority': 5,
    },
    'r': {
        'name': 'Разведчик',
        'distance': 2,
        'hit': '150',
        'cost': 300,
        'hit_priority': 2,
    },
    't': {
        'name': 'Транспорт',
        'distance': 1,
        'hit': '37',
        'cost': 2000,
        'hit_priority': 4,
    },
}

SHIP_TYPES = ((k, v['name']) for k, v in SHIPS.items())


class Ship(models.Model):
    owner = models.ForeignKey(Role, verbose_name='Владелец', related_name='ships')
    alliance = models.ForeignKey(Alliance, verbose_name='Альянс', related_name='alliance_ships')
    in_space = models.BooleanField(verbose_name='В космосе', default=False)
    fleet = models.ForeignKey(
        Fleet, verbose_name='Флот', null=True, blank=True, default=None, on_delete=models.SET_DEFAULT
    )
    position = models.ForeignKey(
        Point, verbose_name='Положение',
        null=True, blank=True, default=None,
        related_name='position',
    )
    type = models.CharField(verbose_name='Тип', max_length=10, choices=SHIP_TYPES)
    name = models.CharField(verbose_name='Название', max_length=100)
    resources = JSONField(verbose_name='Ресурсы', default='{}')  # для транспорта
    diplomats = models.ManyToManyField(Role, verbose_name='Дипломаты', related_name='responsible_for')
    is_alive = models.BooleanField(verbose_name='Живой', default=True)
    home = models.ForeignKey(
        Point, verbose_name='Порт приписки',
        null=True, blank=True, default=None,
        related_name='home',
    )
    friends = models.ManyToManyField('self', verbose_name='Дружба')

    objects = GenericManager(is_alive=True)
    all = GenericManager()

    class Meta:
        verbose_name = 'Корабль'
        verbose_name_plural = 'Корабли'
        permissions = (
            ('can_edit_ship', 'Может редактировать корабли'),
        )

    def get_absolute_url(self):
        return reverse('space:ship', args=[self.id])

    def __unicode__(self):
        return self.name

    @property
    def state(self):
        if not self.is_alive:
            return 'dead'
        if not self.in_space:
            return 'dockyard'
        return 'space'

    @classmethod
    def create(cls, object_type, owner):
        try:
            alliance = Alliance.get_alliance(owner)
        except Alliance.DoesNotExist:
            raise ValueError('Вам необходимо вступить в альянс, чтобы покупать корабли')

        amount = cls.objects.filter(alliance=alliance).count()
        name = '%s%s%s' % (SHIPS[object_type]['name'][0], amount + 1, alliance.name[0])
        return cls.objects.create(
            owner=owner,
            alliance=alliance,
            type=object_type,
            name=name,
        )

    @classmethod
    def get_infinite_goods(cls):
        return [
            {
                'type': k,
                'name': v['name'],
                'description': '',
                'cost': v['cost'],
                'class': cls,
            }
            for k, v in SHIPS.items()
        ]

    @classmethod
    def get_available_for_market(cls, owner):
        return cls.objects.filter(owner=owner)

    def market_name(self):
        return SHIPS[self.type]['name']

    def market_description(self):
        return ''

    def change_owner(self, owner):
        alliance = Alliance.get_alliance(owner)
        self.alliance = alliance
        self.owner = owner
        self.save()

    def destroy(self):
        self.is_alive = False
        self.save()

        print "CHECK", self.fleet.ship_set.filter(is_alive=True).exists()
        if not self.fleet.ship_set.filter(is_alive=True).exists():
            self.fleet.delete()


Goods.register(Ship)


class Picture(models.Model):
    requester = models.ForeignKey(Role, verbose_name='Заказчик')
    point = models.ForeignKey(Point, verbose_name='Откуда')
    direction = models.CharField(verbose_name='Направление', max_length=255)
    photo = YFField(upload_to='cetaganda', null=True, default=None)
    dt = models.DateTimeField(verbose_name='Время', auto_now=True)

    class Meta:
        verbose_name = 'Снимок'
        verbose_name_plural = 'Снимки'


class Report(models.Model):
    content = models.TextField(verbose_name='Отчет')
    dt = models.DateTimeField(auto_now_add=True, verbose_name='Время')

    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'
        ordering = ('-dt',)
