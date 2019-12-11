from django.contrib import admin
import json
from django.utils.html import format_html
from libs.custom_models.json_field import JSONField
from libs.custom_widgets.json_widget import JsonEditorWidget
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
    list_max_show_all = 20
    list_per_page = 20
    formfield_overrides = {
        JSONField: {'widget': JsonEditorWidget}
    }
    filter_horizontal = ('preference_categories', )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_staff:
            return qs
        return qs.filter(creator=request.user)

    class Media:
        from django.conf import settings
        static_url = getattr(settings, 'STATIC_URL')

        css = {
            'all': (static_url + 'css/jsoneditor/jsoneditor.min.css',
                    'http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/css/bootstrap-combined.min.css',
                    'http://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.0.3/css/font-awesome.css', )
        }
        js = (static_url + 'js/jsoneditor/jsoneditor.min.js', )

    def save_model(self, request, obj, form, change):
        print(form)
        super().save_model(request, obj, form, change)
