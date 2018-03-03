# -*- coding: utf-8 -*-
__author__ = 'Eric'
__date__ = '2018/2/20 23:38'

from django.urls import path
from .views import (OrgListView, UserAskView, OrgHomeView, OrgCourseView,
                    OrgDescView, OrgTeacherView, UserFavorateView, TeacherListView,
                    TeacherDetailView)


urlpatterns = [


    path('list/', OrgListView.as_view(), name='list'),
    path('user_ask/', UserAskView.as_view(), name='user_ask'),
    path('home/<int:org_id>', OrgHomeView.as_view(), name='org_home'),
    path('course/<int:org_id>', OrgCourseView.as_view(), name='org_course'),
    path('desc/<int:org_id>', OrgDescView.as_view(), name='org_desc'),
    path('teacher/<int:org_id>', OrgTeacherView.as_view(), name='org_teacher'),
    path('user_fav/', UserFavorateView.as_view(), name='user_fav'),
    path('teacher/list/', TeacherListView.as_view(), name='teacher_list'),
    path('teacher/detail/<int:teacher_id>', TeacherDetailView.as_view(), name='teacher_detail'),
]

app_name = 'organizations'
