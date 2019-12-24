from django.apps import AppConfig


class StocktakingConfig(AppConfig):
    name = 'stocktaking'

    def ready(self):
        import stocktaking.receivers
