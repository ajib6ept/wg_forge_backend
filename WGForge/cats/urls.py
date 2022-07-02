from django.urls import path

from .views import ping, CatListView

urlpatterns = [
    path("ping", ping, name="ping"),
    path("cats", CatListView.as_view(), name="cats"),
]
