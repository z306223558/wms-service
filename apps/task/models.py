import datetime

from django.db import models
from django_mysql.models import Model

from inbound.constants import ImportantLevel
from task.constants import TaskType, TaskStatus, TaskActions


class Task(Model):
    task_number = models.CharField(verbose_name="任务编号", max_length=100)
    order_number = models.CharField(verbose_name="绑定单号", unique=True, max_length=40)
    status = models.PositiveSmallIntegerField(verbose_name="任务状态", default=TaskStatus.CONFIRM,
                                              choices=TaskStatus.CHOICES)
    task_type = models.PositiveSmallIntegerField(verbose_name="任务类型", default=TaskType.INBOUND,
                                                 choices=TaskType.CHOICES)
    important_level = models.PositiveSmallIntegerField(verbose_name="优先级", default=ImportantLevel.NORMAL,
                                                       choices=ImportantLevel.CHOICES)
    material = models.ForeignKey('material.Material',
                                 on_delete=models.CASCADE,
                                 related_name='material_tasks',
                                 verbose_name="操作物料")
    location = models.ForeignKey('location.StoreLocation',
                                 on_delete=models.CASCADE,
                                 related_name='location_tasks',
                                 verbose_name='目标库位')
    action = models.PositiveSmallIntegerField(verbose_name='操作类型',
                                              default=TaskActions.IN,
                                              choices=TaskActions.CHOICES)

    operator = models.ForeignKey('user.User', verbose_name="操作人", on_delete=models.SET_NULL,
                                 related_name="task_operator",
                                 null=True, blank=True)

    relation_tasks = models.ManyToManyField('self', related_name='+', symmetrical=False, blank=True,
                                            verbose_name='关联任务')

    created_at = models.DateTimeField(verbose_name="创建时间", auto_created=True, auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", auto_created=True, auto_now=True)

    class Meta:
        verbose_name = "库内任务"
        ordering = ['-created_at', ]

    def __str__(self):
        return "任务：{}-类型：{}-状态：{}".format(self.task_number, self.get_task_type_display(), self.get_status_display())
