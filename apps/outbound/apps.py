from django.apps import AppConfig


class OutboundConfig(AppConfig):
    name = 'outbound'

    def ready(self):
        import outbound.receivers
