from random import randint

from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from core.models import User, Token
from core.serializers import UserSerializer
from core.utils import token_response, IsAuthenticatedUser


@api_view(['POST'])
def create_account(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response("PARAMS_MISSING", status=400)

    user_exists = User.objects.filter(email=email).exists()

    if user_exists:
        return Response("Email already taken!", status=400)
    else:
        user = User()
        user.email = email
        user.password = password
        user.save()

        return token_response(user)


@api_view(['GET'])
@permission_classes([IsAuthenticatedUser])
def userdetails(request):
    data = UserSerializer(request.user).data
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticatedUser])
def updateprofile(request):
    name = request.data.get("name")
    image = request.FILES.get('file')
    print(image)

    request.user.image = image
    request.user.name = name

    request.user.save()

    data = UserSerializer(request.user).data
    return Response(data)
