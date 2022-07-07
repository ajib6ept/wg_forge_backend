from django.urls import path

from .views import CatCreateView, CatListView, ping_service

urlpatterns = [
    path("ping", ping_service, name="ping_service"),
    path("cats", CatListView.as_view(), name="cats_view"),
    path("cat", CatCreateView.as_view(), name="cat_create"),
]
