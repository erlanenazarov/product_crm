# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-26 14:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_models', '0003_auto_20161226_0526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordercomment',
            name='comment',
            field=models.CharField(max_length=1000, verbose_name='\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439'),
        ),
    ]
