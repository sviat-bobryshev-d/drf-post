from django.http import Http404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from posts.permissions import DoesUserAffectHisObject, IsOwnerOrReadOnly
from posts.serializers import ProfileSerializer
from posts.services import UsersService


class ProfileAPIView(APIView):
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
        DoesUserAffectHisObject,
    )
    users_service = UsersService()

    def post(self, request: Request, *args, **kwargs) -> Response:
        data = request.data | {"owner": kwargs["user_id"]}
        serializer = ProfileSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        headers = self.__get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    def put(self, request: Request, *args, **kwargs) -> Response:
        data = request.data | {"owner": kwargs["user_id"]}
        if not self.users_service.has_profile(user=request.user):
            raise Http404()
        profile = request.user.profile
        self.check_object_permissions(request, profile)
        serializer = ProfileSerializer(profile, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(serializer.data)

    def patch(self, request: Request, *args, **kwargs) -> Response:
        data = request.data | {"owner": kwargs["user_id"]}
        if not self.users_service.has_profile(user=request.user):
            raise Http404()
        profile = request.user.profile
        self.check_object_permissions(request, profile)
        serializer = ProfileSerializer(profile, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(serializer.data)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        if not self.users_service.has_profile(user=request.user):
            raise Http404()
        profile = request.user.profile
        self.check_object_permissions(request, profile)
        profile.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    def __get_success_headers(self, data: dict) -> dict[str, str]:
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
