from datetime import timedelta
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.utils import timezone

from .models import Event


def get_event_analytics(content_object):
    if not hasattr(content_object, "id") or not hasattr(content_object, "__class__"):
        return None
    ModelKlass = content_object.__class__
    ctype = ContentType.objects.get_for_model(ModelKlass)
    now = timezone.now()
    oldest_time = now - timedelta(hours=6)
    # if hasattr(content_object, "created_at"):
    #     oldest_time = content_object.created_at
    range_1 = (now - timedelta(hours=2), now - timedelta(hours=1))
    range_2 = (now - timedelta(hours=1), now)
    qs = Event.objects.filter(
        time__gte=oldest_time, content_type=ctype, object_id=content_object.id
    )
    range_1_qs = (
        qs.filter(time__range=range_1)
        .values("type")
        .annotate(type_counts=Count("type"))
    )
    range_2_qs = (
        qs.filter(time__range=range_2)
        .values("type")
        .annotate(type_counts=Count("type"))
    )
    return {"range_1": range_1_qs, "range_2": range_2_qs}
