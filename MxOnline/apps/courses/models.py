from datetime import datetime

from django.db import models

from organizations.models import Organization, Teacher

# Create your models here.
class Course(models.Model):

    course_org = models.ForeignKey(Organization, verbose_name="课程机构", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name="课程名")
    desc = models.CharField(max_length=300, verbose_name="课程描述")
    detail = models.TextField(verbose_name="课程详情")
    is_banner = models.BooleanField(default=False, verbose_name="是否轮播图")
    teacher = models.ForeignKey(Teacher, verbose_name="讲师", on_delete=models.CASCADE, null=True, blank=True)
    degree = models.CharField(max_length=10, choices=(('cj', '初级'),('zj', '中级'),('gj', '高级')))
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    category = models.CharField(max_length=20, verbose_name='课程类别', default='后端开发')
    tag = models.CharField(max_length=10, verbose_name='课程标签', default='')
    image = models.ImageField(upload_to='courses/%Y/%m', verbose_name='封面图')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    necessary = models.CharField(max_length=300, verbose_name='课程须知', default='')
    notice = models.CharField(max_length=300, verbose_name='教师提示', default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='上传时间')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def get_chapter_nums(self):
        return self.chapter_set.all().count()

    def get_learn_user(self):
        return self.usercourse_set.all()[:5]

    def get_chapter(self):
        return self.chapter_set.all()

    def __str__(self):
        return self.name


class Chapter(models.Model):

    course = models.ForeignKey(Course, verbose_name="课程", on_delete='')
    name = models.CharField(max_length=100, verbose_name="章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name='上传时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def get_video(self):
        return self.video_set.all()

    def __str__(self):
        return self.name


class Video(models.Model):

    chapter = models.ForeignKey(Chapter, verbose_name='章节', on_delete='')
    name = models.CharField(max_length=100, verbose_name='视频名')
    url = models.CharField(max_length=200, verbose_name='视频地址', default='')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='上传时间')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):

    course = models.ForeignKey(Course, verbose_name="课程", on_delete='')
    name = models.CharField(max_length=100, verbose_name="名称")
    download = models.FileField(max_length=100, upload_to='courses/resource/%Y/m', verbose_name='课程资源')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='上传时间')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
