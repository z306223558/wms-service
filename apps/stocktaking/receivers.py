from django.db.models.signals import post_save
from django.dispatch import receiver

from stocktaking.models import StocktakingOrder


@receiver(post_save, sender=StocktakingOrder)
def stocktaking_order_save_handler(sender, instance, **kwargs):
    created = kwargs.get('created', False)
    if not created:
        return
