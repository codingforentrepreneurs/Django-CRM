from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Contact


@login_required
def contacts_list_view(request):
    user = request.user
    qs = Contact.objects.filter(user=user)  # everything
    context = {"object_list": qs}
    return render(request, "contacts/list.html", context)
