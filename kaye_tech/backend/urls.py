from django.urls import include, path
from rest_framework import routers
from backend import views

router = routers.DefaultRouter()
router.register(
    "burritos", views.BurritoViewSet, basename="burritos_base",
)

urlpatterns = [path("", include(router.urls))]
