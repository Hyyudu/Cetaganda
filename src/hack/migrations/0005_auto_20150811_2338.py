# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack', '0004_auto_20150809_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='hack',
            name='hash',
            field=models.CharField(default=None, max_length=32, verbose_name='\u0425\u044d\u0448'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hack',
            name='target',
            field=models.ForeignKey(default=None, verbose_name='\u0426\u0435\u043b\u044c', to='hack.Target'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='hack',
            name='hacker',
            field=models.ForeignKey(verbose_name='\u0425\u0430\u043a\u0435\u0440', to='roles.Role'),
        ),
        migrations.AlterField(
            model_name='hack',
            name='result',
            field=models.CharField(default=None, choices=[(None, '\u0421\u043e\u0437\u0434\u0430\u043d\u043e'), ('inprocess', '\u0418\u0434\u0435\u0442'), ('win', '\u0412\u0437\u043b\u043e\u043c\u0430\u043d\u043e'), ('run', '\u0421\u0431\u0435\u0436\u0430\u043b'), ('failstatic', '\u041d\u0435 \u0445\u0432\u0430\u0442\u0438\u043b\u043e \u043f\u043e\u043f\u043b\u0430\u0432\u043a\u043e\u0432'), ('fail', '\u041d\u0435 \u043e\u0441\u0438\u043b\u0438\u043b'), ('late', '\u041e\u043f\u043e\u0437\u0434\u0430\u043b')], max_length=20, blank=True, null=True, verbose_name='\u0418\u0442\u043e\u0433'),
        ),
        migrations.AlterField(
            model_name='target',
            name='target',
            field=models.CharField(max_length=50, verbose_name='\u0426\u0435\u043b\u044c', choices=[('role.credits', '\u041f\u0435\u0440\u0441\u043e\u043d\u0430\u0436: \u043a\u0440\u0430\u0436\u0430 10 \u043a\u0440\u0435\u0434\u0438\u0442\u043e\u0432'), ('role.official', '\u041f\u0435\u0440\u0441\u043e\u043d\u0430\u0436: \u043e\u0444\u0438\u0446\u0438\u0430\u043b\u044c\u043d\u043e\u0435 \u0434\u043e\u0441\u044c\u0435'), ('role.personal', '\u041f\u0435\u0440\u0441\u043e\u043d\u0430\u0436: \u043f\u0440\u043e\u0444\u0435\u0441\u0441\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0435 \u043e\u0441\u043e\u0431\u0435\u043d\u043d\u043e\u0441\u0442\u0438'), ('role.messages', '\u041f\u0435\u0440\u0441\u043e\u043d\u0430\u0436: \u043f\u0435\u0440\u0435\u043f\u0438\u0441\u043a\u0430'), ('role.info', '\u041f\u0435\u0440\u0441\u043e\u043d\u0430\u0436: \u041b\u0438\u0447\u043d\u043e\u0435 \u0434\u0435\u043b\u043e'), ('role.defence', '\u041f\u0435\u0440\u0441\u043e\u043d\u0430\u0436: \u0421\u043f\u0438\u0441\u043e\u043a \u0437\u0430\u0449\u0438\u0442')]),
        ),
    ]
