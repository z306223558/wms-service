from django.db.models.signals import post_save
from django.dispatch import receiver

from material.models import Material


@receiver(post_save, sender=Material)
def material_save_handler(sender, instance, **kwargs):
    pass
