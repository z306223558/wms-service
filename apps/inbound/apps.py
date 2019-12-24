from django.apps import AppConfig


class InboundConfig(AppConfig):
    name = 'inbound'

    def ready(self):
        import inbound.receivers
