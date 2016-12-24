# coding=utf-8
from django import forms
from crm_models.models import *


class CreateOrderForm(forms.Form):
    class Meta:
        model = Orders

