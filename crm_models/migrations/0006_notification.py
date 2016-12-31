# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-31 08:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crm_models', '0005_auto_20161227_1248'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255, verbose_name='\u0421\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435')),
                ('url', models.CharField(default='/', max_length=255, verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430')),
                ('is_read', models.BooleanField(default=False, verbose_name='\u041f\u0440\u043e\u0447\u0438\u0442\u0430\u043d\u043e?')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_models.Orders', verbose_name='\u041f\u0440\u0438\u0432\u044f\u0437\u043a\u0430 \u043a \u0437\u0430\u043a\u0430\u0437\u0443')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='\u0421\u0432\u044f\u0437\u0430\u043d\u043d\u044b\u0435 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0438')),
            ],
            options={
                'db_table': 'notifications',
                'verbose_name': '\u0423\u0432\u0435\u0434\u043e\u043c\u043b\u0435\u043d\u0438\u0435',
                'verbose_name_plural': '\u0423\u0432\u0435\u0434\u043e\u043c\u043b\u0435\u043d\u0438\u044f',
            },
        ),
    ]
