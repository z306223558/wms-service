from django.db import models
from django_mysql.models import ListCharField, Model, JSONField
from libs.custom_models.json_field import JSONField

from material.models import MaterialCategory
from location.constants import StoreLocationType, StoreLocationWarningType, StoreLocationStatus


class StoreLocation(Model):
    location_name = models.CharField(verbose_name="库位名称", max_length=100, default="默认库位")
    location_code = models.CharField(verbose_name="库位编码", max_length=100, default="编码1")
    location_type = models.PositiveSmallIntegerField(verbose_name="库位类型", default=StoreLocationType.RANDOM_LOCATION,
                                                     choices=StoreLocationType.CHOICES)
    area = models.ForeignKey('area.StoreArea',
                             on_delete=models.SET_NULL,
                             null=True,
                             verbose_name="所属库区",
                             related_name="locations")
    width = models.IntegerField(verbose_name="库位宽度", default=0, blank=True)
    height = models.IntegerField(verbose_name="库位高度", default=0, blank=True)
    length = models.IntegerField(verbose_name="库位长度", default=0, blank=True)

    line_number = models.IntegerField(verbose_name="所在行", default=0, blank=True)
    row_number = models.IntegerField(verbose_name="所在列", default=0, blank=True)
    layer_number = models.IntegerField(verbose_name="所在层", default=0, blank=True)

    entry_distance = models.IntegerField(verbose_name="入口距离", default=0, blank=True)
    exit_distance = models.IntegerField(verbose_name="出口距离", default=0, blank=True)

    store_ratio = models.FloatField(verbose_name="库容系数", default=0, blank=True)

    status = models.PositiveSmallIntegerField(verbose_name="库位状态", default=StoreLocationStatus.NORMAL,
                                              choices=StoreLocationStatus.CHOICES)

    preference_categories = models.ManyToManyField(to=MaterialCategory,
                                                   related_name="liked_locations",
                                                   verbose_name="偏好物料类别",
                                                   blank=True
                                                   )
    store_info = JSONField(verbose_name="库存信息", blank=True, null=True, default={})
    store_count = models.IntegerField(verbose_name="已存物料总数", default=0, blank=True)
    category_count = models.IntegerField(verbose_name="已存物料类别数", default=0, blank=True)
    warning = models.PositiveSmallIntegerField(verbose_name="库位告警状态",
                                               default=StoreLocationWarningType.NORMAL,
                                               blank=True,
                                               choices=StoreLocationWarningType.CHOICES)

    creator = models.ForeignKey('user.User', verbose_name="创建人", on_delete=models.SET_NULL, related_name="location_creator",
                                null=True)
    operator = models.ForeignKey('user.User', verbose_name="负责人", on_delete=models.SET_NULL, related_name="location_operator",
                                 null=True, blank=True)
    note = models.TextField(verbose_name="备注", default="", max_length=500)
    extra_info = JSONField(verbose_name="额外信息(JSON数据)", default={}, blank=True, null=True)

    batch_number = models.CharField(verbose_name="目前最早批次", default='', max_length=100)
    earliest_time = models.DateTimeField(verbose_name="最早入库时间", default='', blank=True, null=True)

    created_at = models.DateTimeField(verbose_name="创建时间", auto_created=True, auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", auto_created=True, auto_now=True)

    class Meta:
        verbose_name = "库位管理"
        ordering = ['-created_at', ]
        indexes = [

        ]

    def __str__(self):
        return "库位：{}-编号：{}-状态：{}".format(self.location_name, self.location_code, self.get_status_display())
