# Generated by Django 2.2.1 on 2019-12-24 18:24

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inbound', '0002_auto_20191224_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inboundorder',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='department_inbound_orders', to='user.Department', verbose_name='入库部门'),
        ),
        migrations.AlterField(
            model_name='inboundorder',
            name='expired_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 1, 23, 18, 24, 11, 373493), null=True, verbose_name='过期时间'),
        ),
        migrations.AlterField(
            model_name='inboundorder',
            name='order_number',
            field=models.CharField(default='L02MS13IN1577183051373S23418', max_length=100, verbose_name='入库单号'),
        ),
        migrations.DeleteModel(
            name='Task',
        ),
    ]