from django.db import models
from material.constants import MaterialQuality, OperateSource, MaterialStatus
from django.forms import ModelForm, forms, ModelChoiceField


class Material(models.Model):

    material_name = models.CharField(verbose_name="物料名称", max_length=100, default="默认物料")
    material_code = models.CharField(verbose_name="物料编号", max_length=100, default='')
    material_sn = models.CharField(verbose_name="物料SN码", max_length=100, default='')
    material_sku = models.CharField(verbose_name="物料SKU码", max_length=100, default='')
    categories = models.ManyToManyField('material.MaterialCategory',
                                        related_name='material_categories',
                                        through='material.MaterialCategoryRecord',
                                        blank=True,
                                        verbose_name='物料分类')

    location = models.ManyToManyField('location.StoreLocation',
                                      related_name='material_locations',
                                      through='material.MaterialLocationRecord',
                                      blank=True,
                                      verbose_name='客户')
    weight = models.IntegerField(verbose_name="物料重量", default=0, blank=True)
    length = models.IntegerField(verbose_name="物料长度", default=0, blank=True)
    width = models.IntegerField(verbose_name="物料宽度", default=0, blank=True)
    height = models.IntegerField(verbose_name="物料高度", default=0, blank=True)

    material_number = models.IntegerField(verbose_name="物料数量", default=0)

    quality_status = models.PositiveSmallIntegerField(verbose_name="物料高度", choices=MaterialQuality.CHOICES,
                                                      default=MaterialQuality.GOOD_PRODUCT)

    status = models.PositiveSmallIntegerField(verbose_name="物料状态", choices=MaterialStatus.CHOICES,
                                              default=MaterialStatus.WAIT_ENTRY)

    product_time = models.DateTimeField(verbose_name="生产日期", default="", blank=True)
    expired_time = models.DateTimeField(verbose_name="过期日期", default="", blank=True)

    created_at = models.DateTimeField(verbose_name="创建时间", auto_created=True, auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", auto_created=True, auto_now=True)

    class Meta:
        verbose_name = "物料信息"
        ordering = ('-created_at',)

    def __str__(self):
        return '{}-{}-{}-{}'.format(self.material_name, self.material_sn, self.material_number, self.get_status_display())


class MaterialCategoryChoiceField(ModelChoiceField):

    def label_from_instance(self, obj):
        return "{}".format(obj.category_name)


class MaterialCategory(models.Model):

    category_name = models.CharField(verbose_name="类别名称", max_length=100, default="")
    created_at = models.DateTimeField(verbose_name="创建时间", auto_created=True, auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", auto_created=True, auto_now=True)

    class Meta:
        verbose_name = "物料类别"
        ordering = ('-created_at',)

    def __str__(self):
        return "{}".format(self.category_name)


class MaterialCategoryChoiceForm(ModelForm):

    categories = MaterialCategoryChoiceField(queryset=MaterialCategory.objects.all(), label="物料分类")

    class Meta:
        models = Material


class MaterialCategoryRecord(models.Model):

    material = models.ForeignKey('Material', verbose_name="物料ID", on_delete=models.CASCADE)
    category = models.ForeignKey('MaterialCategory', verbose_name="物料类别ID", related_name="categories",
                                 on_delete=models.CASCADE)
    operator = models.ForeignKey('user.User', verbose_name="操作人", on_delete=models.SET_NULL,
                                 related_name='material_category_actions', null=True)
    operator_source = models.PositiveSmallIntegerField(verbose_name="操作终端", choices=OperateSource.CHOICES,
                                                       default=OperateSource.PC_WEBSITE, blank=True)
    created_at = models.DateTimeField(verbose_name="创建时间", auto_created=True, auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", auto_created=True, auto_now=True)

    class Meta:
        verbose_name = "物料分类"
        ordering = ('-created_at', )

    def __str__(self):
        return '{}-{}'.format(self.material.material_name, self.category.category_name)


class MaterialLocationRecord(models.Model):

    material = models.ForeignKey('Material', verbose_name="物料ID", related_name='materials', on_delete=models.CASCADE)
    location = models.ForeignKey('location.StoreLocation', verbose_name="库位ID", related_name="locations",
                                 on_delete=models.CASCADE)
    operator = models.ForeignKey('user.User', verbose_name="操作人", on_delete=models.SET_NULL,
                                 related_name='material_location_actions', null=True)
    operator_source = models.PositiveSmallIntegerField(verbose_name="操作终端", choices=OperateSource.CHOICES,
                                                       default=OperateSource.PC_WEBSITE, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="创建时间", auto_created=True, auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", auto_created=True, auto_now=True)

    class Meta:
        verbose_name = "物料所在库位"
        ordering = ('-created_at',)

    def __str__(self):
        return '{}-{}'.format(self.location.location_name, self.material.material_name)
