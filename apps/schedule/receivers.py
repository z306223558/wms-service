from django.db.models.signals import post_save
from django.dispatch import receiver

from schedule.models import ScheduleOrder


@receiver(post_save, sender=ScheduleOrder)
def schedule_order_save_handler(sender, instance, **kwargs):
    created = kwargs.get('created', False)
    if not created:
        return
