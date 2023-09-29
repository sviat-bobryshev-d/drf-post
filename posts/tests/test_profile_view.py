from rest_framework.test import APIClient

from posts.models import Profile
from posts.tests.factories import ProfileFactory


class TestProfileView:
    def setup_class(self):
        self.client = APIClient()

    def test_create(self, django_user_model):
        user = django_user_model.objects.create_user("test-user")
        attributes = {
            "bio": "test-bio",
            "preferences": "test-preferences",
        }

        self.client.force_login(user)
        response = self.client.post(
            f"/users/{user.id}/profile/",
            data=attributes,
            format="json",
        )

        assert response.status_code == 201
        body = response.json()
        assert set(body.keys()) == {"id", "owner", "bio", "preferences"}
        profile = Profile.objects.get(owner=user)
        assert body["id"] == profile.id
        assert body["bio"] == attributes["bio"] == profile.bio
        assert body["preferences"] == attributes["preferences"] == profile.preferences
        assert body["owner"] == user.id

    def test_get_by_owner(self, django_user_model):
        owner = django_user_model.objects.create_user("test-owner")
        ProfileFactory(owner=owner)

        self.client.force_login(owner)
        response = self.client.get(f"/users/{owner.id}/profile/")

        assert response.status_code == 405

    def test_update_by_owner(self, django_user_model):
        owner = django_user_model.objects.create_user("test-owner")
        profile = ProfileFactory(owner=owner)
        attributes = {"bio": "new-bio", "preferences": "new-preferences"}

        self.client.force_login(owner)
        response = self.client.put(
            f"/users/{owner.id}/profile/",
            data=attributes,
            format="json",
        )

        assert response.status_code == 200
        body = response.json()
        profile = Profile.objects.get(owner=owner)
        assert set(body.keys()) == {"id", "owner", "bio", "preferences"}
        assert body["id"] == profile.id
        assert body["bio"] == attributes["bio"] == profile.bio
        assert body["preferences"] == attributes["preferences"] == profile.preferences
        assert body["owner"] == owner.id

    def test_update_by_owner_profile_not_exists(self, django_user_model):
        owner = django_user_model.objects.create_user("test-owner")

        self.client.force_login(owner)
        response = self.client.put(f"/users/{owner.id}/profile/")

        assert response.status_code == 404
        assert not list(Profile.objects.all())

    def test_partial_update_by_owner(self, django_user_model):
        owner = django_user_model.objects.create_user("test-owner")
        profile = ProfileFactory(owner=owner)
        old_preferences = profile.preferences
        attributes = {"bio": "new-bio"}

        self.client.force_login(owner)
        response = self.client.patch(
            f"/users/{owner.id}/profile/",
            data=attributes,
            format="json",
        )

        assert response.status_code == 200
        body = response.json()
        profile = Profile.objects.get(owner=owner)
        assert set(body.keys()) == {"id", "owner", "bio", "preferences"}
        assert body["id"] == profile.id
        assert body["bio"] == attributes["bio"] == profile.bio
        assert body["preferences"] == old_preferences == profile.preferences
        assert body["owner"] == owner.id

    def test_partial_update_by_owner_profile_not_exists(self, django_user_model):
        owner = django_user_model.objects.create_user("test-owner")

        self.client.force_login(owner)
        response = self.client.patch(f"/users/{owner.id}/profile/")

        assert response.status_code == 404
        assert not list(Profile.objects.all())

    def test_delete_by_owner(self, django_user_model):
        owner = django_user_model.objects.create_user("test-owner")
        ProfileFactory(owner=owner)

        self.client.force_login(owner)
        response = self.client.delete(f"/users/{owner.id}/profile/")

        assert response.status_code == 204
        assert not Profile.objects.all()

    def test_delete_by_owner_profile_not_exists(self, django_user_model):
        owner = django_user_model.objects.create_user("test-owner")

        self.client.force_login(owner)
        response = self.client.delete(f"/users/{owner.id}/profile/")

        assert response.status_code == 404
        assert not list(Profile.objects.all())

    def test_create_with_alien_user_id_error(self, django_user_model):
        victim = django_user_model.objects.create_user("victim-user")
        attacker = django_user_model.objects.create_user("attacker-user")

        self.client.force_login(attacker)
        response = self.client.post(f"/users/{victim.id}/profile/")

        assert response.status_code == 403

    def test_update_with_alien_user_id_error(self, django_user_model):
        victim = django_user_model.objects.create_user("victim-user")
        attacker = django_user_model.objects.create_user("attacker-user")

        self.client.force_login(attacker)
        response = self.client.put(f"/users/{victim.id}/profile/", data={})

        assert response.status_code == 403

    def test_partial_update_with_alien_user_id_error(self, django_user_model):
        victim = django_user_model.objects.create_user("victim-user")
        attacker = django_user_model.objects.create_user("attacker-user")

        self.client.force_login(attacker)
        response = self.client.patch(f"/users/{victim.id}/profile/")

        assert response.status_code == 403

    def test_delete_with_alien_user_id_error(self, django_user_model):
        victim = django_user_model.objects.create_user("victim-user")
        attacker = django_user_model.objects.create_user("attacker-user")

        self.client.force_login(attacker)
        response = self.client.delete(f"/users/{victim.id}/profile/")

        assert response.status_code == 403

    def test_get_anonymous_error(self):
        response = self.client.get("/users/1243/profile/")

        assert response.status_code == 403

    def test_create_anonymous_error(self):
        response = self.client.post("/users/1243/profile/")

        assert response.status_code == 403

    def test_update_anonymous_error(self):
        response = self.client.put("/users/1234/profile/")

        assert response.status_code == 403

    def test_partial_update_anonymous_error(self):
        response = self.client.patch("/users/1234/profile/")

        assert response.status_code == 403

    def test_delete_anonymous_error(self):
        response = self.client.delete("/users/1234/profile/")

        assert response.status_code == 403
