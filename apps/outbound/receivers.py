from django.db.models.signals import post_save
from django.dispatch import receiver

from outbound.models import OutboundOrder


@receiver(post_save, sender=OutboundOrder)
def outbound_order_save_handler(sender, instance, **kwargs):
    created = kwargs.get('created', False)
    if not created:
        return
