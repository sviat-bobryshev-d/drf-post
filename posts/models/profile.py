from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    bio = models.TextField(blank=True)
    preferences = models.TextField(blank=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
