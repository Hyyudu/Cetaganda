# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0006_auto_20150809_1522'),
        ('hack', '0003_float_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='duel',
            name='owner',
            field=models.ForeignKey(default=None, verbose_name='\u0417\u0430\u043f\u0443\u0441\u0442\u0438\u0432\u0448\u0438\u0439', to='roles.Role'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='target',
            name='target',
            field=models.CharField(max_length=50, verbose_name='\u0426\u0435\u043b\u044c', choices=[('role.credits', '\u041f\u0435\u0440\u0441\u043e\u043d\u0430\u0436: \u043a\u0440\u0430\u0436\u0430 10 \u043a\u0440\u0435\u0434\u0438\u0442\u043e\u0432'), ('role.official', '\u041f\u0435\u0440\u0441\u043e\u043d\u0430\u0436: \u043e\u0444\u0438\u0446\u0438\u0430\u043b\u044c\u043d\u043e\u0435 \u0434\u043e\u0441\u044c\u0435'), ('role.personal', '\u041f\u0435\u0440\u0441\u043e\u043d\u0430\u0436: \u043f\u0440\u043e\u0444\u0435\u0441\u0441\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0435 \u043e\u0441\u043e\u0431\u0435\u043d\u043d\u043e\u0441\u0442\u0438'), ('role.messages', '\u041f\u0435\u0440\u0441\u043e\u043d\u0430\u0436: \u043f\u0435\u0440\u0435\u043f\u0438\u0441\u043a\u0430'), ('role.info', '\u041f\u0435\u0440\u0441\u043e\u043d\u0430\u0436: \u041b\u0438\u0447\u043d\u043e\u0435 \u0434\u0435\u043b\u043e'), ('role.defence', '\u041f\u0435\u0440\u0441\u043e\u043d\u0430\u0436: \u0421\u043f\u0438\u0441\u043e\u043a \u0437\u0430\u0449\u0438\u0442'), ('corporation.book', '\u041a\u043e\u0440\u043f\u043e\u0440\u0430\u0446\u0438\u044f: \u0433\u043e\u0441\u0442\u0435\u0432\u0430\u044f \u043a\u043d\u0438\u0433\u0430'), ('corporation.money', '\u041a\u043e\u0440\u043f\u043e\u0440\u0430\u0446\u0438\u044f: \u0441\u0443\u043c\u043c\u0430 \u043d\u0430 \u0441\u0447\u0435\u0442\u0443'), ('corporation.docslist', '\u041a\u043e\u0440\u043f\u043e\u0440\u0430\u0446\u0438\u044f: \u0441\u043f\u0438\u0441\u043e\u043a \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u043e\u0432'), ('corporation.doc', '\u041a\u043e\u0440\u043f\u043e\u0440\u0430\u0446\u0438\u044f: \u043a\u0440\u0430\u0436\u0430/\u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0435 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430')]),
        ),
    ]
