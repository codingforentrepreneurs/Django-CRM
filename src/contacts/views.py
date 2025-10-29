from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render

from events.signals import trigger_event
from events import services as events_services
from .models import Contact


@login_required
def contacts_detail_view(request, contact_id=None):
    user = request.user
    instance = Contact.objects.filter(user=user, id=contact_id).first()
    if instance is None:
        raise Http404(f"Contact with id of {contact_id} not found")
    context = {"contact": instance}
    trigger_event(instance, is_viewed=True, user=user, request=request)
    analytics = events_services.get_event_analytics(
        instance, gapfill=True, ignore_types=["unknown", "created"]
    )
    context["analytics"] = analytics
    return render(request, "contacts/detail.html", context)


@login_required
def contacts_list_view(request):
    user = request.user
    qs = Contact.objects.filter(user=user)  # filter -> queryset -> list
    context = {"object_list": qs}
    return render(request, "contacts/list.html", context)
