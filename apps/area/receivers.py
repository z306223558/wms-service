from django.db.models.signals import post_save
from django.dispatch import receiver

from area.models import StoreArea


@receiver(post_save, sender=StoreArea)
def user_save_handler(sender, instance, **kwargs):
    pass
