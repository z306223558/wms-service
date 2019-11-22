# Generated by Django 2.2.7 on 2019-11-22 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(blank=True, max_length=20, verbose_name='用户名')),
                ('mobile', models.CharField(max_length=11, unique=True, verbose_name='手机号码')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='是否有权限进入后台管理界面', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='账号是否被激活', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('date_update', models.DateTimeField(default=django.utils.timezone.now, verbose_name='更新时间')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '账号管理',
                'verbose_name_plural': '账号信息',
                'db_table': 'auth_user',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('M', '男'), ('F', '女')], max_length=1, verbose_name='性别')),
                ('name', models.CharField(max_length=100, verbose_name='用户姓名')),
                ('age', models.PositiveIntegerField(blank=True, verbose_name='年龄')),
                ('avatar', models.ImageField(default='avatar/user.6102e21.jpg', upload_to='avatar', verbose_name='头像')),
                ('tel_info', models.CharField(max_length=20, verbose_name='联系方式')),
                ('birthday', models.CharField(max_length=100, verbose_name='出生年月日')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
            },
        ),
    ]
