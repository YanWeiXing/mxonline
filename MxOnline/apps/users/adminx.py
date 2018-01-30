# -*- coding: utf-8 -*-
__author__ = 'Eric'
__date__ = '2018/1/28 23:08'

import xadmin
from xadmin import views

from .models import EmailVerifyRecord, Banner


class BaseSetting:
    enable_themes = True
    use_bootswatch = True


class GlobalSettings:
    site_title = '慕学在线后台管理系统'
    site_footer = '恒星租赁集团有限公司'
    menu_style = 'accordion'


class EmailVerifyRecordAdmin(object):

    list_display = ['code', 'email', 'sent_type', 'sent_time']
    search_fields = ['code', 'email', 'sent_type', 'sent_time']
    list_filter = ['code', 'email', 'sent_type', 'sent_time']


class BannerAdmin(object):
    pass


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
