from django.urls import include, path
from rest_framework import routers

from .views import UserDetailView


router = routers.DefaultRouter()


urlpatterns = [
    path("", include(router.urls)),
    path("currentuser", UserDetailView.as_view()),
]
