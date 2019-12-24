# Generated by Django 2.2.1 on 2019-12-24 15:46

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('user', '0002_auto_20191202_1817'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.Group')),
                ('updated_at', models.DateTimeField(auto_created=True, auto_now=True, verbose_name='更新时间')),
                ('created_at', models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name='创建时间')),
                ('department_name', models.CharField(max_length=200, verbose_name='部门名称')),
                ('charge_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='部门负责人')),
            ],
            options={
                'verbose_name': '部门',
            },
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
    ]
