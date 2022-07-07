import json
from http import HTTPStatus

from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import View
from django.views.generic.list import ListView

from .forms import CatCreateForm, CatsSearchForm
from .models import Cats


@require_http_methods(["GET"])
def ping_service(request):
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
            return JsonResponse(data, status=HTTPStatus.OK, safe=False)
        else:
            return HttpResponse(
                content="HTTP 400 Bad Request", status=HTTPStatus.BAD_REQUEST
            )

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


@method_decorator(csrf_exempt, name="dispatch")
class CatCreateView(View):
    def post(self, request, *args, **kwargs):
        success_message = "Data successfully added"
        cat_create_form = CatCreateForm(data=self.request.body)
        if cat_create_form.is_valid():
            cat_create_form.save()
            return JsonResponse(
                data=success_message, status=HTTPStatus.OK, safe=False
            )
        else:
            form_error = json.dumps(cat_create_form.errors)
            return HttpResponse(
                content=form_error, status=HTTPStatus.BAD_REQUEST
            )
