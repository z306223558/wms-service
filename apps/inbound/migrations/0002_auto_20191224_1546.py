# Generated by Django 2.2.1 on 2019-12-24 15:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inbound', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0003_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='inboundorder',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='department_inbound_orders', to='user.Department'),
        ),
        migrations.AddField(
            model_name='inboundorder',
            name='operator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inbound_order_operator', to=settings.AUTH_USER_MODEL, verbose_name='操作人'),
        ),
    ]
