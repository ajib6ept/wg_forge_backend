from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.generic.list import ListView

from .forms import CatsSearchForm
from .models import Cats


@require_http_methods(["GET"])
def ping(request):
    return HttpResponse("Cats Service. Version 0.1")


class CatListView(ListView):

    model = Cats

    def get(self, request, *args, **kwargs):
        cat_search_form = CatsSearchForm(self.request.GET)
        if cat_search_form.is_valid():
            queryset = self.get_queryset(
                cleaned_data=cat_search_form.cleaned_data
            )
            data = list(queryset)
            return JsonResponse(data, status=200, safe=False)
        else:
            return HttpResponse(content="HTTP 400 Bad Request", status=400)

    def get_queryset(self, cleaned_data):
        queryset = super().get_queryset().values()
        attribute = cleaned_data.get("attribute")
        order = cleaned_data.get("order")
        offset = cleaned_data.get("offset")
        limit = cleaned_data.get("limit")
        if attribute:
            queryset = queryset.values(attribute)
        if order:
            mark = "" if order == "asc" else "-"
            queryset = queryset.order_by(mark + attribute)
        if offset:
            queryset = queryset[offset:]
        if limit:
            queryset = queryset[:limit]
        return queryset
