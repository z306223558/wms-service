from django.db import models


class Material(models.Model):

    material_name = models.CharField(verbose_name="物料名称", max_length=100, default="默认物料")
    created_at = models.DateTimeField(verbose_name="创建时间", auto_created=True, auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", auto_created=True, auto_now_add=True, auto_now=True)

    class Meta:
        verbose_name = "物料"
        ordering = ('-created_at', )


class MaterialCategory(models.Model):
    category_name = models.CharField(verbose_name="类别名称", max_length=100, default="")
    created_at = models.DateTimeField(verbose_name="创建时间", auto_created=True, auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", auto_created=True, auto_now_add=True, auto_now=True)

    class Meta:
        verbose_name = "物料类别"
        ordering = ('-created_at', )
