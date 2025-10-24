from django.shortcuts import redirect
from django.http import HttpResponse


# Create your views here.
# request -> /dashboard -> django -> urls.py -> view -> response
def dashboard_webpage(request, *args, **kwargs):
    print(request.user, request.user.is_authenticated)
    if not request.user.is_authenticated:
        return redirect("/auth/google/login/")
    return HttpResponse(f"Hi {request.user}")
