# Generated by Django 2.0 on 2018-02-25 21:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_organization_category'),
        ('courses', '0004_video_learn_times'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.Teacher', verbose_name='讲师'),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_org',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.Organization', verbose_name='课程机构'),
        ),
    ]
