from django.contrib.auth.models import User

from posts.models import Profile


class UsersService:
    def has_profile(self, user: User) -> bool:
        try:
            user.profile
            return True
        except Profile.DoesNotExist:
            return False
