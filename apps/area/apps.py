from django.apps import AppConfig


class StoreAreaConfig(AppConfig):
    name = 'area'
    verbose_name = '库区'

    def ready(self):
        import area.receivers