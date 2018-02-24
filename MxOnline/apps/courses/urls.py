# -*- coding: utf-8 -*-
__author__ = 'Eric'
__date__ = '2018/2/24 22:32'

from django.urls import path
from .views import CourseListView, CourseDetailView


urlpatterns = [
    path('list/', CourseListView.as_view(), name='list'),
    path('detail/<int:course_id>', CourseDetailView.as_view(), name='course_detail'),

]

app_name = 'courses'