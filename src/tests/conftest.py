# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
import pytest

from roles.models import Role, GameField


def create_user(username, **kwargs):
    """Создает пользователя с заданным username и таким же паролем."""
    try:
        user = get_user_model().objects.get(username=username)
        user.__dict__.update(kwargs)
        user.save()
    except get_user_model().DoesNotExist:
        user = get_user_model().objects.create_user(username, username + '@example.ru', username, **kwargs)
    return user


def create_superuser(username):
    """Создает super-пользователя с заданным username и таким же паролем."""
    user_model = get_user_model()

    user = user_model.objects.create_superuser(
        username, username + '@example.yandex.ru', username
    )
    return user


@pytest.fixture()
def users():
    return {
        'admin': create_superuser('admin'),
        'frodo': create_user('frodo'),
        'legolas': create_user('legolas'),
        'aragorn': create_user('aragorn'),
        'gendalf': create_user('gendalf'),
    }


@pytest.fixture()
def role_fields():
    GameField.objects.create(
        name='Подданство',
        type=4,
        additional='Барраяр, Цетаганда'
    )
    GameField.objects.create(
        name='Профессия',
        type=4,
        additional='космотактик, дипломат, ученый, хакер, экономист'
    )
    GameField.objects.create(
        name='Ранг',
        type=3,
    )
    GameField.objects.create(
        name='Деньги',
        type=3,
    )


@pytest.fixture()
def roles(users, role_fields):
    frodo_role = Role.objects.create(
        user=users['frodo'],
        name='Frodo',
    )
    frodo_role.set_field('Профессия', 'экономист')
    frodo_role.set_field('Подданство', 'Барраяр')

    legolas_role = Role.objects.create(
        user=users['legolas'],
        name='Legolas',
    )
    legolas_role.set_field('Профессия', 'космотактик')
    legolas_role.set_field('Ранг', 1)

    aragorn_role = Role.objects.create(
        user=users['aragorn'],
        name='Aragorn',
    )
    aragorn_role.set_field('Профессия', 'дипломат')

    return {
        'frodo': frodo_role,
        'legolas': legolas_role,
        'aragorn': aragorn_role,
    }
