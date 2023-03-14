from random import randint

from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from core.models import User, Otp, Token
from core.serializers import UserSerializer
from core.utils import token_response, IsAuthenticatedUser


@api_view(['POST'])
def getotp(request):
    phone = request.data.get('phone')

    if not phone:
        return Response("PARAMS_MISSING",status=400)

    # otp = randint(1000, 9999)
    otp = 1234
    print(otp)

    obj, created = Otp.objects.update_or_create(
        phone=phone,
        defaults={'phone': phone,'otp':otp},
    )
    return Response("SUCCESS")


@api_view(['POST'])
def verifyotp(request):
    phone = request.data.get('phone')
    otp = request.data.get('otp')

    if not otp or not phone:
        return Response("PARAMS_MISSING", status=400)

    try:
        obj = Otp.objects.get(phone=phone,otp=otp)
        obj.delete()

        user, created = User.objects.get_or_create(
            phone=phone,

        )

        return token_response(user)
    except:
        return Response("Invalid otp",status=400)



@api_view(['GET'])
@permission_classes([IsAuthenticatedUser])
def userdetails(request):
    data = UserSerializer(request.user).data
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticatedUser])
def logout(request):
    Token.objects.filter(user=request.user).delete()
    return Response("LOGGED OUT")

