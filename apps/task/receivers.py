from django.db.models.signals import post_save
from django.dispatch import receiver

from task.models import Task


@receiver(post_save, sender=Task)
def task_save_handler(sender, instance, **kwargs):
    created = kwargs.get('created', False)
    if not created:
        return
