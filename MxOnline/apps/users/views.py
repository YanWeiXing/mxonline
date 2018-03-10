import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.hashers import make_password
from pure_pagination import Paginator, PageNotAnInteger
from django.urls.base import reverse

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from utils.email_send import send_verify_code
from utils.mixin_utils import LoginRequiredMixin
from operations.models import UserCourse, UserFavorite, UserMessage
from organizations.models import Organization, Teacher
from courses.models import Course
from .models import Banner

# Create your views here.


class CustomBackend(ModelBackend):
    """
    后台自定义认证，兼容邮箱与用户名
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LogoutView(View):
    """
    退出重定向
    """
    def get(self, request):
        logout(request)

        return HttpResponseRedirect(reverse("index"))


class LoginView(View):
    """
    登录功能
    """

    def get(self, request):
        return render(request, 'login.html', {}) # 渲染登录页面

    def post(self, request):

        login_form = LoginForm(request.POST) # 登录表单加载
        if login_form.is_valid():

            user_name = request.POST.get("username", "") # 取出前端输入用户名
            pass_word = request.POST.get("password", "") # 取出前端输入密码
            user = authenticate(username=user_name, password=pass_word) # 用户验证
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index")) # 用户存在且已激活则进行正常登录并重定向到首页
                else:
                    return render(request, 'login.html', {"msg":"用户未激活"}) # 返回前端错误消息
            else:
                return render(request, 'login.html', {"msg": "用户名或密码错误！"}) # 返回前端错误消息
        else:
            return render(request, 'login.html', {"login_form":login_form}) # 返回表单逻辑，由表单进行再处理



class RegisterView(View):
    """
    用户注册功能
    """
    def get(self, request):

        return render(request, 'register.html', {}) # 渲染注册页面

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {"register_form":register_form, "msg": "用户已存在"})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # 用户消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册慕学在线网"
            user_message.save()

            send_verify_code(user_name, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {"register_form":register_form})


class ActiveCodeView(View):
    """
    用户激活
    """
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()

        else:
            return render(request, 'active_fail.html')

        return render(request, 'login.html')


class ForgetPWDView(View):
    def get(self, request):
        forget_pwd_form = ForgetForm
        return render(request, 'forgetpwd.html', {"forget_pwd_form":forget_pwd_form})

    def post(self, request):
        forget_pwd_form = ForgetForm(request.POST)
        if forget_pwd_form.is_valid():
            email = request.POST.get("email", "")
            send_verify_code(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {"forget_pwd_form": forget_pwd_form})


class ResetCodeView(View):
    """
    用户激活，激活链接过期未做
    """
    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {"email":email})

        else:
            return render(request, 'active_fail.html')

        return render(request, 'login.html')


class ModifyPwdView(View):
    """
    密码修改
    """

    def post(self, request):
        modify_pwd_form = ModifyPwdForm(request.POST)
        if modify_pwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {"email": email, "msg":"密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_pwd_form": modify_pwd_form})


class UserInfoView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):

    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":fail"}', content_type='application/json')


class UpdatePwdView(LoginRequiredMixin, View):
    """
    个人中心密码修改
    """

    def post(self, request):
        modify_pwd_form = ModifyPwdForm(request.POST)
        if modify_pwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse(
                    '{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_pwd_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):

    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse(
                '{"email":"邮箱已存在"}', content_type='application/json')
        send_verify_code(email, 'update_email')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):

    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_record = EmailVerifyRecord.objects.filter(
            email=email, code=code, sent_type='update_email')
        if existed_record:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(
                '{"email":"验证码出错"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):

    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses':user_courses
        })


class MyFavCourseView(LoginRequiredMixin, View):

    def get(self, request):
        course_list = []
        user_fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in user_fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'course_list':course_list
        })


class MyFavOrgView(LoginRequiredMixin, View):

    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = Organization.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'org_list':org_list
        })


class MyFavTeacherView(LoginRequiredMixin, View):

    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list':teacher_list
        })


class MyMessageView(LoginRequiredMixin, View):

    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 3, request=request)
        messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            'all_messages':messages
        })


class IndexView(View):

    def get(self, request):

        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        orgs = Organization.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners':all_banners,
            'courses':courses,
            'banner_courses':banner_courses,
            'orgs':orgs
        })


def page_not_found(request, exception):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def server_error(request):
    response = render(request,'500.html', {})
    response.status_code = 500
    return response


def permission_denied(request, exception):
    response = render(request, '403.html', {})
    response.status_code = 403
    return response