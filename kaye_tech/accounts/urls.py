from django.urls import path, include
from .views import SplashView
from django.contrib.auth import logout
from django.conf import settings
from django.shortcuts import redirect


def logout_view(request):
    logout(request)
    return redirect(request.GET.get('next'))


urlpatterns = [
    path("", include("social_django.urls", namespace="social")),
    path("logout/", logout_view, name="logout"),
    path("splash/", SplashView.as_view(), name="splash"),
]
