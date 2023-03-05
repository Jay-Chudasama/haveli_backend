import time
import uuid

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import BasePermission
from rest_framework.response import Response as InBuiltResponse

from core.models import Token

pagination = LimitOffsetPagination()


def new_token():
    token = uuid.uuid1().hex
    return token


def token_response(user):
    token = new_token()
    Token.objects.create(token=token, user=user)
    return Response({'token': token})


class IsAuthenticatedUser(BasePermission):
    message = 'unauthenticated_user'

    def has_permission(self, request, view):
        return bool(request.user)


class Response(InBuiltResponse):
    def __init__(self, data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):

        # todo remove in prod
        time.sleep(3)

        super().__init__(data=data, status=status,
                       template_name=template_name, headers=headers,
                       exception=exception, content_type=content_type)
