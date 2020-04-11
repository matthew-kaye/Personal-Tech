from django.urls import include, path
from rest_framework import routers
from backend import views

router = routers.DefaultRouter()
router.register("index", views.IndexViewSet, basename="index_base")

urlpatterns = [path("", include(router.urls))]
