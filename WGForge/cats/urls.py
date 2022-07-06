from django.urls import path

from .views import CatCreateView, CatListView, ping

urlpatterns = [
    path("ping", ping, name="ping"),
    path("cats", CatListView.as_view(), name="cats_view"),
    path("cat", CatCreateView.as_view(), name="cat_create"),
]
