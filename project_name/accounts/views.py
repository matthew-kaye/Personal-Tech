from rest_framework import generics
from django.views.generic import TemplateView

from .serializers import UserSerializer


class SplashView(TemplateView):
    template_name = "splash.html"


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
