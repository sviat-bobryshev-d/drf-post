from django.urls import include, path
from rest_framework.routers import DefaultRouter

from posts.views import CategoryViewSet, PostViewSet, ProfileAPIView

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"categories", CategoryViewSet, basename="category")
urlpatterns = [
    path("", include(router.urls)),
    path("users/<int:user_id>/profile/", ProfileAPIView.as_view()),
]
