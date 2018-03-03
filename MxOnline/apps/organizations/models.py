from datetime import datetime

from django.db import models


# Create your models here.
class CityDict(models.Model):

    name = models.CharField(max_length=20, verbose_name='城市名')
    desc = models.CharField(max_length=200, verbose_name='城市描述')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Organization(models.Model):

    name = models.CharField(max_length=50, verbose_name='机构名')
    category = models.CharField(max_length=20, choices=(
        ('pxjg','培训机构'), ('gx','高校'), ('gr','个人')
    ), default='pxjg', verbose_name='机构类别')
    desc = models.TextField(verbose_name='机构描述')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    image = models.ImageField(upload_to='organizations/%Y/%m', verbose_name='机构封面图')
    address = models.CharField(max_length=150, verbose_name='机构地址')
    city = models.ForeignKey(CityDict, verbose_name='所在城市', on_delete='SET_NULL')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    course_nums = models.IntegerField(default=0, verbose_name='课程数')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "机构"
        verbose_name_plural = verbose_name

    def get_teacher_nums(self):
        return self.teacher_set.all().count()

    def __str__(self):
        return self.name


class Teacher(models.Model):

    organization = models.ForeignKey(Organization, verbose_name='所属机构', on_delete='SET_NULL')
    name = models.CharField(max_length=50, verbose_name='教师名')
    work_years = models.IntegerField(default=0, verbose_name='工作年限')
    image = models.ImageField(upload_to='teachers/%Y/%m', verbose_name='教师封面图')
    work_company = models.CharField(max_length=50, verbose_name='工作公司')
    work_positon = models.CharField(max_length=50, verbose_name='工作职位')
    point = models.CharField(max_length=50, verbose_name='教学特点')
    age = models.IntegerField(default=18, verbose_name='年龄')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name

    def get_courses(self):
        return self.course_set.all()

    def __str__(self):
        return self.name