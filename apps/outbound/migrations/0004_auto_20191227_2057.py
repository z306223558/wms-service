# Generated by Django 2.2.1 on 2019-12-27 20:57

from django.db import migrations
import libs.custom_models.json_field


class Migration(migrations.Migration):

    dependencies = [
        ('outbound', '0003_auto_20191224_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outboundorder',
            name='order_info',
            field=libs.custom_models.json_field.JSONField(default=dict, verbose_name='订单信息'),
        ),
    ]