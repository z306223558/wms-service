import datetime

from django.db import models
from django_mysql.models import Model
from libs.custom_models.json_field import JSONField
from inbound.constants import ImportantLevel, OrderStatus
from task.constants import TaskType
from inbound.utils import FunctionUtils


class StocktakingOrder(Model):
    
    order_number = models.CharField(verbose_name="盘点单号", max_length=100)
    status = models.PositiveSmallIntegerField(verbose_name="盘点单状态", default=OrderStatus.AUDIT,
                                              choices=OrderStatus.CHOICES)
    important_level = models.PositiveSmallIntegerField(verbose_name="优先级", default=ImportantLevel.NORMAL,
                                                       choices=ImportantLevel.CHOICES)

    order_info = JSONField(verbose_name="订单信息", default=dict)

    expired_date = models.DateTimeField(verbose_name="过期时间", blank=True, null=True)
    creator = models.ForeignKey('user.User', verbose_name="创建人", on_delete=models.SET_NULL,
                                related_name="stocktaking_order_creator", null=True, blank=True)
    operator = models.ForeignKey('user.User', verbose_name="操作人", on_delete=models.SET_NULL,
                                 related_name="stocktaking_order_operator",
                                 null=True, blank=True)
    department = models.ForeignKey('user.Department', on_delete=models.SET_NULL,
                                   null=True, blank=True,
                                   verbose_name="盘点部门",
                                   related_name='department_stocktaking_orders')
    note = models.TextField(verbose_name="备注", default="", max_length=500)

    created_at = models.DateTimeField(verbose_name="创建时间", auto_created=True, auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", auto_created=True, auto_now=True)

    class Meta:
        verbose_name = "盘点单"
        ordering = ['-created_at', ]

    @staticmethod
    def generate_number():
        return FunctionUtils().generate_order_number(TaskType.INBOUND)

    def __str__(self):
        return "盘点单：{}-状态：{}".format(self.order_number, self.get_status_display(), self.get_status_display())
