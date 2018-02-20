from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.urls.base import reverse
from django.contrib.auth.hashers import make_password

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
from utils.email_send import send_verify_code

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
        return render(request, 'login.html', {})

    def post(self, request):

        login_form = LoginForm(request.POST)
        if login_form.is_valid():

            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {"msg":"用户未激活"})
            else:
                return render(request, 'login.html', {"msg": "用户名或密码错误！"})
        else:
            return render(request, 'login.html', {"login_form":login_form})



class RegisterView(View):
    """
    用户注册功能
    """
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form':register_form})

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










