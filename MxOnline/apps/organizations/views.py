from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger
from django.http import HttpResponse

from .models import Organization, CityDict
from .forms import UserAskForm
from operations.models import UserFavorite

# Create your views here.


class OrgListView(View):
    def get(self, request):
        all_orgs = Organization.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        all_cities = CityDict.objects.all()

        # 城市筛选
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))


        # 类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 排序功能
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')

        org_nums = all_orgs.count()

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 3, request=request)

        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'all_orgs':orgs,
            'all_cities':all_cities,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            'sort': sort
        })


class UserAskView(View):
    """
    用户咨询功能
    """
    def post(self, request):
        user_ask_form = UserAskForm(request.POST)
        if user_ask_form.is_valid():
            user_ask = user_ask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg":"添加出错"}', content_type='application/json')


class OrgHomeView(View):
    def get(self, request, org_id):
        current_page = 'home'
        org = Organization.objects.get(id=int(org_id))
        all_courses = org.course_set.all()[:3]
        all_teachers = org.teacher_set.all()[:1]

        # 收藏状态判断
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(
                    user=request.user, fav_id=org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-homepage.html', {
            'org':org,
            'all_courses':all_courses,
            'all_teachers':all_teachers,
            'current_page':current_page,
            'has_fav':has_fav

        })


class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = 'course'
        org = Organization.objects.get(id=int(org_id))
        all_courses = org.course_set.all()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(
                    user=request.user, fav_id=org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-course.html', {
            'all_courses':all_courses,
            'org': org,
            'current_page': current_page,
            'has_fav':has_fav

        })


class OrgDescView(View):
    def get(self, request, org_id):
        current_page = 'desc'
        org = Organization.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(
                    user=request.user, fav_id=org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-desc.html', {

            'org': org,
            'current_page': current_page,
            'has_fav':has_fav

        })


class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = 'teacher'
        org = Organization.objects.get(id=int(org_id))

        all_teachers = org.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(
                    user=request.user, fav_id=org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-teachers.html', {
            'org':org,
            'all_teachers':all_teachers,
            'current_page': current_page,
            'has_fav':has_fav

        })


class UserFavorateView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        # 判断用户是否登录，否则通过ajax返回登录页面
        if not request.user.is_authenticated:
            return HttpResponse(
                '{"status": "fail", "msg":"用户未登录"}', content_type='application/json')


        exist_record = UserFavorite.objects.filter(
            user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))

        # 记录存在则删除
        if exist_record:
            exist_record.delete()
            return HttpResponse(
                '{"status": "success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse(
                    '{"status": "success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse(
                    '{"status": "fail", "msg":"收藏出错"}', content_type='application/json')


