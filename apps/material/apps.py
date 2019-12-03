from django.apps import AppConfig


class MaterialConfig(AppConfig):
    name = 'material'
    verbose_name = '物料管理'

    def ready(self):
        import material.receivers
