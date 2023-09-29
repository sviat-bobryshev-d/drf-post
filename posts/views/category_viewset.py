from rest_framework.viewsets import ModelViewSet

from posts.models import Category
from posts.permissions import IsAdminOrReadOnly
from posts.serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
