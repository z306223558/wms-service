# Generated by Django 2.2.1 on 2019-12-04 15:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('area', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_created=True, auto_now=True, verbose_name='更新时间')),
                ('created_at', models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name='创建时间')),
                ('location_name', models.CharField(default='默认库位', max_length=100, verbose_name='库位名称')),
                ('location_code', models.CharField(default='编码1', max_length=100, verbose_name='库位编码')),
                ('location_type', models.PositiveSmallIntegerField(choices=[(1, '随机库位'), (2, '生产库位')], default=1, verbose_name='库位类型')),
                ('width', models.IntegerField(blank=True, default=0, verbose_name='库位宽度')),
                ('height', models.IntegerField(blank=True, default=0, verbose_name='库位高度')),
                ('length', models.IntegerField(blank=True, default=0, verbose_name='库位长度')),
                ('line_number', models.IntegerField(blank=True, default=0, verbose_name='所在行')),
                ('row_number', models.IntegerField(blank=True, default=0, verbose_name='所在列')),
                ('layer_number', models.IntegerField(blank=True, default=0, verbose_name='所在层')),
                ('entry_distance', models.IntegerField(blank=True, default=0, verbose_name='入口距离')),
                ('exit_distance', models.IntegerField(blank=True, default=0, verbose_name='出口距离')),
                ('store_ratio', models.FloatField(blank=True, default=0, verbose_name='库容系数')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, '正常'), (0, '停用'), (-1, '已删除'), (2, '检修中')], default=1, verbose_name='库位状态')),
                ('store_info', django_mysql.models.JSONField(default=dict, verbose_name='库存信息')),
                ('store_count', models.IntegerField(blank=True, default=0, verbose_name='已存物料总数')),
                ('category_count', models.IntegerField(blank=True, default=0, verbose_name='已存物料类别数')),
                ('warning', models.PositiveSmallIntegerField(blank=True, choices=[(0, '无'), (1, '利用率低'), (2, '过期接近'), (3, '种类过多')], default=0, verbose_name='库位告警状态')),
                ('note', models.TextField(default='', max_length=500, verbose_name='备注')),
                ('extra_info', django_mysql.models.JSONField(default='', verbose_name='额外信息(JSON数据)')),
                ('batch_number', models.CharField(default='', max_length=100, verbose_name='目前最早批次')),
                ('earliest_time', models.DateTimeField(blank=True, default='', null=True, verbose_name='最早入库时间')),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='locations', to='area.StoreArea', verbose_name='所属库区')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='location_creator', to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
                ('operator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='location_operator', to=settings.AUTH_USER_MODEL, verbose_name='负责人')),
            ],
            options={
                'verbose_name': '库位管理',
                'ordering': ['-created_at'],
            },
        ),
    ]
