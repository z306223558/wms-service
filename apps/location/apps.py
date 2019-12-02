from django.apps import AppConfig


class StoreLocationConfig(AppConfig):
    name = 'location'
    verbose_name = '库位管理'

    def ready(self):
        import location.receivers
