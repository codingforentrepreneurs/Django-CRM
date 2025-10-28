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
    dataset_range = (oldest_time, now)
    chunk_time = "15 minutes"
    # if hasattr(content_object, "created_at"):
    #     oldest_time = content_object.created_at
    dataset = (
        Event.timescale.filter(
            time__range=dataset_range, content_type=ctype, object_id=content_object.id
        )
        .time_bucket("time", chunk_time)
        .values("bucket", "type")
        .annotate(type_count=Count("type"))
        .order_by("bucket", "type")
    )
    return dataset
