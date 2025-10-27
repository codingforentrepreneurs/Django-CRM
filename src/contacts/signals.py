from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

from events.signals import trigger_event

from .models import Contact

User = get_user_model()


@receiver(post_save, sender=Contact)
def contact_post_save(sender, instance, created, *args, **kwargs):
    is_created = created
    is_updated = not created
    trigger_event(
        instance,
        is_created=is_created,
        is_updated=is_updated,
    )


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, *args, **kwargs):
    is_created = created
    is_updated = not created
    trigger_event(
        instance,
        is_created=is_created,
        is_updated=is_updated,
    )
