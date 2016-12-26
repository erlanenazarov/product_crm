# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User as BaseUser


# Create your models here.


class Orders(models.Model):
    class Meta:
        db_table = 'orders'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    title = models.CharField(max_length=255, verbose_name='Наименование')
    price = models.FloatField(verbose_name='Цена товара $')
    final_price = models.FloatField(verbose_name='Конечная цена $', null=True, blank=True)
    status = models.CharField(max_length=255, verbose_name='Статус')
    order_number = models.CharField(max_length=255, verbose_name='Номер заказа')
    link_to_product = models.CharField(max_length=255, verbose_name='Ссылка на продукт')
    site_which_from = models.CharField(max_length=255, verbose_name='Сайт с которого взят', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Созданно')
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Обновлено')
    extra_field = models.TextField(verbose_name='Дополнительно', null=True, blank=True)
    tags = models.ManyToManyField('Tag', verbose_name='Теги', null=True, blank=True)
    client = models.ForeignKey('Client', verbose_name='Клиент')
    manager = models.ManyToManyField(BaseUser, verbose_name='Менеджер')
    done = models.BooleanField(default=False, verbose_name='Заказ закрыт?')

    def __unicode__(self):
        return self.title


class Client(models.Model):
    class Meta:
        db_table = 'client'
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    name = models.CharField(max_length=255, verbose_name='Имя', null=True, blank=True)
    email = models.EmailField(max_length=255, verbose_name='Эл. почта', null=True, blank=True)
    phone_number = models.CharField(max_length=255, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    class Meta:
        db_table = 'tag'
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    name = models.CharField(max_length=255, verbose_name='Наименование')
    color = models.CharField(max_length=100, verbose_name='Цвет тега')

    def __unicode__(self):
        return self.name


class OrderComment(models.Model):
    class Meta:
        db_table = 'order_comment'
        verbose_name = 'Коммент'
        verbose_name_plural = 'Комментарии'

    order_id = models.ForeignKey('Orders')
    user_id = models.ForeignKey(BaseUser)
    comment = models.CharField(max_length=1000, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Дата обновления')

    def __unicode__(self):
        return self.comment[0:20]
