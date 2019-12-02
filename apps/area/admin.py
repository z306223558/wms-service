from django.contrib import admin
import json
from django.utils.html import format_html

from area.models import StoreArea


@admin.register(StoreArea)
class StoreAreaAdmin(admin.ModelAdmin):
    """
    课程后台管理页面功能定制
    """
    list_display = ['area_name', 'area_code', 'area_type', 'status', 'creator', 'created_at']
    list_display_links = ['area_code', ]
    list_filter = ['area_name', 'area_code', 'creator__mobile', ]
    list_editable = ['status', ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_staff:
            return qs
        return qs.filter(creator=request.user)
