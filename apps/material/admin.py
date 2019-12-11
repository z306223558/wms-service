from django.contrib import admin
import json
from django.utils.html import format_html
from material.models import Material, MaterialCategory, MaterialCategoryRecord, MaterialLocationRecord


class MaterialCategoryInline(admin.TabularInline):

    verbose_name_plural = '物料的分类信息'
    model = MaterialCategoryRecord
    extra = 1
    exclude = ('operator', )

    readonly_fields = ['operator', ]

    def has_change_permission(self, request, obj=None):
        return False


class MaterialLocationInline(admin.TabularInline):

    verbose_name_plural = '物料的库位信息'
    model = MaterialLocationRecord
    extra = 0
    exclude = ('operator', )

    readonly_fields = ['operator', ]

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return obj is not None


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    """
    物料管理页面功能定制
    """
    list_display = ['material_name', 'material_code', 'material_sku', 'weight', 'length',
                    'width', 'height', 'material_number', 'quality_status', 'status', 'product_time', 'created_at', ]
    list_display_links = ['material_code', ]
    search_fields = ('material_name', 'material_code', 'material_sku',)
    list_filter = ['material_name', 'material_code', 'material_sku', 'status', ]
    list_editable = ['status', ]
    date_hierarchy = 'created_at'
    empty_value_display = 'N/A'
    show_full_result_count = False

    inlines = [MaterialCategoryInline, MaterialLocationInline, ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_staff:
            return qs
        return qs.filter(creator=request.user)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.pk:
                instance.operator = request.user
            instance.save()
        return super(MaterialAdmin, self).save_formset(request, form, formset, change)


admin.site.register(MaterialCategory)
admin.site.register(MaterialCategoryRecord)
admin.site.register(MaterialLocationRecord)
