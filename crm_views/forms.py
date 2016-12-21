# coding=utf-8
from django import forms


class CreateOrderForm(forms.Form):
    title = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'required': True,
        'class': 'form-control',
        'placeholder': 'Наименование'
    }))
    price = forms.FloatField(widget=forms.NumberInput(attrs={
        'required': True,
        'class': 'form-control',
        'placeholder': '250$'
    }))
    final_price = forms.FloatField(widget=forms.NumberInput(attrs={
        'required': False,
        'class': 'form-control',
        'placeholder': '250$'
    }))
    status = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'required': True,
        'class': 'form-control',
        'placeholder': 'Опишите статус закза'
    }))
    order_number = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'required': True,
        'class': 'form-control',
        'placeholder': '123456789'
    }))
    link_to_product = forms.URLField(widget=forms.URLInput(attrs={
        'required': True,
        'class': 'form-control',
        'placeholder': 'http://koko.kg/'
    }))
    site_which_from = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'required': False,
        'class': 'form-control',
        'placeholder': 'С какого сайта взят товар?'
    }))
    extra = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={
        'required': False,
        'class': 'form-control',

    }))
