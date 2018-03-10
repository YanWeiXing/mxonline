# -*- coding: utf-8 -*-
__author__ = 'Eric'
__date__ = '2018/1/29 20:37'

import xadmin
from .models import Organization, Teacher, CityDict

# 注册app到xadmin
class OrganizationAdmin(object):
    pass


class CityDictAdmin(object):
    pass


class TeacherAdmin(object):
    pass


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(Organization, OrganizationAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
