# coding: utf-8
from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
import pytest

from hack.models import Float
from register.models import Record

pytestmark = pytest.mark.django_db


def test_purchase_no_money(roles, client):
    frodo_role = roles['frodo']
    frodo_role.set_field(settings.MONEY_FIELD, 0)

    client.login(username='frodo', password='frodo')
    response = client.post(reverse('market:buy'), {'product': 'float'})

    assert 'У вас недостаточно средств'.encode('utf8') in response.content


def test_purchase(roles, client):
    frodo_role = roles['frodo']
    float_cost = Float.get_infinite_goods()[0]['cost']
    frodo_role.set_field(settings.MONEY_FIELD, float_cost)

    client.login(username='frodo', password='frodo')
    response = client.post(reverse('market:buy'), {'product': 'float'})

    assert response.status_code == 302

    float = Float.objects.get()
    assert float.owner == frodo_role

    record = Record.objects.get()
    assert record.role == frodo_role
    assert record.category == 'Маркет'
    assert record.message == 'Вы приобрели Поплавок за %s' % float_cost
