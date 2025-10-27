import django.dispatch

from .models import Event

event_did_trigger = django.dispatch.Signal()


def trigger_event(
    instance, is_viewed=None, is_created=None, is_updated=None, user=None, request=None
):
    event_type = Event.EventType.UNKNOWN
    if is_viewed:
        event_type = Event.EventType.VIEWED
    elif is_created:
        event_type = Event.EventType.CREATED
    elif is_updated:
        event_type = Event.EventType.SAVED

    Klass = instance.__class__
    event_did_trigger.send(
        sender=Klass,
        user=user,
        event_type=event_type,
        content_object=instance,
        request=request,
    )
