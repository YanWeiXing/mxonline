# -*- coding: utf-8 -*-
__author__ = 'Eric'
__date__ = '2018/1/29 20:28'

import xadmin
from .models import Course, Chapter, Video, CourseResource


class CourseAdmin(object):
    pass


class ChapterAdmin(object):
    pass


class VideoAdmin(object):
    pass


class CourseResourceAdmin(object):
    pass


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Chapter, ChapterAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
