# -*- coding: utf-8 -*-
__author__ = 'Eric'
__date__ = '2018/3/4 0:52'


from django.urls import path
from .views import (UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView,
                    UpdateEmailView, MyCourseView, MyFavCourseView, MyFavOrgView,
                    MyFavTeacherView, MyMessageView)


urlpatterns = [

    path('info/', UserInfoView.as_view(), name='user_info'),
    path('image/upload/', UploadImageView.as_view(), name='image_upload'),
    path('update/pwd/', UpdatePwdView.as_view(), name='update_pwd'),
    path('sendemail_code/', SendEmailCodeView.as_view(), name='sendemail_code'),
    path('update_email/', UpdateEmailView.as_view(), name='update_email'),
    path('mycourse/', MyCourseView.as_view(), name='mycourse'),
    path('myfav/course/', MyFavCourseView.as_view(), name='myfav_course'),
    path('myfav/org/', MyFavOrgView.as_view(), name='myfav_org'),
    path('myfav/teacher/', MyFavTeacherView.as_view(), name='myfav_teacher'),
    path('mymessage/', MyMessageView.as_view(), name='mymessage')
]

app_name = 'users'
