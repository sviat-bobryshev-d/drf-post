from django.contrib.auth.models import User
from rest_framework import serializers

from posts.serializers import PostSerializer, ProfileSerializer


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "profile",
            "posts",
            "first_name",
            "last_name",
            "email",
            "date_joined",
        )
