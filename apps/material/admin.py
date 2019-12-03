from django.contrib import admin
import json
from django.utils.html import format_html

from material.models import Material, MaterialCategory, MaterialCategoryRecord, MaterialLocationRecord


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    """
    物料管理页面功能定制
    """
    list_display = ['material_name', 'material_code', 'material_sku', 'weight', 'length',
                    'width', 'height', 'material_number', 'quality_status', 'status', 'product_time', 'created_at', ]
    list_display_links = ['material_code', ]
    list_filter = ['material_name', 'material_code', 'material_sku', 'status', ]
    list_editable = ['status', ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_staff:
            return qs
        return qs.filter(creator=request.user)


admin.site.register(MaterialCategory)
# admin.site.register(MaterialCategoryRecord, MaterialAdmin)
# admin.site.register(MaterialLocationRecord, MaterialAdmin)
