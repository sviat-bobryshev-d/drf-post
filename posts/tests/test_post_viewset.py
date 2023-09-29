import pytest
from rest_framework.test import APIClient

from posts.models import Post
from posts.tests.factories import CategoryFactory, PostFactory
from posts.tests.util import datetime_to_iso


class TestPostView:
    def setup_class(self):
        self.client = APIClient()

    def test_create_by_anonymous_error(self):
        response = self.client.post("/posts/")

        assert response.status_code == 403

    @pytest.mark.django_db
    def test_get_one_by_anonymous(self):
        stored_category = CategoryFactory()
        stored_post = PostFactory(categories=(stored_category,))

        response = self.client.get(f"/posts/{stored_post.id}/")

        assert response.status_code == 200
        assert response.json() == {
            "id": stored_post.id,
            "title": stored_post.title,
            "content": stored_post.content,
            "categories": [stored_category.tag],
            "created_at": datetime_to_iso(stored_post.created_at),
            "updated_at": datetime_to_iso(stored_post.updated_at),
            "owner": stored_post.owner.id,
        }

    @pytest.mark.django_db
    def test_get_page_by_anonymous(self):
        stored_categories = CategoryFactory.create_batch(3)
        stored_posts = PostFactory.create_batch(2, categories=stored_categories)

        response = self.client.get("/posts/?page=1&page_size=2")

        assert response.status_code == 200
        assert response.json() == {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": stored_post.id,
                    "title": stored_post.title,
                    "content": stored_post.content,
                    "categories": sorted([c.tag for c in stored_categories]),
                    "created_at": datetime_to_iso(stored_post.created_at),
                    "updated_at": datetime_to_iso(stored_post.updated_at),
                    "owner": stored_post.owner.id,
                }
                for stored_post in stored_posts
            ],
        }

    def test_update_by_anonymous_error(self):
        response = self.client.put("/posts/test-id/")

        assert response.status_code == 403

    def test_partial_update_by_anonymous_error(self):
        response = self.client.patch("/posts/test-id/")

        assert response.status_code == 403

    def test_delete_by_anonymous_error(self):
        response = self.client.delete("/posts/test-id/")

        assert response.status_code == 403

    @pytest.mark.django_db
    def test_create_by_authenticated_user(self, django_user_model):
        user = django_user_model.objects.create_user("test-user")
        stored_category = CategoryFactory()
        attributes = {
            "title": "test-title",
            "content": "test-content",
            "categories": [stored_category.tag],
        }

        self.client.force_login(user)
        response = self.client.post("/posts/", data=attributes)

        assert response.status_code == 201
        body = response.json()
        post = Post.objects.get(pk=body["id"])
        assert body == {
            **attributes,
            "id": post.id,
            "created_at": datetime_to_iso(post.created_at),
            "updated_at": datetime_to_iso(post.updated_at),
            "owner": user.id,
        }

    @pytest.mark.parametrize("current_viewer", ("viewer", "owner"))
    def test_get_page_by_any_authenticated_user(
        self,
        django_user_model,
        current_viewer,
    ):
        categories = CategoryFactory.create_batch(2)
        owner = django_user_model.objects.create_user("test-owner")
        not_owner = django_user_model.objects.create_user("test-not-owner")
        viewers = {"owner": owner, "viewer": not_owner}
        post = PostFactory(categories=categories, owner=owner)

        viewer = viewers[current_viewer]
        self.client.force_login(viewer)
        response = self.client.get("/posts/?page=1&page_size=1")

        assert response.status_code == 200
        assert response.json() == {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "categories": sorted([c.tag for c in categories]),
                    "id": post.id,
                    "title": post.title,
                    "content": post.content,
                    "owner": owner.id,
                    "created_at": datetime_to_iso(post.created_at),
                    "updated_at": datetime_to_iso(post.updated_at),
                }
            ],
        }

    def test_update_by_owner(self, django_user_model):
        categories = CategoryFactory.create_batch(2)
        owner = django_user_model.objects.create_user(username="test-owner")
        before_post = PostFactory(categories=categories, owner=owner)
        attributes = {
            "id": before_post.id,
            "title": "new_title",
            "content": "new_content",
            "categories": sorted([c.tag for c in categories]),
        }

        self.client.force_login(owner)
        response = self.client.put(f"/posts/{before_post.id}/", data=attributes)

        assert response.status_code == 200
        after_post = Post.objects.get(pk=before_post.id)
        assert response.json() == {
            **attributes,
            "owner": owner.id,
            "created_at": datetime_to_iso(after_post.created_at),
            "updated_at": datetime_to_iso(after_post.updated_at),
        }

    def test_partial_update_by_owner(self, django_user_model):
        categories = CategoryFactory.create_batch(2)
        owner = django_user_model.objects.create_user("test-owner")
        before_post = PostFactory(categories=categories, owner=owner)
        attributes = {
            "title": "new_title",
            "categories": [],
        }

        self.client.force_login(owner)
        response = self.client.patch(
            f"/posts/{before_post.id}/",
            data=attributes,
            format="json",
        )

        assert response.status_code == 200
        after_post = Post.objects.get(pk=before_post.id)
        assert response.json() == {
            **attributes,
            "id": after_post.id,
            "content": after_post.content,
            "owner": owner.id,
            "created_at": datetime_to_iso(after_post.created_at),
            "updated_at": datetime_to_iso(after_post.updated_at),
        }

    def test_delete_by_owner(self, django_user_model):
        categories = CategoryFactory.create_batch(2)
        owner = django_user_model.objects.create_user(username="test-owner")
        post = PostFactory(categories=categories, owner=owner)

        self.client.force_login(owner)
        response = self.client.delete(f"/posts/{post.id}/")

        assert response.status_code == 204
        assert not Post.objects.filter(pk=post.id)

    def test_delete_by_not_owner_error(self, django_user_model):
        categories = CategoryFactory.create_batch(2)
        owner = django_user_model.objects.create_user(username="test-owner")
        not_owner = django_user_model.objects.create_user(username="test-not-owner")
        post = PostFactory(categories=categories, owner=owner)

        self.client.force_login(not_owner)
        response = self.client.delete(f"/posts/{post.id}/")

        assert response.status_code == 403
        assert Post.objects.get(pk=post.id)

    def test_create_by_authenticated_user_with_someone_else_id_in_body(
        self,
        django_user_model,
    ):
        not_owner = django_user_model.objects.create_user("not-owner")
        owner = django_user_model.objects.create_user("owner")
        self.client.force_login(owner)
        stored_category = CategoryFactory()
        attributes = {
            "owner": not_owner.id,
            "title": "test-title",
            "content": "test-content",
            "categories": [stored_category.tag],
        }

        response = self.client.post("/posts/", data=attributes)

        assert response.status_code == 201
        created_post = Post.objects.get(pk=response.json()["id"])
        assert response.json() == {
            **attributes,
            "id": created_post.id,
            "created_at": datetime_to_iso(created_post.created_at),
            "updated_at": datetime_to_iso(created_post.updated_at),
            "owner": owner.id,
        }

    def test_partial_update_by_not_owner_error(self, django_user_model):
        categories = CategoryFactory.create_batch(2)
        owner = django_user_model.objects.create_user("test-owner")
        not_owner = django_user_model.objects.create_user("test-not-owner")
        before_post = PostFactory(categories=categories, owner=owner)
        attributes = {
            "title": "new_title",
            "categories": [],
        }

        self.client.force_login(not_owner)
        response = self.client.patch(
            f"/posts/{before_post.id}/",
            data=attributes,
            format="json",
        )

        assert response.status_code == 403
        after_post = Post.objects.get(pk=before_post.id)
        categories = after_post.categories.all()
        assert after_post.title != attributes["title"]
        assert sorted([c.tag for c in categories]) != attributes["categories"]

    def test_update_by_not_owner(self, django_user_model):
        categories = CategoryFactory.create_batch(2)
        owner = django_user_model.objects.create_user("test-owner")
        not_owner = django_user_model.objects.create_user("test-not-owner")
        post = PostFactory(categories=categories, owner=owner)

        self.client.force_login(not_owner)
        response = self.client.put(f"/posts/{post.id}/", data={})

        assert response.status_code == 403
