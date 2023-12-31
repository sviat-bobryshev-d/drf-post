from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = Post
        fields = "__all__"
