# -*- coding: utf-8 -*-
__author__ = 'Eric'
__date__ = '2018/1/30 22:56'
from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile


class LoginForm(forms.Form):
    """
    登录表单校验
    """
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6)
    captcha = CaptchaField(error_messages={"invalid":"验证码错误"})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)


class UploadImageForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birthday', 'gender', 'mobile', 'address']