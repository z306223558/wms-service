# Generated by Django 2.2.1 on 2019-12-24 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='materialcategoryrecord',
            options={'ordering': ('-created_at',), 'verbose_name': '物料分类'},
        ),
        migrations.AlterModelOptions(
            name='materiallocationrecord',
            options={'ordering': ('-created_at',), 'verbose_name': '物料所在库位'},
        ),
    ]
