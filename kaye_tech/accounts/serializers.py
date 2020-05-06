from rest_framework import serializers

from django.contrib.auth.models import User

from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("avatar",)


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ("id", "username", "profile", "first_name", "last_name")
