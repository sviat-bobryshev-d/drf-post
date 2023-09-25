from django.urls import include, path
from rest_framework.routers import DefaultRouter

from posts import views

router = DefaultRouter()
router.register("posts", views.PostViewSet, basename="post")

urlpatterns = [path("", include(router.urls))]
