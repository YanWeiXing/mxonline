# -*- coding: utf-8 -*-
__author__ = 'Eric'
__date__ = '2018/2/24 22:32'

from django.urls import path
from .views import (CourseListView, CourseDetailView, CourseInfoView,
                    CommentsView, AddCommentView, VideoPlayView)


urlpatterns = [
    path('list/', CourseListView.as_view(), name='list'),
    path('detail/<int:course_id>', CourseDetailView.as_view(), name='course_detail'),
    path('info/<int:course_id>', CourseInfoView.as_view(), name='course_info'),
    path('comment/<int:course_id>', CommentsView.as_view(), name='course_comment'),
    path('add_comment/', AddCommentView.as_view(), name='add_comment'),
    path('video/<int:video_id>', VideoPlayView.as_view(), name='video_play'),
]

app_name = 'courses'