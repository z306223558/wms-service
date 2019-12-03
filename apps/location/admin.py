from django.contrib import admin
import json
from django.utils.html import format_html

from location.models import StoreLocation


@admin.register(StoreLocation)
class StoreLocationAdmin(admin.ModelAdmin):
    """
    课程后台管理页面功能定制
    """
    list_display = ['location_name', 'location_code', 'location_type', 'width', 'height', 'length', 'line_number', 'row_number', 'layer_number', 'status', 'created_at']
    list_display_links = ['location_code', ]
    list_filter = ['location_name', 'location_code', 'creator__mobile', ]
    list_editable = ['status', ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_staff:
            return qs
        return qs.filter(creator=request.user)
