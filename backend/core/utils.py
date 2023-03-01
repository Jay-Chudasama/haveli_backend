import uuid

from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from core.models import Token


def new_token():
    token = uuid.uuid1().hex
    return token


def token_response(user):
    token = new_token()
    Token.objects.create(token=token, user=user)
    return Response('token ' + token)




class IsAuthenticatedUser(BasePermission):
    message = 'unauthenticated_user'

    def has_permission(self, request, view):
        return bool(request.user)