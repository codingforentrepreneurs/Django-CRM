from django.shortcuts import redirect
from django.http import HttpResponse


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
    html = "<h1 style='color:red'>Hello World</h1>"
    html = """
    <!doctype html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
  </head>
  <body>
    <h1 class="text-3xl font-bold text-red-500">
      Hello world!
    </h1>
  </body>
</html>
"""
    return HttpResponse(html)
