from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User


@receiver(post_save, sender=User)
def user_save_handler(sender, instance, **kwargs):
    created = kwargs.get('created', False)
    if not created:
        return
