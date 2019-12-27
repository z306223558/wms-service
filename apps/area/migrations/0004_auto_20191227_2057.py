# Generated by Django 2.2.1 on 2019-12-27 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0003_merge_20191227_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storearea',
            name='extra_info',
            field=models.TextField(blank=True, default='', null=True, verbose_name='额外信息(JSON数据)'),
        ),
        migrations.AlterField(
            model_name='storearea',
            name='note',
            field=models.TextField(blank=True, default='', max_length=500, null=True, verbose_name='备注'),
        ),
    ]