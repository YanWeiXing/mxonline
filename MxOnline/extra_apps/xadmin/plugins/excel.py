# -*- coding: utf-8 -*-
__author__ = 'Eric'
__date__ = '2018/3/10 23:16'

import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView
from django.template import loader


class ListImportExcelPlugin(BaseAdminPlugin):
    import_excel = False

    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)

    def block_top_toolbar(self, contex, nodes):
        nodes.append(loader.render_to_string()) # 指定excel导入存放的地方，是一个html文件


xadmin.site.register_plugin(ListImportExcelPlugin, ListAdminView)