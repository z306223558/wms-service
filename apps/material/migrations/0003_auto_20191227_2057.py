# Generated by Django 2.2.1 on 2019-12-27 20:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('material', '0002_auto_20191224_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialcategory',
            name='category_code',
            field=models.CharField(default='', max_length=100, verbose_name='类别编码'),
        ),
        migrations.AddField(
            model_name='materialcategory',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='material_cate_creator', to=settings.AUTH_USER_MODEL, verbose_name='创建人'),
        ),
        migrations.AddField(
            model_name='materialcategory',
            name='import_level',
            field=models.PositiveSmallIntegerField(choices=[(1, '低优先级'), (2, '一般'), (3, '高优先级')], default=2, verbose_name='优先级'),
        ),
    ]
