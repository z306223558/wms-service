from django.db import models
from django_mysql.models import JSONField, Model
from area.constants import StoreAreaType, StoreAreaStatus
from user.models import User


class StoreArea(Model):
    area_name = models.CharField(verbose_name="库区名称", max_length=100, default="默认库区")
    area_code = models.CharField(verbose_name="库区编码", max_length=100, default="编码1")
    area_type = models.PositiveSmallIntegerField(verbose_name="库区类型", default=StoreAreaType.BREAD_LINE,
                                                 choices=StoreAreaType.CHOICES)
    status = models.PositiveSmallIntegerField(verbose_name="库区状态", default=StoreAreaStatus.NORMAL,
                                              choices=StoreAreaStatus.CHOICES)
    creator = models.ForeignKey(User, verbose_name="创建人", on_delete=models.SET_NULL, related_name="area_creator")
    operator = models.ForeignKey(User, verbose_name="操作人", on_delete=models.SET_NULL, related_name="area_operator",
                                 null=True, blank=True)
    note = models.TextField(verbose_name="备注", default="", max_length=500)
    extra_info = models.TextField(verbose_name="额外信息(JSON数据)", default="")
    created_at = models.DateTimeField(verbose_name="创建时间", auto_created=True, auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", auto_created=True, auto_now_add=True, auto_now=True)

    class Meta:
        verbose_name = "库区管理"
        ordering = ['-created_at', ]

    def __str__(self):
        return "库区：{}-编号：{}-状态：{}".format(self.area_name, self.area_code, self.get_status_display())
