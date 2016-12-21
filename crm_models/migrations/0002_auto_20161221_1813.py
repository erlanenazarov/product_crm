# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-21 18:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crm_models', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(verbose_name='\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f')),
            ],
            options={
                'db_table': 'order_comment',
                'verbose_name': '\u041a\u043e\u043c\u043c\u0435\u043d\u0442',
                'verbose_name_plural': '\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0438',
            },
        ),
        migrations.AlterField(
            model_name='orders',
            name='done',
            field=models.BooleanField(default=False, verbose_name='\u0417\u0430\u043a\u0430\u0437 \u0437\u0430\u043a\u0440\u044b\u0442?'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='extra_field',
            field=models.TextField(blank=True, null=True, verbose_name='\u0414\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u043e'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='crm_models.Tag', verbose_name='\u0422\u0435\u0433\u0438'),
        ),
        migrations.AddField(
            model_name='ordercomment',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_models.Orders'),
        ),
        migrations.AddField(
            model_name='ordercomment',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
