from rest_framework import generics
from django.views.generic import TemplateView
from django.shortcuts import redirect
from .serializers import UserSerializer


class SplashView(TemplateView):
    template_name = "splash.html"


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        try:
            if self.request.user.profile is False:
                raise ("No profile")
            return self.request.user
        except Exception as e:
            print(e)
            self.request.user.profile = {
                "avatar": "https://winaero.com/blog/wp-content/uploads/2019/09/Chrome-Incognito-Mode-Icon-256.png"
            }
            return self.request.user
