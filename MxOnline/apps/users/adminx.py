# -*- coding: utf-8 -*-
__author__ = 'Eric'
__date__ = '2018/1/28 23:08'

import xadmin
from xadmin import views

from .models import EmailVerifyRecord, Banner


class BaseSetting:
    """
    xadmin的主题功能调用
    """
    enable_themes = True
    use_bootswatch = True


class GlobalSettings:
    """
    xadmin的全局设置
    """
    site_title = '慕学在线后台管理系统' # 设置网站名
    site_footer = '恒星租赁集团有限公司' # 设置页脚信息
    menu_style = 'accordion' # 设置菜单样式


class EmailVerifyRecordAdmin(object):
    """
    设置app的显示方式，在搜索中的字段，过滤中的字段
    """

    list_display = ['code', 'email', 'sent_type', 'sent_time']
    search_fields = ['code', 'email', 'sent_type', 'sent_time']
    list_filter = ['code', 'email', 'sent_type', 'sent_time']


class BannerAdmin(object):
    pass


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin) # 注册app到xadmin
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting) # 修改xadmin的基本设置
xadmin.site.register(views.CommAdminView, GlobalSettings) # 重加载全局自定义设置到xadmin
