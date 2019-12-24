# Generated by Django 2.2.1 on 2019-12-24 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outbound', '0002_auto_20191224_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outboundorder',
            name='expired_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='过期时间'),
        ),
        migrations.AlterField(
            model_name='outboundorder',
            name='order_number',
            field=models.CharField(max_length=100, verbose_name='出库单号'),
        ),
    ]
