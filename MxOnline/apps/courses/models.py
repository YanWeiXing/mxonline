from datetime import datetime

from django.db import models

# Create your models here.
class Course(models.Model):

    name = models.CharField(max_length=50, verbose_name="课程名")
    desc = models.CharField(max_length=300, verbose_name="课程描述")
    detail = models.TextField(verbose_name="课程详情")
    degree = models.CharField(max_length=10, choices=(('cj', '初级'),('zj', '中级'),('gj', '高级')))
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%m', verbose_name='封面图')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='上传时间')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Chapter(models.Model):

    course = models.ForeignKey(Course, verbose_name="课程", on_delete='')
    name = models.CharField(max_length=100, verbose_name="章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name='上传时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(models.Model):

    chapter = models.ForeignKey(Chapter, verbose_name='章节', on_delete='')
    name = models.CharField(max_length=100, verbose_name='视频名')
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