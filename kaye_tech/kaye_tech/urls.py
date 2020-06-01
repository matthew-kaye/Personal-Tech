"""kaye_tech URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
    path("canvas/", IndexView.as_view()),
    path("news/", IndexView.as_view()),
    path("books/", IndexView.as_view()),
    path("burritos/", IndexView.as_view()),
    url(r"^book/?[0-9]*$", IndexView.as_view()),
    path("jokes/", IndexView.as_view()),
    path("games/", IndexView.as_view()),
    path("games/<str:roomName>/", IndexView.as_view()),
    url(r"^$", IndexView.as_view()),
]
