# Generated by Django 2.0 on 2018-02-23 20:49

from django.db import migrations, models
import django.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0003_auto_20180221_1543'),
        ('courses', '0002_auto_20180220_1836'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_org',
            field=models.ForeignKey(null=True, on_delete=django.db.models.fields.CharField, to='organizations.Organization', verbose_name='课程机构'),
        ),
    ]
