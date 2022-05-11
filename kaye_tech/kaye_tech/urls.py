from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from .views import IndexView

urlpatterns = [
    path("accounts/", include("accounts.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("backend.urls")),
    path("api/", include("accounts.urls_api")),
    path("home/", IndexView.as_view()),
    path("fluids/", IndexView.as_view()),
    path("news/", IndexView.as_view()),
    path("books/", IndexView.as_view()),
    path("burritos/", IndexView.as_view()),
    path("jokes/", IndexView.as_view()),
    path("games/", IndexView.as_view()),
    path("games/<str:roomName>/", IndexView.as_view()),
    url(r"^$", IndexView.as_view()),
]
