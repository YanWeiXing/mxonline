from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger
from django.http import HttpResponse

from .models import Course, CourseResource, Video
from operations.models import UserFavorite, UserComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin

# Create your views here.


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = all_courses.order_by('-click_nums')[:3]

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)
        courses = p.page(page)
        return render(request, 'course-list.html', {
            'all_courses':courses,
            'hot_courses':hot_courses,
            'sort':sort
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(
                    user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
            if UserFavorite.objects.filter(
                    user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
        tag = course.tag
        if tag:
            related_courses = Course.objects.filter(tag=tag)
        else:
            related_courses = []
        return render(request, 'course-detail.html', {
            'course':course,
            'related_courses':related_courses,
            'has_fav_course':has_fav_course,
            'has_fav_org':has_fav_org

        })


class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()

        # 查询用户与课程是否关联
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()

        # 查找学习当前课程的所有用户
        user_courses_table = UserCourse.objects.filter(course=course)

        # 取出所有用户的ID
        user_ids = [user_course.user.id for user_course in user_courses_table]

        # 取出当前课程所用用户的相关学习课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_courses.course.id for user_courses in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course':course,
            'resources':resources,
            'relate_courses':relate_courses
        })


class CommentsView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()
        # 查找学习当前课程的所有用户
        user_courses_table = UserCourse.objects.filter(course=course)

        # 取出所有用户的ID
        user_ids = [user_course.user.id for user_course in user_courses_table]

        # 取出当前课程所用用户的相关学习课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_courses.course.id for user_courses in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        resources = CourseResource.objects.filter(course=course)
        comments = UserComments.objects.all()
        return render(request, 'course-comment.html', {
            'course':course,
            'resources':resources,
            'comments':comments,
            'relate_courses': relate_courses
        })


class VideoPlayView(View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.chapter.course
        course.students += 1
        course.save()

        # 查询用户与课程是否关联
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()

        # 查找学习当前课程的所有用户
        user_courses_table = UserCourse.objects.filter(course=course)

        # 取出所有用户的ID
        user_ids = [user_course.user.id for user_course in user_courses_table]

        # 取出当前课程所用用户的相关学习课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_courses.course.id for user_courses in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-play.html', {
            'course': course,
            'resources': resources,
            'relate_courses': relate_courses,
            'video':video
        })


class AddCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse(
                '{"status": "fail", "msg":"用户未登录"}', content_type='application/json')

        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", '')
        if int(course_id) > 0 and comments:
            course_comments = UserComments()
            course_comments.user = request.user
            course_comments.course = Course.objects.get(id=int(course_id))
            course_comments.comments = comments
            course_comments.save()
            return HttpResponse(
                '{"status": "success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse(
                '{"status": "fail", "msg":"添加失败"}', content_type='application/json')
