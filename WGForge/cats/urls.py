from django.urls import path

from .views import ping, CatListView, CatCreateView

urlpatterns = [
    path("ping", ping, name="ping"),
    path("cats", CatListView.as_view(), name="cats"),
    path("cat", CatCreateView.as_view(), name="cat"),
]
