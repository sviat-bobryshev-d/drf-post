from django.http import Http404
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from posts.permissions import DoesUserAffectHisObject, IsOwnerOrReadOnly
from posts.serializers import ProfileSerializer
from posts.services import UsersService


class ProfileAPIView(APIView):
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )
    users_service = UsersService()

    def post(self, request: Request, *args, **kwargs) -> Response:
        user_id = kwargs.get("user_id")
        if request.user.id != user_id:
            raise PermissionDenied()

        serializer = ProfileSerializer(data=request.data | {"owner": user_id})

        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        headers = self.__get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def put(self, request: Request, *args, **kwargs) -> Response:
        user_id = kwargs.get("user_id")
        if request.user.id != user_id:
            raise PermissionDenied()

        data = request.data | {"owner": user_id}
        if not self.users_service.has_profile(user=request.user):
            raise Http404()

        profile = request.user.profile
        self.check_object_permissions(request, profile)
        serializer = ProfileSerializer(profile, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(serializer.data)

    def patch(self, request: Request, *args, **kwargs) -> Response:
        user_id = kwargs.get("user_id")
        if request.user.id != user_id:
            raise PermissionDenied()
        data = request.data | {"owner": user_id}
        if not self.users_service.has_profile(user=request.user):
            raise Http404()

        profile = request.user.profile
        self.check_object_permissions(request, profile)
        serializer = ProfileSerializer(profile, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(serializer.data)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        user_id = kwargs.get("user_id")
        if request.user.id != user_id:
            raise PermissionDenied()
        if not self.users_service.has_profile(user=request.user):
            raise Http404()

        profile = request.user.profile
        self.check_object_permissions(request, profile)
        profile.delete()
        return Response(status=204)

    def __get_success_headers(self, data: dict) -> dict[str, str]:
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
