from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(("GET",))
def ping(request):
    return Response(data="Cats Service. Version 0.1")
