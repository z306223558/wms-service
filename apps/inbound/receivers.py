from django.db.models.signals import post_save
from django.dispatch import receiver

from inbound.models import InboundOrder


@receiver(post_save, sender=InboundOrder)
def inbound_order_save_handler(sender, instance, **kwargs):
    created = kwargs.get('created', False)
    if not created:
        return
