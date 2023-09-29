from django.contrib.auth.models import User
from rest_framework import serializers

from posts.serializers import ProfileSerializer


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    posts = ...

    class Meta:
        model = User
        fields = (
            "pofile",
            "posts",
            "first_name",
            "last_name",
            "email",
            "date_joined",
        )
