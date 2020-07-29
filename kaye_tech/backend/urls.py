from django.urls import include, path
from rest_framework import routers
from backend import views

router = routers.DefaultRouter()
router.register("burritos", views.BurritoViewSet, basename="burritos_base")
router.register("snake", views.SnakeViewSet, basename="snake_base")
router.register("calculator", views.CalculatorViewSet, basename="calculator_base")

urlpatterns = [path("", include(router.urls))]
