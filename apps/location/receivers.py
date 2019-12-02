from django.db.models.signals import post_save
from django.dispatch import receiver

from location.models import StoreLocation


@receiver(post_save, sender=StoreLocation)
def user_save_handler(sender, instance, **kwargs):
    pass
