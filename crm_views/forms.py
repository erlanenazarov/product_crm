# coding=utf-8
from django import forms
from crm_models.models import *
from django.contrib.auth.models import User as BaseUser


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        exclude = ()


class CommentForm(forms.ModelForm):
    class Meta:
        model = OrderComment
        exclude = ()


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ()


class UserForm(forms.ModelForm):
    class Meta:
        model = BaseUser
        exclude = ()
