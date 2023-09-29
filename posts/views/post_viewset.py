from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from posts.models.post import Post
from posts.permissions import IsOwnerOrReadOnly
from posts.serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
