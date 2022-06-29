from django.urls import path, include

urlpatterns = [
    path("", include("WGForge.cats.urls")),
]
