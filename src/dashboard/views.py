from random import randint

from django.conf import settings
from django.shortcuts import redirect, render

TEMPLATES_DIR = settings.TEMPLATES_DIR
print("TEMPLATES_DIR", TEMPLATES_DIR, TEMPLATES_DIR.exists())


# Create your views here.
# request -> /dashboard -> django -> urls.py -> view -> response
# request -> html
# request -> json -> api
# request -> ai agent -> mcp
# request -> xml -> podcast feeds
def dashboard_webpage(request, *args, **kwargs):
    print(request.user, request.user.is_authenticated)
    if not request.user.is_authenticated:
        return redirect("/auth/google/login/")
    my_value = str(request.user) + f"{randint(0, 129039109202)}"
    template_context = {
        "my_value": my_value,
        "not_actual_context": "now it's ready",
        "colors": ["red", "blue"],
    }
    return render(request, "dashboard.html", template_context)
    # html = "<h1 style='color:red'>Hello World</h1>"
    # dashboard_html = TEMPLATES_DIR / "dashboard.html"
    # if not dashboard_html.exists():
    #     return HttpResponse("Not found", status=404)
    # dashboard_html_val = dashboard_html.read_text()
    # _html = dashboard_html_val.format(my_value=str(request.user))
    # return HttpResponse(_html)


def about_us_page(request):
    return render(request, "about.html")
