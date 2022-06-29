from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def ping(request):
    return HttpResponse("Cats Service. Version 0.1")
