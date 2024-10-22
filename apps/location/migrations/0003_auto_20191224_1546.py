# Generated by Django 2.2.1 on 2019-12-24 15:46

from django.db import migrations
import libs.custom_models.json_field


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_storelocation_preference_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storelocation',
            name='extra_info',
            field=libs.custom_models.json_field.JSONField(blank=True, default={}, null=True, verbose_name='额外信息(JSON数据)'),
        ),
        migrations.AlterField(
            model_name='storelocation',
            name='store_info',
            field=libs.custom_models.json_field.JSONField(blank=True, default={}, null=True, verbose_name='库存信息'),
        ),
    ]
