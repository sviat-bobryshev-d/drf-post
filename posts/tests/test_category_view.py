import pytest
from rest_framework.test import APIClient

from posts.tests.factories import CategoryFactory


class TestCategoryView:
    def setup_class(self):
        self.client = APIClient()

    def test_create_by_admin(self, admin_client):
        attributes = {
            "tag": "tag",
            "name": "test-tag",
        }

        response = admin_client.post("/categories/", data=attributes)

        assert response.status_code == 201
        assert response.json() == attributes

    def test_update_by_admin(self, admin_client):
        stored = CategoryFactory()
        attributes = {"tag": "upd", "name": "upd-name"}

        response = admin_client.put(
            f"/categories/{stored.tag}/",
            data=attributes,
            content_type="application/json",
        )

        assert response.status_code == 200
        assert response.json() == attributes

    def test_delete_by_admin(self, admin_client):
        stored = CategoryFactory()

        response = admin_client.delete(f"/categories/{stored.tag}/")

        assert response.status_code == 204

    @pytest.mark.django_db
    def test_get_page_by_not_admin_user(self):
        stored_category = CategoryFactory()

        response = self.client.get("/categories/")

        assert response.status_code == 200
        assert response.json() == {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "tag": stored_category.tag,
                    "name": stored_category.name,
                }
            ],
        }

    @pytest.mark.django_db
    def test_get_one_by_not_admin_user(self):
        stored_category = CategoryFactory()

        response = self.client.get(f"/categories/{stored_category.tag}/")

        assert response.status_code == 200
        assert response.json() == {
            "tag": stored_category.tag,
            "name": stored_category.name,
        }

    def test_create_by_not_admin_user_error(self):
        response = self.client.post("/categories/", data={})

        assert response.status_code == 403

    def test_update_by_not_admin_user_error(self):
        response = self.client.put("/categories/", data={})

        assert response.status_code == 403

    def test_delete_by_not_admin_user_error(self):
        response = self.client.delete("/categories/", data={})

        assert response.status_code == 403
