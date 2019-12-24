# Generated by Django 2.2.1 on 2019-12-04 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('material', '0001_initial'),
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='storelocation',
            name='preference_categories',
            field=models.ManyToManyField(blank=True, related_name='liked_locations', to='material.MaterialCategory', verbose_name='偏好物料类别'),
        ),
    ]
