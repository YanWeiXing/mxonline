# -*- coding: utf-8 -*-
__author__ = 'Eric'
__date__ = '2018/1/29 20:28'

import xadmin
from .models import Course, Chapter, Video, CourseResource, BannerCourse
from organizations.models import Organization


class ChapterInline(object):
    model = Chapter
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class VideoInline(object):
    model = Video
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times']
    ordering = ['-click_nums']
    exclude = ['click_nums', 'fav_nums', 'students']
    inlines = [ChapterInline, CourseResourceInline]
    style_fields = {"detail":"ueditor"}
    # import_excel = True 在某个模块中显示excel导入

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()

    # def post(self, request, *args, **kwargs):
    #     """
    #     重载post方法，增加自己的逻辑
    #     :param request:
    #     :param args:
    #     :param kwargs:
    #     :return:
    #     """
    #     if 'excel' in request.FILES:
    #         pass
    #     return super(CourseAdmin, self).post(request, args, kwargs)


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times']
    ordering = ['-click_nums']
    exclude = ['click_nums', 'fav_nums', 'students']
    inlines = [ChapterInline, CourseResourceInline]

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class ChapterAdmin(object):
    inlines = [VideoInline]


class VideoAdmin(object):
    pass


class CourseResourceAdmin(object):
    pass


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Chapter, ChapterAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
