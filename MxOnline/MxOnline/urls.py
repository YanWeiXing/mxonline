"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
import xadmin
from django.views.generic import TemplateView
from django.views.static import serve

from users.views import (LoginView, LogoutView, RegisterView, ActiveCodeView,
                         ForgetPWDView, ResetCodeView, ModifyPwdView)
from MxOnline.settings import MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    # 验证码路由
    path('captcha/', include('captcha.urls')),
    path('active/<active_code>', ActiveCodeView.as_view(), name='user_active'),
    path('forget/', ForgetPWDView.as_view(), name='forget_pwd'),
    path('reset/<reset_code>', ResetCodeView.as_view(), name='reset_pwd'),
    path('modify_pwd/', ModifyPwdView.as_view(), name='modify_pwd'),

    # 配置上传文件的处理
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root":MEDIA_ROOT}),

    # 课程机构URL路由集合
    path('orgs/', include('organizations.urls', namespace='orgs')),
    path('courses/', include('courses.urls', namespace='courses')),

]
