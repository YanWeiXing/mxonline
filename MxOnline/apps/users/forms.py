# -*- coding: utf-8 -*-
__author__ = 'Eric'
__date__ = '2018/1/30 22:56'
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)
