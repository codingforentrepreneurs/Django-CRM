from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Event


@receiver(post_save)
def handle_post_save_signal(sender, instance, created, *args, **kwargs):
    print(sender, instance, created, args, kwargs)
    if sender == Event:
        return
    elif isinstance(instance, Event):
        return
    event_type = Event.EventType.SAVED
    if created:
        event_type = Event.EventType.CREATED
    Event.objects.create(type=event_type, content_object=instance)
