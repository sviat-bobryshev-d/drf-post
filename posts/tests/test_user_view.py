from rest_framework.test import APIClient

from posts.tests.factories import (
    CategoryFactory,
    PostFactory,
    ProfileFactory,
)
from posts.tests.util import datetime_to_iso


class TestUserView:
    def setup_class(self):
        self.client = APIClient()

    def test_get_by_authenticated_user(self, django_user_model):
        user = django_user_model.objects.create_user("user")
        profile = ProfileFactory(owner=user)
        viewer = django_user_model.objects.create_user("test-viewer")

        posts = PostFactory.create_batch(2, owner=user)
        for post in posts:
            post.categories.set(CategoryFactory.create_batch(2))
            post.save()

        self.client.force_login(viewer)
        response = self.client.get(f"/users/{user.id}/")

        assert response.status_code == 200
        assert response.json() == {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "date_joined": datetime_to_iso(user.date_joined),
            "profile": {
                "bio": profile.bio,
                "preferences": profile.preferences,
            },
            "posts": [
                {
                    "id": post.id,
                    "title": post.title,
                    "content": post.content,
                    "owner": user.id,
                    "categories": [c.tag for c in post.categories.all()],
                    "created_at": datetime_to_iso(post.created_at),
                    "updated_at": datetime_to_iso(post.updated_at),
                }
                for post in posts
            ],
        }

    def test_get_anonymous(self):
        response = self.client.get("/users/123/")

        assert response.status_code == 403
