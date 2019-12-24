from django.contrib import admin
from libs.custom_models.json_field import JSONField
from libs.custom_widgets.json_widget import JsonEditorWidget
from schedule.models import ScheduleOrder


@admin.register(ScheduleOrder)
class ScheduleOrderAdmin(admin.ModelAdmin):
    """
    入库单功能定制
    """
    list_display = ['order_number', 'status_display', 'important_level_display', 'department', 'creator', 'created_at', ]
    list_display_links = ['order_number', ]
    list_filter = ['order_number', 'status', 'department', ]
    list_max_show_all = 20
    list_per_page = 20

    formfield_overrides = {
        JSONField: {'widget': JsonEditorWidget}
    }

    def status_display(self, obj):
        return obj.get_status_display()
    status_display.short_description = '状态'

    def important_level_display(self, obj):
        return obj.get_important_level_display()
    important_level_display.short_description = '优先级'

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
        super().save_model(request, obj, form, change)
