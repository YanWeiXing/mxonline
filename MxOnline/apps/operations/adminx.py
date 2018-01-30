# -*- coding: utf-8 -*-
__author__ = 'Eric'
__date__ = '2018/1/29 20:41'

import xadmin
from .models import UserAsk, UserComments, UserFavorite, UserMessage, UserCourse


class UserAskAdmin:
    pass


class UserCommentsAdmin:
    pass


class UserFavoriteAdmin:
    pass


class UserMessageAdmin:
    pass


class UserCourseAdmin:
    pass


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserComments, UserCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
