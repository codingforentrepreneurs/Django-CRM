from datetime import timedelta
from django.contrib.contenttypes.models import ContentType
from django.db.models.functions import Coalesce
from django.db.models import Count
from django.utils import timezone

from .models import Event


def get_event_analytics(content_object, gapfill=False, ignore_types=[]):
    if not hasattr(content_object, "id") or not hasattr(content_object, "__class__"):
        return None
    ModelKlass = content_object.__class__
    ctype = ContentType.objects.get_for_model(ModelKlass)
    now = timezone.now()
    oldest_time = now - timedelta(hours=6)

    chunk_time = "5 minutes"
    if hasattr(content_object, "created_at"):
        oldest_time = content_object.created_at

    start_date = oldest_time
    end_date = now
    dataset_range = (start_date, end_date)
    # caching -> redis data store
    if gapfill:
        dataset = (
            Event.timescale.filter(
                time__range=dataset_range,
                content_type=ctype,
                object_id=content_object.id,
            )
            .exclude(type__in=ignore_types)
            .time_bucket_gapfill("time", chunk_time, start_date, end_date)
            .values("bucket", "type")
            .annotate(type_count=Coalesce(Count("type"), 0))
            .order_by("bucket", "type")
        )
    else:
        dataset = (
            Event.timescale.filter(
                time__range=dataset_range,
                content_type=ctype,
                object_id=content_object.id,
            )
            .exclude(type__in=ignore_types)
            .time_bucket("time", chunk_time)
            .values("bucket", "type")
            .annotate(type_count=Count("type"))
            .order_by("bucket", "type")
        )
    return dataset
