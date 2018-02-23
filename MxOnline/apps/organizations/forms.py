# -*- coding: utf-8 -*-
__author__ = 'Eric'
__date__ = '2018/2/21 18:50'

import re

from django import forms

from operations.models import UserAsk


class UserAskForm(forms.ModelForm):
    """
    ModelForm用法
    """

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course']

    def clean_mobile(self):

        # 对字段进行过滤处理
        mobile = self.cleaned_data['mobile']
        REG_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REG_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("手机号码非法", code="mobile_invalid")

