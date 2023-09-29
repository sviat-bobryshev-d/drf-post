from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user


class DoesUserAffectHisObject(BasePermission):
    def has_permission(self, request, view):
        return view.kwargs.get("user_id") == request.user.id

    def has_object_permission(self, request, view, obj):
        return view.kwargs.get("user_id") == request.user.id
