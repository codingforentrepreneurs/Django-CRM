from django.contrib.contenttypes.models import ContentType
from .models import Event


def get_event_analytics(content_object):
    if not hasattr(content_object, "id") or not hasattr(content_object, "__class__"):
        return None
    ModelKlass = content_object.__class__
    ctype = ContentType.objects.get_for_model(ModelKlass)
    qs = Event.objects.filter(content_type=ctype, object_id=content_object.id)
    return qs.count()
